import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
from parser_ui import Ui_MainWindow
import re


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Parser")

        self.move_to_center()
        self.data_dict = {}

        self.pushButton_go.clicked.connect(self.parse)
        self.pushButton_reset.clicked.connect(self.reset)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_load.clicked.connect(self.load)

        self.parameter_name = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
                               "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
                               "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega"]

        self.keys_widgets = [self.key_1, self.key_2, self.key_3, self.key_4, self.key_5,
                             self.key_6, self.key_7, self.key_8, self.key_9, self.key_10]

        self.values_widgets = [self.value_1, self.value_2, self.value_3, self.value_4, self.value_5,
                               self.value_6, self.value_7, self.value_8, self.value_9, self.value_10]

        self.symbols_and_signs = [
            "!", ":", ";", "-", "+", "/", "*", "&", "%", "$", "#", "@", "~", "^", "|",
            "<", ">", "(", ")", "[", "]", "{", "}"
        ]

    def move_to_center(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def load(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Выберите текстовый файл",
            directory="",
            filter="Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                self.textEdit_text.setText(file_content)
                self.label_sysdirectory.setText(file_path)

            except Exception as e:
                print(f"Ошибка при открытии файла: {e}")

    def save(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Сохранить файл как",
            directory="",
            filter="Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_path:
            if not file_path.endswith('.txt'):
                file_path += '.txt'

            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file_content = self.textEdit_text.toPlainText()
                    file.write(file_content)

                self.label_sysdirectory.setText(f"Сохранено: {file_path}")
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")

    def add_to_log(self, message, log_type="OKW"):
        item = QListWidgetItem(message)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        if log_type == "error":
            item.setForeground(QColor("Maroon"))
        elif log_type == "read":
            item.setForeground(QColor("#000033"))
        else:
            item.setForeground(QColor("#000033"))

        self.listWidget_result.addItem(item)
        self.listWidget_result.scrollToBottom()

    def parse(self):
        text = self.textEdit_text.toPlainText()

        pattern = r'(\w+\s*=\s*[^,]+)(?=\s+\w+\s*=)'
        matches = re.findall(pattern, text)

        if matches:
            for match in matches:
                next_start = text.find(match) + len(match)
                next_token_match = re.search(r'\w+\s*=\s*[^,]+', text[next_start:])
                next_token = next_token_match.group(0) if next_token_match else "unknown"

                if next_token != "unknown":
                    incorrect_segment = f"{match} {next_token}"
                    self.add_to_log(
                        f"NOK 400: syntax error: missing comma between '{match}' and '{next_token}'.",
                        log_type="error"
                    )
                    text = text.replace(incorrect_segment, "")

        pairs = text.split(",")
        self.data = {}

        for pair in pairs:
            pair = pair.strip()
            if "=" not in pair:
                if "?" in pair:
                    key, value = pair.split("?", 1)
                    key = key.strip()
                    value = "?"
                elif pair.isalpha():
                    pair += "=None"
                    key, value = pair.split("=", 1)
                elif pair.isdigit():
                    key = pair
                    value = "error"
                elif pair.isalpha():
                    key = pair
                    value = None
                else:
                    value = None
                    for sym in self.symbols_and_signs:
                        if sym in pair:
                            key, value = pair.split(sym, 1)
                            key = key.strip()
                            value = sym
                            break
                    if value is None:
                        continue
            else:
                key, value = pair.split("=", 1)

            key = key.strip()
            value = value.strip()
            if value.replace('.', '', 1).isdigit() and '.' in value:
                self.data[key] = float(value)
            elif value.isdigit():
                self.data[key] = int(value)
            else:
                self.data[key] = str(value)

        self.validate_and_display(self.data)

    def validate_and_display(self, data):
        self.current_index = 0

        for key, value in data.items():
            if key not in self.parameter_name:
                self.add_to_log(f"NOKW 300: not allowed key '{key}'", log_type="error")
                continue
            if key in self.parameter_name:
                if value == "":
                    self.add_to_log(f"NOKW 500: not value for '{key}'", log_type="error")
                    continue

                if value == None:
                    self.add_to_log(f"NOKW 800: command no field filled '{key}'", log_type="error")
                    continue

                if value == "None":
                    self.add_to_log(f"NOKW 800: command no field filled '{key}'", log_type="error")
                    continue

                if value == "?":
                    if key in self.data_dict:
                        resolved_value = self.data_dict[key]
                        self.data[key] = resolved_value
                        self.add_to_log(f"OKR: command '{key} = {resolved_value}' ", log_type="read")
                        if self.current_index < len(self.keys_widgets):
                            self.keys_widgets[self.current_index].setText(f"{key}")
                            self.values_widgets[self.current_index].setText(f"{resolved_value}")
                            self.current_index += 1
                            self.data_dict[key] = resolved_value
                        else:
                            self.add_to_log("NOKW 700: The number of teams is no more than 10", log_type="error")
                    else:
                        self.add_to_log(f"NOKR 300: not exist '{key}'", log_type="error")
                    continue

                if isinstance(value, str) and any(sym in value for sym in self.symbols_and_signs):
                    self.add_to_log(f"NOK 600: the task is not clear (invalid symbol) '{value}'", log_type="error")
                    continue

                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    resolved_value = float(value) if '.' in str(value) else int(value)
                    self.data[key] = resolved_value
                    self.add_to_log("OKW")
                    if self.current_index < len(self.keys_widgets):
                        self.keys_widgets[self.current_index].setText(f"{key}")
                        self.values_widgets[self.current_index].setText(f"{resolved_value}")
                        self.current_index += 1
                        self.data_dict[key] = resolved_value
                    else:
                        self.add_to_log("NOKW 700: The number of teams is no more than 10", log_type="error")
                    continue

                if isinstance(value, str) and value != "None":
                    value = value.strip('"')
                    self.data[key] = value
                    self.add_to_log("OKW")
                    self.data_dict[key] = value
                    if self.current_index < len(self.keys_widgets):
                        self.keys_widgets[self.current_index].setText(f"{key}")
                        self.values_widgets[self.current_index].setText(f"{value}")
                        self.current_index += 1
                    else:
                        self.add_to_log("NOKW 700: The number of teams is no more than 10", log_type="error")
                    continue
                if value == "error":
                    self.add_to_log(f"NOKW 300: not allowed key '{key}'", log_type="error")
                else:
                    self.add_to_log(f"NOK 1000", log_type="error")

    def reset(self):
        self.listWidget_result.clear()
        self.textEdit_text.clear()
        self.list_widget_Label = [self.label_sysdirectory, self.key_1, self.key_2, self.key_3,
                                  self.key_4, self.key_5, self.key_6, self.key_7, self.key_8,
                                  self.key_9, self.key_10, self.value_1, self.value_2, self.value_3,
                                  self.value_4, self.value_5, self.value_6, self.value_7,
                                  self.value_8, self.value_9, self.value_10]
        for label in self.list_widget_Label:
            label.setText("")
        self.label_sysdirectory.setText(" /Users/...")
        self.data = {}
        self.data_dict = {}
        self.current_index = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
