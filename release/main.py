import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication, QWidget
from PyQt5 import QtCore, QtWidgets


class DataBaseCoffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 300, 800, 509)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 771, 411))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(210, 450, 171, 31))
        self.pushButton.setObjectName("pushButton")
        self.redact = QtWidgets.QPushButton(self)
        self.redact.setGeometry(QtCore.QRect(10, 450, 171, 31))
        self.redact.setObjectName("redact")
        self.edit = QtWidgets.QPushButton(self)
        self.edit.setGeometry(QtCore.QRect(410, 450, 171, 31))
        self.edit.setObjectName("edit")
        self.delete_ = QtWidgets.QPushButton(self)
        self.delete_.setGeometry(QtCore.QRect(610, 450, 161, 31))
        self.delete_.setObjectName("delete_")
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "название сорта"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "степень обжарки"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "описание вкуса"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "молотый/ в зёрнах"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "цена"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "объём упаковки(в нраммах)"))
        self.pushButton.setText(_translate("Form", "Обновить данные"))
        self.redact.setText(_translate("Form", "Редактировать"))
        self.edit.setText(_translate("Form", "Добавить"))
        self.delete_.setText(_translate("Form", "Удалить"))
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.tableWidget.resizeColumnsToContents()
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM MainTable").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.k = result[-1][0]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        self.flag = True
        self.pushButton.clicked.connect(self.update)
        self.redact.clicked.connect(self.red)
        self.edit.clicked.connect(self.add)
        self.delete_.clicked.connect(self.delete_coffee)

    def update(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM MainTable").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def add(self):
        self.flag = False
        self.second_form = SecondForm(self.k, 0, self.flag)
        self.second_form.show()
        self.flag = True

    def red(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if ids:
            self.second_form = SecondForm(self.k, ids, self.flag)
            self.second_form.show()
        else:
            QMessageBox.about(self, "Ошибка", "Вы не выбрали кофе!")

    def delete_coffee(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if ids:
            valid = QMessageBox.question(self, '', "Действительно удалить элементы с id " + ",".join(ids),
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur = self.con.cursor()
                for i in ids:
                    data = cur.execute("delete FROM MainTable WHERE id = '{}'".format(i)).fetchone()
                self.con.commit()
        else:
            QMessageBox.about(self, "Ошибка", "Вы не выбрали кофе!")


class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.setGeometry(400, 300, 700, 500)
        self.name = QtWidgets.QLineEdit(self)
        self.name.setGeometry(QtCore.QRect(240, 30, 251, 31))
        self.name.setObjectName("name")
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(20, 30, 181, 31))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 181, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 181, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 210, 181, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 270, 181, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 330, 221, 31))
        self.label_6.setObjectName("label_6")
        self.text = QtWidgets.QLineEdit(self)
        self.text.setGeometry(QtCore.QRect(240, 140, 251, 31))
        self.text.setObjectName("text")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(230, 430, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.degree = QtWidgets.QComboBox(self)
        self.degree.setGeometry(QtCore.QRect(240, 90, 251, 31))
        self.degree.setObjectName("degree")
        self.degree.addItem("")
        self.degree.addItem("")
        self.degree.addItem("")
        self.kind = QtWidgets.QComboBox(self)
        self.kind.setGeometry(QtCore.QRect(240, 210, 251, 31))
        self.kind.setObjectName("kind")
        self.kind.addItem("")
        self.kind.addItem("")
        self.value = QtWidgets.QSpinBox(self)
        self.value.setGeometry(QtCore.QRect(240, 270, 251, 31))
        self.value.setMaximum(1000000000)
        self.value.setProperty("value", 100)
        self.value.setObjectName("value")
        self.volume = QtWidgets.QSpinBox(self)
        self.volume.setGeometry(QtCore.QRect(240, 330, 251, 31))
        self.volume.setMaximum(1000000000)
        self.volume.setProperty("value", 100)
        self.volume.setObjectName("volume")
        _translate = QtCore.QCoreApplication.translate
        self.label_1.setText(_translate("Form", "название сорта"))
        self.label_2.setText(_translate("Form", "степень прожарки"))
        self.label_3.setText(_translate("Form", "описание вкуса"))
        self.label_4.setText(_translate("Form", "молотый/ в зёрнах"))
        self.label_5.setText(_translate("Form", "цена"))
        self.label_6.setText(_translate("Form", "объём упаковки(в граммах)"))
        self.pushButton.setText(_translate("Form", "сохранить"))
        self.degree.setItemText(0, _translate("Form", "слабая"))
        self.degree.setItemText(1, _translate("Form", "средняя"))
        self.degree.setItemText(2, _translate("Form", "высокая"))
        self.kind.setItemText(0, _translate("Form", "молотый"))
        self.kind.setItemText(1, _translate("Form", "в зёрнах"))
        self.n = args[0]
        self.i = args[1]
        self.fl = args[2]
        self.con = sqlite3.connect("data/coffee.sqlite")
        if self.fl:
            cur = self.con.cursor()
            info = cur.execute(
                "SELECT * from MainTable where id = '{}'".format(*self.i)).fetchone()
            self.name.setText(info[1])
            self.degree.setCurrentText(info[2])
            self.text.setText(info[3])
            self.kind.setCurrentText(info[4])
            self.value.setValue(info[5])
            self.volume.setValue(info[6])
        self.pushButton.clicked.connect(self.update_result)

    def update_result(self):
        cur = self.con.cursor()
        self.n += 1
        if self.fl:
            rez = cur.execute("""UPDATE MainTable SET 'название сорта' = '{}', 'степень прожарки' = '{}'
            , 'описание вкуса' = '{}', 'молотый/ в зёрнах' = '{}', 'цена(в рублях)' = '{}'
            , 'объем упаковки(в граммах)' = '{}'  where id = '{}'""".format(self.name.text(),
                                                                            self.degree.currentText(),
                                                                            self.text.text(),
                                                                            self.kind.currentText(),
                                                                            self.value.value(),
                                                                            self.volume.value(),
                                                                            int(*self.i)))
        else:
            rez = cur.execute(
                """insert into MainTable (id, 'название сорта', 'степень прожарки', 'описание вкуса', 'молотый/ в зёрнах', 'цена(в рублях)',
                 'объем упаковки(в граммах)') values('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.n,
                                                                                                         self.name.text(),
                                                                                                         self.degree.currentText(),
                                                                                                         self.text.text(),
                                                                                                         self.kind.currentText(),
                                                                                                         int(
                                                                                                             self.value.value()),
                                                                                                         int(
                                                                                                             self.volume.value())))
        self.con.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataBaseCoffee()
    window.show()
    sys.exit(app.exec())
