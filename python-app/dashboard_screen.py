import base64
import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
import pandas as pd
import fitz  # PyMuPDF para manejar archivos PDF
import re
from conect import conectar_mysql, conectar_mongo  # Importamos las funciones de conexión

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()

        global id_selected

        self.tab_widget = QTabWidget(self)

        self.tab_1 = self.create_tab_1()  
        self.tab_2 = self.create_tab_2()  
        self.tab_3 = self.create_tab_3()  

        self.tab_widget.addTab(self.tab_1, "Pestaña 1")
        self.tab_widget.addTab(self.tab_2, "Pestaña 2")
        self.tab_widget.addTab(self.tab_3, "Pestaña 3")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.tab_widget.currentChanged.connect(self.on_tab_change)
        

    def on_tab_change(self, index):
        if index == 0:  # Índice de la pestaña 1
            self.populate_table()

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

    def populate_table(self):
        mysql_db = conectar_mysql()
        mongo_db = conectar_mongo()

        if mysql_db:
            query = "SELECT nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv FROM empleados"
            df_mysql = pd.read_sql(query, mysql_db)
            mysql_db.close()
        else:
            df_mysql = pd.DataFrame() 

        df_mongo = pd.DataFrame() 

        df_final = pd.concat([df_mysql, df_mongo]).drop_duplicates().reset_index(drop=True)

        self.table.setRowCount(df_final.shape[0])
        self.table.setColumnCount(df_final.shape[1] + 1)  
        self.table.setHorizontalHeaderLabels(list(df_final.columns) + ['Acción'])

        def handle_details(row):
            print(self.id_selected)
            self.tab_widget.setCurrentIndex(2)


        # Ahora en el ciclo, puedes hacer lo siguiente:
        for i in range(df_final.shape[0]):
            for j in range(df_final.shape[1]):
                cell_value = str(df_final.iloc[i, j])

                if "data:image" in cell_value:
                    try:
                        # Extraer y agregar padding si es necesario
                        img_data = cell_value.split(',')[1]  # Extraer la parte base64
                        padding = '=' * (4 - len(img_data) % 4)  # Añadir el padding necesario
                        img_data = base64.b64decode(img_data + padding)

                        # Convertir los datos en una QPixmap
                        pixmap = QPixmap()
                        pixmap.loadFromData(QByteArray(img_data))

                        # Ajustar el tamaño de la imagen para que se ajuste a la celda
                        pixmap = pixmap.scaled(self.table.columnWidth(j), self.table.rowHeight(i), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        
                        # Crear un QLabel para mostrar la imagen
                        label = QLabel()
                        label.setPixmap(pixmap)
                        label.setAlignment(Qt.AlignCenter)  # Centrar la imagen

                        # Colocar el QLabel en la celda de la tabla
                        self.table.setCellWidget(i, j, label)
                    except (binascii.Error, IndexError) as e:
                        print(f"Error al decodificar la imagen: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value))  # Colocar texto en lugar de la imagen
                        
                # Si es un archivo PDF (base64)
                elif "data:application/pdf" in cell_value:
                    try:
                        match = re.search(r'name=([^;]+)', cell_value)  # Busca el nombre en la cadena
                        if match:
                            pdf_name = match.group(1)  # Extraemos el nombre del archivo
                        else:
                            pdf_name = "Hoja de Vida"  # Si no se encuentra el nombre, asignamos un nombre por defecto
                        
                        # Guardamos la URI base64 completa para la celda en la tabla
                        self.table.setItem(i, j, QTableWidgetItem(pdf_name))
                        self.table.item(i, j).setData(1000, cell_value)  # Establecemos los datos personalizados para la celda (base64 PDF)

                        # Conectamos el evento de clic en la celda
                        self.table.cellClicked.connect(self.handle_cell_click)

                    except Exception as e:
                        print(f"Error al decodificar el archivo PDF: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value))  # Colocar texto en lugar del nombre del archivo
                else:
                    self.table.setItem(i, j, QTableWidgetItem(cell_value))

            action_button = QPushButton("Ver Detalles")
            action_button.clicked.connect(lambda checked, row=i: handle_details(row))

            self.table.setCellWidget(i, df_final.shape[1], action_button) 

    def handle_cell_click(self, row, column):
        # Verificamos si la celda contiene un archivo PDF (base64)
        cell_value = self.table.item(row, column).data(1000)
        if cell_value and "data:application/pdf" in cell_value:
            pdf_data = cell_value.split(',')[1]  # Extraemos la parte base64
            try:
                # Decodificamos el contenido base64 del PDF
                pdf_bytes = base64.b64decode(pdf_data)
                
                # Obtener el nombre del archivo de la celda
                pdf_name = self.table.item(row, column).text()

                # Abrimos un cuadro de diálogo para guardar el archivo PDF con el nombre extraído
                file_path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", pdf_name, "PDF Files (*.pdf)")
                if file_path:
                    # Guardamos el PDF como un archivo
                    with open(file_path, "wb") as f:
                        f.write(pdf_bytes)
                    QMessageBox.information(self, "Descarga Completa", "El archivo PDF se ha descargado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo descargar el archivo PDF: {e}")

    def create_tab_2(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Campos de entrada
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        layout.addWidget(self.name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Número de Identidad")
        layout.addWidget(self.id_input)

        self.type_id_input = QLineEdit()
        self.type_id_input.setPlaceholderText("Tipo de Identidad")
        layout.addWidget(self.type_id_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Dirección")
        layout.addWidget(self.address_input)

        self.cargo_input = QLineEdit()
        self.cargo_input.setPlaceholderText("Cargo")
        layout.addWidget(self.cargo_input)

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
        record = {
            "nombre": self.name_input.text(),
            "numero_identidad": self.id_input.text(),
            "tipo_identidad": self.type_id_input.text(),
            "direccion": self.address_input.text(),
            "cargo": self.cargo_input.text(),
            "foto": f"data:image/jpeg;base64,{self.photo_data}" if self.photo_data else None,
            "hv": f"data:application/pdf;name={self.hv_name};base64,{self.hv_data}" if self.hv_data else None
        }

            # Conexión a la base de datos MySQL
        mysql_db = conectar_mysql()

        if mysql_db:
            try:
                cursor = mysql_db.cursor()
                query = """
                    INSERT INTO empleados (nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    record["nombre"],
                    record["numero_identidad"],
                    record["tipo_identidad"],
                    record["direccion"],
                    record["foto"],
                    record["cargo"],
                    record["hv"]
                )
                cursor.execute(query, values)
                mysql_db.commit() 
                QMessageBox.information(self, "Registro Guardado", "El registro se ha guardado correctamente.")
            except Exception as e:
                print(f"Error al guardar el registro: {e}")
                QMessageBox.critical(self, "Error", "No se pudo guardar el registro.")
            finally:
                cursor.close()
                mysql_db.close()

        QMessageBox.information(self, "Registro Guardado", "El registro se ha guardado correctamente.")

    def create_tab_3(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Crear los campos de entrada para mostrar los datos del empleado
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        layout.addWidget(self.name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Número de Identidad")
        layout.addWidget(self.id_input)

        self.type_id_input = QLineEdit()
        self.type_id_input.setPlaceholderText("Tipo de Identidad")
        layout.addWidget(self.type_id_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Dirección")
        layout.addWidget(self.address_input)

        self.cargo_input = QLineEdit()
        self.cargo_input.setPlaceholderText("Cargo")
        layout.addWidget(self.cargo_input)

        

        widget.setLayout(layout)
        return widget

    def fetch_data_by_id(self, id_selected):
        print(id_selected)
        """Busca los datos del empleado con el id_selected y los carga en los campos de entrada."""
        mysql_db = conectar_mysql()

        if mysql_db:
            try:
                cursor = mysql_db.cursor()
                query = """
                    SELECT nombre, numero_identidad, tipo_identidad, direccion, foto, cargo, hv
                    FROM empleados
                    WHERE numero_identidad = %s
                """
                cursor.execute(query, (id_selected,))
                result = cursor.fetchone()  # Obtiene una fila de la base de datos

                if result:
                    # Si encontramos resultados, los mostramos en los campos de entrada
                    self.name_input.setText(result[0])
                    self.id_input.setText(result[1])
                    self.type_id_input.setText(result[2])
                    self.address_input.setText(result[3])
                    self.cargo_input.setText(result[5])

                    # Si hay una foto (base64), también puedes manejarla aquí
                    if result[4]:  # foto
                        self.photo_data = result[4]
                    
                    # Si hay un archivo de hoja de vida (base64), también puedes manejarlo aquí
                    if result[6]:  # hv
                        self.hv_data = result[6]

                else:
                    QMessageBox.warning(self, "No Encontrado", "No se encontraron datos para este ID.")

            except Exception as e:
                print(f"Error al buscar el empleado: {e}")
                QMessageBox.critical(self, "Error", "No se pudo realizar la búsqueda.")
            finally:
                cursor.close()
                mysql_db.close()
