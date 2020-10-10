import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QFileDialog

import src.gen_and_parse as gen_and_parse
import sys
from src.db import nexys_ddr_portlist, nexys_portlist

ddr_chosen = False


class Ui_MainWindow(object):
    input_file_path = ''
    output_file_path = ''
    xdc_ports = {}
    input_file_name = ''
    project_path = ''
    using_onboard_clock = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.move(100, 10)
        self.pushButton.setMinimumHeight(31)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.move(10, 10)
        self.pushButton_2.setMinimumHeight(31)
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 620, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.verticalHeader().setVisible(False)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.move(500, 10)
        self.pushButton_3.setMinimumHeight(31)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.move(20, 50)
        self.radioButton.setMinimumHeight(17)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.move(110, 50)
        self.radioButton_2.setMinimumHeight(17)
        self.radioButton_2.setObjectName("radioButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(220, 50, 151, 17))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TestBench and Constraint Generator"))
        self.pushButton.setText(_translate("MainWindow", "Generate TestBench"))
        self.pushButton.clicked.connect(self.generate_tb)
        self.pushButton_2.setText(_translate("MainWindow", "Browse"))
        self.pushButton_2.clicked.connect(self.browse)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Signals"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "I/O"))
        self.pushButton_3.setText(_translate("MainWindow", "Generate Constraint"))
        self.pushButton_3.clicked.connect(self.generate_constraint)
        self.radioButton.setText(_translate("MainWindow", "Nexys4"))
        self.radioButton_2.setText(_translate("MainWindow", "Nexys4 DDR"))
        self.radioButton.clicked.connect(self.chosen_nexys)
        self.radioButton_2.clicked.connect(self.chosen_nexys_ddr)
        self.checkBox.setText(_translate("MainWindow", "Use onboard 100MHz clock"))
        self.checkBox.clicked.connect(self.onboard_clock_clicked)

    def onboard_clock_clicked(self):
        if self.checkBox.checkState():
            self.using_onboard_clock = True
        else:
            self.using_onboard_clock = False

    def chosen_nexys(self):
        global ddr_chosen
        ddr_chosen = False
        if self.input_file_name != '':
            for i in range(self.tableWidget.rowCount()):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(nexys_portlist.keys())
                self.tableWidget.setCellWidget(i, 1, combobox)

    def chosen_nexys_ddr(self):
        global ddr_chosen
        ddr_chosen = True
        if self.input_file_name != '':
            for i in range(self.tableWidget.rowCount()):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(nexys_ddr_portlist.keys())
                self.tableWidget.setCellWidget(i, 1, combobox)

    def browse(self):
        qfd = QFileDialog()
        file_filter = 'VHDL file(*.vhd);;All files(*)'
        self.input_file_path = QFileDialog.getOpenFileName(qfd, 'Open source file',  'C:/', file_filter)[0]
        self.input_file_name = self.input_file_path.split("/")[-1]
        self.project_path = '/'.join(self.input_file_path.split("/")[:-1]) + '/'
        self.xdc_ports = {}
        if self.input_file_path != '':
            ports, module_name, libs = gen_and_parse.get_stuff(self.input_file_path)

            for key, value in ports.items():
                self.xdc_ports[key] = value
                try:
                    num1, num2 = re.search(r'(\d+).*(\d+)', value[1]).groups()
                    del self.xdc_ports[key]

                    num1 = int(num1)
                    num2 = int(num2)
                    if num1 > num2:
                        for i in range(num2, num1 + 1):
                            self.xdc_ports[f'{key}[{i}]'] = ''
                    else:
                        for i in range(num1, num2 + 1):
                            self.xdc_ports[f'{key}[{i}]'] = ''
                except:
                    pass

            self.tableWidget.setRowCount(len(self.xdc_ports.keys()))
            global ddr_chosen
            for i, port in enumerate(self.xdc_ports, start=0):
                temp_w = QTableWidgetItem(port)
                self.tableWidget.setItem(i, 0, temp_w)

                combobox = QtWidgets.QComboBox()
                if ddr_chosen:
                    combobox.addItems(nexys_ddr_portlist.keys())
                else:
                    combobox.addItems(nexys_portlist.keys())
                self.tableWidget.setCellWidget(i, 1, combobox)

    def generate_tb(self):
        if self.input_file_name != '':
            qfd = QFileDialog()
            file_filter = 'VHDL file(*.vhd)'
            tb_file_path = f'{self.project_path}tb_{self.input_file_name}'
            self.output_file_path = QFileDialog.getSaveFileName(qfd, f'Save TestBench file', tb_file_path, file_filter)[0]
            if self.output_file_path != '':
                gen_and_parse.generate_tb(self.input_file_path, self.output_file_path)

    def generate_constraint(self):
        if self.input_file_name != '':
            qfd = QFileDialog()
            file_filter = 'XDC file(*.xdc)'
            tb_file_path = f'{self.project_path}constraints.xdc'
            constraint_output_file_path = QFileDialog.getSaveFileName(qfd, f'Save Constraint file', tb_file_path, file_filter)[0]
            if constraint_output_file_path != '':
                constr_ports = {}
                for i in range(self.tableWidget.rowCount()):
                    port_name = self.tableWidget.item(i, 0).text()
                    if 'Clock' == self.tableWidget.cellWidget(i, 1).currentText():
                        constr_ports['Clock'] = port_name
                        continue
                    else:
                        if ddr_chosen:
                            package_name = nexys_ddr_portlist[self.tableWidget.cellWidget(i, 1).currentText()]  # package_pin
                        else:
                            package_name = nexys_portlist[self.tableWidget.cellWidget(i, 1).currentText()]  # package_pin
                        constr_ports[port_name] = package_name
                gen_and_parse.write_const_to_file(constr_ports, constraint_output_file_path, self.using_onboard_clock)


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
