import clr
import os

from pprint import pprint


# Path to the currently running script
script_path = os.path.abspath(__file__)

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

print("Sub", Scheduler.__all__)
print("Sub", Scheduler.Models.__all__)
print("Sub", Scheduler.Logger.__all__)
# print("Sub", Scheduler.Exceptions.__all__)

pprint(Scheduler.__dict__)