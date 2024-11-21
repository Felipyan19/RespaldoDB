# login_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.label_usuario = QLabel('Usuario:')
        self.label_contrasena = QLabel('Contraseña:')
        self.input_usuario = QLineEdit(self)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setEchoMode(QLineEdit.Password)  
        self.boton_login = QPushButton('Iniciar sesión', self)
        self.mensaje_error = QLabel('')
        self.mensaje_error.setStyleSheet("color: red;")

        layout_usuario = QHBoxLayout()
        layout_usuario.addWidget(self.label_usuario)
        layout_usuario.addWidget(self.input_usuario)

        layout_contrasena = QHBoxLayout()
        layout_contrasena.addWidget(self.label_contrasena)
        layout_contrasena.addWidget(self.input_contrasena)

        layout = QVBoxLayout()
        layout.addLayout(layout_usuario)
        layout.addLayout(layout_contrasena)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.mensaje_error)

        self.setLayout(layout)

    def setup_login_function(self, validar_login):
        """Configura la función de validación del login"""
        self.boton_login.clicked.connect(validar_login)
