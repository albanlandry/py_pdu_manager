from ui.app import MainWindow, PduEventHandler
from manager.pdu import PduController
from PyQt6.QtWidgets import QApplication
import sys
import lib.pdu as lib_pdu
from lib.pdu import ApplicationSettings, AppSettings, ConfigLoader, PduController, PduStatus, PduStruct
from lib.network import HttpRequest

if __name__ == '__main__':
    appsetting:AppSettings = ConfigLoader.LoadSettings(lib_pdu.app_config_file_path)
    pduConfig:PduStruct = ConfigLoader.LoadPDUSettings(lib_pdu.pdu_config_file_path)
    pduCtrl:PduController = PduController.GetInstance(5001)
    pduStatus:PduStatus = None # pduCtrl.Status(pduConfig)

    print(appsetting, pduConfig, pduStatus)


    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    # Update the pdu settings
    main.updatePdu(1, pduConfig, appsetting)

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