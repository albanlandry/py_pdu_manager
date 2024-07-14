from ui.app import MainWindow, PduEventHandler, SwitchButton
from manager.pdu import PduController
from PyQt6.QtWidgets import QApplication
import sys, os
import lib.pdu as lib_pdu
from lib.pdu import ApplicationSettings, AppSettings, ConfigLoader, PduController, PduStatus, PduStruct
from lib.network import HttpRequest
from lib.config import config

def onChannelPressed(args):
    pduConfig:PduStruct = ConfigLoader.LoadPDUSettings(lib_pdu.pdu_config_file_path)
    
    print(f"IP: {pduConfig.Ip}")
    
    if(args.status == SwitchButton.ON):
        pduCtrl.TurnPinOn(pduConfig, args.channel + 1)
    elif args.status == SwitchButton.OFF:
        pduCtrl.TurnPinOff(pduConfig, args.channel + 1)

def onChannelPressed2(args):
    pduConfig:PduStruct = ConfigLoader.LoadPDUSettings(lib_pdu.pdu_config_file_path)
    
    print(f"IP: {pduConfig.Ip}")
    
    if(args.status == SwitchButton.ON):
        pduCtrl.TurnPinOn(pduConfig, args.channel + 1)
    elif args.status == SwitchButton.OFF:
        pduCtrl.TurnPinOff(pduConfig, args.channel + 1)

if __name__ == '__main__':
    appconfig = config.load_app_config(os.path.join(os.path.dirname(__file__), config.config_file_path))

    print(lib_pdu.pdu_config_file_path)
    print(lib_pdu.pdu_config_file_path2)

    # PDU 1
    appsetting:AppSettings = ConfigLoader.LoadSettings(lib_pdu.app_config_file_path)
    pduConfig:PduStruct = ConfigLoader.LoadPDUSettings(lib_pdu.pdu_config_file_path)
    
    # PDU 2
    appsetting2:AppSettings = ConfigLoader.LoadSettings(lib_pdu.app_config_file_path2)
    pduConfig2:PduStruct = ConfigLoader.LoadPDUSettings(lib_pdu.pdu_config_file_path2)

    pduEvent1 = PduEventHandler()
    pduEvent1.pduEvent.onChannelPressed = onChannelPressed
    
    pduEvent2 = PduEventHandler()
    pduEvent2.pduEvent.onChannelPressed = onChannelPressed2
   
    # onChannelPressed = Callable[[bool], None]
 
    # pduEvent1.timeEvent.onEndTimeChanged

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    print(f"ip adrress1: {pduConfig.Ip}")
    print(f"ip adrress2: {pduConfig2.Ip}")

    # Update the pdu settings
    main.updatePdu(1, pduConfig, appsetting, pduEvent1)
    main.updatePdu(2, pduConfig2, appsetting2, pduEvent2)

    # Setting the global style of the application.
    app.setStyleSheet("""
        QMainWindow {
            background-color: #EBEBEB;
        }
        QWidget#pdu {
            background-color: white;
            border: 2px solid #B8C2CB;
            border-radius: 29px;
        }
    """)

    app.exec()

    
    ''' Events handling functions '''
    def onValidateEndTime():
        pass

    def onValidateStartTime():
        pass