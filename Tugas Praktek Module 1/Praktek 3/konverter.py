import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

class TemperatureConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konverter Suhu")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.label_c=QLabel("Celsius:")
        self.input_c = QLineEdit()
        self.input_c.setPlaceholderText("Masukkan suhu Celsius")

        self.label_f=QLabel("Fahrenheit:")
        self.output_f = QLabel("0 Fahrenheit")
        self.output_f.setStyleSheet("font-seize: 16px; font-weight: bold;")

        layout.addWidget(self.label_c)
        layout.addWidget(self.input_c)
        layout.addWidget(self.label_f)
        layout.addWidget(self.output_f)

        self.setLayout(layout)

        # Signal connection
        self.input_c.textChanged.connect(self.convert)

    def convert(self):
        try:
            celsius = float(self.input_c.text())
            fahrenheit = (celsius * 9/5) + 32
            self.output_f.setText(f"{fahrenheit:.2f} Fahrenheit")
        except ValueError:
            self.output_f.setText("Invalid input")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperatureConverter()
    window.show()
    sys.exit(app.exec_())