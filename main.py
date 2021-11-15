# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 创建主窗口


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setWindowTitle('抽号工具')
        self.setWindowIcon(QIcon('icons/lottery-win.png'))
        self.webview = QWebEngineView()
        self.webview.load(
            QUrl(QFileInfo('./html/main.html').absoluteFilePath()))
        self.setCentralWidget(self.webview)
        self.webview.loadFinished.connect(self.call_js)
    
    def call_js(self):
        self.webview.page().runJavaScript(
            'change_tab("number", false)'
        )


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())
