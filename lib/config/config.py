import configparser
import os
import yaml
from lib.pdu import AppSettings, PduStruct, PinData
import xml.etree.ElementTree as ET
import clr
import html

# External libraries
clr.AddReference('System.Collections')

from System.Collections.Generic import List as LinkedList

# Application constant
CONFIG_SECTION_SCHEDULER = "Scheduler"
SCHEDULER_APPLICATION_FOLDER = "ApplicationFolder"
SCHEDULER_VIDEO_FOLDER = "VideoFolder"
SCHEDULER_VIDEO_PLAYER = "VideoPlayer"
SCHEDULER_VIDEO_PLAYER_PARAMS = "VideoPlayerParams"
SCHEDULER_START_TIME = "start_time"
SCHEDULER_END_TIME = "end_time"
SCHEDULER_CONTENT = "content"
SCHEDULER_MACHINE_ID = "ID"
SCHEDULER_PORT = "Port"
SCHEDULER_KEEP_ORDER = "KeepOrder"
SCHEDULER_STARTUP = "Startup"
CONFIG_SECTION_PINS = "Pins"
CONFIG_PIN_NAMES = "PinNes"
CONFIG_PIN_VALUES = "PinValues"
CONFIG_PIN_COUNT = "Count"
CONFIG_SECTION_PROJECTORS = "Projectors"
CONFIG_PROJECTOR_NAME = "NEC"
CONFIG_PROJECTOR_IP = "IP"
CONFIG_PROJECTOR_PORT = "PORT"
CONFIG_NEC_PROJECTOR_STATUS = "NEC_PJ_STATUS"

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

def load_app_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    return config

def loadSettings(file_path: str):
    '''
    Load settings

    Parameters:
    - path (str): path to the pdu configuration file

    Return: A AppSettings object containing the settings of the application
    '''
    configFile = configparser.ConfigParser()
    configFile.read(file_path)

    settings = AppSettings()
    settings.ApplicationFolder = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_APPLICATION_FOLDER]
    settings.VideoFolder = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_VIDEO_FOLDER]
    settings.VideoPlayer = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_VIDEO_PLAYER]
    settings.VideoPlayerParams = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_VIDEO_PLAYER_PARAMS]
    settings.StartTime = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_START_TIME]
    settings.EndTime = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_END_TIME]
    settings.Content = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_CONTENT]
    settings.MachineID = configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_MACHINE_ID]

    try:
        settings.Startup = bool(configFile[CONFIG_SECTION_SCHEDULER, SCHEDULER_STARTUP])
    except:
        settings.Startup = False

    try:
        # Server port
        settings.Port = int(configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_PORT])
    except:
        settings.Port = 8080 # Default value for the server port

    try:
        # Should the scheduler maintain the order of the content as listed in the interface
        settings.KeepOrder = bool(configFile[CONFIG_SECTION_SCHEDULER][SCHEDULER_KEEP_ORDER])
    except:
        settings.KeepOrder = False

    return settings

def loadPduSettings(path: str):
    '''
    Load Pdu Configuration

    Parameters:
    - path (str): path to the pdu configuration file

    Return: A PduStruct object representing the pdu configuration file.
    '''
    with open(path, 'r') as file:
        # Read the entire file content into a string
        file_content = file.read()

    # tree = ET.parse(path)
    # root = tree.getroot()
    root = ET.fromstring(html.unescape(file_content))

    # Load the data of the pdu configuration file into a PduStructt
    pdu = PduStruct(
        root.get("header"),
        root.get("mac"),
        int(root.get("flag")),
        root.get("ip"),
        root.get("subnet"),
        root.get("gateway"),
        int(root.get("port")),
        root.get("message"),
        root.get("other"),
    )

    # Retrieve the list of pdu Pins
    pins = LinkedList[PinData]()
    for pinNode in root.find("pins").findall('pin'):
        pin = PinData()
        pin.Pin = int(pinNode.get("channel"))
        pin.CanTurnOff = bool(pinNode.get("turnoff"))
        pin.DeviceName = pinNode.find("device").text
        
        # Optional elements
        # The followings nodes may not appear in every single pin
        if pinNode.find("device") is not None:
            pin.DeviceType = pinNode.find("type").text

        if pinNode.find("ip") is not None:
            pin.Ip = pinNode.find("ip").text
        
        try:
            portNode = pinNode.find("port")

            if portNode is not None:
                pin.Port = int(portNode.text)
        except:
            pass

        pins.Add(pin)
    
    # Attributes the list of pins to the Pdu
    pdu.Pins = pins

    return pdu


# Path to the config file
CONFIG_FILE_PATH = os.path.join('config', 'app.yaml')