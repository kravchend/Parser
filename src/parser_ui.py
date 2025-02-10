from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QScrollArea
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor



class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.gradient_position = -0.1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_gradient)
        self.fixed_width = 0.25
        self.overlap = 0.21
        self.is_animating_forward = True
        self.is_clicked = False
        self.font_size = 20

        # Эффект свечения
        self.glow_effect = QGraphicsDropShadowEffect(self)
        self.glow_effect.setBlurRadius(45)
        self.glow_effect.setColor(QColor(0, 255, 255, 100))
        self.glow_effect.setOffset(2, 2)
        self.setGraphicsEffect(self.glow_effect)

        # Установка стиля
        self.setStyleSheet(self.get_gradient())

    def get_gradient(self):
        """Градиентный стиль кнопки."""
        border_width = 1 if not self.is_clicked else 2.2
        font_size = self.font_size if not self.is_clicked else self.font_size - 3
        gradient = f"""
                    QPushButton {{
                        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                            stop:0 rgba(0, 0, 25, 1),                        
                            stop:{self.gradient_position} rgba(67, 189, 161, 0.15), 
                            stop:{self.gradient_position + self.fixed_width} rgba(0, 0, 35, 1)); 
                        color: Aqua;
                        border: {border_width}px solid cyan;
                        border-radius: 5px;
                        font-size: {font_size}px;
                    }}
                """
        return gradient

    def animate_gradient(self):
        """Анимация градиента."""
        step = 0.035
        if self.is_animating_forward:
            if self.gradient_position + self.fixed_width <= 1.0 + self.overlap:
                self.gradient_position += step
            else:
                self.timer.stop()
        else:
            if self.gradient_position > 0.0:
                self.gradient_position -= step
            else:
                self.timer.stop()

        self.setStyleSheet(self.get_gradient())

    def enterEvent(self, event):
        """Обработка наведения курсора."""
        self.is_animating_forward = True
        self.timer.start(5)

        self.glow_effect.setColor(QColor(0, 255, 255, 190)) 
        self.glow_effect.setBlurRadius(80) 
        self.update()

    def leaveEvent(self, event):
        """Обработка ухода курсора."""
        self.is_animating_forward = False
        self.timer.start(5)

        # Ослабляем свечение
        self.glow_effect.setColor(QColor(0, 255, 255, 100))
        self.glow_effect.setBlurRadius(40) 
        self.update()

    def mousePressEvent(self, event):
        """Обработка нажатия кнопки."""
        super().mousePressEvent(event)
        self.is_clicked = True

        self.glow_effect.setColor(QColor(0, 0, 0, 250)) 
        self.setStyleSheet(self.get_gradient())
        self.update()

    def mouseReleaseEvent(self, event):
        """Обработка отпускания кнопки."""
        super().mouseReleaseEvent(event)
        self.is_clicked = False

        self.glow_effect.setColor(QColor(0, 255, 255, 190)) 
        self.setStyleSheet(self.get_gradient())
        self.update()


