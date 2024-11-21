import base64
import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
import pandas as pd
import fitz 
from conect import conectar_mysql, conectar_mongo  # Importamos las funciones de conexión

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()

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
        self.table.setColumnCount(df_final.shape[1])
        self.table.setHorizontalHeaderLabels(df_final.columns)

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
                        
                        label = QLabel()
                        label.setPixmap(pixmap)
                        label.setFixedSize(pixmap.size())
                        
                        self.table.setCellWidget(i, j, label)
                    except (binascii.Error, IndexError) as e:
                        print(f"Error al decodificar la imagen: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value))  
                elif "data:application/pdf" in cell_value:
                    try:
                        pdf_data = cell_value.split(',')[1]
                        padding = '=' * (4 - len(pdf_data) % 4)
                        pdf_data = base64.b64decode(pdf_data + padding)

                        pdf_path = "/tmp/temp_file.pdf"
                        with open(pdf_path, "wb") as f:
                            f.write(pdf_data)

                        pdf_document = fitz.open(pdf_path)
                        page = pdf_document.load_page(0)  
                        pix = page.get_pixmap()  
                        
                        img = QPixmap()
                        img.loadFromData(pix.tobytes())
                        
                        label_pdf = QLabel()
                        label_pdf.setPixmap(img)
                        label_pdf.setFixedSize(img.size())
                        
                        self.table.setCellWidget(i, j, label_pdf)

                    except Exception as e:
                        print(f"Error al decodificar el archivo PDF: {e}")
                        self.table.setItem(i, j, QTableWidgetItem(cell_value))
                else:
                    self.table.setItem(i, j, QTableWidgetItem(cell_value))

    def create_tab_2(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Formulario para Crear Nuevo Registro")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def create_tab_3(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Formulario para Actualizar Registro")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget
