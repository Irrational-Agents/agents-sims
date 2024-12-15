from logger_config import setup_logger
import json
import csv
import numpy as np

logger = setup_logger('Map-translator')


class MapTranslator:
    def __init__(self, map_data, meta_data, block_data):
        """
        Initializes the MapTranslator with metadata, map data, and block data.

        Args:
            map_data (dict): Contains the raw maze matrices.
            meta_data (dict): Contains metadata like maze dimensions and tile size.
            block_data (dict): Contains information about arena, game objects, sectors, and spawning locations.
        """
        self.maze_width = meta_data["maze_width"]
        self.maze_height = meta_data["maze_height"]
        self.sq_tile_size = meta_data["sq_tile_size"]

        self.collision_maze = self.parse_maze(map_data['collision_maze'])
        self.sector_maze = self.parse_maze(map_data['sector_maze'])
        self.arena_maze = self.parse_maze(map_data['arena_maze'])
        self.game_object_maze = self.parse_maze(map_data['game_object_maze'])
        self.spawning_location_maze = self.parse_maze(map_data['spawning_location_maze'])

        self.arena_blocks = self.convert_to_id_based_dict(block_data["arena_blocks"])
        self.game_object_blocks = self.convert_to_id_based_dict(block_data["game_object_blocks"])
        self.sector_blocks = self.convert_to_id_based_dict(block_data["sector_blocks"])
        self.spawning_location_blocks = self.convert_to_id_based_dict(block_data["spawning_location_blocks"])

        self.tiles = self.initialize_tiles()
        self.address_tiles = self.initialize_address_tiles()

    def convert_to_id_based_dict(self,data):
        """
        Converts a list of dictionaries into a dictionary with 'id' as the key
        and the remaining fields as the value.
        """
        return {
            entry['id']: {key: value for key, value in entry.items() if key != 'id'}
            for entry in data
        }


    def parse_maze(self, csv_text):
        # Use csv reader to convert text into a 2D list
         # Initialize an empty maze of given dimensions
        maze_matrix = np.zeros((self.maze_height, self.maze_width), dtype=int)

        # Use csv.reader to process the text into rows
        rows = csv_text.splitlines()
        for i, row in enumerate(rows):
            if i >= self.maze_height:
                break  # Stop if we exceed the maze height
            cells = [int(cell) for cell in row.split(',')]
            for j, cell in enumerate(cells):
                if j >= self.maze_width:
                    break  # Stop if we exceed the maze width
                maze_matrix[i, j] = cell

        return maze_matrix
    
    def initialize_tiles(self):
        """
        Converts the raw maze data into a structured format with tile details.

        Returns:
            list: A 2D list where each element is a dictionary with tile details.
        """
        tiles = []
        for i in range(self.maze_height):
            row = []
            for j in range(self.maze_width):
                tile_details = {
                    "collision": self.collision_maze[i][j] != "0",
                    "sector": self.sector_blocks.get(self.sector_maze[i][j], ""),
                    "arena": self.arena_blocks.get(self.arena_maze[i][j], ""),
                    "game_object": self.game_object_blocks.get(self.game_object_maze[i][j], ""),
                    "spawning_location": self.spawning_location_blocks.get(self.spawning_location_maze[i][j], ""),
                    "events": set()
                }
                # Add default event for game objects
                if tile_details["game_object"]:
                    object_name = f"{tile_details['arena']}:{tile_details['game_object']}"
                    tile_details["events"].add((object_name, None, None))
                row.append(tile_details)
            tiles.append(row)
        logger.info("Tiles initialized.")
        logger.info(tiles)
        return tiles

    def initialize_address_tiles(self):
        """
        Creates a reverse mapping from addresses to tile coordinates.

        Returns:
            dict: A dictionary mapping addresses to sets of tile coordinates.
        """
        address_tiles = {}
        for i in range(self.maze_height):
            for j in range(self.maze_width):
                tile = self.tiles[i][j]
                addresses = []
                if tile["sector"]:
                    addresses.append(tile["sector"])
                if tile["arena"]:
                    addresses.append(f"{tile['sector']}:{tile['arena']}")
                if tile["game_object"]:
                    addresses.append(f"{tile['arena']}:{tile['game_object']}")
                if tile["spawning_location"]:
                    addresses.append(f"<spawn_loc>{tile['spawning_location']}")

                for address in addresses:
                    if address not in address_tiles:
                        address_tiles[address] = set()
                    address_tiles[address].add((j, i))

        logger.info("Address tiles initialized.")
        logger.info(address_tiles)
        return address_tiles

    def get_tile_details(self, tile):
        """
        Retrieves the details of a tile at a given coordinate.

        Args:
            tile (tuple): Tile coordinates in (x, y) format.

        Returns:
            dict: The details of the specified tile.
        """
        x, y = tile
        if 0 <= y < self.maze_height and 0 <= x < self.maze_width:
            return self.tiles[y][x]
        else:
            logger.error(f"Invalid tile coordinate: {tile}")
            return None

    def get_nearby_tiles(self, tile, vision_r):
        """
        Retrieves all tiles within a given radius of a specified tile.

        Args:
            tile (tuple): Tile coordinates in (x, y) format.
            vision_r (int): Vision radius.

        Returns:
            list: A list of tile coordinates within the radius.
        """
        x, y = tile
        nearby_tiles = []
        for i in range(max(0, y - vision_r), min(self.maze_height, y + vision_r + 1)):
            for j in range(max(0, x - vision_r), min(self.maze_width, x + vision_r + 1)):
                nearby_tiles.append((j, i))
        return nearby_tiles

    def add_event_to_tile(self, tile, event):
        """
        Adds an event to a specified tile.

        Args:
            tile (tuple): Tile coordinates in (x, y) format.
            event (tuple): Event to be added.

        Returns:
            None
        """
        x, y = tile
        if 0 <= y < self.maze_height and 0 <= x < self.maze_width:
            self.tiles[y][x]["events"].add(event)
            logger.info(f"Event {event} added to tile {tile}.")
        else:
            logger.error(f"Invalid tile coordinate: {tile}")

    def remove_event_from_tile(self, tile, event):
        """
        Removes an event from a specified tile.

        Args:
            tile (tuple): Tile coordinates in (x, y) format.
            event (tuple): Event to be removed.

        Returns:
            None
        """
        x, y = tile
        if 0 <= y < self.maze_height and 0 <= x < self.maze_width:
            if event in self.tiles[y][x]["events"]:
                self.tiles[y][x]["events"].remove(event)
                logger.info(f"Event {event} removed from tile {tile}.")
            else:
                logger.warning(f"Event {event} not found in tile {tile}.")
        else:
            logger.error(f"Invalid tile coordinate: {tile}")

    def turn_pixel_to_tile(self, px_coordinate):
        """
        Converts pixel coordinates to tile coordinates.

        Args:
            px_coordinate (tuple): Pixel coordinates in (x, y) format.

        Returns:
            tuple: Tile coordinates in (x, y) format.
        """
        x = px_coordinate[0] // self.sq_tile_size
        y = px_coordinate[1] // self.sq_tile_size
        return (x, y)

    def get_address_tiles(self, address):
        """
        Retrieves all tile coordinates associated with a given address.

        Args:
            address (str): Address string.

        Returns:
            set: A set of tile coordinates associated with the address.
        """
        return self.address_tiles.get(address, set())
