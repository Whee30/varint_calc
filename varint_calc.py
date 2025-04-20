import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt


# Notes for converting to pyqt6

# declare the window
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Establish the tab position and settings

        self.setWindowTitle("Varint de-varinter v0.1")
        # self.setFixedWidth(810)
        # self.setMinimumHeight(600)
        self.main_window = QWidget()
        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_window.setLayout(self.main_window_layout)

        # declare a widget
        self.varint_entry = QLineEdit()
        self.varint_entry.setPlaceholderText("ff9103")
        self.varint_entry.setFixedWidth(120)

        self.display_value = QLineEdit()
        self.display_value.setPlaceholderText("69")
        self.display_value.setFixedWidth(120)
        self.display_value.setFocusPolicy(Qt.FocusPolicy.NoFocus)


        self.submit_button = QPushButton()
        self.submit_button.setText("De-Varint-ify ™")
        self.submit_button.clicked.connect(lambda: self.decode_varint())

        self.entry_widget = QWidget()
        self.entry_layout = QHBoxLayout()
        self.entry_layout.setContentsMargins(0,0,0,0)
        self.entry_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_widget.setLayout(self.entry_layout)

        self.main_window_layout.addWidget(QLabel("Enter the varint below with no formatting or spaces"))
        self.main_window_layout.addWidget(self.entry_widget)
        self.entry_layout.addWidget(QLabel("Enter Varint:"))
        self.entry_layout.addWidget(self.varint_entry)
        self.entry_layout.addWidget(QLabel(" = "))
        self.entry_layout.addWidget(self.display_value)
        self.main_window_layout.addWidget(self.submit_button)

        self.setCentralWidget(self.main_window)

    def decode_varint(self):
        try:
            entered_value = self.varint_entry.text()
            entered_value = bytes.fromhex(entered_value)
            shift = 0
            offset = 0
            value = 0

            while True:
                byte = entered_value[offset]  # Read a byte at the current offset
                offset += 1  # Increment the offset for the next byte

                value |= (byte & 0x7F) << shift  # Mask the MSB and shift bits into place
                shift += 7  # Move to the next group of bits

                if (byte & 0x80) == 0:  # If MSB is 0, end of varint
                    break
            self.display_value.setText(str(value))
        except IndexError:
            self.display_value.setText("enter something...")
        except ValueError:
            self.display_value.setText("0-9a-f only please...")
        
    def encode_varint(self):
        value = self.varint_entry.text()
        varint = []
        while value >= 0x80:  # Continue while there are more chunks to encode
            varint.append((value & 0x7F) | 0x80)  # Add the lower 7 bits + MSB set to 1
            value >>= 7  # Shift right by 7 bits
        varint.append(value & 0x7F)  # Add the last chunk with MSB set to 0
        print(bytes(varint))  # Convert to byte format

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()
