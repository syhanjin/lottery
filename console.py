# -*- coding: utf-8 -*-
import os
import sys
from subprocess import Popen

from PyQt5.QtCore import QCoreApplication, QRect
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QPushButton
from win32api import ShellExecute

import utils


# 创建主窗口
class MainWindow(QMainWindow):
    btn = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("mainWindow")  # 设置窗口名
        self.setWindowTitle('抽号工具 控制台')  # 设置标题
        self.setWindowIcon(QIcon('icons/console.png'))  # 设置图标
        self.resize(800, 600)  # 重置大小
        # 引入字体
        self.font = QFont()
        self.font.setFamily("霞鹜文楷")
        self.font.setPointSize(14)
        self.font.setKerning(True)

        # 构建窗口内控件
        self.title = self.label('抽号工具 控制台', (300, 10, 200, 40))

        self.btn['load'] = self.button('导入', self.load, (150, 80, 100, 40))
        self.load_tip = self.label('请导入标准花名册', (270, 80, 200, 40))
        self.btn['clear'] = self.button('清除', self.clear, (150, 150, 100, 40))
        self.clear_tip = self.label('清除所有列表', (270, 150, 200, 40))
        self.btn['start'] = self.button('启动', self.start, (150, 220, 100, 40))
        self.start_tip = self.label('启动抽号器', (270, 220, 500, 40))
        self.cprt = self.label(
            '<html><head/><body><p align="center">©2020-2021 sakuyark.com 版权所有</p></body></html>', (0, 550, 800, 40)
        )
        self.cprt.setMouseTracking(True)
        self.explain = self.label(
            QCoreApplication.translate(
                "mainWindow",
                u"""<html><head/><body><p>本抽号器由 hanjin@Sakuyark 制作</p><p>Github: <a 
                href="https://github.com/syhanjin/lottery"><span style="text-decoration: underline; 
                color:#0000ff;">https://github.com/syhanjin/lottery</span></a></p><p><span 
                style="font-weight:600;">因为比较懒，数据方面比较简洁</span></p></body></html>""",
                None
            ),
            (150, 350, 500, 200)
        )

    def label(
            self,
            text: 'str',
            geometry: 'tuple[int, int, int, int]',
    ):
        """
        构建label控件
        :param text: 标签文本
        :param geometry: x, y, width, height
        """
        label = QLabel(self)
        if hasattr(self, 'font'):
            label.setFont(self.font)
        label.setText(text)
        label.setGeometry(QRect(*geometry))
        return label

    def button(
            self,
            text: 'str',
            action,
            geometry: 'tuple[int, int, int, int]'
    ) -> QPushButton:
        """
        构建button控件
        :param text: 按钮文本
        :param action: 点击事件
        :param geometry: x, y, width, height
        """
        btn = QPushButton(text, self)
        if hasattr(self, 'font'):
            btn.setFont(self.font)
        btn.setGeometry(QRect(*geometry))
        btn.clicked.connect(action)
        return btn

    def load(self):
        """
        导入名单，名单内至少包含两列 姓名 学号
        """
        self.load_tip.setText('准备导入...')
        try:
            fileName, fileType = QFileDialog.getOpenFileName(
                self,
                "导入", os.getcwd(), "excel(*.xls; *.xlsx; *.xlsm; *.xlsb)"
            )
            self.load_tip.setText('导入中...')
            utils.data.load(fileName)
            self.load_tip.setText('导入成功！')
        except Exception as e:
            print(e)
            self.load_tip.setText('导入失败！')

    def start(self):
        """
        启动抽号器主程序 main.exe or main.py
        """
        self.start_tip.setText('启动中...')
        try:
            if os.path.exists('main.exe'):
                ShellExecute(0, 'open', 'main.exe', '', '', 1)
            else:
                Popen(
                    'conda activate lottery&&python main.py', shell=True
                )
            self.start_tip.setText('启动成功！请等待窗口弹出...')
        except Exception as e:
            print(e)
            self.start_tip.setText('启动失败！')

    def clear(self):
        """
        清除已经导入的名单
        """
        self.clear_tip.setText('正在清除所有已导入的列表...')
        try:
            os.remove(utils.data.listjs)
            self.clear_tip.setText('清除成功！')
        except Exception as e:
            print(e)
            self.clear_tip.setText('清除失败！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())
