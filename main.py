from ui.app import App, MainWindow, Color
from manager.pdu import PduController
from PyQt6.QtWidgets import QApplication
import sys
import lib.pdu as lib_pdu
from lib.pdu import ApplicationSettings, AppSettings, ConfigLoader


if __name__ == '__main__':
    appsetting:AppSettings = ConfigLoader.LoadSettings(lib_pdu.app_config_file_path)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

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