class StyleSheet(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 170);"
                            "border-width: 4px 4px 4px 4px;"
                            "border-style: solid;"
                            "border-top-color: black;"
                            "border-right-color: black;"
                            "border-bottom-color: black;"
                            "border-left-color: black;"
                            "color: #02023D;")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 920)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 920))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 920))
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(1100, 920))
        self.centralwidget.setMaximumSize(QtCore.QSize(1100, 920))
        self.centralwidget.setStyleSheet("background: qlineargradient(\n"
                                         "        spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
                                         "        stop:0 #0D1B2A,\n"
                                         "        stop:0.4 #1B263B,\n"
                                         "        stop:0.8 #415A77,\n"
                                         "        stop:1 #0A0F1E\n"
                                         "    );")

        self.textEdit_text = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_text.setGeometry(QtCore.QRect(35, 145, 580, 380))
        self.textEdit_text.setStyleSheet("background-color: rgba(255, 255, 255, 170);"
                            "border-width: 5px 5px 5px 5px;"
                            "border-radius: 5px;"
                            "border-style: solid;"
                            "border-top-color: black;"
                            "border-right-color: black;"
                            "border-bottom-color: black;"
                            "border-left-color: black;"
                            "color: #000033;")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        self.textEdit_text.setFont(font)
        self.textEdit_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.textEdit_text.setCursorWidth(5)
        self.textEdit_text.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.textEdit_text.setFocus()

        self.label_Parser = QtWidgets.QLabel(self.centralwidget)
        self.label_Parser.setGeometry(QtCore.QRect(480, 10, 141, 41))
        self.label_Parser.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_Parser.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_Parser.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_Parser.setObjectName("label_Parser")

        self.label_sysdirectory = QtWidgets.QLabel(self.centralwidget)
        self.label_sysdirectory.setGeometry(QtCore.QRect(35, 68, 490, 50))
        self.label_sysdirectory.setStyleSheet("background-color: rgba(255, 255, 255, 170);"
                                              "border-color: rgb(16, 16, 16);"
                                              "border-radius: 5px;"
                                              "border: 5px solid;"
                                              "color: #000033;")
        self.label_sysdirectory.setText(" /Users/...")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        self.label_sysdirectory.setFont(font)
        self.label_sysdirectory.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(self.label_sysdirectory.geometry())
        self.scroll_area.setStyleSheet("""
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0);
                height: 3px; 
                margin: 1px 5px 0px 5px;
            }
            QScrollBar::handle:horizontal {
                background: #55FFFF;  /* Цвет ползунка */
                min-width: 20px;
                border-radius: 0px;  /* Закруглённые края */
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;  /* Убираем кнопки по краям */
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;  /* Устранение заливки полосы прокрутки */
            }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.label_sysdirectory)

        self.pushButton_load = AnimatedButton("LOAD", self.centralwidget)
        self.pushButton_load.setGeometry(QtCore.QRect(530, 70, 90, 45))
        self.pushButton_save = AnimatedButton("SAVE", self.centralwidget)
        self.pushButton_save.setGeometry(QtCore.QRect(625, 70, 90, 45))
        self.pushButton_go = AnimatedButton("GO", self.centralwidget)
        self.pushButton_go.setGeometry(QtCore.QRect(800, 820, 120, 45))
        self.pushButton_reset = AnimatedButton("RESET", self.centralwidget)
        self.pushButton_reset.setGeometry(QtCore.QRect(940, 820, 120, 45))
        self.key_1 = StyleSheet(self.centralwidget)
        self.key_1.setGeometry(QtCore.QRect(690, 160, 240, 45))
        self.key_2 = StyleSheet(self.centralwidget)
        self.key_2.setGeometry(QtCore.QRect(690, 220, 240, 45))
        self.key_3 = StyleSheet(self.centralwidget)
        self.key_3.setGeometry(QtCore.QRect(690, 280, 240, 45))
        self.key_4 = StyleSheet(self.centralwidget)
        self.key_4.setGeometry(QtCore.QRect(690, 340, 240, 45))
        self.key_5 = StyleSheet(self.centralwidget)
        self.key_5.setGeometry(QtCore.QRect(690, 400, 240, 45))
        self.key_6 = StyleSheet(self.centralwidget)
        self.key_6.setGeometry(QtCore.QRect(690, 460, 240, 45))
        self.key_7 = StyleSheet(self.centralwidget)
        self.key_7.setGeometry(QtCore.QRect(690, 520, 240, 45))
        self.key_8 = StyleSheet(self.centralwidget)
        self.key_8.setGeometry(QtCore.QRect(690, 580, 240, 45))
        self.key_9 = StyleSheet(self.centralwidget)
        self.key_9.setGeometry(QtCore.QRect(690, 640, 240, 45))
        self.key_10 = StyleSheet(self.centralwidget)
        self.key_10.setGeometry(QtCore.QRect(690, 700, 240, 45))

        self.label_TextToType = QtWidgets.QLabel(self.centralwidget)
        self.label_TextToType.setGeometry(QtCore.QRect(270, 110, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Academy Engraved LET")
        font.setPointSize(16)
        self.label_TextToType.setFont(font)
        self.label_TextToType.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_TextToType.setObjectName("label_TextToType")
        self.label_AnswerWindows = QtWidgets.QLabel(self.centralwidget)
        self.label_AnswerWindows.setGeometry(QtCore.QRect(245, 517, 201, 51))
        font = QtGui.QFont()
        font.setFamily("Academy Engraved LET")
        font.setPointSize(16)
        self.label_AnswerWindows.setFont(font)
        self.label_AnswerWindows.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_AnswerWindows.setObjectName("label_AnswerWindows")
        self.value_1 = StyleSheet(self.centralwidget)
        self.value_1.setGeometry(QtCore.QRect(960, 160, 100, 45))
        self.value_2 = StyleSheet(self.centralwidget)
        self.value_2.setGeometry(QtCore.QRect(960, 220, 100, 45))
        self.value_3 = StyleSheet(self.centralwidget)
        self.value_3.setGeometry(QtCore.QRect(960, 280, 100, 45))
        self.value_4 = StyleSheet(self.centralwidget)
        self.value_4.setGeometry(QtCore.QRect(960, 340, 100, 45))
        self.value_5 = StyleSheet(self.centralwidget)
        self.value_5.setGeometry(QtCore.QRect(960, 400, 100, 45))
        self.value_6 = StyleSheet(self.centralwidget)
        self.value_6.setGeometry(QtCore.QRect(960, 460, 100, 45))
        self.value_7 = StyleSheet(self.centralwidget)
        self.value_7.setGeometry(QtCore.QRect(960, 520, 100, 45))
        self.value_8 = StyleSheet(self.centralwidget)
        self.value_8.setGeometry(QtCore.QRect(960, 580, 100, 45))
        self.value_9 = StyleSheet(self.centralwidget)
        self.value_9.setGeometry(QtCore.QRect(960, 640, 100, 45))
        self.value_10 = StyleSheet(self.centralwidget)
        self.value_10.setGeometry(QtCore.QRect(960, 700, 100, 45))
        self.label_ParsedFields = QtWidgets.QLabel(self.centralwidget)
        self.label_ParsedFields.setGeometry(QtCore.QRect(800, 80, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Academy Engraved LET")
        font.setPointSize(18)
        self.label_ParsedFields.setFont(font)
        self.label_ParsedFields.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_ParsedFields.setObjectName("label_ParsedFields")
        self.listWidget_result = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_result.setGeometry(QtCore.QRect(35, 555, 580, 330))
        self.listWidget_result.setStyleSheet("background-color: rgba(255, 255, 255, 170);"
                            "border-width: 5px 5px 5px 5px;"
                            "border-radius: 5px;"
                            "border-style: solid;"
                            "border-top-color: black;"
                            "border-right-color: black;"
                            "border-bottom-color: black;"
                            "border-left-color: black;"
                            "color: #000033;")
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        font.setBold(True)
        self.listWidget_result.setFont(font)
        self.listWidget_result.setSpacing(0)

        self.label_AnswerWindows.raise_()
        self.label_TextToType.raise_()
        self.textEdit_text.raise_()
        self.label_Parser.raise_()
        self.label_sysdirectory.raise_()
        self.pushButton_load.raise_()
        self.pushButton_save.raise_()
        self.pushButton_go.raise_()
        self.pushButton_reset.raise_()
        self.key_1.raise_()
        self.key_2.raise_()
        self.key_3.raise_()
        self.key_4.raise_()
        self.key_5.raise_()
        self.key_6.raise_()
        self.key_7.raise_()
        self.key_8.raise_()
        self.key_9.raise_()
        self.key_10.raise_()
        self.value_1.raise_()
        self.value_2.raise_()
        self.value_3.raise_()
        self.value_4.raise_()
        self.value_5.raise_()
        self.value_6.raise_()
        self.value_7.raise_()
        self.value_8.raise_()
        self.value_9.raise_()
        self.value_10.raise_()
        self.label_ParsedFields.raise_()
        self.listWidget_result.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Parser.setText(_translate("MainWindow",
                                             "<html><head/><body><p><span style=\" font-size:35pt; font-weight:600; color:#55ffff;\">P</span><span style=\" font-size:24pt; font-style:italic; text-decoration: underline; color:#ffffff;\">A R S E R</span></p></body></html>"))
        self.pushButton_load.setText(_translate("MainWindow", "LOAD"))
        self.pushButton_save.setText(_translate("MainWindow", "SAVE"))
        self.pushButton_go.setText(_translate("MainWindow", "GO"))
        self.pushButton_reset.setText(_translate("MainWindow", "RESET"))
        self.label_TextToType.setText(_translate("MainWindow", "TEXT TO TYPE "))
        self.label_AnswerWindows.setText(_translate("MainWindow", "ANSWER  WINDOWS  "))
        self.label_ParsedFields.setText(_translate("MainWindow", "PARSED  FIELDS"))
