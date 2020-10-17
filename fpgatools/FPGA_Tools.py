import copy
import json
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QEvent
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QFileDialog, QTreeView, QFrame

import fpgatools.gen_and_parse as gen_and_parse
import sys
from fpgatools.db import Nexys_4_DDR, Nexys_4

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
    all_port = [Nexys_4, Nexys_4_DDR]
    chosen_portlist = {}
    pinout_name_list = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(640, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.tableWidget, 2, 0, 1, 5)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 1, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 623, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuGenerate = QtWidgets.QMenu(self.menuBar)
        self.menuGenerate.setObjectName("menuGenerate")
        MainWindow.setMenuBar(self.menuBar)
        self.actionBrowse = QtWidgets.QAction(MainWindow)
        self.actionBrowse.setObjectName("actionBrowse")
        self.actionGenerate_TestBench = QtWidgets.QAction(MainWindow)
        self.actionGenerate_TestBench.setObjectName("actionGenerate_TestBench")
        self.actionGenerate_Constraint = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Constraint.setObjectName("actionGenerate_Constraint")
        self.actionTestBench = QtWidgets.QAction(MainWindow)
        self.actionTestBench.setObjectName("actionTestBench")
        self.actionConstraint = QtWidgets.QAction(MainWindow)
        self.actionConstraint.setObjectName("actionConstraint")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionBrowse)
        self.menuFile.addAction(self.actionGenerate_TestBench)
        self.menuGenerate.addAction(self.actionTestBench)
        self.menuGenerate.addAction(self.actionConstraint)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuGenerate.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TestBench and Constraint Generator"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Signlas"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "I/O"))
        self.checkBox.setText(_translate("MainWindow", "Use onboard 100MHz clock"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuGenerate.setTitle(_translate("MainWindow", "Generate"))
        self.actionBrowse.setText(_translate("MainWindow", "Browse"))
        self.actionGenerate_TestBench.setText(_translate("MainWindow", "Import Pinout"))
        self.actionGenerate_Constraint.setText(_translate("MainWindow", "Generate Constraint"))
        self.actionTestBench.setText(_translate("MainWindow", "TestBench"))
        self.actionConstraint.setText(_translate("MainWindow", "Constraint"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

        self.actionBrowse.triggered.connect(self.browse)
        self.actionTestBench.triggered.connect(self.generate_tb)
        self.actionConstraint.triggered.connect(self.generate_constraint)
        self.actionGenerate_TestBench.triggered.connect(self.add_custom_pinout)
        self.checkBox.clicked.connect(self.onboard_clock_clicked)
        self.comboBox.view().pressed.connect(self.picked_board)
        self.actionAbout.triggered.connect(self.print_help)

        for element in self.all_port:
            try:
                self.pinout_name_list.append(element['Name'])
            except:
                self.pinout_name_list.append(element['name'])
        self.pinout_name_list = sorted(self.pinout_name_list)
        self.comboBox.addItems(self.pinout_name_list)

        self.chosen_portlist = copy.deepcopy(self.all_port[self.comboBox.currentIndex()])
        del self.chosen_portlist['Name']

    def print_help(self):
        showdialog('For more information visit <a href="https://github.com/Fint0r/FPGA_Tools/">Our GitHub page.</a><br><br>Feel free to contact is if you have any question', 'info')

    def add_custom_pinout(self):
        qfd = QFileDialog()
        file_filter = 'JSON file(*.json)'
        json_path = QFileDialog.getOpenFileName(qfd, 'Open json file', 'C:/', file_filter)[0]
        if json_path != '':
            try:
                with open(json_path, 'r')as f:
                    content = json.loads(f.read())
                self.pinout_name_list.append(content['Name'])
                self.pinout_name_list = sorted(self.pinout_name_list)
                self.all_port.append(content)
                self.comboBox.clear()
                self.comboBox.addItems(self.pinout_name_list)
            except:
                showdialog('Invalid custom port list format!\nCheck help for more information.')

    def picked_board(self, index):
        item = self.pinout_name_list[index.row()]
        for element in self.all_port:
            if element['Name'] == item:
                self.chosen_portlist = copy.deepcopy(element)
                del self.chosen_portlist['Name']
        if self.input_file_name != '':
            for i in range(self.tableWidget.rowCount()):
                self.set_items_in_table(i)

        if (item == 'Nexys 4 DDR') or (item == 'Nexys 4'):
            self.checkBox.show()
            self.using_onboard_clock = False
            self.checkBox.setChecked(False)
        else:
            self.checkBox.hide()
            self.using_onboard_clock = False
            self.checkBox.setChecked(False)

    def onboard_clock_clicked(self):
        if self.checkBox.checkState():
            self.using_onboard_clock = True
        else:
            self.using_onboard_clock = False

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

        for key, value in self.chosen_portlist.items():
            for port_name, pin in value.items():
                self.flattened_portlist[port_name] = pin

        for key, value_list in self.chosen_portlist.items():
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
        else:
            showdialog('Browse VHDL file first.', 'info')

    def generate_constraint(self):
        if self.input_file_name != '':
            qfd = QFileDialog()
            file_filter = 'XDC file(*.xdc)'
            tb_file_path = f'{self.project_path}constraints.xdc'
            constraint_output_file_path = QFileDialog.getSaveFileName(qfd, f'Save Constraint file', tb_file_path, file_filter)[0]
            if constraint_output_file_path != '':
                constr_ports = {}
                clock_var = ''
                for i in range(self.tableWidget.rowCount()):
                    port_name = self.tableWidget.item(i, 0).text()
                    try:
                        constr_ports[port_name] = self.flattened_portlist[self.tableWidget.cellWidget(i, 1).currentText()]  # package_pin
                    except:
                        pass
                    if 'Clock' == self.tableWidget.cellWidget(i, 1).currentText():
                        clock_var = constr_ports[port_name]
                gen_and_parse.write_const_to_file(constr_ports, constraint_output_file_path, self.using_onboard_clock, clock_var)
        else:
            showdialog('Browse VHDL file first.', 'info')


def showdialog(message, severity='warning'):
    msg = QtWidgets.QMessageBox()
    if severity == 'warning':
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle('Warning')
    elif severity == 'info':
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle('Info')
    elif severity == 'critical':
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle('Critical')
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setText(message)
    msg.setTextFormat(QtCore.Qt.RichText)
    msg.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
    return msg.exec_()


def showwindow():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    showwindow()
