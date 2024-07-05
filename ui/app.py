import tkinter as tk
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject, QPoint, QSize, Qt, QTime
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QTimeEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor, QIcon, QPalette, QPixmap, QResizeEvent
from PyQt6.QtSvgWidgets import QSvgWidget
import os

path = os.path

CONFIG = {
    "res_folder": "res",
    "image_folder": "res/images" 
}

Channels = {"CH1": "PC", 
            "CH5": "", 
            "CH2": "빔프로젝터", 
            "CH6": "조명", 
            "CH3": "HDMI 리피터",
            "CH7": "",
            "CH4": "",
            "CH8": "앰프(오디오)"
            }

class App(tk.Tk):
    '''
    '''
    def __init__(self, title = "App", width = 800, height = 600):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")

class TitleBarWidget(QWidget):
    def __init__(self, title = "App", parent: QWidget = None):
        super().__init__(parent)
        # Create a horizontal layout for the title bar
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        title_layout = QVBoxLayout()

        # The title displayed on the title bar.
        titleLabel = LabelWidget(text=title, parent=parent, size=20, color="#ffffff", alignment=Qt.AlignmentFlag.AlignCenter)
        titleLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Addinig to the parent layoout.
        title_layout.addWidget(titleLabel)

        # Load icons
        close_icon = QIcon(path.join(CONFIG["image_folder"], "icons8-cross-100.png"))
        minimize_icon = QIcon(path.join(CONFIG["image_folder"], "icons8-minimize-50.png"))

        # Create custom buttons for close and minimize
        # Close buttons
        close_button = QPushButton()
        close_button.setObjectName("close_button")
        close_button.setIcon(close_icon)
        close_button.setIconSize(QSize(32, 32))
        close_button.setFixedSize(32, 32)
        close_button.setStyleSheet("#close_button{background-color: transparent; border: none; vertical-align: top;}")  # Set black background and remove border

        # Minimize buttons
        minimize_button = QPushButton()
        minimize_button.setObjectName("minimize_button")
        minimize_button.setIcon(minimize_icon)
        minimize_button.setFixedSize(30, 30)
        minimize_button.setIconSize(QSize(30, 30))
        minimize_button.setStyleSheet("#minimize_button{background-color: transparent; border: none;}")  # Set black background and remove border

        # Add buttons to the title bar layout
        title_bar_layout.addLayout(title_layout, 1)
        title_bar_layout.addWidget(minimize_button)
        title_bar_layout.addWidget(close_button)

        # Connect button signals to the appropriate slots
        close_button.clicked.connect(self.window().close)
        minimize_button.clicked.connect(self.window().showMinimized)

        # The widget container to be added as the title bar
        self.setLayout(title_bar_layout)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#414951"))
        self.setPalette(palette)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint((event.globalPosition() - self.oldPos).toPoint())
            self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
            self.oldPos = event.globalPosition()


