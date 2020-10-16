import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QEvent
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QFileDialog, QTreeView, QFrame

import fpgatools.gen_and_parse as gen_and_parse
import sys
from fpgatools.db import nexys_ddr_portlist, nexys_portlist

ddr_chosen = False


class TreeComboBox(QComboBox):
    def __init__(self, *args):
        super().__init__(*args)

        self.__skip_next_hide = False

        tree_view = QTreeView(self)
        tree_view.setFrameShape(QFrame.NoFrame)
        tree_view.setEditTriggers(tree_view.NoEditTriggers)
        tree_view.setAlternatingRowColors(True)
        tree_view.setSelectionBehavior(tree_view.SelectRows)
        tree_view.setWordWrap(True)
        tree_view.setAllColumnsShowFocus(True)
        tree_view.setHeaderHidden(True)
        self.setView(tree_view)
        self.view().viewport().installEventFilter(self)

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        super().showPopup()

    def hidePopup(self):
        self.setRootModelIndex(self.view().currentIndex().parent())
        self.setCurrentIndex(self.view().currentIndex().row())
        if self.__skip_next_hide:
            self.__skip_next_hide = False
        else:
            super().hidePopup()

    def selectIndex(self, index):
        self.setRootModelIndex(index.parent())
        self.setCurrentIndex(index.row())

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is self.view().viewport():
            index = self.view().indexAt(event.pos())
            self.__skip_next_hide = not self.view().visualRect(index).contains(event.pos())
        return False


class Ui_MainWindow(object):
    input_file_path = ''
    output_file_path = ''
    xdc_ports = {}
    input_file_name = ''
    project_path = ''
    using_onboard_clock = False
    flattened_portlist = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
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
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 4)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.gridLayout.addWidget(self.radioButton, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 2, 1, 1)

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
                self.set_items_in_table(i)

    def chosen_nexys_ddr(self):
        global ddr_chosen
        ddr_chosen = True
        if self.input_file_name != '':
            for i in range(self.tableWidget.rowCount()):
                self.set_items_in_table(i)

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
                self.set_items_in_table(i)

    def set_items_in_table(self, current_row_id):
        model = QtGui.QStandardItemModel()
        if ddr_chosen:
            chosen_portlist = nexys_ddr_portlist
        else:
            chosen_portlist = nexys_portlist

        for key, value in chosen_portlist.items():
            for port_name, pin in value.items():
                self.flattened_portlist[port_name] = pin

        for key, value_list in chosen_portlist.items():
            group = QtGui.QStandardItem(key)
            for value in value_list:
                group.appendRow(QtGui.QStandardItem(value))
            model.appendRow(group)
        combobox = TreeComboBox()
        combobox.setModel(model)
        combobox.setMaxVisibleItems(combobox.count())
        self.tableWidget.setCellWidget(current_row_id, 1, combobox)

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
                        try:
                            constr_ports[port_name] = self.flattened_portlist[self.tableWidget.cellWidget(i, 1).currentText()]  # package_pin
                        except:
                            pass
                gen_and_parse.write_const_to_file(constr_ports, constraint_output_file_path, self.using_onboard_clock)


def showwindow():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    showwindow()
