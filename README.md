 
# PSBapp   
Para este  proyecto se utiliza el sistema operativo `Ubuntu:18.04`

### Dependencias 
1. [Docker](https://docs.docker.com/)
2. [Docker-Compose](https://docs.docker.com/compose/)

## Inicio
1. Decargar el repositorio, ingresar a este y darle permiso de ejecución a los ejecutables (.sh)

        
        git clone https://github.com/skilletComatose/PSBapp.git
        cd PSBapp/  
        chmod +x deploy.sh
        chmod +x App/APIRESTful/deployApi.sh
         

2. Crear un archivo llamado `config.py` , dentro de `App/APIRESTful/src `donde deberá incluir las siguientes variables :
    
    credentials = <string de conexión de mongo atlas>
    
    databaseName = <nombre de la base de datos donde se guardarán los psb>
    
    collection = <nombre de la collección dentro donde se guardaran los datos>

    adminDatabase = <nombre de la base de datos donde se guardarán los datos del admin>
    
    Admincollection = <nombre de la collección donde se guardaran los datos del admin>

    verysecret = <llave secreta, para hacer cifrados(cualquier string)>

    salt = <una salt gererada por la librería `bcrypt`, puede ser generada así : `salt = bcrypt.gensalt()` >
    * nota : La salt es única solo debes generarla una vez y guardar ese resultado en la varible, porque de esta forma (`salt = bcrypt.gensalt()`) se generará una diferente cada vez .
    
     
  Dentro de esta misma ruta , crear el directorio img, allí se crea un volumen persistencia de datos,para las imagenes registradas en el contenedor 
                
     mkdir img
                


3. Una vez hecho esto usar el ejecutable `deploy.sh` que se encuentra en `PSBapp/`  
       
        ./deploy.sh


        
