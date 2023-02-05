import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QSize, QTimer
import requests
import concurrent.futures
import time

id = 0
windowIdWithStartTime = {}
htmlContents = {}
sub_window_cordinates = {
    0: [20, 20],
    1: [1000, 20]
}

"""
This class for New Window
"""
class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QWebEngineView()
        self.page = self.view.page()
        self.startTime = 0
        self.windowId = None

    # set geometry for page
    def setPosition(self, windowId):
        cordinate = sub_window_cordinates[windowId]
        self.view.setGeometry(cordinate[0], cordinate[1], 720, 460)

    # setting new html content to page
    def HTML(self, html):
        self.page.setHtml(html)
        self.view.show()

    # closing the window
    def Close(self):
        self.view.close()

"""
Main Window class
"""
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # keeping references of two new sub windows in main window 
        self.windows = [
            AnotherWindow(), 
            AnotherWindow()
        ]
        # creating timers for two sub window
        self.timers = [QTimer(), QTimer()]
        self.setMinimumSize(QSize(920, 460))    
        self.setWindowTitle("Concurrent Programming Language Project") 
        self.text = QLabel(self)
        self.text.move(370, 40)
        self.text.resize(200, 50)
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('URL:')
        self.line = QLineEdit(self)
        self.line.move(370, 90)
        self.line.resize(200, 32)
        self.nameLabel.move(310, 90)
        pybutton = QPushButton('Click', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(370, 130)        

    # download html content from url
    def downloadSite(self, url):
        global result
        html = ""
        with requests.Session() as session:
            with session.get(url) as response:
                html = response.content.decode("UTF-8") 
        return html

    # closing all sub windows when main window closed
    def closeEvent(self, event):
        for w in self.windows:
            if w:
                w.Close()


    # when button clicked this will run
    def clickMethod(self):
        global id
        print('Entered Url: ' + self.line.text())
        urls = self.line.text().strip().split(" ")
        if  len(urls) != 0:
            for url in urls:
            # getting html content concurrently from urls
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.downloadSite, url)
                    return_html = future.result()
                    if id < 2:
                        self.windows[id].setPosition(id)
                        self.windows[id].HTML(return_html)
                        htmlContents[id] = return_html
                        self.windows[id].startTime = time.time()
                        windowIdWithStartTime[id] = time.time()
                        self.assignTimer(id)
                        id += 1
                    else:
                        windowId = calculateAge(time.time())
                        self.windows[windowId].close()
                        self.windows[windowId].setPosition(windowId)
                        self.windows[windowId].HTML(return_html)
                        htmlContents[windowId] = return_html
                        self.windows[windowId].startTime = time.time()
                        windowIdWithStartTime[windowId] = time.time()
                        self.assignTimer(windowId)
                    
        else:
            self.text.setText("Url should not be empty")

    # assigning a timer for sub window
    def assignTimer(self, windowId):
        self.timer = self.timers[windowId]
        self.timer.timeout.connect(lambda: self.afterTimeRefreshPage(windowId=windowId))
        self.timer.start(60000)

    # after timeout refresh page function
    def afterTimeRefreshPage(self, windowId):
        self.windows[windowId] = None
        refreshPage = AnotherWindow()
        self.windows[windowId] = refreshPage 
        return_html = htmlContents[windowId]
        self.windows[windowId].setPosition(windowId)
        self.windows[windowId].HTML(return_html)
        self.windows[windowId].startTime = windowIdWithStartTime[windowId]

# callculating age of windows
def calculateAge(newWindowTime):
    calcAge = {}
    for key, value in windowIdWithStartTime.items():
        calcAge[key] = newWindowTime - value
    return max(calcAge, key=calcAge.get)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    stylesheet = """
        MainWindow {
            background-image: url("background.jpg"); 
            background-repeat: no-repeat; 
        }
    """
    app.setStyleSheet(stylesheet)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )