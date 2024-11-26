import sys
import mysql.connector
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtGui import QIcon
from login_screen import LoginScreen
from dashboard_screen import DashboardScreen
from model import sync_data
from conect import conectar_login

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Respaldo de Datos')
        self.setWindowIcon(QIcon('./assets/2612467.png'))

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

        self.tarea_thread = threading.Thread(target=sync_data, daemon=True)
        self.tarea_thread.start()

    def setup_login_screen(self):
        def validar_login():
            usuario = self.login_screen.input_usuario.text()
            contrasena = self.login_screen.input_contrasena.text()
            conexion = conectar_login()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    consulta = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
                    cursor.execute(consulta, (usuario, contrasena))

                    if cursor.fetchone():
                        self.show_message_box("¡Login exitoso!", f"Bienvenido, {usuario}.", QMessageBox.Information)
                        self.stacked_widget.setCurrentIndex(1)
                    else:
                        self.show_message_box("Error", "Usuario o contraseña incorrectos.", QMessageBox.Critical)
                        self.login_screen.input_contrasena.clear()
                except mysql.connector.Error as e:
                    self.show_message_box("Error", f"Error de base de datos: {e}", QMessageBox.Critical)
                finally:
                    cursor.close()
                    conexion.close()
            else:
                self.show_message_box("Error", "Error al conectar con la base de datos.", QMessageBox.Critical)

        self.login_screen.setup_login_function(validar_login)

    def setup_dashboard_screen(self):
        """Configurar la pantalla después del login"""
        pass

    def show_message_box(self, title, message, icon):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

    def center(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = LoginApp()
    ventana.show()
    sys.exit(app.exec_())
