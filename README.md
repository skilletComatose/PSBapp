# Proyecto PSBapp  
Para este  proyecto se utiliza el sistema operativo `Ubuntu:18.04`

## API RESTful

### Dependencias
1. [Docker](https://docs.docker.com/)
2. [Docker-Compose](https://docs.docker.com/compose/)

### Información
* [Acerca la app](https://github.com/skilletComatose/PSBapp/blob/master/App/APIRESTful/docs.md)
* [Front-end](https://github.com/PabloArrietaL/psb-leaflet-angular)
* El Front-end fue construido en el Framework [AngularJS](https://angularjs.org/) integrado en el entorno de [Node.js](https://nodejs.org/es/docs/)
* [Framework usado en la API](https://flask.palletsprojects.com/en/1.1.x/)
* [Seguridad implementada en la API](https://openwebinars.net/blog/que-es-json-web-token-y-como-funciona/)
* [Base de datos usada](https://www.mongodb.com/cloud/atlas/efficiency?utm_source=google&utm_campaign=gs_americas_colombia_search_brand_atlas_desktop&utm_term=atlas%20mongo&utm_medium=cpc_paid_search&utm_ad=e&gclid=EAIaIQobChMI-dHnpIPr6QIVB_7jBx0_jwPQEAAYASABEgLaqPD_BwE)


## Inicio
1. Descargar el repositorio, ingresar a este y darle permiso de ejecución a los ejecutables (.sh)

      
       git clone https://github.com/skilletComatose/PSBapp.git
       cd PSBapp/ 
       chmod +x deploy.sh
       chmod +x App/APIRESTful/deployApi.sh
       

2. Crear un archivo de configuración llamado  `config.py` , dentro de `App/APIRESTful/src `donde deberá incluir las siguientes variables :
  
           credentials = <string de conexión de mongo atlas>
      
           databaseName = <nombre de la base de datos donde se guardarán los psb>
      
           collection = <nombre de la colección dentro donde se guardaran los datos>

           adminDatabase = <nombre de la base de datos donde se guardarán los datos del admin>
      
           Admincollection = <nombre de la colección donde se guardaran los datos del admin>

           verysecret = <llave secreta, para hacer cifrados(cualquier string)>

           salt = <una salt generada por la librería `bcrypt`, puede ser generada así : `salt = bcrypt.gensalt()` >

           ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
           CORS_HEADERS = 'Content-Type'
           UPLOAD_FOLDER = '/api/img' #ruta donde se guardan las imágenes

* nota : La salt es única solo debes generarla una vez y guardar ese resultado en la variable, porque de esta forma (`salt = bcrypt.gensalt()`) se generará una diferente cada vez .


Dentro de esta misma ruta , crear el directorio `img/`, allí se crea un volumen persistencia de datos,para las imágenes registradas en el contenedor
              
     mkdir img
              
      
              


3. Una vez hecho esto usar el ejecutable `deploy.sh` que se encuentra en `PSBapp/` 
     
       ./deploy.sh


Una vez ejecutado el comando anterior se debe esperar a que aparezca la siguiente imagen.         !

![deploy image](https://github.com/skilletComatose/PSBapp/blob/master/img/deploy.jpeg)                



4. Verificar que la API está corriendo, para esto se ingresa a la ruta http://localhost/, debería aparecer el siguiente mensaje

![first image](https://github.com/skilletComatose/PSBapp/blob/master/img/first.jpeg)

una vez salga esta, dar click en api y deberá verse así :
![localhost image](https://github.com/skilletComatose/PSBapp/blob/master/img/running.jpeg)
