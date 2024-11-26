from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Iniciar sesión")
        self.label_imagen = QLabel(self)
        self.setFixedSize(800, 600)  
        
        pixmap = QPixmap('./assets/2612467.png')
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio) 
        self.label_imagen.setPixmap(scaled_pixmap)
        self.label_imagen.setAlignment(Qt.AlignCenter)
        
        self.label_usuario = QLabel('Usuario:           ')
        self.label_contrasena = QLabel('Contraseña:    ')
        self.input_usuario = QLineEdit(self)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.boton_login = QPushButton('Iniciar sesión', self)
        self.mensaje_error = QLabel('')
        self.mensaje_error.setStyleSheet("color: red; font-weight: bold;")

        self.set_style()

        layout_usuario = QHBoxLayout()
        layout_usuario.addWidget(self.label_usuario)
        layout_usuario.addWidget(self.input_usuario)

        layout_contrasena = QHBoxLayout()
        layout_contrasena.addWidget(self.label_contrasena)
        layout_contrasena.addWidget(self.input_contrasena)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) 

        layout.addWidget(self.label_imagen) 
        layout.addLayout(layout_usuario)
        layout.addLayout(layout_contrasena)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.mensaje_error)

        container = QWidget()
        container.setLayout(layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(container)

    def set_style(self):
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                font-size: 16px;
                margin-bottom: 15px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                background-color: #ffffff;
            }
        """)
        self.input_contrasena.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 5px;
                font-size: 16px;
                margin-bottom: 15px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                background-color: #ffffff;
            }
        """)

        self.boton_login.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)

        self.label_usuario.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #343a40;
        """)
        self.label_contrasena.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #343a40;
        """)

        self.mensaje_error.setStyleSheet("""
            font-size: 12px;
            color: red;
            font-weight: bold;
        """)

    def setup_login_function(self, validar_login):
        self.boton_login.clicked.connect(validar_login)