# app.py
import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from login_screen import LoginScreen
from dashboard_screen import DashboardScreen

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login - PyQt')
        self.setFixedSize(500, 300)  
        self.setStyleSheet("background-color: #f0f0f0;")  

        self.center()

        self.stacked_widget = QStackedWidget(self)

        self.login_screen = LoginScreen()
        self.dashboard_screen = DashboardScreen()

        self.setup_login_screen()
        self.setup_dashboard_screen()

        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.dashboard_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def setup_login_screen(self):
        """Configurar la pantalla de login"""
        def validar_login():
            usuario = self.login_screen.input_usuario.text()
            contrasena = self.login_screen.input_contrasena.text()

            conexion = self.conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
                cursor.execute(consulta, (usuario, contrasena))

                if cursor.fetchone():
                    self.login_screen.mensaje_error.setText('Login exitoso!')
                    self.login_screen.mensaje_error.setStyleSheet("color: green;")
                    self.stacked_widget.setCurrentIndex(1)
                else:
                    self.login_screen.mensaje_error.setText('Usuario o contraseña incorrectos.')
                    self.login_screen.mensaje_error.setStyleSheet("color: red;")
                    self.login_screen.input_contrasena.clear() 
                    
                cursor.close()
                conexion.close()
            else:
                self.login_screen.mensaje_error.setText('Error al conectar con la base de datos.')
                self.login_screen.mensaje_error.setStyleSheet("color: red;")

        self.login_screen.setup_login_function(validar_login)

    def setup_dashboard_screen(self):
        """Configurar la pantalla después del login"""
        pass

    def conectar_bd(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",  
                user="crud_user", 
                password="crudpassword", 
                database="crud_db" 
            )
            if conexion.is_connected():
                print("Conexión exitosa a la base de datos.")
                return conexion
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def center(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = LoginApp()
    ventana.show()
    sys.exit(app.exec_())
