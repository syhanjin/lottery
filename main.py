# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 创建主窗口
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setWindowTitle('抽号工具')
        self.setWindowIcon(QIcon('icons/lottery-win.png'))
        self.webview = QWebEngineView()
        self.webview.load(QUrl(QFileInfo('./html/main.html').absoluteFilePath()))
        self.setCentralWidget(self.webview)
        self.webview.urlChanged.connect(self.new_url)
    def new_url(self, p):
        self.webview.load(QUrl(p))


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())