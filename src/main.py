import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QFileDialog

import gen_and_parse
import sys

port_list = {
    'SW0': 'J15',
    'SW1': 'L16',
    'SW2': 'M13',
    'SW3': 'R15',
    'SW4': 'R17',
    'SW5': 'T18',
    'SW6': 'U18',
    'SW7': 'R13',
    'SW8': 'T8',
    'SW9': 'U8',
    'SW10': 'R16',
    'SW11': 'T13',
    'SW12': 'H6',
    'SW13': 'U12',
    'SW14': 'U11',
    'SW15': 'V10',

    'LED0': 'H17',
    'LED1': 'K15',
    'LED2': 'J13',
    'LED3': 'N14',
    'LED4': 'R18',
    'LED5': 'V17',
    'LED6': 'U17',
    'LED7': 'U16',
    'LED8': 'V16',
    'LED9': 'T15',
    'LED10': 'U14',
    'LED11': 'T16',
    'LED12': 'V15',
    'LED13': 'V14',
    'LED14': 'V12',
    'LED15': 'V11',
    'LED16_B': 'R12',
    'LED16_G': 'M16',
    'LED16_R': 'N15',
    'LED17_B': 'G14',
    'LED17_G': 'R11',
    'LED17_R': 'N16',

    '7SEG_CA': 'T10',
    '7SEG_CB': 'R10',
    '7SEG_CC': 'K16',
    '7SEG_CD': 'K13',
    '7SEG_CE': 'P15',
    '7SEG_CF': 'T11',
    '7SEG_CG': 'L18',
    '7SEG_DP': 'H15',
    '7SEG_AN0': 'J17',
    '7SEG_AN1': 'J18',
    '7SEG_AN2': 'T9',
    '7SEG_AN3': 'J14',
    '7SEG_AN4': 'P14',
    '7SEG_AN5': 'T14',
    '7SEG_AN6': 'K2',
    '7SEG_AN7': 'U13',

    'CPU_RESETN': 'C12',

    'BTN3': 'N17',
    'BTN2': 'M18',
    'BTN1': 'P17',
    'BTN0': 'M17',
    'BTND': 'P18',

    'VGA_RED0': 'A3',
    'VGA_RED1': 'B4',
    'VGA_RED2': 'C5',
    'VGA_RED3': 'A4',
    'VGA_GREEN0': 'C6',
    'VGA_GREEN1': 'A5',
    'VGA_GREEN2': 'B6',
    'VGA_GREEN3': 'A6',
    'VGA_BLUE0': 'B7',
    'VGA_BLUE1': 'C7',
    'VGA_BLUE2': 'D7',
    'VGA_BLUE3': 'D8',
    'VGA_HSYNC': 'B11',
    'VGA_VSYNC': 'B12',

    'UART_TXD_IN': 'C4',
    'UART_RXD_OUT': 'D4',
    'UART_CTS': 'D3',
    'UART_RTS': 'E5',

    'PS2_CLK': 'F4',
    'PS2_DATA': 'B2',

    'ACL_MISO': 'E15',
    'ACL_MOSI': 'F14',
    'ACL_SCLK': 'F15',
    'ACL_CSN': 'D15',
    'ACL_INT1': 'B13',
    'ACL_INT2': 'C16',

    'TMP_SCL': 'C14',
    'TMP_SDA': 'C15',
    'TMP_INT': 'D13',
    'TMP_CT': 'B14',

    'AUD_PWM': 'A11',
    'AUD_SD': 'D12',

    'SD_RESET': 'E2',
    'SD_CD': 'A1',
    'SD_SCK': 'B1',
    'SD_CMD': 'C1',
    'SD_DAT0': 'C2',
    'SD_DAT1': 'E1',
    'SD_DAT2': 'F1',
    'SD_DAT3': 'D2',

    'MIC_CLK': 'J5',
    'MIC_DATA': 'H5',
    'MIC_LRSEL': 'F5',

    'QSPI_D0': 'K17',
    'QSPI_D1': 'K18',
    'QSPI_D2': 'L14',
    'QSPI_D3': 'M14',
    'QSPI_CSN': 'L13'
}


class Ui_MainWindow(object):
    input_file_path = ''
    output_file_path = ''
    xdc_ports = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 10, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 121, 31))
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
        self.pushButton_3.setGeometry(QtCore.QRect(460, 10, 151, 31))
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

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

    def browse(self):
        self.input_file_path = QFileDialog.getOpenFileName()[0]
        self.xdc_ports = {}
        if self.input_file_path != '':
            ports, module_name, libs = gen_and_parse.get_stuff(self.input_file_path)

            # : in std_logic_vector (7 downto 0);

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

            for i, port in enumerate(self.xdc_ports, start=0):
                temp_w = QTableWidgetItem(port)
                self.tableWidget.setItem(i, 0, temp_w)

                combobox = QtWidgets.QComboBox()
                combobox.addItems(port_list.keys())
                self.tableWidget.setCellWidget(i, 1, combobox)

    def generate_tb(self):
        self.output_file_path = QFileDialog.getSaveFileName()[0]
        if self.output_file_path != '':
            gen_and_parse.generate_tb(self.input_file_path, self.output_file_path)

    def generate_constraint(self):
        constraint_output_file_path = QFileDialog.getSaveFileName()[0]
        if constraint_output_file_path != '':
            constr_ports = {}
            for i in range(self.tableWidget.rowCount()):
                port_name = self.tableWidget.item(i, 0).text()  # port_name
                package_name = port_list[self.tableWidget.cellWidget(i, 1).currentText()]  # package_pin
                constr_ports[port_name] = package_name
                gen_and_parse.write_const_to_file(constr_ports, constraint_output_file_path)


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
