from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QFormLayout, QMessageBox
import pymysql
import os
import json

class ShopManagement(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QHBoxLayout()

        # Tabla para mostrar las tiendas
        self.shop_table = QTableWidget()
        self.shop_table.setColumnCount(3)  # vnum, name, npc_vnum
        self.shop_table.setHorizontalHeaderLabels(["vnum", "name", "npc_vnum"])
        self.shop_table.setMinimumWidth(400)
        self.shop_table.itemSelectionChanged.connect(self.load_selected_shop)
        main_layout.addWidget(self.shop_table)

        # Formulario para añadir/editar tiendas
        form_layout = QFormLayout()
        form_layout.setSpacing(5)  # Reducir el espaciado entre los elementos
        form_layout.setContentsMargins(0, 0, 0, 0)  # Reducir márgenes alrededor del layout

        # Campos del formulario
        self.vnum_input = QLineEdit()
        self.vnum_input.setPlaceholderText("Número único para la tienda")
        form_layout.addRow("vnum:", self.vnum_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la tienda")
        form_layout.addRow("name:", self.name_input)

        self.npc_vnum_input = QLineEdit()
        self.npc_vnum_input.setPlaceholderText("Vnum del NPC asociado")
        form_layout.addRow("npc_vnum:", self.npc_vnum_input)

        # Botones para interactuar con las tiendas
        button_layout = QVBoxLayout()
        self.insert_button = QPushButton("Insertar")
        self.insert_button.clicked.connect(self.insert_shop)
        button_layout.addWidget(self.insert_button)

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_shop)
        button_layout.addWidget(self.update_button)

        self.clear_button = QPushButton("Limpiar formulario")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)

        # Nuevo botón para eliminar
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_shop)
        button_layout.addWidget(self.delete_button)

        # Añadir el layout de botones al layout del formulario
        form_layout.addRow(button_layout)

        # Añadir el layout del formulario al layout principal
        main_layout.addLayout(form_layout)

        # Configurar el layout del widget
        self.setLayout(main_layout)

        # Cargar tiendas y datos iniciales
        self.load_shops()

    def load_shops(self):
        # Leer la configuración de la base de datos
        config_path = os.path.abspath(os.path.join("config", "config_server.json"))

        if not os.path.exists(config_path):
            QMessageBox.critical(self, "Error", "No se encontró el archivo de configuración.")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)

            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT vnum, name, npc_vnum FROM shop")
            rows = cursor.fetchall()
            self.shop_table.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.shop_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            connection.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las tiendas: {str(e)}")

    def load_selected_shop(self):
        # Obtener la fila seleccionada
        selected_row = self.shop_table.currentRow()
        if selected_row == -1:
            return

        # Cargar los valores de la fila seleccionada en el formulario
        self.vnum_input.setText(self.shop_table.item(selected_row, 0).text())
        self.name_input.setText(self.shop_table.item(selected_row, 1).text())
        self.npc_vnum_input.setText(self.shop_table.item(selected_row, 2).text())

    def insert_shop(self):
        # Obtener los valores del formulario
        vnum = self.vnum_input.text()
        name = self.name_input.text()
        npc_vnum = self.npc_vnum_input.text()

        if not vnum or not name or not npc_vnum:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            # Leer la configuración de la base de datos
            config_path = os.path.abspath(os.path.join("config", "config_server.json"))
            if not os.path.exists(config_path):
                QMessageBox.critical(self, "Error", "No se encontró el archivo de configuración.")
                return

            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)

            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
            
            cursor = connection.cursor()
            cursor.execute("INSERT INTO shop (vnum, name, npc_vnum) VALUES (%s, %s, %s)", (vnum, name, npc_vnum))
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Tienda insertada correctamente.")
            self.load_shops()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al insertar la tienda: {str(e)}")

    def update_shop(self):
        selected_row = self.shop_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione una tienda para actualizar.")
            return

        # Obtener los valores del formulario
        vnum = self.vnum_input.text()
        name = self.name_input.text()
        npc_vnum = self.npc_vnum_input.text()

        if not vnum or not name or not npc_vnum:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            # Leer la configuración de la base de datos
            config_path = os.path.abspath(os.path.join("config", "config_server.json"))
            if not os.path.exists(config_path):
                QMessageBox.critical(self, "Error", "No se encontró el archivo de configuración.")
                return

            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)

            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
            
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE shop SET name=%s, npc_vnum=%s WHERE vnum=%s",
                (name, npc_vnum, vnum)
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Tienda actualizada correctamente.")
            self.load_shops()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar la tienda: {str(e)}")

    def delete_shop(self):
        selected_row = self.shop_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione una tienda para eliminar.")
            return

        # Obtener el vnum de la fila seleccionada
        vnum = self.shop_table.item(selected_row, 0).text()

        try:
            # Leer la configuración de la base de datos
            config_path = os.path.abspath(os.path.join("config", "config_server.json"))
            if not os.path.exists(config_path):
                QMessageBox.critical(self, "Error", "No se encontró el archivo de configuración.")
                return

            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)

            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
            
            cursor = connection.cursor()
            cursor.execute("DELETE FROM shop WHERE vnum = %s", (vnum,))
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Tienda eliminada correctamente.")
            self.load_shops()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar la tienda: {str(e)}")

    def clear_form(self):
        # Limpiar todos los campos del formulario
        self.vnum_input.clear()
        self.name_input.clear()
        self.npc_vnum_input.clear()
