# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGroupBox, QLineEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.Qt import QFont, QIntValidator, QDoubleValidator
import sys
import win32process
import win32api
import ctypes
import win32gui
import time


class checkKRHD(QThread):
    KRHDID = pyqtSignal(int)

    def __init__(self, parent=None):
        super(checkKRHD, self).__init__(parent)

    def run(self):
        while True:
            window = win32gui.FindWindow("UnityWndClass", "Kingdom Rush HD")
            self.KRHDID.emit(window)
            time.sleep(0.5)


class checkTotalWave(QThread):
    totalWave = pyqtSignal(int)

    def __init__(self, parent=None, phand=None, moduleHd=None):
        super(checkTotalWave, self).__init__(parent)
        self.phand = phand
        self.moduleHd = moduleHd

    def run(self):
        data = ctypes.c_long()
        kernelDll = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32.dll")
        kernelDll.ReadProcessMemory(int(self.phand), self.moduleHd + 0x20A554, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x10, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x238, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x0, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x8, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x20, ctypes.byref(data), 4, None)
        kernelDll.ReadProcessMemory(int(self.phand), data.value + 0xC, ctypes.byref(data), 4, None)
        self.totalWave.emit(data.value)


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(347, 347)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(u'KR1 Steam版 V2.2 跳波修改器')
        self.showMSG = QLabel(self)
        self.showMSG.setGeometry(QRect(30, 10, 300, 15))
        self.showChange = QLabel(self)
        self.showChange.setGeometry(QRect(200, 10, 147, 15))

        self.moneyGroup = QGroupBox(self)
        self.moneyGroup.setGeometry(QRect(23, 40, 300, 80))
        self.moneyGroup.setTitle(u'修改金钱 ')
        self.moneyLineEdit = QLineEdit(self)
        self.moneyLineEdit.setValidator(QIntValidator())
        self.moneyLineEdit.setGeometry(QRect(40, 65, 180, 35))
        self.moneyLineEdit.setText('10000')
        self.moneyLineEdit.setStyleSheet('color:#4F4F4F;')
        self.moneyLineEdit.setFont(QFont('Arial', 15))
        self.moneyButton = QPushButton(self)
        self.moneyButton.setGeometry(QRect(238, 64, 65, 37))
        self.moneyButton.setText(u'修改')
        self.moneyButton.clicked.connect(self.moneyModify)

        self.enemyHealthGroup = QGroupBox(self)
        self.enemyHealthGroup.setGeometry(QRect(23, 140, 300, 80))
        self.enemyHealthGroup.setTitle(u'修改Hard难度敌人血量倍数')
        self.enemyHealthLineEdit = QLineEdit(self)
        self.enemyHealthLineEdit.setValidator(QDoubleValidator())
        self.enemyHealthLineEdit.setGeometry(QRect(40, 165, 180, 35))
        self.enemyHealthLineEdit.setText('2.5')
        self.enemyHealthLineEdit.setStyleSheet('color:#4F4F4F;')
        self.enemyHealthLineEdit.setFont(QFont('Arial', 15))
        self.enemyHealthButton = QPushButton(self)
        self.enemyHealthButton.setGeometry(QRect(238, 164, 65, 37))
        self.enemyHealthButton.setText(u'修改')
        self.enemyHealthButton.setEnabled(False)
        self.enemyHealthLineEdit.setEnabled(False)
#         self.enemyHealthButton.clicked.connect(self.enemyHealthModify)

        self.enemyWaveGroup = QGroupBox(self)
        self.enemyWaveGroup.setGeometry(QRect(23, 240, 300, 80))
        self.enemyWaveGroup.setTitle(u'跳波功能 这关共有 0 波敌人')
        self.enemyWaveLineEdit = QLineEdit(self)
        self.enemyWaveLineEdit.setValidator(QIntValidator())
        self.enemyWaveLineEdit.setGeometry(QRect(40, 265, 180, 35))
        self.enemyWaveLineEdit.setText('0')
        self.enemyWaveLineEdit.setStyleSheet('color:#4F4F4F;')
        self.enemyWaveLineEdit.setFont(QFont('Arial', 15))
        self.enemyWaveButton = QPushButton(self)
        self.enemyWaveButton.setGeometry(QRect(238, 264, 65, 37))
        self.enemyWaveButton.setText(u'修改')
        self.enemyWaveButton.clicked.connect(self.skipWave)

        self.checkTotalWave = None
