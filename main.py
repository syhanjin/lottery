# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QFileInfo, QUrl, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QAction, QApplication, QLabel, QMainWindow, QMenu, QSystemTrayIcon, QWidget,
)

from utils import prpc


# 创建主窗口
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = QIcon('icons/lottery-win.png')
        self.popup = Popup()
        self.popup.MainShow.connect(self.show)
        self.popup.show()
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(self.icon)
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        # 重置大小
        self.resize(800, 600)
        # 设置标题
        self.setWindowTitle('抽号工具')
        # 设置图标
        self.setWindowIcon(self.icon)
        # 浏览器空间
        self.webview = QWebEngineView()
        # 指定页面
        self.webview.load(
            QUrl(QFileInfo('./html/main.html').absoluteFilePath())
        )
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

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

    # def eventFilter(self, widget, event):
    #     if event.type() == QEvent.FocusOut:
    #         self.popup.show()
    #         self.hide()
    #         return False
    #     return False

    def quit(self):
        self.popup.close()
        self.close()
        sys.exit(0)


class Popup(QWidget):
    MainShow = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_Position = None
        self.image = None
        self.moved = None
        self.setObjectName("popup")  # 设置窗口名
        self.m_flag = False
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # QApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
        # QApplication.setAttribute(Qt.AA_NativeWindows, False)
        # self.setAttribute(Qt.WA_DontCreateNativeAncestors)
        desktop = QApplication.desktop()
        self.size = (desktop.width(), desktop.height())
        self.setGeometry(int(self.size[0] * 0.02), int(self.size[1] * 0.7), 50, 50)
        self.setWindowOpacity(0.5)
        self.setupUi()

    def setupUi(self):
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap("icons/lottery-win.png"))
        self.image.setGeometry(0, 0, 50, 50)
        fp = "icons/lottery-win.png"
        img = QImage(fp)

        # self.image = QPushButton(self)
        self.image.setObjectName("image")

        self.image.setFixedWidth(50)
        self.image.setFixedHeight(50)

        # 按照label1的尺寸缩放图片
        result = img.scaled(self.image.width(), self.image.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # icon1 = QIcon()
        # icon1.addPixmap(QPixmap(fp), QIcon.Normal, QIcon.Off)
        # self.image.setIcon(icon1)
        # self.image.setIconSize(QSize(50, 50))
        self.image.setPixmap(QPixmap.fromImage(result))
        self.image.setStyleSheet("""#image{background-color: rgba(255, 255, 255, 128);border-radius: 25px;}""")
        # self.image.clicked.connect(self.click)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moved = False
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            self.moved = True
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        if not self.moved:
            self.click()

    @pyqtSlot()
    def click(self):
        # self.hide()
        self.MainShow.emit()


# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow()
    browser.show()
    # popup = Popup()
    # popup.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())
