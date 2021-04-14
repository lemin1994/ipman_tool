import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QButtonGroup

from ipman_tool.ipman_workthread import ServiceHelper,PTNServiceHelper, ServiceCheckHelper

class Ui_Dialog(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1118, 602)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1121, 601))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet("QTabBar::tab{width:240;height:40}")
        self.tab1 = QtWidgets.QTabWidget()
        self.tab2 = QtWidgets.QTabWidget()
        self.tab3 = QtWidgets.QTabWidget()
        self.tab4 = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.tab1, "Tab1")
        self.tabWidget.addTab(self.tab2, "Tab2")
        self.tabWidget.addTab(self.tab3, "Tab3")
        self.tabWidget.addTab(self.tab4, "Tab4")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

        self.translate(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # 第一个页面的变量
        self.sw_file = None
        self.sr01_file = None
        self.sr02_file = None
        self.save_file_path = None
        self.ptn_service_file = None

        # 第三个页面的变量
        self.pre_file = None
        self.after_file = None

    def tab1UI(self):
        # SW选择
        self.pushButton_2 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 30, 141, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label_2 = QtWidgets.QLabel(self.tab1)
        self.label_2.setGeometry(QtCore.QRect(50, 40, 72, 15))
        self.label_2.setObjectName("label_2")

        self.textBrowser_6 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_6.setGeometry(QtCore.QRect(330, 670, 731, 192))
        self.textBrowser_6.setObjectName("textBrowser_6")

        # 选择 SR02 文件
        self.pushButton_9 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_9.setGeometry(QtCore.QRect(410, 170, 141, 28))
        self.pushButton_9.setObjectName("pushButton_9")
        
        
        self.target_lag_editor = QtWidgets.QTextEdit(self.tab1)
        self.target_lag_editor.setGeometry(QtCore.QRect(140, 70, 251, 31))
        self.target_lag_editor.setObjectName("target_lag_editor")

        self.pushButton_10 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_10.setGeometry(QtCore.QRect(370, 340, 261, 61))
        self.pushButton_10.setObjectName("pushButton_10")

        self.label_10 = QtWidgets.QLabel(self.tab1)
        self.label_10.setGeometry(QtCore.QRect(50, 80, 72, 15))
        self.label_10.setObjectName("label_10")

        self.label_11 = QtWidgets.QLabel(self.tab1)
        self.label_11.setGeometry(QtCore.QRect(50, 180, 72, 15))
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.tab1)
        self.label_12.setGeometry(QtCore.QRect(20, 270, 101, 20))
        self.label_12.setObjectName("label_12")

        # SR01
        self.pushButton_11 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_11.setGeometry(QtCore.QRect(410, 120, 141, 28))
        self.pushButton_11.setObjectName("pushButton_11")

        # 保存文件路径
        self.pushButton_12 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_12.setGeometry(QtCore.QRect(410, 270, 141, 28))
        self.pushButton_12.setObjectName("pushButton_12")

        self.label_13 = QtWidgets.QLabel(self.tab1)
        self.label_13.setGeometry(QtCore.QRect(50, 230, 72, 15))
        self.label_13.setObjectName("label_13")

        
        
        self.label_14 = QtWidgets.QLabel(self.tab1)
        self.label_14.setGeometry(QtCore.QRect(420, 80, 81, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab1)
        self.label_15.setGeometry(QtCore.QRect(50, 130, 72, 15))
        self.label_15.setObjectName("label_15")

        self.pushButton_14 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_14.setGeometry(QtCore.QRect(790, 70, 141, 28))
        self.pushButton_14.setObjectName("pushButton_14")

        self.label_16 = QtWidgets.QLabel(self.tab1)
        self.label_16.setGeometry(QtCore.QRect(450, 80, 51, 16))
        self.label_16.setObjectName("label_16")

        # 目标SW选择
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_2.setGeometry(QtCore.QRect(140, 30, 256, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")

        # PTN文件选择框
        self.textBrowser_11 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_11.setGeometry(QtCore.QRect(510, 70, 261, 31))
        self.textBrowser_11.setObjectName("textBrowser_11")

        # SR01
        self.textBrowser_14 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_14.setGeometry(QtCore.QRect(140, 120, 256, 31))
        self.textBrowser_14.setObjectName("textBrowser_14")

        # SR02
        self.textBrowser_10 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_10.setGeometry(QtCore.QRect(140, 170, 256, 31))
        self.textBrowser_10.setObjectName("textBrowser_10")

        # vlan尾数
        self.textedit_vlan = QtWidgets.QTextEdit(self.tab1)
        self.textedit_vlan.setGeometry(QtCore.QRect(140, 220, 256, 31))
        self.textedit_vlan.setObjectName("textBrowser_13")

        # 最后的回显框
        self.textBrowser_12 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_12.setGeometry(QtCore.QRect(130, 440, 761, 111))
        self.textBrowser_12.setObjectName("textBrowser_12")

        # 保存文件的路径
        self.textBrowser_9 = QtWidgets.QTextBrowser(self.tab1)
        self.textBrowser_9.setGeometry(QtCore.QRect(140, 270, 256, 31))
        self.textBrowser_9.setObjectName("textBrowser_9")

        self.sw_port_editor = QtWidgets.QTextEdit(self.tab1)
        self.sw_port_editor.setGeometry(QtCore.QRect(510, 70, 261, 31))
        self.sw_port_editor.setObjectName("sw_port_editor")
        
        self.radioButton = QtWidgets.QRadioButton(self.tab1)
        self.radioButton.setGeometry(QtCore.QRect(600, 30, 120, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab1)
        self.radioButton_2.setGeometry(QtCore.QRect(710, 30, 120, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton.setText("框式OLT集客")
        self.radioButton_2.setText("PTN集客")
        self.radioButton.setChecked(True)
        self.radioButton.toggled.connect(lambda: self.radioButtonStart(self.radioButton))
        self.radioButton_2.toggled.connect(lambda: self.radioButtonStart2(self.radioButton_2))

        self.label_16.setVisible(True)
        self.sw_port_editor.setVisible(True)
        self.label_14.setHidden(True)
        self.textBrowser_11.setHidden(True)
        self.pushButton_14.setHidden(True)

        self.pushButton_2.clicked.connect(self.on_click_button_2)

        self.pushButton_9.clicked.connect(self.on_click_button_9)
        self.pushButton_10.clicked.connect(self.on_click_button_10)
        self.pushButton_11.clicked.connect(self.on_click_button_11)
        self.pushButton_12.clicked.connect(self.on_click_button_12)
        self.pushButton_14.clicked.connect(self.on_click_button_14)

    def tab2UI(self):
        self.label = QtWidgets.QLabel(self.tab2)
        self.label.setGeometry(QtCore.QRect(50, 70, 54, 12))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab2)
        self.textBrowser.setGeometry(QtCore.QRect(80, 60, 256, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.tab2)
        self.pushButton.setGeometry(QtCore.QRect(350, 60, 131, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.tab2)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 51, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.tab2)
        self.label_5.setGeometry(QtCore.QRect(50, 180, 51, 16))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.tab2)
        self.label_4.setGeometry(QtCore.QRect(410, 121, 81, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit.setGeometry(QtCore.QRect(490, 110, 161, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_7 = QtWidgets.QLabel(self.tab2)
        self.label_7.setGeometry(QtCore.QRect(410, 181, 81, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_3.setGeometry(QtCore.QRect(490, 170, 161, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.textBrowser_24 = QtWidgets.QTextBrowser(self.tab2)
        self.textBrowser_24.setGeometry(QtCore.QRect(180, 380, 761, 111))
        self.textBrowser_24.setObjectName("textBrowser_24")
        self.pushButton_24 = QtWidgets.QPushButton(self.tab2)
        self.pushButton_24.setGeometry(QtCore.QRect(420, 300, 261, 61))
        self.pushButton_24.setObjectName("pushButton_24")
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab2)
        self.radioButton_3.setGeometry(QtCore.QRect(350, 120, 61, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab2)
        self.radioButton_4.setGeometry(QtCore.QRect(350, 180, 51, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 110, 231, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 170, 231, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.tab2)
        self.radioButton_5.setGeometry(QtCore.QRect(50, 230, 89, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.tab2)
        self.radioButton_6.setGeometry(QtCore.QRect(180, 230, 89, 16))
        self.radioButton_6.setObjectName("radioButton_6")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab2)
        self.textBrowser_3.setGeometry(QtCore.QRect(100, 270, 256, 31))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.label_9 = QtWidgets.QLabel(self.tab2)
        self.label_9.setGeometry(QtCore.QRect(50, 280, 54, 12))
        self.label_9.setObjectName("label_9")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab2)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 270, 141, 31))
        self.pushButton_3.setObjectName("pushButton_15")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab2)
        self.pushButton_7.setGeometry(QtCore.QRect(910, 270, 141, 31))
        self.pushButton_7.setObjectName("pushButton_16")
        self.label_17 = QtWidgets.QLabel(self.tab2)
        self.label_17.setGeometry(QtCore.QRect(590, 280, 54, 12))
        self.label_17.setObjectName("label_17")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab2)
        self.textBrowser_4.setGeometry(QtCore.QRect(640, 270, 256, 31))
        self.textBrowser_4.setObjectName("textBrowser_4")
        reg = '[0-9][/][0-9][/][0-9]'
        regExp = QRegExp(reg)
        reg2 = 'GDGZ-MS-IPMAN-BNG[0-9]{2}-[a-zA-Z]+[0-9]?-[HW|AL]{2}'
        regExp2 = QRegExp(reg2)
        self.lineEdit.setValidator(QRegExpValidator(regExp, self.tab2))
        self.lineEdit_3.setValidator(QRegExpValidator(regExp, self.tab2))
        self.lineEdit_2.setValidator(QRegExpValidator(regExp2, self.tab2))

        self.qbg = QButtonGroup()
        self.qbg2 = QButtonGroup()

        self.qbg.addButton(self.radioButton_3, 1)
        self.qbg.addButton(self.radioButton_4, 2)
        self.qbg2.addButton(self.radioButton_5, 1)
        self.qbg2.addButton(self.radioButton_6, 2)

        self.radioButton_5.setChecked(True)
        self.label_9.setHidden(True)
        self.label_17.setHidden(True)
        self.textBrowser_3.setHidden(True)
        self.textBrowser_4.setHidden(True)
        self.pushButton_3.setHidden(True)
        self.pushButton_7.setHidden(True)
        self.radioButton_5.toggled.connect(lambda: self.radioButtonStart5(self.radioButton_5))
        self.radioButton_6.toggled.connect(lambda: self.radioButtonStart6(self.radioButton_6))


        self.pushButton.clicked.connect(self.on_click_button)
        self.pushButton_3.clicked.connect(self.on_click_button_3)
        self.pushButton_7.clicked.connect(self.on_click_button_7)
        self.pushButton_24.clicked.connect(self.on_click_button_24)

    def changeSelect(self):
        if self.comboBox.currentText().strip() != "SW":
            self.label.setVisible(False)
            self.textBrowser.setVisible(False)
            self.pushButton.setVisible(False)
        else:
            self.label.setVisible(True)
            self.textBrowser.setVisible(True)
            self.pushButton.setVisible(True)

    def tab3UI(self):
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.tab3)
        self.textBrowser_5.setGeometry(QtCore.QRect(170, 30, 256, 31))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.label_6 = QtWidgets.QLabel(self.tab3)
        self.label_6.setGeometry(QtCore.QRect(50, 40, 107, 16))
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.tab3)
        self.label_8.setGeometry(QtCore.QRect(50, 100, 107, 16))
        self.label_8.setObjectName("label_8")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.tab3)
        self.textBrowser_7.setGeometry(QtCore.QRect(170, 90, 256, 31))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab3)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 30, 151, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab3)
        self.pushButton_8.setGeometry(QtCore.QRect(450, 90, 151, 31))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab3)
        self.pushButton_13.setGeometry(QtCore.QRect(410, 200, 251, 71))
        self.pushButton_13.setObjectName("pushButton_13")
        self.textBrowser_8 = QtWidgets.QTextBrowser(self.tab3)
        self.textBrowser_8.setGeometry(QtCore.QRect(180, 310, 721, 192))
        self.textBrowser_8.setObjectName("textBrowser_8")

        self.pushButton_4.clicked.connect(self.on_click_button_4)
        self.pushButton_8.clicked.connect(self.on_click_button_8)
        self.pushButton_13.clicked.connect(self.on_click_button_13)

    def tab4UI(self):
        self.sw_choice_file_tab4_label = QtWidgets.QLabel(self.tab4)
        self.sw_choice_file_tab4_label.setGeometry(QtCore.QRect(50, 40, 107, 16))
        self.sw_choice_file_tab4_label.setObjectName("sw_choice_file_tab4_label")
        self.sw_file_tab4_textBrowser = QtWidgets.QTextBrowser(self.tab4)
        self.sw_file_tab4_textBrowser.setGeometry(QtCore.QRect(170, 30, 256, 31))
        self.sw_file_tab4_textBrowser.setObjectName("sw_file_tab4_textBrowser")

    def translate(self,Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "城域网割接助手"))
        self.pushButton_2.setText(_translate("Dialog", "选择SW配置文件"))
        self.label_2.setText(_translate("Dialog", "SW:"))
        self.pushButton_9.setText(_translate("Dialog", "选择SR02配置文件"))
        self.pushButton_10.setText(_translate("Dialog", "业务分析"))
        self.label_10.setText(_translate("Dialog", "目标lag："))
        self.label_11.setText(_translate("Dialog", "SR02："))
        self.label_12.setText(_translate("Dialog", "保存文件路径："))
        self.pushButton_11.setText(_translate("Dialog", "选择SR01配置文件"))
        self.pushButton_12.setText(_translate("Dialog", "选择保存文件路径"))
        self.label_13.setText(_translate("Dialog", "VLAN尾数："))
        self.label_14.setText(_translate("Dialog", "PTN集客业务："))
        self.label_15.setText(_translate("Dialog", "SR01："))
        self.pushButton_14.setText(_translate("Dialog", "选择PTN集客清单"))
        self.label_16.setText(_translate("Dialog", "SW端口："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("Dialog", "业务分析"))
        self.label.setText(_translate("Dialog", "SW："))
        self.pushButton.setText(_translate("Dialog", "选择SW文件"))
        self.label_3.setText(_translate("Dialog", "BNG01："))
        self.label_5.setText(_translate("Dialog", "BNG02："))
        self.label_4.setText(_translate("Dialog", "BNG01端口："))
        self.label_7.setText(_translate("Dialog", "BNG02端口："))
        self.pushButton_24.setText(_translate("Dialog", "生成脚本"))
        self.radioButton_3.setText(_translate("Dialog", "主"))
        self.radioButton_4.setText(_translate("Dialog", "主"))
        self.radioButton_5.setText(_translate("Dialog", "自动配置"))
        self.radioButton_6.setText(_translate("Dialog", "手动配置"))
        self.label_9.setText(_translate("Dialog", "BNG01："))
        self.pushButton_3.setText(_translate("Dialog", "选择配置文件"))
        self.pushButton_7.setText(_translate("Dialog", "选择配置文件"))
        self.label_17.setText(_translate("Dialog", "BNG02："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("Dialog", "生成脚本"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("Dialog", "割接核查"))
        self.label_6.setText(_translate("Dialog", "SW配置文件："))
        self.label_8.setText(_translate("Dialog", "输出文件路径："))
        self.pushButton_4.setText(_translate("Dialog", "选择配置文件"))
        self.pushButton_8.setText(_translate("Dialog", "选择配置文件"))
        self.pushButton_13.setText(_translate("Dialog", "执行"))

        self.sw_choice_file_tab4_label.setText(_translate("Dialog", "选择SW文件"))

    def radioButtonStart(self,rbn):
        if rbn.isChecked() == True:
            self.label_16.setVisible(True)
            self.sw_port_editor.setVisible(True)
            self.label_14.setHidden(True)
            self.textBrowser_11.setHidden(True)
            self.pushButton_14.setHidden(True)

    def radioButtonStart2(self, rbn):
        if rbn.isChecked() == True:
            self.label_16.setHidden(True)
            self.sw_port_editor.setHidden(True)
            self.label_14.setVisible(True)
            self.textBrowser_11.setVisible(True)
            self.pushButton_14.setVisible(True)

    def radioButtonStart6(self, rbn):
        if rbn.isChecked() == True:
            self.label_9.setVisible(True)
            self.label_17.setVisible(True)
            self.textBrowser_3.setVisible(True)
            self.textBrowser_4.setVisible(True)
            self.pushButton_3.setVisible(True)
            self.pushButton_7.setVisible(True)
            self.pushButton_24.setGeometry(QtCore.QRect(420, 350, 261, 61))
            self.textBrowser_24.setGeometry(QtCore.QRect(180, 420, 761, 111))

    def radioButtonStart5(self, rbn):
        if rbn.isChecked() == True:
            self.label_9.setHidden(True)
            self.label_17.setHidden(True)
            self.textBrowser_3.setHidden(True)
            self.textBrowser_4.setHidden(True)
            self.pushButton_3.setHidden(True)
            self.pushButton_7.setHidden(True)
            self.pushButton_24.setGeometry(QtCore.QRect(420, 300, 261, 61))
            self.textBrowser_24.setGeometry(QtCore.QRect(180, 380, 761, 111))


    @pyqtSlot()
    def on_click_button(self):
        print(1)

    # 选择SW文件
    @pyqtSlot()
    def on_click_button_2(self):
        if self.sw_file is not None:
            self.textBrowser_2.setText(self.sw_file)
        sw_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                            "All Files(*);;Text Files(*.txt)")
        if sw_file.strip() != "":
            self.textBrowser_2.setText(sw_file)
        self.sw_file = sw_file

    # 选择SR01的文件
    @pyqtSlot()
    def on_click_button_11(self):
        if self.sr01_file is not None:
            self.textBrowser_14.setText(self.sr01_file)
        sr01_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                            "All Files(*);;Text Files(*.txt)")
        if sr01_file.strip() != "":
            self.textBrowser_14.setText(sr01_file)
        self.sr01_file = sr01_file

    # 选择SR02的文件
    @pyqtSlot()
    def on_click_button_9(self):
        if self.sr02_file is not None:
            self.textBrowser_10.setText(self.sr02_file)
        sr02_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                            "All Files(*);;Text Files(*.txt)")
        if sr02_file.strip() != "":
            self.textBrowser_10.setText(sr02_file)

        self.sr02_file = sr02_file

    # 保存文件的路径
    def on_click_button_12(self):
        if self.save_file_path is not None:
            self.textBrowser_9.setText(self.save_file_path)
        save_file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件", os.getcwd())
        if not os.path.isdir(save_file_path):
            QMessageBox.information(self, "提示信息", "请选择文件夹！！")
        else:
            if save_file_path.strip() != "":
                self.textBrowser_9.setText(save_file_path)
            self.save_file_path = save_file_path

    @pyqtSlot()
    def on_click_button_10(self):
        if self.radioButton.isChecked():
            print("olt")
            if self.sw_file is None or self.sr01_file is None or self.sr02_file is None:
                QMessageBox.information(self, "提示信息", "缺少必要的配置文件！！")
            elif self.target_lag_editor.toPlainText() == "":
                QMessageBox.information(self, "提示信息", "缺少必要的条件信息！！")
            else:
                vlan_last = None
                sw_port = None
                if self.sw_port_editor.toPlainText().strip() != "":
                    sw_port = self.sw_port_editor.toPlainText()
                if self.textedit_vlan.toPlainText().strip() == "":
                    vlan_last = self.textedit_vlan.toPlainText()
                self.sh = ServiceHelper(self.sw_file, self.sr01_file, self.sr02_file, self.save_file_path,sw_port, self.target_lag_editor.toPlainText().strip(),
                                        vlan_last)
                self.sh.update_str.connect(self.handleDisplay)
                self.sh.start()
        else:
            print("PTN")
            if self.sw_file is None or self.sr01_file is None or self.sr02_file is None:
                QMessageBox.information(self, "提示信息", "缺少必要的配置文件！！")
            else:
                self.ptnsh = PTNServiceHelper(self.sw_file, self.sr01_file, self.sr02_file, self.save_file_path,
                                              self.ptn_service_file, self.target_lag_editor.toPlainText().strip())
                self.ptnsh.update_str.connect(self.handleDisplay)
                self.ptnsh.start()

    @pyqtSlot()
    def on_click_button_14(self):
        if self.ptn_service_file is not None:
            self.textBrowser_11.setText(self.ptn_service_file)
        ptn_service_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                                    "All Files(*);;Text Files(*.txt)")
        if ptn_service_file.strip() != "":
            self.textBrowser_11.setText(ptn_service_file)
        self.ptn_service_file = ptn_service_file

    def handleDisplay(self, info):
        self.textBrowser_12.append(info)

    @pyqtSlot()
    def on_click_button_3(self):
        print(1)
    @pyqtSlot()
    def on_click_button_6(self):
        print(1)
    @pyqtSlot()
    def on_click_button_7(self):
        print(1)


    """第三个页面的点击事件"""
    @pyqtSlot()
    def on_click_button_4(self):
        if self.pre_file is not None:
            self.textBrowser_5.setText(self.sr01_file)
        pre_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(),
                                                             "All Files(*);;Text Files(*.txt)")
        if pre_file.strip() != "":
            self.textBrowser_5.setText(pre_file)
        self.pre_file = pre_file

    @pyqtSlot()
    def on_click_button_8(self):
        if self.after_file is not None:
            self.textBrowser_7.setText(self.sr01_file)
        after_file = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件", os.getcwd())
        if after_file.strip() != "":
            self.textBrowser_7.setText(after_file)
        self.after_file = after_file

    @pyqtSlot()
    def on_click_button_13(self):
        if self.pre_file is None or self.after_file is None:
            QMessageBox.information(self, "提示信息", "缺少必要的配置信息！！")
        else:
            self.sch = ServiceCheckHelper(self.pre_file, self.after_file)
            self.sch.update_str.connect(self.handleDisplay_tab3)
            self.sch.start()

    def handleDisplay_tab3(self, info):
        self.textBrowser_8.append(info)

    @pyqtSlot()
    def on_click_button_24(self):
        print(1)
    @pyqtSlot()
    def on_click_button_25(self):
        print(1)
    @pyqtSlot()
    def on_click_button_26(self):
        print(1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.setupUi(ui)
    ui.show()
    sys.exit(app.exec_())