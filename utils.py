from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *

class WebView(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)
        cookies = self.page().profile().cookieStore()

    def goto(self, url:str):
        self.load(QUrl(url))