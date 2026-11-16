import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
import db_helper

class KembaliBukuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(KembaliBukuWindow, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'kembali_buku.ui')
        uic.loadUi(ui_path, self)

        self.dateKembali.setDate(QDate.currentDate())
        self.btnKembaliProses.clicked.connect(self.process_return)
        self.btnBersihkan.clicked.connect(self.clear_fields)
        self.btnKembali.clicked.connect(self.close)

        self.tableAktif.itemSelectionChanged.connect(self.on_table_select)
        self.tableAktif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.load_active_loans()

    def load_active_loans(self):
        self.tableAktif.setRowCount(0)
        loans = db_helper.get_active_loans()
        for row_number, row_data in enumerate(loans):
            self.tableAktif.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableAktif.setItem(row_number, column_number, item)

    def on_table_select(self):
        selected_rows = self.tableAktif.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        self.txtIdPinjam.setText(self.tableAktif.item(row, 0).text())

    def process_return(self):
        id_pinjam = self.txtIdPinjam.text().strip()
        if not id_pinjam:
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "ID Pinjam harus diisi!")
            return

        tanggal_kembali = self.dateKembali.date().toString("yyyy-MM-dd")
        
        try:
            denda = float(self.txtDenda.text().strip())
            if denda < 0:
                raise ValueError()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Validasi Gagal", "Denda harus berupa angka valid!")
            return

        success, message = db_helper.return_book(id_pinjam, tanggal_kembali, denda)
        if success:
            QtWidgets.QMessageBox.information(self, "Berhasil", message)
            self.load_active_loans()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Gagal", message)

    def clear_fields(self):
        self.txtIdPinjam.clear()
        self.dateKembali.setDate(QDate.currentDate())
        self.txtDenda.setText("0")
        self.tableAktif.clearSelection()