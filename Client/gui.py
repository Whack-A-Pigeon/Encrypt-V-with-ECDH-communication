import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt6.QtGui import QGuiApplication, QMovie

class EncryptiVGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Encrypti V")
        screen_res = QGuiApplication.primaryScreen().availableGeometry().size()
        self.setGeometry(screen_res.width() // 2 - 200, screen_res.height() // 2 - 125, 400, 250)
        self.setFixedSize(400, 250)

        self.setBackground()
        self.createLabels()
        self.createButtons()
        self.hideComponents(1)

    def setBackground(self):
        self.backgroundLabel = QLabel(self)
        self.movie = QMovie("Client/background.gif")
        self.movie.setSpeed(25)
        self.backgroundLabel.setMovie(self.movie)
        self.movie.start()
        self.backgroundLabel.setGeometry(0, 0, 400, 250)

    def createLabels(self):
        self.welcomeLabel = self.createLabel("Welcome to Encrypti V", 90, 30, 250, 20, 16)
        self.usernameLabel = self.createLabel("Username:", 50, 80, 80, 20)
        self.passwordLabel = self.createLabel("Password:", 50, 120, 80, 20)

    def createLabel(self, text, x, y, width, height, font_size=None):
        label = QLabel(text, self)
        label.setGeometry(x, y, width, height)
        if font_size:
            label.setStyleSheet(f"font-size: {font_size}pt; color: white; font-weight: bold;")
        else:
            label.setStyleSheet("color: white; font-weight: bold;")
        return label

    def createButtons(self):
        self.usernameField = self.createTextField(140, 80, 200, 25)
        self.passwordField = self.createTextField(140, 120, 200, 25, True)
        self.loginButton = self.createButton("Login", 140, 160, 90, 30)
        self.registerButton = self.createButton("Register", 250, 160, 90, 30)
        self.encryptFileButton = self.createButton("Encrypt", 100, 110, 90, 30)
        self.decryptFileButton = self.createButton("Decrypt", 210, 110, 90, 30)

    def createTextField(self, x, y, width, height, password=False):
        field = QLineEdit(self)
        field.setGeometry(x, y, width, height)
        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)
        return field

    def createButton(self, text, x, y, width, height):
        button = QPushButton(text, self)
        button.setGeometry(x, y, width, height)
        return button

    def hideComponents(self, button_id):
        if button_id == 1:
            for widget in [self.encryptFileButton, self.decryptFileButton]:
                widget.hide()
        elif button_id == 2:
            widgets_to_hide = [
                self.usernameLabel, self.usernameField,
                self.passwordLabel, self.passwordField,
                self.loginButton, self.registerButton, self.welcomeLabel
            ]
            for widget in widgets_to_hide:
                widget.hide()

    def showMessage(self, message):
        QMessageBox.information(self, "Message", message)

    def showButtons(self):
        for widget in [self.encryptFileButton, self.decryptFileButton]:
            widget.show()

    def pickFile(self):
        return QFileDialog.getOpenFileName(self, "Pick a file")

    def pickDir(self):
        return QFileDialog.getExistingDirectory(self, "Pick a directory")