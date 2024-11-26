import base64
import io
from PyQt5.QtCore import QSize 
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QComboBox, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QByteArray
import binascii 
from model import fetch_data, insert_data, update_data
import re

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(self.get_styles()) 

        # Resto de tu código...
        self.selected_data = None
        self.selected_edit_data = None
        self.id_Respaldo = None 

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

    def get_styles(self):
        return """
        QWidget {
            background-color: #f0f4f8;
            font-family: Arial, sans-serif;
            font-size: 10px;
            color: #333333;
        }
        QTabWidget::pane {
            border: none;
            background: white;
            border-radius: 5px;
            padding: 6px;
        }
        QTabBar::tab {
            background: #e1ecf7;
            border: 1px solid #c0d9f1;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 15px 26px; 
            font-size: 11px;
            color: #1a73e8;
        }
        QTabBar::tab:selected {
            background: #1a73e8;
            color: white;
            border-color: #1a73e8;
            border: none;
            text-decoration:none;
        }
        QLabel {
            font-size: 10px;
            font-weight: bold;
            color: #444444;
        }
        QLineEdit {
            border: 1px solid #ced4da;
            border-radius: 5px;
            padding: 8px;
            font-size: 10px;
            background-color: #f8f9fa;
        }
        QLineEdit:focus {
            border-color: #80bdff;
            background-color: #ffffff;
        }
        QPushButton {
            background-color: #1a73e8;
            color: white;
            border: none;  
            font-size: 10px;
            border-radius: 5px;
            cursor: pointer;
            padding: 8px 16px;
        }
        QPushButton:hover {
            background-color: #155cb0;
        }
        QPushButton:pressed {
            background-color: #0e47a1;
        }
        QTableWidget {
            border: 1px solid #ced4da;
            border-radius: 5px;
            gridline-color: #ced4da;
            background-color: white;
        }
        QTableWidget::item {
            padding: 6px;
            color: #333333;
        }
        QHeaderView::section {
            background-color: #1a73e8;
            color: white;
            font-weight: bold;
            border: none;
            padding: 6px;
        }
        QComboBox {
            border: 1px solid #ced4da;
            border-radius: 5px;
            padding: 8px;
            font-size: 10px;
            background-color: #f8f9fa;
        }
        QComboBox:focus {
            border-color: #80bdff;
            background-color: #ffffff;
        }
        QComboBox::drop-down {
            border-left: 1px solid #ced4da;
        }
        QComboBox::down-arrow {
            image: url('./assets/seleccione.png');
            width: 12px;  
            height: 12px;  
        }
        """
        
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

        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        self.selected_data = {
            "nombre": QLineEdit(),
            "numero_identidad": QLineEdit(),
            "tipo_identidad": QComboBox(),
            "direccion": QLineEdit(),
            "cargo": QComboBox()
        }

        for key, field in self.selected_data.items():
            label = QLabel(key.replace("_", " ").title())
            form_layout.addWidget(label)
            placeholder_text = key.replace("_", " ").title()  
            if isinstance(field, QLineEdit):  
                field.clear() 
                field.setPlaceholderText(placeholder_text)  
                form_layout.addWidget(field)
            elif isinstance(field, QComboBox):  
                field.clear()  
                field.addItem(f"Seleccione {placeholder_text.lower()}")  
                form_layout.addWidget(field)

        self.selected_data["tipo_identidad"].addItems([
            "Seleccione una opción", 
            "Cédula de Ciudadanía",
            "Tarjeta de Identidad",
            "Pasaporte",
            "Otro"
        ])

        self.selected_data["tipo_identidad"].setCurrentIndex(0)

        self.selected_data["cargo"].addItems([
            "Seleccione un cargo",
            "Administrador",
            "Auxiliar",
            "Monitor",
            "Otro"
        ])
        self.selected_data["cargo"].setCurrentIndex(0)

        form_layout.addSpacing(30)

        submit_button = QPushButton("Guardar Registro")
        submit_button.clicked.connect(self.save_record)
        form_layout.addWidget(submit_button)

        main_layout.addLayout(form_layout)

        image_layout = QVBoxLayout()

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("border: 1px solid #ced4da;")
        self.photo_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.photo_label)

        self.photo_button = QPushButton("Cargar Foto")
        self.photo_button.clicked.connect(self.load_photo)
        image_layout.addWidget(self.photo_button)

        self.hv_button = QPushButton("Cargar HV")
        self.hv_button.clicked.connect(self.load_hv)
        image_layout.addWidget(self.hv_button)

        main_layout.addLayout(image_layout)  

        widget.setLayout(main_layout)  
        return widget

    def create_tab_3(self):
        widget = QWidget()

        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        self.selected_edit_data = {
            "nombre": QLineEdit(),
            "numero_identidad": QLineEdit(),
            "tipo_identidad": QComboBox(),
            "direccion": QLineEdit(),
            "cargo": QComboBox()
        }

        for key, field in self.selected_edit_data.items():
            label = QLabel(key.replace("_", " ").title())
            form_layout.addWidget(label)
            placeholder_text = key.replace("_", " ").title()  
            if isinstance(field, QLineEdit):  
                field.clear() 
                field.setPlaceholderText(placeholder_text)  
                form_layout.addWidget(field)
            elif isinstance(field, QComboBox):  
                field.clear()  
                field.addItem(f"Seleccione {placeholder_text.lower()}")  
                form_layout.addWidget(field)

        self.selected_edit_data["tipo_identidad"].addItems([
            "Seleccione una opción", 
            "Cédula de Ciudadanía",
            "Tarjeta de Identidad",
            "Pasaporte",
            "Otro"
        ])
        self.selected_edit_data["tipo_identidad"].setCurrentIndex(0)

        self.selected_edit_data["cargo"].addItems([
            "Seleccione un cargo",
            "Administrador",
            "Auxiliar",
            "Monitor",
            "Otro"
        ])
        self.selected_edit_data["cargo"].setCurrentIndex(0)

        form_layout.addSpacing(30)

        submit_button = QPushButton("Actualizar Registro")
        submit_button.clicked.connect(self.update_record)
        form_layout.addWidget(submit_button)

        main_layout.addLayout(form_layout)

        image_layout = QVBoxLayout()

        self.photo_label2 = QLabel()
        self.photo_label2.setFixedSize(150, 150)
        self.photo_label2.setStyleSheet("border: 1px solid #ced4da;")
        self.photo_label2.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.photo_label2)

        self.photo_button = QPushButton("Cargar Foto")
        self.photo_button.clicked.connect(self.load_photo)
        image_layout.addWidget(self.photo_button)

        self.hv_button = QPushButton("Cargar HV")
        self.hv_button.clicked.connect(self.load_hv)
        image_layout.addWidget(self.hv_button)
    
        main_layout.addLayout(image_layout)  
        widget.setLayout(main_layout)  
        return widget

    def on_tab_change(self, index):
        if index == 0:
            self.populate_table()
        if index == 1:
            self.update_selected_row_label(1)        
    def update_selected_row_label(self,index=0):   

        if index == 1:
            self.selected_data["nombre"].setText("")
            self.selected_data["numero_identidad"].setText("")
            self.selected_data["tipo_identidad"].setCurrentIndex(0)
            self.selected_data["direccion"].setText("")
            self.selected_data["cargo"].setCurrentIndex(0)
            self.photo_label.setPixmap(QPixmap())
            self.photo_data = None
            self.hv_data = None
            return

        if self.selected_data is not None and index == 2:
            
            self.selected_edit_data["nombre"].setText(self.selected_data["nombre"])
            self.selected_edit_data["numero_identidad"].setText(self.selected_data["numero_identidad"])
            self.selected_edit_data["tipo_identidad"].setCurrentText(self.selected_data["tipo_identidad"])
            self.selected_edit_data["direccion"].setText(self.selected_data["direccion"])
            self.selected_edit_data["cargo"].setCurrentText(self.selected_data["cargo"])
            if self.selected_data["foto"] is not None:
                img_data = self.selected_data["foto"].split(',')[1]
                padding = '=' * (4 - len(img_data) % 4) 
                img_data = base64.b64decode(img_data + padding) 
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(img_data)) 
                pixmap = pixmap.scaled(self.photo_label2.width(), self.photo_label2.height(),
                                    Qt.KeepAspectRatio, Qt.SmoothTransformation)

                self.photo_label2.setPixmap(pixmap)
            if self.selected_data["hv"] is not None: 
                self.hv_button.setStyleSheet("background-color: #28a745; color: white;")
                  
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
            self.id_Respaldo = df_final.iloc[row]["id_Respaldo"]
            self.tab_widget.setCurrentIndex(2) 
            self.update_selected_row_label(2)

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

            action_button = QPushButton()
            icon = QIcon("./assets/1159633.png") 
            action_button.setIcon(icon)
            action_button.setIconSize(QSize(10, 10)) 

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
            pixmap = QPixmap(file_path)
            self.photo_label.setPixmap(pixmap.scaled(self.photo_label.width(), self.photo_label.height(), Qt.KeepAspectRatio))
            self.photo_label2.setPixmap(pixmap.scaled(self.photo_label2.width(), self.photo_label2.height(), Qt.KeepAspectRatio))
            with open(file_path, "rb") as f:
                self.photo_data = base64.b64encode(f.read()).decode('utf-8')
            QMessageBox.information(self, "Foto Cargada", "La foto se ha cargado correctamente.")

    def load_hv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar HV", "", "PDF Files (*.pdf)")
        if file_path:
            with open(file_path, "rb") as f:
                self.hv_data = base64.b64encode(f.read()).decode('utf-8')
            self.hv_name = file_path.split("/")[-1]

            if self.hv_data:  
                self.hv_button.setStyleSheet("background-color: #28a745; color: white;")
            else:  
                self.hv_button.setStyleSheet("background-color: #f8f9fa; color: black;")

            QMessageBox.information(self, "HV Cargada", "La hoja de vida se ha cargado correctamente.")

    def save_record(self):
        self._handle_record_action(self.selected_data, insert_data)

    def update_record(self):
        self._handle_record_action(self.selected_edit_data, update_data)

    def _extract_record_data(self, data_source):
        return {
            "nombre": data_source["nombre"].text(),
            "numero_identidad": data_source["numero_identidad"].text(),
            "tipo_identidad": data_source["tipo_identidad"].currentText(),
            "direccion": data_source["direccion"].text(),
            "cargo": data_source["cargo"].currentText(),
            "foto": f"data:image/jpeg;base64,{self.photo_data}" if self.photo_data else None,
            "hv": f"data:application/pdf;base64,{self.hv_data}" if self.hv_data else None,
            "id_Respaldo": self.id_Respaldo
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



        