class MainWindow(QMainWindow):
    spacing: int = 60
    '''
    '''
    def __init__(self, title: str = "", width: int = 800, height: int = 450):
        super().__init__()

        self.title = title
        self.width = width
        self.height = height
        self.initialize_layout()        

    def initialize_layout(self) -> None:
        self.setWindowTitle(self.title)
        self.setMinimumSize(QSize(self.width, self.height))

        # The widgets
        self.titleBar = TitleBarWidget("밀양 우주천문대, 스포츠센터 PC 스케줄러", self) # The title bar
        self.pduCtrl1 = self.createPduCtrl() # First pdu controller
        self.pduCtrl2 = self.createPduCtrl() # Second pdu controller
        self.bottomBar = QVBoxLayout()
        self.bottomBar.setContentsMargins(0, int(self.spacing/3), 0, int(self.spacing/3))
        self.bottomBar.addWidget(QLabel(text = "POPSLINE", parent = self))
        self.bottomBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottomBar = QWidget(self)
        bottomBar.setLayout(self.bottomBar)
        bottomBar.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #5E6A75;
            }""")

        # PDU layout
        pduLayout = QHBoxLayout()
        pduLayout.addWidget(self.pduCtrl1)
        pduLayout.addSpacing(80)
        pduLayout.addWidget(self.pduCtrl2)
        pduLayout.setContentsMargins(self.spacing, 0, self.spacing, 0)

        pduWidget = QWidget() # Holds the PDU layout
        pduWidget.setLayout(pduLayout)

        # Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addSpacing(8)
        self.mainLayout.addWidget(LabelWidget(text='담당자 외 제어금지', alignment= Qt.AlignmentFlag.AlignCenter, color="#FF0000"))
        self.mainLayout.addWidget(LabelWidget(text='주의 : 우주천문대의 PC는 PDU제어로 강제종료 하지 말것, 센서의 디바이스 연결이 끊길 수 있음\n부득이 한 상황 외 pdu 채널 off하지 말것', color="#5E6A75", alignment= Qt.AlignmentFlag.AlignCenter))
        self.mainLayout.addSpacing(4)
        self.mainLayout.addWidget(pduWidget)
        self.mainLayout.addWidget(bottomBar)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

        # Remove the decoration of the window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.CustomizeWindowHint)

    def createPduCtrl(self):
        '''
        '''
        pdu = PduControlWidget()
        return pdu
    
    def resizeEvent(self, evt):
        self.setFixedSize(evt.size())


class Color(QWidget):
    '''
    '''
    def __init__(self, color, w: int = 0, h: int = 0):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        if h > 0:
            self.setFixedHeight(h)

        if w > 0:
            self.setFixedWidth(h)

class LabelWidget(QLabel):
    def __init__(self, text: str = "", parent: QWidget = None, size: int = 12, sizeUnit = "px", color: str = "black",
                 weight: str|int = "normal", alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft):
        '''
        Parameters:
        - text (str): The text to be displayed.
        - parent (QWidget): The parent widget of the label.
        - size (int): The size of the text to be displayed, default is 12.
        - sizeUnit (str): The unit of the text to be displayed, default is "px".
        - color: str: The color of the text to be displayed, default is "black".
        - alignment: Qt.AlignmentFlag: The alignment of the text within the label.
        '''
        super().__init__(text=text, parent=parent)
        # Initialize the properties of the widget
        self.size = size
        self.sizeUnit = sizeUnit
        self.alignment = alignment
        self.color = color

        # Initialize the widget
        self.setAlignment(self.alignment)
        self.setStyleSheet(f"""
                        LabelWidget {{
                            font-size: {self.size}{self.sizeUnit};
                            font-weight: {weight};
                            color: {color};
                        }}""")

class ControlButtonWidget(QPushButton):
     '''
     '''
     def __init__(self, label: str = "", w: int = 50, h: int = 50,
                  color: str = "#84CE26", pressedColor: str = "darkgreen"):
        super().__init__()

        self.setText(label)
        self.setFixedSize(QSize(w, h))
        self.setStyleSheet("""
            QPushButton {{
                background-color: {color};
                color: white;
                font-weight: bold;
                border-radius: 8px; 
                border: none;
                text-align: center;
            }}
            QPushButton:pressed {{
                background-color: {pressedColor};
            }}
        """.format(color=color, pressedColor=pressedColor))

BUTTON_W = 64
BUTTON_H = 32

class ControlInputWidget(QWidget):
    spacing: int = 20
    '''
    '''
    def __init__(self, label: str =""):
        super().__init__()
    
        mLayout = QHBoxLayout()
        mLabel = LabelWidget(label, parent=self, size = 16, weight = 600, color="#5E6A75", alignment=Qt.AlignmentFlag.AlignVCenter)

        # Time input
        self.mTimeInput = QTimeEdit()
        self.mTimeInput.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.mTimeInput.setFixedHeight(BUTTON_H)
        self.mTimeInput.setDisplayFormat("HH:mm")
        self.mTimeInput.setTime(QTime.currentTime())
        self.mTimeInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.mTimeInput.setStyleSheet("""
        #     QTimeEdit {
        #         font-family: Arial;
        #         font-size: 14px;
        #         color: #5E6A75;
        #         background-color: white;
        #         border: 1px solid #B8C2CB;
        #         padding: 5px;
        #     }""")

        # Validate button
        self.validate = QPushButton(text="확인")
        self.validate.setFixedSize(64, 32)
        self.validate.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #dddddd;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 800;
                color: #5E6A75;
            }
                                    
            QPushButton:pressed{
                background-color: #dedede;
            }
        """)

        self.setObjectName("control-input-widget")

        # self.setStyleSheet(""" QWidget { background-color: transparent; border: none; } """)

        # Adding the widgets to the layout
        mLayout.addWidget(mLabel)
        mLayout.addSpacing(self.spacing)
        mLayout.addWidget(self.mTimeInput)
        mLayout.addSpacing(self.spacing)
        mLayout.addWidget(self.validate)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mLayout)
    
    def setTime(self, time: str|QTime):
        '''
        Sets the time displayed by the widget. It accepts a QTime object or a time string in HH:mm format.

        Parameters:
        - time (str|QTime): The time to set.
        '''
        if isinstance(time, str):
            self.mTimeInput.setTime(QTime.fromString(time))
        elif isinstance(time, QTime):
            self.mTimeInput.setTime(time)
        else:
            raise ValueError(f"Invalid time input. Expect [str|QTime], receive [{type(time)}]")


class SwitchWidget(QWidget):
     '''
     '''
     def __init__(self, label: str =""):
        super().__init__()

        self.mLayout = QVBoxLayout(self)
        self.mLayout.setContentsMargins(0, 0, 0, 0)
        self.labelUI = QLabel(text=label, parent=self)

        self.buttons_layout = QHBoxLayout()
        self.btnOn = ControlButtonWidget(label="ON", w=BUTTON_W, h=BUTTON_H)
        self.btnOff = ControlButtonWidget(label="OFF", w=BUTTON_W, h=BUTTON_H, color="#E3694E", pressedColor="crimson")
        
        # Putting the button together horizontally with a space in-between
        self.buttons_layout.addWidget(self.btnOn)
        # self.buttons_layout.addSpacing(4)
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.btnOff)

        container: QWidget = QWidget()
        container.setLayout(self.buttons_layout)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Adding elements to the container
        self.mLayout.addWidget(self.labelUI)
        self.mLayout.addWidget(container)

        self.setLayout(self.mLayout)


class ChannelWidget(QWidget):
    '''
    '''
    def __init__(self):
        super().__init__()

        mLayout = QGridLayout()
        mLayout.setHorizontalSpacing(35)

        #Adding all the buttons
        row = 0
        for index, (key, value) in enumerate(Channels.items()):
            switch = SwitchWidget(f"{key}: {value}")
            mLayout.addWidget(switch, row, index % 2)

            row = row + (index % 2)
        
        self.setLayout(mLayout)


class SectionWidget(QWidget):
    '''
    Widget for that presents a section with a time and a container
    the container can be modified before adding new widgets to the widget.
    '''
    def __init__(self, title: str = ""):
        super().__init__()

        self.contentWidget: QWidget = QWidget()
        self.contentLayout: QLayout = QVBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)

        self.contentWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contentWidget.setLayout(self.contentLayout)
        self.contentWidget.setContentsMargins(0, 0, 0, 0)
        
        self.mLayout = QVBoxLayout()
        self.mLayout.setSpacing(0)
        self.mLayout.setContentsMargins(0, 0, 0, 0)

        # Building the container of the title label
        # Title of the section container
        self.mTitle = QLabel(text=title)
        self.mTitle.setContentsMargins(0, 4, 0, 4)
        self.mTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mTitle.setStyleSheet("""
            QLabel {
                text-align: center;
                font-size: 16px;
                font-weight: 600;
                color: #5E6A75;
                border-left: 0px solid green;
                border-right: 0px solid red;
                border-top: 0px solid blue;
                border-bottom: 2px solid #B8C2CB;
            }
        """)

        # Layout that contains the title
        titleLayout = QHBoxLayout()
        titleLayout.setContentsMargins(60, 20, 60, 10)
        titleLayout.addWidget(self.mTitle)

        # The widget that contains the layout of the title
        titleWidget = QWidget()
        titleWidget.setLayout(titleLayout)
        
        # Adding widgets to the main container
        self.mLayout.addWidget(titleWidget)
        self.mLayout.addWidget(self.contentWidget)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mLayout)

    def setContainer(self, container: QLayout):
        '''
        Defines the main layout of the container
        '''
        self.contentLayout = container
        self.contentWidget.setLayout(self.contentLayout)

    def addWidget(self, wdg: QWidget):
        self.contentLayout.addWidget(wdg)
    

class PduControlWidget(QWidget):
    '''
    '''
    def __init__(self, title: str = ""):
        super().__init__()
        
        # Time configuration section
        self.timeSection = SectionWidget("우주천문대 PC")
        self.mStartTime = ControlInputWidget("시작시간")
        self.mEndTime = ControlInputWidget("종료시간")
        self.timeSection.addWidget(self.mStartTime)
        self.timeSection.addWidget(self.mEndTime)

        # PDU controller section
        self.pduSection = SectionWidget("PDU 채널 제어")
        self.pduChannels = ChannelWidget()
        self.pduChannels.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.pduSection.addWidget(self.pduChannels)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(self.timeSection)
        self.layout.addWidget(self.pduSection)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.setObjectName("pdu")
        # self.setStyleSheet("""
        #     QWidget {
        #         background-color: white;
        #         border: 2px solid #000000;
        #         border-radius: 20px;
        #     }
        # """)

        self.setLayout(self.layout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