#         self.widgetList = [self.moneyLineEdit, self.moneyButton, self.enemyHealthLineEdit, self.enemyHealthButton, self.enemyWaveLineEdit, self.enemyWaveButton]
        self.widgetList = [self.moneyLineEdit, self.moneyButton, self.enemyWaveLineEdit, self.enemyWaveButton]
        self.checkKRHD = checkKRHD()
        self.checkKRHD.KRHDID.connect(self.KRModify)
        self.checkKRHD.start()

    def KRModify(self, KRHDID):
        self.KRHDID = KRHDID
        if not KRHDID:
            self.showMSG.setStyleSheet('color:red;')
            self.showMSG.setText(u'Kingdom Rush HD 未启动 请先启动游戏')
            self.showChange.setText('')
            for i in self.widgetList:
                i.setEnabled(False)
        else:
            self.showMSG.setStyleSheet('color:black;')
            self.showMSG.setText(u'Kingdom Rush HD 已运行')
            for i in self.widgetList:
                i.setEnabled(True)
            PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
            _, pid = win32process.GetWindowThreadProcessId(self.KRHDID)
            self.phand = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            moduleHdList = win32process.EnumProcessModules(self.phand)
            for moduleHd in moduleHdList:
                moduleName = win32process.GetModuleFileNameEx(self.phand, moduleHd)
                if "mono.dll" in moduleName:
                    break
            self.moduleHd = moduleHd
            self.checkTotalWave = checkTotalWave(self, phand=self.phand, moduleHd=self.moduleHd)
            self.checkTotalWave.totalWave.connect(self.refreshWave)
            self.checkTotalWave.start()

    def refreshWave(self, totalWave):
        self.enemyWaveGroup.setTitle(u'跳波功能 这关共有 %s 波敌人' % totalWave)

    def moneyModify(self):
        if not self.moneyLineEdit.text():
            self.showChange.setStyleSheet('color:red;')
            self.showChange.setText(u"金钱不能输入为空")
        else:
            data = ctypes.c_long()
            kernelDll = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32.dll")
            kernelDll.ReadProcessMemory(int(self.phand), self.moduleHd + 0x20A554, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x10, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x238, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x0, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x8, ctypes.byref(data), 4, None)
            moneyBaseAddr = data.value + 0x108
            kernelDll.WriteProcessMemory(int(self.phand), moneyBaseAddr, ctypes.byref(ctypes.c_long(int(self.moneyLineEdit.text()))), 4, None)
            self.showChange.setStyleSheet('color:black;')
            self.showChange.setText(u"已修改金钱为%s" % self.moneyLineEdit.text())

    def skipWave(self):
        if not self.enemyWaveLineEdit.text():
            self.showChange.setStyleSheet('color:red;')
            self.showChange.setText(u"波数不能输入为空")
        else:
            data = ctypes.c_long()
            kernelDll = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32.dll")
            kernelDll.ReadProcessMemory(int(self.phand), self.moduleHd + 0x20A554, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x10, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x238, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x0, ctypes.byref(data), 4, None)
            kernelDll.ReadProcessMemory(int(self.phand), data.value + 0x8, ctypes.byref(data), 4, None)
            moneyBaseAddr = data.value + 0xE8
            kernelDll.WriteProcessMemory(int(self.phand), moneyBaseAddr, ctypes.byref(ctypes.c_long(int(self.enemyWaveLineEdit.text()))), 4, None)
            self.showChange.setStyleSheet('color:black;')
            self.showChange.setText(u"已跳转至第%s波敌人" % self.enemyWaveLineEdit.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
