import yaml

def load_folders(yaml_path):
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == '__main__':
    try:
        folders = load_folders('./data/folders_path.yml')
        print("Loaded folders:", folders)
    except yaml.YAMLError as e:
        print("Error loading YAML file:", e)