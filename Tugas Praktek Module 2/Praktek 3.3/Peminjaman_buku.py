import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox, QAbstractItemView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QDate

class PeminjamanBukuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Peminjaman Buku")
        self.setGeometry(200, 200, 700, 400)

        self.init_db()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_kelola = QWidget()
        self.tab_pinjam = QWidget()
        self.tab_kembali = QWidget()
        self.tab_laporan = QWidget()

        self.tabs.addTab(self.tab_kelola, "Kelola Buku")
        self.tabs.addTab(self.tab_pinjam, "Pinjam Buku")
        self.tabs.addTab(self.tab_kembali, "Kembalikan Buku")
        self.tabs.addTab(self.tab_laporan, "Laporan")

        self.setup_tab_kelola()
        self.setup_tab_pinjam()
        self.setup_tab_kembali()
        self.setup_tab_laporan()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "perpustakaan.db")
        self.db.setDatabaseName(db_path)
        
        self.db.open()

        query = QSqlQuery()
        query.exec_("""
            CREATE TABLE IF NOT EXISTS buku (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                stok INTEGER
            )
        """)
        query.exec_("""
            CREATE TABLE IF NOT EXISTS peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                borrower TEXT,
                loan_date TEXT,
                return_date TEXT,
                status TEXT
            )
        """)

    def setup_tab_kelola(self):
        layout = QVBoxLayout(self.tab_kelola)
        
        self.model_buku = QSqlTableModel()
        self.model_buku.setTable("buku")
        self.model_buku.select()

        self.tv_buku = QTableView()
        self.tv_buku.setModel(self.model_buku)
        layout.addWidget(self.tv_buku)

        form = QFormLayout()
        self.in_judul = QLineEdit()
        self.in_stok = QLineEdit()
        form.addRow("Judul Buku:", self.in_judul)
        form.addRow("Jumlah Stok:", self.in_stok)
        layout.addLayout(form)

        btn = QPushButton("Tambah Buku")
        btn.clicked.connect(self.tambah_buku)
        layout.addWidget(btn)

    def tambah_buku(self):
        query = QSqlQuery()
        query.prepare("INSERT INTO buku (judul, stok) VALUES (?, ?)")
        query.addBindValue(self.in_judul.text())
        query.addBindValue(int(self.in_stok.text() or 0))
        query.exec_()
        
        self.model_buku.select()
        self.in_judul.clear()
        self.in_stok.clear()

    def setup_tab_pinjam(self):
        layout = QVBoxLayout(self.tab_pinjam)
        
        form = QFormLayout()
        self.in_book_id = QLineEdit()
        self.in_borrower = QLineEdit()
        form.addRow("ID Buku (Lihat di Kelola):", self.in_book_id)
        form.addRow("Nama Peminjam:", self.in_borrower)
        layout.addLayout(form)

        btn = QPushButton("Pinjam Buku")
        btn.clicked.connect(self.pinjam_buku)
        layout.addWidget(btn)

    def pinjam_buku(self):
        query = QSqlQuery()
        query.prepare("INSERT INTO peminjaman (book_id, borrower, loan_date, return_date, status) VALUES (?, ?, ?, '', 'active')")
        query.addBindValue(self.in_book_id.text())
        query.addBindValue(self.in_borrower.text())
        query.addBindValue(QDate.currentDate().toString("yyyy-MM-dd"))
        
        if query.exec_():
            self.model_kembali.select()
            self.in_book_id.clear()
            self.in_borrower.clear()
            QMessageBox.information(self, "Sukses", "Buku berhasil dipinjam!")

    def setup_tab_kembali(self):
        layout = QVBoxLayout(self.tab_kembali)
        layout.addWidget(QLabel("Peminjaman Aktif:"))

        self.model_kembali = QSqlTableModel()
        self.model_kembali.setTable("peminjaman")
        self.model_kembali.setFilter("status = 'active'")
        self.model_kembali.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model_kembali.select()

        self.tv_kembali = QTableView()
        self.tv_kembali.setModel(self.model_kembali)
        self.tv_kembali.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_kembali.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tv_kembali)

        btn = QPushButton("Kembalikan Buku")
        btn.clicked.connect(self.kembali_buku)
        layout.addWidget(btn)

    def kembali_buku(self):
        row = self.tv_kembali.currentIndex().row()
        if row >= 0:
            record = self.model_kembali.record(row)
            record.setValue("status", "returned")
            record.setValue("return_date", QDate.currentDate().toString("yyyy-MM-dd"))
            
            self.model_kembali.setRecord(row, record)
            self.model_kembali.submitAll()
            self.model_kembali.select()
            QMessageBox.information(self, "Sukses", "Buku telah dikembalikan!")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data di tabel terlebih dahulu!")

    def setup_tab_laporan(self):
        layout = QVBoxLayout(self.tab_laporan)
        self.lbl_laporan = QLabel("Klik tombol di bawah untuk memuat laporan terkini.")
        
        btn = QPushButton("Refresh Laporan")
        btn.clicked.connect(self.refresh_laporan)
        
        layout.addWidget(self.lbl_laporan)
        layout.addWidget(btn)

    def refresh_laporan(self):
        aktif = 0
        kembali = 0
        
        query = QSqlQuery("SELECT COUNT(*) FROM peminjaman WHERE status='active'")
        if query.next():
            aktif = query.value(0)
            
        query = QSqlQuery("SELECT COUNT(*) FROM peminjaman WHERE status='returned'")
        if query.next():
            kembali = query.value(0)
            
        self.lbl_laporan.setText(f"Total Peminjaman Aktif: {aktif}\nTotal Buku Dikembalikan: {kembali}")

    def closeEvent(self, event):
        if self.db.isOpen():
            self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeminjamanBukuApp()
    window.show()
    sys.exit(app.exec_())