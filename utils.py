from PyQt5.QtWebEngineWidgets import QWebEngineView
from requests import get
from bs4 import BeautifulSoup as BS
from PyQt5.QtWidgets import QTabWidget, QTabBar, QPushButton, QInputDialog, QWidget
from PyQt5.QtCore import *


class TabBarPlus(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = pyqtSignal()

    def __init__(self, parent):
        super(TabBarPlus, self).__init__(parent)

        #self.setStyleSheet(
        """
            QTabBar::tab {
                width: 80px;
            }
           QTabBar::tab:selected {
                font-family: Roboto;
                font-size: 18px;
                font: italic;
                color: rgb(0,0,0,255);
                background: rgb(234,234,234,255);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border:1px;
                border-color: rgb(197,197,199,255);
                border-top-style: solid;
                border-right-style: solid;
                border-left-style: solid;
                padding: 10px 50px 10px 24px;
           }
           QTabBar::tab:!selected{
                font-family: Roboto;
                font-size: 18px;
                font: italic;
                color: rgb(255,255,255,255);
                background: rgb(175,175,175,255);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
               border:1px;
                border-color: rgb(197,197,199,255);
                border-top-style: solid;
                border-right-style: solid;
                border-bottom-style: ;
                border-left-style: solid;
                padding: 10px 50px 10px 24px;
            }
        """#)
        # Plus Button
        self.plusButton = QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(20, 20) # Small Fixed size
        self.plusButton.setMinimumSize(20, 20) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location
    # end Constructor

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+25, height)
    # end tabSizeHint

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super().resizeEvent(event)

        self.movePlusButton()
    # end resizeEvent

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super().tabLayoutChange()

        self.movePlusButton()
    # end tabLayoutChange

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            super(TabBarPlus, self).mouseDoubleClickEvent(event)

        idx = self.currentIndex()
        ok = True
        self.input_dialog = QInputDialog()
        print(type(self.input_dialog.textEchoMode()))

        newName, ok = QInputDialog.getText(self, 'Mudar nome',
                                        'Novo nome:')

        if ok:
            self.setTabText(idx, newName)

    def open_kb(self):
        print("open keyboard")



    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size, h)

    # end movePlusButton
# end class MyClass

class NewTab(QWidget):
    def __init__(self, parent:QTabWidget):
        super().__init__()
        self.parent:QTabWidget = parent
        self.parent.currentChanged.connect(self.handleNewTab)

    def handleNewTab(self, index):
        if self.parent.widget(index) == self:
            self.parent.insertTab(index, WebView(self.parent), '')
            self.parent.setCurrentIndex(index)


class WebTab(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.barPlus = TabBarPlus(self)
        self.setTabBar(self.barPlus)
        self.addTab(WebView(self, 'https://google.com'), '')
        #self.addTab(NewTab(self), '+')

    def addTab(self, widget, text):
        if type(widget) == WebView:
            widget.pageChangeSgn.connect(self.setTabText)
        return super().addTab(widget, text)

    def insertTab(self, index:int, widget, text:str):
        if type(widget) == WebView:
            widget.pageChangeSgn.connect(self.setTabText)
        return super().insertTab(index, widget, text)

    def setTabText(self, index: int, a1: str) -> None:
        print(a1)
        return super().setTabText(index, a1)

class WebView(QWebEngineView):
    backwardSgn = pyqtSignal()
    forwardSgn = pyqtSignal()
    pageChangeSgn = pyqtSignal(int, str)

    def __init__(self, parent:QTabWidget, url:str=None):
        super().__init__(parent)
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.setMouseTracking(True)
        self.cookies = self.page().profile().cookieStore()
        self.installEventFilter(self)
        self.parent:QTabWidget = parent
        self.urlChanged.connect(self.updateTabText)
        if url:
            self.goto(url)

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
    

    def updateTabText(self, url:QUrl):
        ans = get(url.toString(), headers=self.header)
        soup = BS(ans.content, 'html.parser')
        title = soup.title.string
        if title:
            self.pageChangeSgn.emit(self.parent.indexOf(self), title)