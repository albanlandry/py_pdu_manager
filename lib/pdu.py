import clr
import os
from pprint import pprint
import xml.etree.ElementTree as ET
import html

# Path to the currently running script
script_path = os.path.abspath(__file__)
# app_config_file_path = os.path.join(os.path.dirname(script_path), "..", "config", "config.cnf")
app_config_file_path = "/Volumes/Storage/Python/PDUManager/config/config.cnf"

# pdu_config_file_path = os.path.join(os.path.dirname(script_path), "..", "config", "pdu.config.xml")
pdu_config_file_path = "/Volumes/Storage/Python/PDUManager/config/pdu.config.xml"

# Add reference to the DLL
clr.AddReference(os.path.join(os.path.dirname(script_path), "pdu_lib", "pdu_library.dll"))
clr.AddReference('System.Windows.Forms')

from pdu_library import PDUStruct, PDUController
from Scheduler.Models import PinData
from Scheduler import ConfigLoader as ConfLdr, ApplicationSettings as appsettings
import Scheduler

PduStruct = PDUStruct
PduController = PDUController
ConfigLoader = ConfLdr
ApplicationSettings = appsettings
AppSettings = ApplicationSettings.Settings

def loadPDUConfig(path: str = pdu_config_file_path):
    file_content = ''
    with open(path, 'r') as file:
        # Read the entire file content into a string
        file_content = file.read()

    pduDataXml = ET.fromstring(html.unescape(file_content))
    # Print the file content
    print(ET.fromstring(html.unescape(file_content)))

    return pduDataXml
# print(app_config_file_path, pdu_config_file_path)
print("Sub", Scheduler.__all__)
print("Sub", Scheduler.Models.__all__)
print("Sub", Scheduler.Logger.__all__)
# # print("Sub", Scheduler.Exceptions.__all__)
pprint(Scheduler.__dict__)

# # Parse the XML file
# tree = ET.parse(pdu_config_file_path)
# root = tree.getroot()

# print(os.path.exists(pdu_config_file_path))
# pduConfig:PDUStruct = ConfigLoader.LoadPDUSettings(pdu_config_file_path)
# appsetting:AppSettings = ConfigLoader.LoadSettings(app_config_file_path) # type: ignore
# # appsetting:ApplicationSettings.Settings = ConfigLoader.LoadSettings(app_config_file_path) # type: ignore

# print(ConfigLoader.IsValid(appsetting))
# print(pduConfig.Ip)
# # print(root)

# print(f"{ConfigLoader.LoadSettings()}")