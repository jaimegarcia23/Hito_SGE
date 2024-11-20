# Hito\_SGE: Sistema de Gestión Empresarial

Este proyecto consiste en una aplicación para la gestión de encuestas, utilizando Python y MySQL. A continuación, se detallan los pasos necesarios para instalar, configurar y ejecutar el sistema en Windows.

---

## 1. Requisitos previos

Antes de comenzar, asegúrate de contar con los siguientes elementos instalados y configurados en tu sistema:

### 1.1. Python

1. *Verificar si Python está instalado*:

Abre una terminal o el símbolo del sistema (cmd) y ejecuta:

bash
python --version

Si Python no está instalado:

Descárgalo desde https://www.python.org/.

Durante la instalación, marca la casilla "Add Python to PATH" para asegurarte de que Python se agregue correctamente a la variable de entorno PATH.

### 1.2. MySQL

Descargar e instalar MySQL:

Ve al sitio oficial de MySQL: https://dev.mysql.com/downloads/mysql/.

Descarga la versión Community Server y sigue las instrucciones del instalador.

Configuración de usuario:

Durante la instalación, se te pedirá crear un usuario administrativo (por defecto root) con una contraseña segura. Recuerda esta contraseña ya que la necesitarás más tarde.

Verificar la instalación de MySQL:

Abre el símbolo del sistema y ejecuta:

bash
mysql --version

Si no se reconoce el comando, agrega el directorio bin de MySQL a la variable de entorno PATH.

### 1.3. Librerías de Python

Instalar las librerías necesarias:

Abre una terminal o símbolo del sistema y ejecuta el siguiente comando para instalar las dependencias necesarias:

bash
pip install sqlalchemy pymysql pandas matplotlib

1. Configuración de la base de datos
   1. Crear la base de datos y tabla

Abrir la línea de comandos de MySQL:

Ejecuta el siguiente comando en la terminal o cmd:

bash
mysql -u root -p

Ingresa tu contraseña de administrador cuando se te solicite.

Crear la base de datos y la tabla:

Ejecuta los siguientes comandos dentro de MySQL para crear la base de datos y la tabla que utilizará la aplicación:

sql
CREATE DATABASE ENCUESTAS;

USE ENCUESTAS;

CREATE TABLE ENCUESTA (

idEncuesta INT PRIMARY KEY,

edad INT,

Sexo VARCHAR(7),

BebidasSemana INT,

CervezasSemana INT,

BebidasFinSemana INT,

BebidasDestiladasSemana INT,

VinosSemana INT,

PerdidasControl INT,

DiversionDependenciaAlcohol CHAR(2),

ProblemasDigestivos CHAR(2),

TensionAlta CHAR(12),

DolorCabeza CHAR(12)

);

INSERT INTO ENCUESTA VALUES

(1, 57, 'Mujer', 5, 5, 5, 0, 3, 1, 'No', 'Sí', 'No lo sé', 'Alguna vez');

1. Configuración de la aplicación
   1. Clonar o copiar el código

Crear una carpeta:

Crea una carpeta en tu sistema para almacenar la aplicación, por ejemplo: C:\EncuestaApp.

Guardar el código:

Guarda el código proporcionado en un archivo llamado encuesta\_app.py dentro de esa carpeta.

1. Configurar conexión a MySQL

Abrir el archivo encuesta_app.py:

Abre el archivo encuesta_app.py en un editor de texto como Notepad, PyCharm o Visual Studio Code.

Configurar la conexión:

Asegúrate de que esta línea coincida con tus credenciales de MySQL:

python
engine = create\_engine("mysql+pymysql://root:curso@localhost/ENCUESTAS")

Reemplaza root con el usuario de MySQL.

Reemplaza curso con la contraseña que configuraste para MySQL.

1. Ejecutar la aplicación

Abrir el símbolo del sistema (cmd).

Navegar a la carpeta donde guardaste el archivo encuesta\_app.py:

Ejecuta el siguiente comando para ir a la carpeta:

bash
cd C:\EncuestaApp

Ejecutar el programa:

Ejecuta el siguiente comando para iniciar la aplicación:

bash
python encuesta\_app.py

Esto abrirá una ventana con la aplicación de encuestas.

1. Operaciones CRUD y gráficos
   1. Agregar un registro

Haz clic en el botón "Agregar Registro".

Completa los campos en la nueva ventana.

Haz clic en el botón "Agregar" para agregar el registro a la base de datos.

1. Eliminar un registro

Haz clic en el botón "Eliminar Registro".

Ingresa el ID del registro que deseas eliminar.

Confirma la acción para eliminar el registro.

1. Filtrar registros

Haz clic en el botón "Filtrar Registros".

Ingresa el criterio de filtro en formato SQL. Ejemplo:

Para filtrar por sexo masculino:

sql
sexo='Hombre'

Para filtrar por edad de 25 años:

sql
edad=25

1. Actualizar la tabla

Haz clic en el botón "Actualizar Tabla" para refrescar los datos mostrados en la aplicación.

1. Generar gráficos

Haz clic en uno de los siguientes botones para visualizar gráficos:

"Ver Gráfico Consumo por Sexo": Muestra el número de registros agrupados por sexo.

"Ver Gráfico Consumo por Edad": Muestra el número de registros agrupados por edad.

"Ver Gráfico de Problemas de Salud": Muestra los problemas de salud relacionados con el consumo de alcohol.

1. Exportar datos a Excel

Haz clic en el botón "Exportar a Excel" para guardar los datos de la tabla en un archivo Excel llamado encuesta\_registros.xlsx en el mismo directorio donde se encuentra la aplicación.

1. Solución de problemas
   1. Error: ModuleNotFoundError

Si al ejecutar el programa aparece un error indicando que falta algún módulo (por ejemplo, pymysql), instala el módulo con el siguiente comando:

bash
pip install pymysql

1. Error de conexión a MySQL

Si la aplicación no puede conectarse a la base de datos MySQL, sigue estos pasos:

Verifica que MySQL esté en ejecución:

Abre el Administrador de servicios de Windows (presiona Win + R, escribe services.msc y presiona Enter).

Busca el servicio MySQL y asegúrate de que esté en estado Ejecutándose.

Verifica las credenciales de conexión:

Asegúrate de que las credenciales (usuario y contraseña) en la línea:

python
engine = create\_engine("mysql+pymysql://root:curso@localhost/ENCUESTAS")

sean correctas.


