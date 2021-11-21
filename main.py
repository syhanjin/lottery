# -*- coding: utf-8 -*-

import sys
from utils import prpc
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView


# 创建主窗口
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 重置大小
        self.resize(800, 600)
        # 设置标题
        self.setWindowTitle('抽号工具')
        # 设置图标
        self.setWindowIcon(QIcon('icons/lottery-win.png'))
        # 浏览器空间
        self.webview = QWebEngineView()
        # 指定页面
        self.webview.load(
            QUrl(QFileInfo('./html/main.html').absoluteFilePath()))
        self.setCentralWidget(self.webview)
        # 加载完成后后台对前端进行一些处理
        self.webview.loadFinished.connect(self.call_js)
    
    def call_js(self):
        # 解码加密的名单
        self.webview.page().runJavaScript(
            f'list_decrypt("{prpc.key.decode("utf-8")}")'
        )
        # 将页面设置为 学号模式
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
