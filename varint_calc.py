import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Varint de-varinter v0.1")
        self.main_window = QWidget()
        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_window.setLayout(self.main_window_layout)

        self.entry_label = QLabel()
        self.entry_label.setText("Enter Varint Hex:")
        self.entry_label.setFixedWidth(120)
        
        self.varint_entry = QLineEdit()
        self.varint_entry.setPlaceholderText("ff9103")
        self.varint_entry.setFixedWidth(120)

        self.display_value = QLineEdit()
        self.display_value.setPlaceholderText("69")
        self.display_value.setFixedWidth(120)
        self.display_value.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.varint_toggle = QPushButton()
        self.varint_toggle.setText("Toggle direction:")
        self.varint_toggle.setCheckable(True)
        self.varint_toggle.clicked.connect(lambda: self.toggle_direction())
        
        self.direction_label = QLabel()
        self.direction_label.setText("Hex to Decimal")
        
        self.toggle_widget = QWidget()
        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setContentsMargins(0,0,0,0)
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.toggle_widget.setLayout(self.toggle_layout)
    
        self.submit_button = QPushButton()
        self.submit_button.setText("De-Varint-ify ™")
        self.submit_button.clicked.connect(lambda: self.run_conversion())

        self.entry_widget = QWidget()
        self.entry_layout = QHBoxLayout()
        self.entry_layout.setContentsMargins(0,0,0,0)
        self.entry_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.entry_widget.setLayout(self.entry_layout)

        self.main_window_layout.addWidget(self.toggle_widget)
        self.toggle_layout.addWidget(self.varint_toggle)
        self.toggle_layout.addWidget(self.direction_label)
        self.main_window_layout.addWidget(QLabel("Enter the value below with no formatting or spaces"))
        self.main_window_layout.addWidget(self.entry_widget)
        self.entry_layout.addWidget(self.entry_label)
        self.entry_layout.addWidget(self.varint_entry)
        self.entry_layout.addWidget(QLabel(" = "))
        self.entry_layout.addWidget(self.display_value)
        self.main_window_layout.addWidget(self.submit_button)

        self.setCentralWidget(self.main_window)

    def toggle_direction(self):
        if self.varint_toggle.isChecked():
            self.direction_label.setText("Decimal to Hex")
            self.entry_label.setText("Enter Decimal Value:")
            self.submit_button.setText("Varint-ify ™")
            self.varint_entry.setPlaceholderText("")
        else:
            self.direction_label.setText("Hex to Decimal")
            self.entry_label.setText("Enter Varint Hex:")
            self.submit_button.setText("De-Varint-ify ™")
            self.varint_entry.setPlaceholderText("ff9103")

    def run_conversion(self):
        if self.varint_toggle.isChecked():
            try:
                value = int(self.varint_entry.text())
                varint = []
                while value >= 0x80:  # Continue while there are more chunks to encode
                    varint.append((value & 0x7F) | 0x80)  # Add the lower 7 bits + MSB set to 1
                    value >>= 7  # Shift right by 7 bits
                varint.append(value & 0x7F)  # Add the last chunk with MSB set to 0
                varint_bytes = bytes(varint)
                formatted_bytes = ' '.join(f'{byte:02X}' for byte in varint_bytes)
                self.display_value.setText(formatted_bytes)  # Convert to byte format
            except IndexError:
                self.display_value.setText("enter something...")
            except ValueError:
                self.display_value.setText("0-9 only please...")
        else:
            try:
                entered_value = self.varint_entry.text().replace(" ","")
                print(entered_value)
                entered_value = bytes.fromhex(entered_value)
                print(entered_value)
                shift = 0
                offset = 0
                value = 0
                while offset < len(entered_value):  # Ensure offset stays in bounds
                    byte = entered_value[offset]
                    offset += 1
                    value |= (byte & 0x7F) << shift
                    shift += 7
                    if (byte & 0x80) == 0:  # Stop if MSB is 0
                        break
                self.display_value.setText(str(value))
            except IndexError:
                self.display_value.setText("enter something...")
            except ValueError:
                self.display_value.setText("0-9a-f only please...")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()
