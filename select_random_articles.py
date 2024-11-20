import json
import random

def main(input_file, output_file):
    try:
        with open(input_file, "r") as file:
            data = json.load(file)  # Load the JSON data
        
        # Ensure the input is a list
        if not isinstance(data, list):
            raise ValueError("Input JSON file must contain a list of objects.")
        
        # Randomly select 200 objects
        random_selection = random.sample(data, min(200, len(data)))  # Handles cases where less than 200 objects exist

        # Save the selected objects to a new JSON file
        with open(output_file, "w") as file:
            json.dump(random_selection, file, indent=4)
        
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {input_file}. Please check the file format.")
    except ValueError as ve:
        print(str(ve))
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main("remaining_articles.json", "open_coding.json")
    