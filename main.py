import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QTextBrowser, QLineEdit
import json
from structure import ST_FIlE_NAME, ST_PROGRAM_DATE_NAME

with open('data.json', 'r') as data:
    FILE_DATA = json.load(data)


class Ui(QDialog):
    while_action = False

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("untitled.ui", self)
        self.text_browser = self.findChild(QTextBrowser, "textBrowser")
        self.button = self.findChild(QPushButton, "pushButton")
        self.line_edit = self.findChild(QLineEdit, "lineEdit")
        self.button.clicked.connect(self.click_btn)
        data = FILE_DATA['UseTime'].get(ST_PROGRAM_DATE_NAME)
        text = ''
        if data:
            for app in data:
                time_use = FILE_DATA['UseTime'][ST_PROGRAM_DATE_NAME].get(app)
                text += f'{app.title()} -- {time_use}\n'
        self.text_browser.setPlainText(text)
        self.show()

    def click_btn(self):
        with open('data.json', 'r') as data:
            FILE_DATA = json.load(data)
        name_program = str(self.line_edit.text())
        is_exists = FILE_DATA['Appname']
        if name_program in is_exists:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(msg.Warning)
            msg.setWindowTitle("Warning")
            msg.setText("This app already exists.")
            msg.exec_()
        else:
            with open(ST_FIlE_NAME, 'w') as data:
                FILE_DATA['Appname'].append(name_program)
                json.dump(FILE_DATA, data, indent=2)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(msg.Information)
            msg.setWindowTitle("Successfully")
            msg.setText("The application was added successfully")
            msg.exec_()


app = QApplication(sys.argv)
UIWindow = Ui()
app.exec_()
