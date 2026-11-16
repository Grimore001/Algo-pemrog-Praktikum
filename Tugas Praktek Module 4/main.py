import sys
import os
from PyQt5 import QtWidgets, uic
import db_helper
from kelola_buku import KelolaBukuWindow
from pinjam_buku import PinjamBukuWindow
from kembali_buku import KembaliBukuWindow
from laporan import LaporanWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'main.ui')
        uic.loadUi(ui_path, self)

        db_helper.init_db()

        self.btnKelolaBuku.clicked.connect(self.open_kelola_buku)
        self.btnPinjamBuku.clicked.connect(self.open_pinjam_buku)
        self.btnKembaliBuku.clicked.connect(self.open_kembali_buku)
        self.btnLaporan.clicked.connect(self.open_laporan)
        self.btnKeluar.clicked.connect(self.close)

        self.kelola_buku_win = None
        self.pinjam_buku_win = None
        self.kembali_buku_win = None
        self.laporan_win = None

    def open_kelola_buku(self):
        if not self.kelola_buku_win:
            self.kelola_buku_win = KelolaBukuWindow()
        else:
            self.kelola_buku_win.load_books()
        self.kelola_buku_win.show()
        self.kelola_buku_win.raise_()
        self.kelola_buku_win.activateWindow()

    def open_pinjam_buku(self):
        if not self.pinjam_buku_win:
            self.pinjam_buku_win = PinjamBukuWindow()
        else:
            self.pinjam_buku_win.load_books_combo()
            self.pinjam_buku_win.load_active_loans()
        self.pinjam_buku_win.show()
        self.pinjam_buku_win.raise_()
        self.pinjam_buku_win.activateWindow()

    def open_kembali_buku(self):
        if not self.kembali_buku_win:
            self.kembali_buku_win = KembaliBukuWindow()
        else:
            self.kembali_buku_win.load_active_loans()
        self.kembali_buku_win.show()
        self.kembali_buku_win.raise_()
        self.kembali_buku_win.activateWindow()

    def open_laporan(self):
        if not self.laporan_win:
            self.laporan_win = LaporanWindow()
        else:
            self.laporan_win.load_report_data()
        self.laporan_win.show()
        self.laporan_win.raise_()
        self.laporan_win.activateWindow()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())