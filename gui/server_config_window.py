from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
import os
import json

class ServerConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración del Servidor")
        self.setGeometry(150, 150, 400, 300)

        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Layout de la izquierda con los campos de configuración
        config_layout = QVBoxLayout()

        # Campos de configuración
        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText("Host o IP")
        config_layout.addWidget(QLabel("Host o IP:"))
        config_layout.addWidget(self.host_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Usuario")
        config_layout.addWidget(QLabel("Usuario:"))
        config_layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        config_layout.addWidget(QLabel("Contraseña:"))
        config_layout.addWidget(self.password_input)

        self.db_name_input = QLineEdit(self)
        self.db_name_input.setPlaceholderText("Nombre de la Base de Datos")
        config_layout.addWidget(QLabel("Nombre de la Base de Datos:"))
        config_layout.addWidget(self.db_name_input)

        # Botones de guardar y probar conexión
        self.save_button = QPushButton("Guardar", self)
        self.save_button.clicked.connect(self.save_config)
        config_layout.addWidget(self.save_button)

        self.test_button = QPushButton("Probar Conexión", self)
        self.test_button.clicked.connect(self.test_connection)
        config_layout.addWidget(self.test_button)

        # Añadir el layout de la configuración al layout principal
        main_layout.addLayout(config_layout)

        # Configurar el layout principal en la ventana de diálogo
        self.setLayout(main_layout)

        # Cargar la configuración si existe
        self.load_config()

    def load_config(self):
        # Ruta al archivo de configuración
        config_file_path = "config/config_server.json"

        # Si el archivo de configuración existe, cargar los datos
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, "r") as config_file:
                    config_data = json.load(config_file)
                    # Rellenar los campos con los valores cargados
                    self.host_input.setText(config_data.get("host", ""))
                    self.user_input.setText(config_data.get("user", ""))
                    self.password_input.setText(config_data.get("password", ""))
                    self.db_name_input.setText(config_data.get("database", ""))
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "El archivo de configuración no es válido. Asegúrate de que el formato sea correcto.")

    def save_config(self):
        # Crear el directorio "config" si no existe
        if not os.path.exists("config"):
            os.makedirs("config")

        # Guardar la configuración en un archivo JSON
        config_data = {
            "host": self.host_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "database": self.db_name_input.text()
        }

        with open("config/config_server.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4)

        QMessageBox.information(self, "Éxito", "Configuración guardada con éxito.")

    def test_connection(self):
        # Intentar conectarse a la base de datos usando la configuración ingresada
        import pymysql
        try:
            connection = pymysql.connect(
                host=self.host_input.text(),
                user=self.user_input.text(),
                password=self.password_input.text(),
                database=self.db_name_input.text()
            )
            connection.close()
            QMessageBox.information(self, "Éxito", "Conexión exitosa a la base de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {str(e)}")
