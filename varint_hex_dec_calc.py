import sys
from PyQt6.QtWidgets import QApplication, QTextEdit, QFrame, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Varint, Hex and Decimal Converter v0.2")
        self.main_window = QWidget()
        self.main_window_layout = QVBoxLayout()
        self.main_window_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_window.setLayout(self.main_window_layout)

        self.entry_label = QLabel()
        self.entry_label.setText("Enter Decimal Number:")
        self.entry_label.setFixedWidth(120)
        
        self.varint_entry = QLineEdit()
        self.varint_entry.setFixedWidth(120)

        self.display_value = QLineEdit()
        self.display_value.setFixedWidth(200)
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

        self.main_window_layout.addWidget(QLabel("Varint Calculator:"))
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

        # Start the bottom half of the calculator

        self.second_entry_label = QLabel()
        self.second_entry_label.setText("Enter Decimal Number:")
        self.second_entry_label.setFixedWidth(120)
        
        self.second_entry = QLineEdit()
        self.second_entry.setFixedWidth(120)

        self.second_display_value = QTextEdit()
        self.second_display_value.setFixedWidth(200)
        self.second_display_value.setFixedHeight(80)
        #self.second_display_value.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.second_varint_toggle = QPushButton()
        self.second_varint_toggle.setText("Toggle direction:")
        self.second_varint_toggle.setCheckable(True)
        self.second_varint_toggle.clicked.connect(lambda: self.second_toggle_direction())
        
        self.second_direction_label = QLabel()
        self.second_direction_label.setText("Hex to Decimal")
        
        self.second_toggle_widget = QWidget()
        self.second_toggle_layout = QHBoxLayout()
        self.second_toggle_layout.setContentsMargins(0,0,0,0)
        self.second_toggle_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.second_toggle_widget.setLayout(self.second_toggle_layout)
    
        self.second_submit_button = QPushButton()
        self.second_submit_button.setText("Converterize ™")
        self.second_submit_button.clicked.connect(lambda: self.second_run_conversion())

        self.second_entry_widget = QWidget()
        self.second_entry_layout = QHBoxLayout()
        self.second_entry_layout.setContentsMargins(0,0,0,0)
        self.second_entry_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.second_entry_widget.setLayout(self.second_entry_layout)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.HLine)
        self.divider.setFixedHeight(20)
        self.main_window_layout.addWidget(self.divider)
        self.main_window_layout.addWidget(QLabel("Decimal/Hex Variations:"))
        self.main_window_layout.addWidget(self.second_toggle_widget)
        self.second_toggle_layout.addWidget(self.second_varint_toggle)
        self.second_toggle_layout.addWidget(self.second_direction_label)
        self.main_window_layout.addWidget(QLabel("Enter the value below with no formatting or spaces"))
        self.main_window_layout.addWidget(self.second_entry_widget)
        self.second_entry_layout.addWidget(self.second_entry_label)
        self.second_entry_layout.addWidget(self.second_entry)
        self.second_entry_layout.addWidget(QLabel(" = "))
        self.second_entry_layout.addWidget(self.second_display_value)
        self.main_window_layout.addWidget(self.second_submit_button)

        self.setCentralWidget(self.main_window)

    def toggle_direction(self):
        if self.varint_toggle.isChecked():
            self.direction_label.setText("Decimal to Hex")
            self.entry_label.setText("Enter Decimal Value:")
            self.submit_button.setText("Varint-ify ™")
        else:
            self.direction_label.setText("Hex to Decimal")
            self.entry_label.setText("Enter Varint Hex:")
            self.submit_button.setText("De-Varint-ify ™")

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
                entered_value = bytes.fromhex(entered_value)
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

    # Second half functions

    def second_toggle_direction(self):
        if self.second_varint_toggle.isChecked():
            self.second_direction_label.setText("Decimal to Hex")
            self.second_entry_label.setText("Enter Decimal:")
        else:
            self.second_direction_label.setText("Hex to Decimal")
            self.second_entry_label.setText("Enter Hex:")


    def second_run_conversion(self):
        source_value = ""
        if self.second_varint_toggle.isChecked(): # Decimal to Hex
            try:
                source_value = int(self.second_entry.text())
                abs_source_value = abs(int(self.second_entry.text()))
                byte_num = (source_value.bit_length() + 7) // 8  # Calculate required bytes
                LE_bytes = abs_source_value.to_bytes(byte_num, byteorder="little").hex()
                BE_bytes = abs_source_value.to_bytes(byte_num, byteorder="big").hex()
                signed_LE_bytes = source_value.to_bytes(byte_num, byteorder="little", signed=True).hex()
                signed_BE_bytes = source_value.to_bytes(byte_num, byteorder="big", signed=True).hex()
                if source_value < 0:
                    self.second_display_value.setText(
                        'signed LE: ' +  str(signed_LE_bytes) + '\n' +
                        'signed BE: ' +  str(signed_BE_bytes))
                else:
                    self.second_display_value.setText(
                        'LE:   ' + str(LE_bytes) + '\n' + 
                        'BE:   ' +  str(BE_bytes))
            except ValueError:
                self.second_display_value.setText("Only 0-9 Please...")
            except IndexError:
                self.second_display_value.setText("Enter Something...")
        else: # Hex to Decimal
            try:
                source_value = self.second_entry.text()
                entered_value = source_value.replace(" ","")
                entered_value = bytes.fromhex(entered_value)
                self.second_display_value.setPlainText(
                    'LE Unsigned: ' + str(int.from_bytes(entered_value, byteorder='little', signed=False)) + '\n'
                    'LE Signed: ' + str(int.from_bytes(entered_value, byteorder='little', signed=True)) + '\n'
                    'BE Unsigned: ' + str(int.from_bytes(entered_value, byteorder='big', signed=False)) + '\n'
                    'BE Signed: ' + str(int.from_bytes(entered_value, byteorder='big', signed=True)))
            except ValueError:
                self.second_display_value.setPlainText("Enter hex characters in pairs, no formatting.")
                print("Value")
            except IndexError:
                self.second_display_value.setPlainText("Only 0-9,A-F please...")
                print("Index)")
        print(source_value)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.setStyle('Fusion')
app.exec()
