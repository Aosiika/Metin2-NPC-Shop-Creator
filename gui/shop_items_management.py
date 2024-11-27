from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox, QFormLayout
import pymysql
import os
import json

class ShopItemsManagement(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QHBoxLayout()

        # Crear el layout vertical para el combobox y la tabla
        left_layout = QVBoxLayout()

        # ComboBox para seleccionar la tienda
        self.shop_combobox = QComboBox()
        self.shop_combobox.currentIndexChanged.connect(self.load_items)
        left_layout.addWidget(self.shop_combobox)

        # Tabla para mostrar los ítems
        self.items_table = QTableWidget()
        self.items_table.setMinimumWidth(400)
        self.items_table.itemSelectionChanged.connect(self.load_selected_item)
        left_layout.addWidget(self.items_table)

        # Añadir el layout de la izquierda al layout principal
        main_layout.addLayout(left_layout)

        # Formulario para añadir/editar ítems
        form_layout = QFormLayout()
        form_layout.setSpacing(5)  # Reducir el espaciado entre los elementos
        form_layout.setContentsMargins(0, 0, 0, 0)  # Reducir márgenes alrededor del layout

        # Campos del formulario
        self.item_vnum_input = QLineEdit()
        self.item_vnum_input.setPlaceholderText("Vnum del Ítem")
        form_layout.addRow("item_vnum:", self.item_vnum_input)

        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Cantidad")
        form_layout.addRow("count:", self.count_input)

        # Botones para interactuar con los ítems
        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Insertar")
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_item)
        button_layout.addWidget(self.update_button)

        # Nuevo botón para eliminar
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_item)
        button_layout.addWidget(self.delete_button)

        # Añadir el layout de botones al layout del formulario
        form_layout.addRow(button_layout)

        # Añadir el layout del formulario al layout principal
        main_layout.addLayout(form_layout)

        # Configurar el layout del widget
        self.setLayout(main_layout)

        # Configurar la tabla de ítems
        self.setup_items_table()

        # Cargar tiendas y datos iniciales
        self.load_shops()

    def setup_items_table(self):
        # Leer la configuración de la tabla de ítems desde el archivo JSON
        config_path = os.path.abspath(os.path.join("config", "shop_form_config.json"))

        if not os.path.exists(config_path):
            QMessageBox.critical(self, "Error", "No se encontró el archivo de configuración.")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)

            table_config = config.get("shop_items_table", {})
            columns = table_config.get("columns", [])

            # Configurar las columnas de la tabla
            self.items_table.setColumnCount(len(columns))
            self.items_table.setHorizontalHeaderLabels([col["label"] for col in columns])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al configurar la tabla de ítems: {str(e)}")

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
            cursor.execute("SELECT vnum, name FROM shop")
            rows = cursor.fetchall()
            for row in rows:
                self.shop_combobox.addItem(row[1], userData=row[0])

            connection.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las tiendas: {str(e)}")

    def load_items(self):
        # Limpiar la tabla
        self.items_table.setRowCount(0)

        # Obtener el vnum de la tienda seleccionada
        shop_vnum = self.shop_combobox.currentData()
        if shop_vnum is None:
            return

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
            cursor.execute("SELECT shop_vnum, item_vnum, count FROM shop_item WHERE shop_vnum = %s", (shop_vnum,))
            rows = cursor.fetchall()
            self.items_table.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, data in enumerate(row_data):
                    self.items_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

            connection.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los ítems: {str(e)}")

    def load_selected_item(self):
        # Obtener la fila seleccionada
        selected_row = self.items_table.currentRow()
        if selected_row == -1:
            return

        # Cargar los valores de la fila seleccionada en el formulario
        self.item_vnum_input.setText(self.items_table.item(selected_row, 1).text())
        self.count_input.setText(self.items_table.item(selected_row, 2).text())

    def add_item(self):
        # Obtener los valores de los campos del formulario
        shop_vnum = self.shop_combobox.currentData()
        item_vnum = self.item_vnum_input.text()
        count = self.count_input.text()

        if not item_vnum or not count or shop_vnum is None:
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
            cursor.execute("INSERT INTO shop_item (shop_vnum, item_vnum, count) VALUES (%s, %s, %s)", (shop_vnum, item_vnum, count))
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Ítem insertado correctamente.")
            self.load_items()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al insertar el ítem: {str(e)}")

    def update_item(self):
        selected_row = self.items_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un ítem para actualizar.")
            return

        # Obtener los valores de los campos del formulario
        shop_vnum = self.shop_combobox.currentData()
        item_vnum = self.item_vnum_input.text()
        count = self.count_input.text()

        if not item_vnum or not count or shop_vnum is None:
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
                "UPDATE shop_item SET count=%s WHERE shop_vnum=%s AND item_vnum=%s",
                (count, shop_vnum, item_vnum)
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Ítem actualizado correctamente.")
            self.load_items()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar el ítem: {str(e)}")

    def delete_item(self):
        selected_row = self.items_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un ítem para eliminar.")
            return

        # Obtener los valores de la fila seleccionada
        shop_vnum = self.shop_combobox.currentData()
        item_vnum = self.items_table.item(selected_row, 1).text()

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
            cursor.execute("DELETE FROM shop_item WHERE shop_vnum=%s AND item_vnum=%s", (shop_vnum, item_vnum))
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Éxito", "Ítem eliminado correctamente.")
            self.load_items()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el ítem: {str(e)}")
