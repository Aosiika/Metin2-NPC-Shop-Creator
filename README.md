# NPC Shop Creator - Gestor de Tiendas para Metin2

## Descripción

**NPC Shop Creator** es una herramienta poderosa y fácil de usar que permite gestionar tiendas NPC para el juego **Metin2** conectándose directamente a la base de datos del servidor. Con esta aplicación, puedes **crear, actualizar o eliminar NPCs de tiendas** así como **gestionar los objetos que venden** de manera eficiente y sin complicaciones.

### Características principales:

- **Creación de NPCs de tiendas**: Agrega NPCs de manera sencilla que actuarán como tiendas dentro del juego.
- **Actualización de NPCs existentes**: Modifica la configuración de tiendas actuales, incluyendo el nombre, vnum y otros atributos clave.
- **Eliminación de NPCs**: Borra tiendas NPC de manera segura y rápida.
- **Gestión de Objetos de Tienda**: Añade, actualiza o elimina los objetos que vende cada tienda, con una interfaz visual intuitiva que permite el manejo de los items de manera precisa.

## Requisitos

Antes de poder usar **NPC Shop Creator**, necesitas tener lo siguiente:

1. **Python 3.8+**
2. **Entorno Virtual** (recomendado para aislar las dependencias).
3. **PyMySQL**: Para conectarse a la base de datos de Metin2.
4. **PyQt6**: Para la interfaz gráfica de usuario.
5. **Base de Datos de Metin2**: Configurada y accesible.
6. **PyInstaller** (opcional): Si deseas compilar la aplicación como un ejecutable.

Para instalar las dependencias necesarias, puedes usar el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Instalación y Ejecución

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/Aosiika/npc-shop-creator.git
   cd npc-shop-creator
   ```

2. **Configura el entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate    # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuración del Servidor**:

   Crea o edita el archivo `config/config_server.json` para introducir los datos de conexión de tu base de datos del servidor:

   ```json
   {
     "host": "IP_DEL_SERVIDOR",
     "user": "TU_USUARIO",
     "password": "TU_CONTRASEÑA",
     "database": "NOMBRE_BASE_DE_DATOS"
   }
   ```

5. **Ejecuta la Aplicación**:

   ```bash
   python main.py
   ```

6. **Compilación (Opcional)**: Para crear un ejecutable con PyInstaller:

   ```bash
   pyinstaller --onefile --windowed --icon=resources/logo.ico main.py
   ```

## Uso del Programa

Al abrir **NPC Shop Creator**, te encontrarás con una interfaz gráfica que permite:

- **Crear y editar tiendas** en la pestaña correspondiente, introduciendo detalles como el `vnum`, el `name` y otros atributos.
- **Administrar objetos** que vende cada tienda, donde podrás agregar, modificar y eliminar los objetos listados de una manera sencilla.
- **Configuración del Servidor**: El menú "Configuración" te permite definir los datos de conexión de la base de datos.
- **Recargar Datos**: Si ocurre algún cambio en la base de datos externa, puedes utilizar la opción de recarga para actualizar la información en la aplicación.
- **Acerca de**: Muestra información sobre el programa y el creador, Ryen.

## Estructura del Proyecto

```
project/
│
├── main.py
├── gui/
│   ├── main_window.py
│   ├── shop_management.py
│   └── shop_items_management.py
├── config/
│   └── config_server.json
│   └── shop_form_config.json
│   └── tabs_config.json
├── resources/
│   └── logo.ico
├── requirements.txt
└── README.md
```

- **main.py**: Punto de entrada principal para la aplicación.
- **gui/**: Contiene los módulos que definen la interfaz de usuario.
- **config/**: Archivos de configuración como `config_server.json`.
- **resources/**: Archivos de recursos como el logo.

## Contribuciones

Las contribuciones son bienvenidas. Puedes abrir **issues** para reportar errores o hacer sugerencias, y también realizar **pull requests** si deseas mejorar el código.

Para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con la funcionalidad o el error que deseas arreglar: `git checkout -b nueva-funcionalidad`.
3. Realiza tus cambios y sube tu código: `git push origin nueva-funcionalidad`.
4. Crea un pull request hacia el repositorio principal.

## Licencia

Este proyecto está bajo la licencia **MIT**. Puedes usar, modificar y distribuir este software libremente.

## Contacto

Para cualquier duda o sugerencia, puedes contactar al creador del proyecto, **Ryen**, a través de su perfil de GitHub.

---

