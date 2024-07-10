import configparser
import os

def create_default_config(file_path):
    config = configparser.ConfigParser()

    # Define default settings
    config['Scheduler'] = {
        'ApplicationFolder': '',
        'VideoFolder': '',
        'CompressionLevel': '9'
    }
    config['bitbucket.org'] = {
        'User': 'hg'
    }
    config['topsecret.server.com'] = {
        'Port': '50022',
        'ForwardX11': 'no'
    }

    # Write the configuration file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def ensure_config_exists(file_path):
    if not os.path.exists(file_path):
        create_default_config(file_path)
        print(f"Created default config file at {file_path}")
    else:
        print(f"Config file already exists at {file_path}")

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    for section in config.sections():
        print(f"Section: {section}")
        for key in config[section]:
            print(f"  {key} = {config[section][key]}")

# Path to the config file
config_file_path = 'config.ini'
ensure_config_exists(config_file_path)
read_config(config_file_path)
