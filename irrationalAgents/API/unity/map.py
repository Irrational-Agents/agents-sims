from logger_config import setup_logger
import json
import csv
import numpy as np

logger = setup_logger('Map-translator')


class Map:
    def __init__(self, data):
        """
        Initializes the MapTranslator with metadata, map data, and block data.

        Args:
            map_data (dict): Contains the raw maze matrices.
            meta_data (dict): Contains metadata like maze dimensions and tile size.
            block_data (dict): Contains information about arena, game objects, sectors, and spawning locations.
        """
        meta_data = data['mapMeta']
        map_data = data['mapData']
        block_data = data['blockData']

        self.maze_width = meta_data["maze_width"]
        self.maze_height = meta_data["maze_height"]
        self.sq_tile_size = meta_data["sq_tile_size"]

        self.collision_maze = self.parse_maze(map_data['collision_maze'])
        self.sector_maze = self.parse_maze(map_data['sector_maze'])
        self.arena_maze = self.parse_maze(map_data['arena_maze'])
        self.game_object_maze = self.parse_maze(map_data['game_object_maze'])
        self.spawning_location_maze = self.parse_maze(map_data['spawning_location_maze'])

        self.arena_blocks = self.id_based_dict(block_data["arena_blocks"])
        self.game_object_blocks = self.id_based_dict(block_data["game_object_blocks"])
        self.sector_blocks = self.id_based_dict(block_data["sector_blocks"])
        self.spawning_location_blocks = self.id_based_dict(block_data["spawning_location_blocks"])

        self.tiles = self.initialize_tiles()
        self.address_tiles = self.initialize_address_tiles()


    def id_based_dict(self,data):
        """convert json to id"""
        return {
            entry['id']: {key: str(value) for key, value in entry.items() if key != 'id'}
            for entry in data
        }

    def parse_maze(self, text):
        """
        Convert a comma-separated text into a 2D NumPy maze matrix.
        """
        # Initialize the maze matrix
        maze_matrix = np.zeros((self.maze_height, self.maze_width), dtype=int)

        # Convert the comma-separated text into a list of integers
        data = list(map(lambda x: x.strip(), text.split(',')))

        # Validate that the input matches the expected size
        expected_size = self.maze_height * self.maze_width
        if len(data) != expected_size:
            raise ValueError(f"Input data size ({len(data)}) does not match the maze size ({expected_size}).")

        # Fill the matrix row by row
        k = 0
        for i in range(maze_matrix.shape[0]):  # Loop over rows
            for j in range(maze_matrix.shape[1]):  # Loop over columns
                maze_matrix[i, j] = data[k]
                k += 1

        return maze_matrix
    
    def add_npc_to_tile(self, npc_name, tile):
        x, y = tile
        if 0 <= y < self.maze_height and 0 <= x < self.maze_width:
            self.tiles[y][x]['npc'] = npc_name
        else:
            logger.error(f"Invalid tile coordinate: {tile}")
            return None

        
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
                # Retrieve maze block values
                sector_data = self.sector_blocks.get(self.sector_maze[i][j], {})
                arena_data = self.arena_blocks.get(self.arena_maze[i][j], {})
                spawn_data = self.spawning_location_blocks.get(self.spawning_location_maze[i][j], {})
                item_value = self.game_object_blocks.get(self.game_object_maze[i][j], "")

                # Build tile details
                tile_details = {
                    "collision": self.collision_maze[i][j] != 0,
                    "location": sector_data.get("location", ""),  # Previously sector
                    "room": arena_data.get("room", ""),          # Previously arena
                    "item": item_value,                          # Previously game_object
                    "space": spawn_data.get("space", ""),        # spawn location detail
                    "spawning_location": {
                        "location": spawn_data.get("location", ""),
                        "room": spawn_data.get("room", ""),
                        "space": spawn_data.get("space", "")
                    },
                    "events": set(), # events can be anything, like you can set events on tiles that sale is going on
                    "npc": '_' 
                }

                # Add default event for items
                if tile_details["item"]:
                    object_name = f"{tile_details['room']}:{tile_details['item']}"
                    tile_details["events"].add((object_name, None, None))

                row.append(tile_details)
            tiles.append(row)

        logger.info("Tiles initialized.")
        return tiles

    def initialize_address_tiles(self):
        """
        Creates a reverse mapping from addresses to tile coordinates.

        Returns:
            dict: A dictionary mapping addresses to sets of tile coordinates.
        """
        address_tiles = {}

        def add_address(address, x, y):
            """Helper to add an address and coordinate pair to the mapping."""
            if address not in address_tiles:
                address_tiles[address] = set()
            address_tiles[address].add((x, y))

        for i in range(self.maze_height):
            for j in range(self.maze_width):
                tile = self.tiles[i][j]
                
                # Build addresses based on available data
                location = tile.get("location", "")
                room = tile.get("room", "")
                item = tile.get("item", "")
                spawning_location = tile.get("spawning_location", {}).get("location", "")

                if location:
                    add_address(location, j, i)
                if room:
                    add_address(f"{location}:{room}", j, i)
                if item:
                    add_address(f"{room}:{item}", j, i)
                if spawning_location:
                    add_address(f"<spawn_loc>{spawning_location}", j, i)

        logger.info("Address tiles initialized.")
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
