from utils import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sys import argv
import keyboard as kb


class KeyboardShortcuts(QObject):
    showSgn = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        kb.add_hotkey('alt+shift+k', self.showSgn.emit, suppress=True)


class Test(QWidget):
    closeSgn = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.tab = WebTab(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.setWindowFlag(Qt.Tool)
        self.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closeSgn.emit()
        return super().closeEvent(a0)

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.manager = KeyboardShortcuts(self)
        self.manager.showSgn.connect(self.start)
        self.win =None

    def start(self):
        if not self.win:
            self.win = Test()
            self.win.closeSgn.connect(self.start)
        else:
            self.win.close()
            self.win = None
            

if __name__=='__main__':
    app = App(argv)
    app.exec()
