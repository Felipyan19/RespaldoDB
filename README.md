# 🛠️ **Respaldo de Bases de Datos** 🛠️

**¡Bienvenido al proyecto de respaldo automático de bases de datos MySQL y MongoDB!** 🎉 Este proyecto te permite gestionar respaldos de bases de datos con una **interfaz gráfica** desarrollada en **PyQt5**. Además, puedes ejecutarlo de manera local o dentro de contenedores **Docker**. 🙌

---

## 📋 **Contenido**

- [Instalación y Configuración](#instalación-y-configuración)
- [Funcionalidades](#funcionalidades)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requerimientos](#requerimientos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## 🏗️ **Instalación y Configuración**

Sigue estos pasos para comenzar a usar el proyecto en tu entorno local:

### 1. **Clonar el repositorio**

Para clonar el repositorio y comenzar a trabajar con él en tu máquina local, utiliza el siguiente comando:

 ```bash 
git clone https://github.com/tuusuario/respaldo-bases-datos.git
cd respaldo-bases-datos
 ``` 

### 2. **Instalar las dependencias**

Asegúrate de tener **Python** y **pip** instalados. Luego, instala todas las dependencias necesarias con:

 ```bash 
pip install -r requirements.txt
 ``` 

### 3. **Configurar las credenciales de las bases de datos**

Antes de ejecutar el proyecto, necesitas configurar las credenciales de tus bases de datos en los archivos de configuración. Edita los siguientes archivos:

- `config/mysql_config.json` (Credenciales para MySQL)
- `config/mongo_config.json` (Credenciales para MongoDB)

¡Asegúrate de que las credenciales sean correctas! 🔑

### 4. **Ejecutar el proyecto localmente**

Con todo configurado, puedes ejecutar la aplicación de manera local con:

 ```bash 
python app.py
 ``` 

¡Esto iniciará la interfaz gráfica donde podrás gestionar los respaldos! 💻

### 5. **(Opcional) Ejecutar con Docker**

Si prefieres ejecutar el proyecto dentro de un contenedor **Docker**, utiliza el archivo `docker-compose.yml` para construir y levantar los servicios. Asegúrate de tener **Docker** y **Docker Compose** instalados. Para levantar los contenedores, ejecuta:

 ```bash 
docker-compose up --build
 ``` 

Este comando construirá los contenedores y pondrá en marcha el servicio de Python, MySQL y MongoDB.

---

## 🛠️ **Funcionalidades**

Este proyecto permite las siguientes funcionalidades:

- **Respaldos de bases de datos MySQL y MongoDB**: ¡Haz copias de seguridad de tus datos con facilidad! 💾
- **Visualizar el estado de los respaldos realizados**: Consulta el historial de respaldos para tus bases de datos. 📈
- **Recuperar respaldos desde las bases de datos**: Recupera cualquier respaldo realizado para restaurar tus datos. 🔄

Todo esto se puede hacer de manera sencilla con la interfaz gráfica desarrollada en **PyQt5**. 🌐

---

## 🗂️ **Estructura del Proyecto**

La estructura del proyecto es la siguiente:

 ```py
respaldosDB/
│
├── python-app/
│   ├── app.py
│   ├── conect.py
│   ├── dashboard_screen.py
│   ├── login_screen.py
│   └── requirements.txt
│
└── docker-compose.yml                 
```
---

## ⚙️ **Requerimientos**

Para ejecutar este proyecto, necesitas tener instalados los siguientes programas:

- **Python 3.10 o superior** 🐍
- **MySQL 8.0 o superior** 🗄️
- **MongoDB 6.0 o superior** 🗄️
- **PyQt5** para la interfaz gráfica 🖥️

---

## 🧑‍💻 **Contribuciones**

¡Tu ayuda es bienvenida! 😃 Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un **fork** del repositorio.
2. Crea una nueva rama para tus cambios (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit de ellos (`git commit -am 'Agrega nueva funcionalidad'`).
4. Empuja tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un **Pull Request** para discutir tus cambios.

---

## 📄 **Licencia**

Este proyecto está bajo la **Licencia MIT**. Puedes ver más detalles en el archivo [LICENSE](LICENSE).

---

## 🎉 ¡Gracias por usar este proyecto!

Si tienes alguna pregunta o sugerencia, no dudes en abrir un **issue** o **pull request**. ¡Estaré encantado de ayudarte! 😄
