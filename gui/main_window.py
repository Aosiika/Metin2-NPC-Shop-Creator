from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMenuBar, QTabWidget, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import os
import json
from gui.server_config_window import ServerConfigWindow
from gui.shop_management import ShopManagement
from gui.shop_items_management import ShopItemsManagement  # Importamos la nueva clase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NPC Shop Creator")
        self.setGeometry(100, 100, 800, 600)

        # Configurar el ícono de la ventana
        icon_path = os.path.abspath(os.path.join("resources", "logo.ico"))
        self.setWindowIcon(QIcon(icon_path))

        # Configurar el menú
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menú Configuración
        config_menu = menu_bar.addMenu("Configuración")

        # Acción de Configuración del Servidor
        config_server_action = QAction("Configuración del Servidor", self)
        config_server_action.triggered.connect(self.open_server_config)
        config_menu.addAction(config_server_action)

        # Acción "Acerca de"
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about_dialog)
        config_menu.addAction(about_action)

        # Crear un botón para recargar datos
        reload_action = QAction("Recargar Datos", self)
        reload_action.triggered.connect(self.reload_tabs)
        menu_bar.addAction(reload_action)

        # Crear el widget de pestañas
        self.tab_widget = QTabWidget()
        self.load_tabs_from_config()

        # Configurar el widget principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_tabs_from_config(self):
        # Ruta al archivo de configuración de pestañas
        tabs_config_path = os.path.abspath(os.path.join("config", "tabs_config.json"))

        # Leer la configuración de las pestañas
        if os.path.exists(tabs_config_path):
            try:
                with open(tabs_config_path, "r", encoding="utf-8") as config_file:
                    tabs_config = json.load(config_file)
                    for tab in tabs_config.get("tabs", []):
                        tab_type = tab.get("type", "text")
                        tab_name = tab.get("name", "Sin Nombre")
                        if tab_type == "shop_management":
                            self.add_shop_management_tab(tab_name)
                        elif tab_type == "shop_items_management":
                            self.add_shop_items_management_tab(tab_name)
                        elif tab_type == "text":
                            content = tab.get("content", "Contenido vacío")
                            self.add_text_tab(tab_name, content)
            except json.JSONDecodeError:
                print("Error: El archivo de configuración de pestañas no es válido.")
        else:
            print(f"Error: No se encontró el archivo de configuración en la ruta: {tabs_config_path}")

    def add_shop_management_tab(self, tab_name):
        # Añadir una pestaña de gestión de tiendas
        shop_management_widget = ShopManagement()
        self.tab_widget.addTab(shop_management_widget, tab_name)

    def add_shop_items_management_tab(self, tab_name):
        # Añadir una pestaña para añadir/editar items
        shop_items_management_widget = ShopItemsManagement()
        self.tab_widget.addTab(shop_items_management_widget, tab_name)

    def add_text_tab(self, tab_name, content):
        # Añadir una pestaña con contenido de texto
        text_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(content)
        layout.addWidget(label)
        text_widget.setLayout(layout)
        self.tab_widget.addTab(text_widget, tab_name)

    def open_server_config(self):
        # Abrir la ventana de configuración del servidor
        self.server_config_window = ServerConfigWindow()
        self.server_config_window.show()

    def show_about_dialog(self):
        # Mostrar un cuadro de diálogo con la información del programa y el creador
        QMessageBox.information(self, "Acerca de", "NPC Shop Creator\nVersión 1.0\nCreado por Ryen")

    def reload_tabs(self):
        # Recargar las pestañas eliminando las existentes y volviendo a cargarlas desde la configuración
        self.tab_widget.clear()
        self.load_tabs_from_config()
