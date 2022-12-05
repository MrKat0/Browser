from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import *

class WebView(QWebEngineView):
    backwardSgn = pyqtSignal()
    forwardSgn = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.cookies = self.page().profile().cookieStore()
        self.installEventFilter(self)

    def goto(self, url:str):
        self.load(QUrl(url))

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:

        if type(event) == QChildEvent:
            event.child().installEventFilter(self)

        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.BackButton:
                self.back()
            if event.button() == Qt.MouseButton.ForwardButton:
                self.forward()
            

        return super().eventFilter(obj, event)
    