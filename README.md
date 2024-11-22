# 🛠️ **Respaldo de Bases de Datos** 🛠️

**¡Bienvenido al proyecto de respaldo automático de bases de datos MySQL y MongoDB!** 🎉 Este proyecto permite realizar respaldos automáticos de bases de datos en **MySQL** y **MongoDB**, utilizando **Docker Compose** para gestionar las bases de datos y ejecutando la aplicación en **Python** localmente. 👌

El objetivo principal del proyecto es crear una herramienta visual en Python con un **login** que se conecta a una base de datos MySQL aislada. Una vez que el usuario ingresa, podrá visualizar un CRUD conectado a ambas bases de datos (MySQL y MongoDB), asegurando que, en caso de caída de una base de datos, la otra se mantenga operativa. Además, cuando ambas bases estén activas, se actualizarán para reflejar la misma información. 🙌

---

## 📋 **Contenido**

- [Requisitos](#Requisitos)
- [Instalación](#Instalación)
- [Funcionalidades](#Funcionalidades)
- [Iniciar la Aplicación](#Iniciar-la-Aplicación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Redirección de puertos](#Redirección-de-puertos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## 🛠 **Requisitos**

- **Docker**: Para levantar los servicios de las bases de datos con Docker Compose.
- **Python 3.x**: Para ejecutar la aplicación localmente.
- **PyQt5**: Para la interfaz gráfica de usuario.

---

## ⚙ Instalación

### Usar Docker Compose

1. **Clonar el repositorio**:

  ```bash 
git clone https://github.com/tuusuario/respaldo-bases-datos.git
cd respaldo-bases-datos
  ``` 

2. **Levantar los servicios de bases de datos**: Ejecuta el siguiente comando para levantar los contenedores de **MySQL** y **MongoDB** usando Docker Compose.

  ```bash 
docker-compose up --build
  ``` 

Esto levantará los contenedores con las bases de datos necesarias. 🚀

3. **Instalar las dependencias de Python**: Asegúrate de tener un entorno Python configurado localmente, y luego instala las dependencias necesarias.

  ```bash 
pip install -r python-app/requirements.txt
  ``` 

4. **Ejecutar la aplicación Python**: Ejecuta el archivo `app.py` para iniciar la aplicación.

  ```bash 
python python-app/app.py
  ``` 

La aplicación se conectará automáticamente a las bases de datos levantadas por Docker Compose y te permitirá gestionar los respaldos de las bases de datos. 📂

---

## 🛠️ **Funcionalidades**

- **Pantalla de Login**: Permite a los usuarios autenticarse mediante su nombre de usuario y contraseña. 🔒
- **Pantalla de Dashboard**: Muestra un CRUD con las bases de datos **MySQL** y **MongoDB**, permitiendo realizar operaciones de respaldo. 💻
- **Sincronización entre MySQL y MongoDB**: La información se mantiene sincronizada entre ambas bases de datos. 🔄
- **Respaldo Automático**: Si una base de datos se cae, la otra sigue operativa, garantizando la disponibilidad de la información. ✅

---

## 🚀 **Iniciar la Aplicación**

Para ejecutar la aplicación con Docker Compose:

1. **Levanta los contenedores de las bases de datos** usando Docker Compose:

  ```bash 
docker-compose up --build
  ``` 

2. **Instala las dependencias** de Python:

  ```bash 
pip install -r python-app/requirements.txt
  ``` 

3. **Ejecuta la aplicación Python** localmente:

  ```bash 
python python-app/app.py
  ``` 

---

## 🗂️ **Estructura del Proyecto**

La estructura del proyecto es la siguiente:

  ```bash 
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

- **python-app/**: Contiene los scripts de la aplicación Python.
  - **app.py**: Script principal para la ejecución de la aplicación. 🚀
  - **conect.py**: Contiene la lógica de conexión con las bases de datos MySQL y MongoDB. 🔌
  - **dashboard_screen.py**: Pantalla principal donde se gestionan los respaldos de bases de datos. 📊
  - **login_screen.py**: Pantalla de inicio de sesión. 🔑
  - **requirements.txt**: Archivo de dependencias de Python. 📜

- **docker-compose.yml**: Define los servicios para levantar las bases de datos **MySQL** y **MongoDB**. 🛠️

---

## 🌐 **Redirección de puertos**

Si deseas acceder a las bases de datos desde tu máquina local, los puertos expuestos son:

- **MySQL** (login_mysql_container): `3306` 🔑
- **MySQL** (mysql_container): `3307` 🗃️
- **MongoDB** (mongodb_container): `27017` 📦

---

## 🧑‍💻 **Contribuciones**

¡Tu ayuda es bienvenida! 😃 Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un **fork** del repositorio. 🍴
2. Crea una nueva rama para tus cambios (`git checkout -b feature/nueva-funcionalidad`). 🌱
3. Realiza los cambios y haz commit de ellos (`git commit -am 'Agrega nueva funcionalidad'`). 💻
4. Empuja tus cambios (`git push origin feature/nueva-funcionalidad`). 🚀
5. Abre un **Pull Request** para discutir tus cambios. 📥

---

## 📄 **Licencia**

Este proyecto está bajo la **Licencia MIT**. Puedes ver más detalles en el archivo [LICENSE](LICENSE). 📜

---

## 🎉 ¡Gracias por usar este proyecto!

Si tienes alguna pregunta o sugerencia, no dudes en abrir un **issue** o **pull request**. ¡Estaré encantado de ayudarte! 😄

