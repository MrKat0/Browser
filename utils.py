from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData, QWebEnginePage as WebPage
from PyQt5.QtWidgets import QTabWidget, QMenu, QAction, QWidget, QTabBar, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from requests import get
from bs4 import BeautifulSoup as BS


class NewTab(QWidget):
    def __init__(self, parent:QTabWidget):
        super().__init__()
        self.parent = parent
        self.parent.currentChanged.connect(self.handleNewTab)

    def handleNewTab(self, index, url=None):
        if self.parent.widget(index) == self:
            self.parent.insertTab(index, WebView(self.parent))
            self.parent.setCurrentIndex(index)


class CloseBtn(QPushButton):
    def __init__(self, parent):
        super().__init__(parent, text='x')
        self.setFixedSize(12, 12)
        self.setStyleSheet('''text-align: center;
                                    color: white;
                                    background-color: red;
                                    border-style: outset;''')


class WebTab(QTabWidget):
    tabChangeSgn = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.addTab(WebView(self, 'https://google.com'))
        super().addTab(NewTab(self), '+')
        self.currentChanged.connect(lambda: self.tabChangeSgn.emit(self.currentWidget().getUrl()))

    def addTab(self, widget):
        widget.pageChangeSgn.connect(self.setTabText)
        widget.newTabSgn.connect(self.newTab)
        super().addTab(widget, '')
        btn = CloseBtn(self)
        btn.clicked.connect(lambda: self.removeTab(self.indexOf(widget)))
        self.tabBar().setTabButton(self.indexOf(widget), QTabBar.RightSide, btn)

    def insertTab(self, index:int, widget):
        widget.pageChangeSgn.connect(self.setTabText)
        widget.newTabSgn.connect(self.newTab)
        super().insertTab(index, widget, str(index))
        btn = CloseBtn(self)
        btn.clicked.connect(lambda: self.removeTab(self.indexOf(widget)))
        self.tabBar().setTabButton(self.indexOf(widget), QTabBar.RightSide, btn)

    def newTab(self, source, url):
        index = self.indexOf(source) + 1
        widget = WebView(self, url)
        self.insertTab(index, widget)

    def setTabText(self, index: int, text: str):
        return super().setTabText(index, text)

class WebView(QWebEngineView):
    backwardSgn = pyqtSignal()
    forwardSgn = pyqtSignal()
    pageChangeSgn = pyqtSignal(int, str)
    newTabSgn = pyqtSignal(QWidget, str)

    def __init__(self, parent: WebTab, url:str = None):
        super().__init__(parent)
        self.header = {'User-Agent': 'Qui-kitty Browser/0.3.2 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.setMouseTracking(True)
        self.cookies = self.page().profile().cookieStore()
        self.cookies.deleteAllCookies()
        self.installEventFilter(self)
        self.urlChanged.connect(self.updateTabText)
        self.page().installEventFilter(self)
        self.cntxAction = WebPage.WebAction
        if url:
            self.goto(url)

    def goto(self, url:str):
        self.load(QUrl(url))

    def eventFilter(self, obj: 'QObject', event:QEvent or QChildEvent) -> bool:
       
        if type(event) == QChildEvent:
            event.child().installEventFilter(self)
            if type(event.child()) == QMenu:
                menu:QMenu = event.child()
                event.child().installEventFilter(self)
            if type(event.child()) == QActionEvent:
                print(event.data())

        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.BackButton:
                self.back()
            if event.button() == Qt.MouseButton.ForwardButton:
                self.forward()

        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Left and event.modifiers() == Qt.ControlModifier:
                self.back()
            if event.key() == Qt.Key.Key_Right and event.modifiers() == Qt.ControlModifier:
                self.forward()
        return super().eventFilter(obj, event)

    def updateTabText(self, url:QUrl):
            try:
                ans = get(url.toString(), headers=self.header)
                soup = BS(ans.content, 'html.parser')
                title = soup.title.string
                if title:
                    self.pageChangeSgn.emit(self.parentWidget().indexOf(self), title)
            except:
                pass

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        data = self.page().contextMenuData()

        newTab = self.page().action(self.cntxAction.OpenLinkInNewTab)
        newTab.triggered.connect(lambda: self.newTabSgn.emit(self, data.linkUrl().toString()))
        print(data.linkText())

        super().contextMenuEvent(a0)

    def getUrl(self):
        return self.url().toString()
