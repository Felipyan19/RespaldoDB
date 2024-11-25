import base64
import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
from model import fetch_data, insert_data, update_data
import fitz  
import re

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_data = None
        self.selected_edit_data = None

        self.tab_widget = QTabWidget(self)

        self.tab_1 = self.create_tab_1()  
        self.tab_2 = self.create_tab_2()  
        self.tab_3 = self.create_tab_3()  

        self.tab_widget.addTab(self.tab_1, "Listar empleados")
        self.tab_widget.addTab(self.tab_2, "Crear empleado")
        self.tab_widget.addTab(self.tab_3, "Actualizar empleado")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.tab_widget.currentChanged.connect(self.on_tab_change)
        
    def create_tab_1(self):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Datos de la Base de Datos")
        layout.addWidget(label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.populate_table()

        widget.setLayout(layout)
        return widget

    def create_tab_2(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Crear un diccionario para almacenar todos los datos
        self.selected_data = {
            "nombre": QLineEdit(),
            "numero_identidad": QLineEdit(),
            "tipo_identidad": QLineEdit(),
            "direccion": QLineEdit(),
            "foto": QLineEdit(),
            "cargo": QLineEdit(),
            "hv": QLineEdit()
        }

        # Configurar el campo "nombre"
        self.selected_data["nombre"].setPlaceholderText("Nombre")
        layout.addWidget(self.selected_data["nombre"])

        # Configurar el campo "numero_identidad"
        self.selected_data["numero_identidad"].setPlaceholderText("Número de Identidad")
        layout.addWidget(self.selected_data["numero_identidad"])

        # Configurar el campo "tipo_identidad"
        self.selected_data["tipo_identidad"].setPlaceholderText("Tipo de Identidad")
        layout.addWidget(self.selected_data["tipo_identidad"])

        # Configurar el campo "direccion"
        self.selected_data["direccion"].setPlaceholderText("Dirección")
        layout.addWidget(self.selected_data["direccion"])

        # Configurar el campo "cargo"
        self.selected_data["cargo"].setPlaceholderText("Cargo")
        layout.addWidget(self.selected_data["cargo"])

        # Botón para cargar foto
        self.photo_data = None  # Para almacenar la foto en base64
        self.photo_button = QPushButton("Cargar Foto")
        self.photo_button.clicked.connect(self.load_photo)
        layout.addWidget(self.photo_button)

        # Botón para cargar HV (PDF)
        self.hv_data = None  # Para almacenar el PDF en base64
        self.hv_button = QPushButton("Cargar HV")
        self.hv_button.clicked.connect(self.load_hv)
        layout.addWidget(self.hv_button)

        # Botón de enviar
        submit_button = QPushButton("Guardar Registro")
        submit_button.clicked.connect(self.save_record)
        layout.addWidget(submit_button)

        widget.setLayout(layout)
        return widget

    def create_tab_3(self):
        
        widget = QWidget()
        layout = QVBoxLayout()

        self.selected_edit_data = {
            "nombre": QLineEdit(),
            "numero_identidad": QLineEdit(),
            "tipo_identidad": QLineEdit(),
            "direccion": QLineEdit(),
            "foto": QLineEdit(),
            "cargo": QLineEdit(),
            "hv": QLineEdit()
        }

        self.photo_data = None  # Para almacenar la foto en base64
        self.photo_button = QPushButton("Cargar Foto")
        self.photo_button.clicked.connect(self.load_photo)
        
        # Botón para cargar HV (PDF)
        self.hv_data = None  # Para almacenar el PDF en base64
        self.hv_button = QPushButton("Cargar HV")
        self.hv_button.clicked.connect(self.load_hv)
        
        self.selected_row_label = QLabel()
        self.selected_row_label.setFixedSize(200, 15)

        submit_button = QPushButton("Actualizar Registro")
        submit_button.clicked.connect(self.update_record)

        layout.addWidget(self.selected_row_label)
        if self.selected_data is not None:
            layout.addWidget(self.selected_edit_data["nombre"])
            layout.addWidget(self.selected_edit_data["numero_identidad"])
            layout.addWidget(self.selected_edit_data["tipo_identidad"])
            layout.addWidget(self.selected_edit_data["direccion"])
            layout.addWidget(self.selected_edit_data["cargo"])
            layout.addWidget(self.photo_button)
            layout.addWidget(self.hv_button)
            layout.addWidget(submit_button)
        widget.setLayout(layout)
        return widget  

    def on_tab_change(self, index):
        if index == 0:
            self.populate_table()
        
    def update_selected_row_label(self):
        print(self.selected_data)
        print(self.selected_edit_data)
        if self.selected_data is not None:
            self.selected_row_label.setText(f"Actualizar registro # {self.selected_data["numero_identidad"]}")
            for key, value in self.selected_data.items():
                self.selected_edit_data[key].setText(value)
        else:
            self.selected_row_label.setText("No se ha seleccionado ninguna fila")
    
    def populate_table(self):
        df_final = fetch_data()

        self.table.setRowCount(df_final.shape[0])
        self.table.setColumnCount(df_final.shape[1] + 1)  
        self.table.setHorizontalHeaderLabels(list(df_final.columns) + ['Acción'])

        def handle_details(row):
            self.selected_data = {
                "nombre": df_final.iloc[row]["nombre"],
                "numero_identidad": df_final.iloc[row]["numero_identidad"],
                "tipo_identidad": df_final.iloc[row]["tipo_identidad"],
                "direccion": df_final.iloc[row]["direccion"],
                "foto": df_final.iloc[row]["foto"],
                "cargo": df_final.iloc[row]["cargo"],
                "hv": df_final.iloc[row]["hv"]
            }
            self.tab_widget.setCurrentIndex(2) 
            self.update_selected_row_label()

        for i in range(df_final.shape[0]):
            for j in range(df_final.shape[1]):
                cell_value = str(df_final.iloc[i, j])

                if "data:image" in cell_value:
                    try:
                        img_data = cell_value.split(',')[1]  
                        padding = '=' * (4 - len(img_data) % 4)  
                        img_data = base64.b64decode(img_data + padding)

                        pixmap = QPixmap()
                        pixmap.loadFromData(QByteArray(img_data))

                        pixmap = pixmap.scaled(self.table.columnWidth(j), self.table.rowHeight(i), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        
                        label = QLabel()
                        label.setPixmap(pixmap)
                        label.setAlignment(Qt.AlignCenter)  

                        self.table.setCellWidget(i, j, label)
                    except (binascii.Error, IndexError) as e:
                        print(f"Error al decodificar la imagen: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value)) 

                elif "data:application/pdf" in cell_value:
                    try:
                        match = re.search(r'name=([^;]+)', cell_value)  
                        if match:
                            pdf_name = match.group(1)  
                        else:
                            pdf_name = "Hoja de Vida"  
                        
                        self.table.setItem(i, j, QTableWidgetItem(pdf_name))
                        self.table.item(i, j).setData(1000, cell_value)  
                        self.table.cellClicked.connect(self.handle_cell_click)

                    except Exception as e:
                        print(f"Error al decodificar el archivo PDF: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value)) 
                else:
                    self.table.setItem(i, j, QTableWidgetItem(cell_value))

            action_button = QPushButton("Ver Detalles")
            action_button.clicked.connect(lambda checked, row=i: handle_details(row))

            self.table.setCellWidget(i, df_final.shape[1], action_button) 

    def handle_cell_click(self, row, column):
        cell_value = self.table.item(row, column).data(1000)
        
        if cell_value and "data:application/pdf" in cell_value:
            pdf_data = cell_value.split(',')[1]  
            try:
                pdf_bytes = base64.b64decode(pdf_data)
                pdf_name = self.table.item(row, column).text()
                file_path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", pdf_name, "PDF Files (*.pdf)")

                if file_path:
                    with open(file_path, "wb") as f:
                        f.write(pdf_bytes)
                    QMessageBox.information(self, "Descarga Completa", "El archivo PDF se ha descargado correctamente.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo descargar el archivo PDF: {e}")

    def load_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            with open(file_path, "rb") as f:
                self.photo_data = base64.b64encode(f.read()).decode('utf-8')
            QMessageBox.information(self, "Foto Cargada", "La foto se ha cargado correctamente.")

    def load_hv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar HV", "", "PDF Files (*.pdf)")
        if file_path:
            with open(file_path, "rb") as f:
                self.hv_data = base64.b64encode(f.read()).decode('utf-8')
            self.hv_name = file_path.split("/")[-1]
            QMessageBox.information(self, "HV Cargada", "La hoja de vida se ha cargado correctamente.")

    def save_record(self):
        self._handle_record_action(self.selected_data, insert_data)

    def update_record(self):
        self._handle_record_action(self.selected_edit_data, update_data)

    def _extract_record_data(self, data_source):
        return {
            "nombre": data_source["nombre"].text(),
            "numero_identidad": data_source["numero_identidad"].text(),
            "tipo_identidad": data_source["tipo_identidad"].text(),
            "direccion": data_source["direccion"].text(),
            "cargo": data_source["cargo"].text(),
            "foto": f"data:image/jpeg;base64,{self.photo_data}" if self.photo_data else None,
            "hv": f"data:application/pdf;base64,{self.hv_data}" if self.hv_data else None
        }

    def _validate_record(self, record):
        
        if not record["nombre"] or not record["numero_identidad"] or not record["tipo_identidad"]:
            QMessageBox.warning(self, "Error", "Todos los campos obligatorios deben ser llenados.")
            return False
        return True

    def _show_message(self, title, message):
        if title == "Error":
            QMessageBox.warning(self, title, message)
        else:
            QMessageBox.information(self, title, message)

    def _handle_record_action(self, data_source, action_function):
        record = self._extract_record_data(data_source)
        
        if not self._validate_record(record):
            return
        
        title, message = action_function(record)
        self._show_message(title, message)



        




