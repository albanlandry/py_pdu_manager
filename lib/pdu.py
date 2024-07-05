import clr
import os
import importlib
import pkgutil
import sys

from pprint import pprint

def find_abs_modules(module):
    path_list = []
    spec_list = []
    for importer, modname, ispkg in pkgutil.walk_packages(module.__path__):
        import_path = f"{module.__name__}.{modname}"
        if ispkg:
            spec = pkgutil._get_spec(importer, modname)
            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        else:
            path_list.append(import_path)
    for spec in spec_list:
        del sys.modules[spec.name]
    return path_list

# Path to the currently running script
script_path = os.path.abspath(__file__)

# Add reference to the DLL
clr.AddReference(os.path.join(os.path.dirname(script_path), "pdu_lib", "pdu_library.dll"))
clr.AddReference('System.Windows.Forms')

from pdu_library import PDUStruct, PDUController
from Scheduler.Models import PinData
import Scheduler

PduStruct = PDUStruct
PduController = PDUController

print("Sub", Scheduler.__all__)
print("Sub", Scheduler.Models.__all__)
print("Sub", Scheduler.Logger.__all__)
# print("Sub", Scheduler.Exceptions.__all__)

pprint(Scheduler.__dict__)