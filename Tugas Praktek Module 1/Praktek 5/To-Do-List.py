import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt # <- IMPORT INI PENTING!
from PyQt5.QtGui import QFont, QColor

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(300, 300, 400, 400)

        layout = QVBoxLayout()

        # Input area
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Tugas baru...")
        self.add_btn = QPushButton("Tambah")
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_btn)

        # List tugas
        self.task_list = QListWidget()

        # Tombol aksi
        button_layout = QHBoxLayout()
        self.complete_btn = QPushButton("Tandai Selesai")
        self.delete_btn = QPushButton("Hapus")
        button_layout.addWidget(self.complete_btn)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Signal connections
        self.add_btn.clicked.connect(self.add_task)
        self.complete_btn.clicked.connect(self.complete_task)
        self.delete_btn.clicked.connect(self.delete_task)
        self.task_input.returnPressed.connect(self.add_task)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            item = QListWidgetItem(task)
            self.task_list.addItem(item)
            self.task_input.clear()

    def complete_task(self):
        # "Menandai tugas selesai dengan warna hijau"
        current_item = self.task_list.currentItem()

        if current_item:
            # === CARA 1: PAKAI Qt.green (PERLU IMPORT Qt) ===
            current_item.setForeground(Qt.green) # SEKARANG BISA

            # Tambahkan centang di depan teks
            current_text = current_item.text()
            if not current_text.startswith("✓ "):
                current_item.setText(f"✓ {current_text}")

    def delete_task(self):
        current_row = self.task_list.currentRow()
        if current_row >= 0:
            self.task_list.takeItem(current_row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())