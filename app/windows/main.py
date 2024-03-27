from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget

class JotaleaWebView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(JotaleaWebView, self).__init__(*args, **kwargs)

        self.window = QWidget()
        self.window.setWindowTitle("TaskHub")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.bar_url = QTextEdit()
        self.bar_url.setMaximumHeight(30)

        self.btn_go = QPushButton("Go")
        self.btn_go.setMinimumHeight(30)

        self.btn_back = QPushButton("<")
        self.btn_back.setMinimumHeight(30)

        self.btn_forward = QPushButton(">")
        self.btn_forward.setMinimumHeight(30)

        self.horizontal.addWidget(self.bar_url)
        self.horizontal.addWidget(self.btn_go)
        self.horizontal.addWidget(self.btn_back)
        self.horizontal.addWidget(self.btn_forward)

        self.browser = QWebEngineView()

        #self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl("http://tarea.jotalea.com.ar"))

        self.window.setLayout(self.layout)
        self.window.show()


app = QApplication([])
window = JotaleaWebView()
app.exec_()
