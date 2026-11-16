import sys
import os
from PyQt5 import QtWidgets, uic
import db_helper

class LaporanWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LaporanWindow, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'laporan.ui')
        uic.loadUi(ui_path, self)

        self.btnRefresh.clicked.connect(self.load_report_data)
        self.btnKembali.clicked.connect(self.close)

        self.tablePopuler.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.load_report_data()

    def load_report_data(self):
        stats = db_helper.get_general_statistics()
        self.lblTotalBuku.setText(f"Total Buku: {stats['total_buku']}")
        self.lblActiveLoans.setText(f"Buku Dipinjam: {stats['active_loans']}")
        self.lblTotalDenda.setText(f"Total Denda: Rp {stats['total_denda']:,.0f}")

        self.tablePopuler.setRowCount(0)
        populer_books = db_helper.get_most_borrowed_books()
        for row_number, row_data in enumerate(populer_books):
            self.tablePopuler.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tablePopuler.setItem(row_number, column_number, item)