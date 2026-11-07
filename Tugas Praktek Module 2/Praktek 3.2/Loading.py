import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoadingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(300, 300, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.title_label = QLabel("Welcome to the Main Application!")
        self.title_label.setFont(QFont("Arial", 18))
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                background: white;
                height: 20px;
                text-align: right;
                padding-right: 5px;
            }
            QProgressBar::chunk {
                background-color: green;
            }
        """)
        
        self.status_label = QLabel("Loading data...")
        
        self.layout.addStretch()
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch()

    def start_loading(self):
        self.show()
        for i in range(1, 101):
            time.sleep(0.03)
            self.progress_bar.setValue(i)
            QApplication.processEvents()
        
        self.progress_bar.hide()
        self.status_label.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadingApp()
    window.start_loading()
    sys.exit(app.exec_())