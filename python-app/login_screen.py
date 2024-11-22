# login_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Definimos el tamaño de la ventana
        self.setWindowTitle("Iniciar sesión")
        self.setFixedSize(600, 400)  # Tamaño fijo de la ventana (1000x700)

        # Elementos de la interfaz
        self.label_usuario = QLabel('Usuario:')
        self.label_contrasena = QLabel('Contraseña:')
        self.input_usuario = QLineEdit(self)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.boton_login = QPushButton('Iniciar sesión', self)
        self.mensaje_error = QLabel('')
        self.mensaje_error.setStyleSheet("color: red; font-weight: bold;")

        # Estilo para los elementos
        self.set_style()

        # Layouts de entrada de usuario y contraseña
        layout_usuario = QHBoxLayout()
        layout_usuario.addWidget(self.label_usuario)
        layout_usuario.addWidget(self.input_usuario)

        layout_contrasena = QHBoxLayout()
        layout_contrasena.addWidget(self.label_contrasena)
        layout_contrasena.addWidget(self.input_contrasena)

        # Layout principal (centrado)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Centra todo el contenido en el layout

        layout.addLayout(layout_usuario)
        layout.addLayout(layout_contrasena)
        layout.addWidget(self.boton_login)
        layout.addWidget(self.mensaje_error)

        # Espaciadores para asegurarnos de que los elementos estén centrados verticalmente
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaciador arriba
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaciador abajo

        # Crear un contenedor central para asegurarse de que el contenido se centre
        container = QWidget()
        container.setLayout(layout)

        # Establecemos el layout en el contenedor
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(container)

    def set_style(self):
        """Establece el estilo para los elementos de la interfaz"""
        # Estilo para los campos de texto
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #45a049;
            }
        """)
        self.input_contrasena.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #45a049;
            }
        """)

        # Estilo para el botón
        self.boton_login.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 10px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)

        # Estilo para las etiquetas
        self.label_usuario.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
        """)
        self.label_contrasena.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
        """)

        # Estilo para el mensaje de error
        self.mensaje_error.setStyleSheet("""
            font-size: 12px;
            color: red;
            font-weight: bold;
        """)

        # Fondo de la ventana (si deseas agregar una imagen)
        self.setStyleSheet("background-color: #f4f4f9;")  # Color de fondo claro
        # Si deseas agregar una imagen de fondo:
        # self.setStyleSheet("background-image: url('path/to/your/background.jpg');")

    def setup_login_function(self, validar_login):
        """Configura la función de validación del login"""
        self.boton_login.clicked.connect(validar_login)
