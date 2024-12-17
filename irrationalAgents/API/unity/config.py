import json

class Config:
    """
    A class to manage configuration files for simulations.
    """

    @staticmethod
    def get_sim_config(sim_name):
        """
        Retrieves the simulation configuration JSON file.
        
        Args:
            sim_name (str): The name of the simulation.
        
        Returns:
            dict: The contents of the simulation configuration file.
        """
        file_path = f'../storage/sample_data/{sim_name}/{sim_name}.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def get_spawn_config(sim_name):
        """
        Retrieves the spawn configuration JSON file for a simulation.
        
        Args:
            sim_name (str): The name of the simulation.
        
        Returns:
            dict: The contents of the spawn configuration file.
        """
        file_path = f'../storage/sample_data/{sim_name}/agents/spawn.json'  # Correct path
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")