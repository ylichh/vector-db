## ls

### Descripción:

Lista los ficheros de una carpeta, mostrando por defecto los nombres de los archivos y directorios contenidos en el directorio actual.
Puede usarse con opciones para mostrar información adicional como permisos, tamaño, fecha de modificación, y para listar contenidos de otros directorios.

### Comando
ls

### Instrucción:
ls [OPCIONES] [DIRECTORIO]
[OPCIONES]
  -a, --all: muestra todos los archivos incluidos los ocultos
  -l: muestra información detallada (permisos, tamaño, fecha, etc.)
[DIRECTORIO] (opcional): ruta del directorio a listar; si se omite, se usa el directorio actual

---

## cd

### Descripción:
Cambia el directorio de trabajo actual a otro especificado. Permite navegar por el sistema de archivos moviéndose entre carpetas.

### Comando
cd

### Instrucción:
cd [directorio]
[directorio] (opcional): ruta del directorio al que se desea cambiar; si se omite, se cambia al directorio personal del usuario

---

## pwd

### Descripción
Muestra la ruta completa del directorio de trabajo actual. Es útil para saber en qué parte del sistema de archivos se está trabajando.

### Comando
pwd

### Instrucción
pwd
No acepta opciones ni argumentos adicionales.

---

## docker build

### Descripción:
Construye una imagen docker utilizando un fichero dockerfile. Permite especificar el fichero dockerfile, el nombre/tag y la vComando y Argumentosersión de la imagen, y la ruta de contexto.

### Comando
docker

### Instrucción:
docker build [opciones] [ruta]
[opciones] (opcional):
  -t <nombre:tag>`: asigna una etiqueta a la imagen
  -f <archivo>`: ruta al dockerfile que se va a utilizar, por defecto busca el dockerfile en el directorio actual
[ruta] (opcional): ruta al directorio de contexto; por defecto es el directorio actual

---

## docker image prune

### Descripción:
Borra las imágenes colgantes de docker. Las imágenes colgantes son imágenes que no tienen un tag identificativo. Permite liberar el espacio ocupado por esas imágenes.

### Comando
docker

### Instrucción
docker image prune
No acepta opciones ni argumentos adicionales.

---

## pyenv virtualenv

### Descripción:
Crea un entorno virtual utilizando pyenv. Puedes especificar la versión de python que quieres utilizar y el nombre del entorno virtual creado.

### Comando
pyenv

### Instrucción
pyenv virtualenv [VERSION_PYTHON] [NOMBRE_DEL_ENTORNO]
[VERSION_PYTHON] (opcional): indica la versión de python que se va a utilizar, por defecto utiliza la versión del sistema
[NOMBRE_DEL_ENTORNO] (obligatorio): nombre del entorno que se va a crear

---

## docker compose up

### Descripción:
Levanta un docker compose utilizando el docker compose presente en la carpeta actual. Puede indicarse qué aplicación o aplicaciones especificadas dentro del docker compose se van a levantar. Si no se especifica se levantan todas las aplicaciones. Este comando te permite levantar el servicio en modo "watch" o supervisor, de modo que cada vez que guardas alguno de los ficheros que están bajo supervisión se reinician las aplicaciones implicadas. También podemos indicar al comando que queremos que las imágenes utilizadas por el docker compose se reconstruyan.

### Comando
docker

### Instrucción
docker compose up [opciones] [aplicaciones]
[opciones] (opcional):
  `--watch`: inicia el docker compose en modo supervisor`--build`: reconstruye las imágenes docker al levantar el sistema
[aplicaciones] (opcional): el nombre de las aplicaciones que queremos que se inicien o levanten

---

## start_boja.sh

### Descripción:
Es un script que inicia la conexión con la vpn de la nube del boja. Inicia la vpn del boja.

### Comando
start_boja.sh

### Instrucción
`~/./Documentos/boja/certificados/start_boja.sh`
No acepta opciones ni argumentos adicionales.

---
