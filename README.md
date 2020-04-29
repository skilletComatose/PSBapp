 PSBapp
 ======
Los Puntos de Basura Satelite (PSB) son un problema diario que se vive en la ciudad de Cartagena, ya que en ocasiones, estos basureros llegan a perdurar varios días emitiendo malos olores, generando problemas de salubridad, entre otros factores que incomodan a la ciudadanía, es por esta razón que se realiza el desarrollo de PSBapp, la cual es una aplicación que permite tener un mayor control del estado de estos PSB, para así facilitar a las autoridades y entidades correspondientes, la ubicación y el estado actual de estos PSB, para que de esta forma haya una solución rápida y eficiente.
Como propósito de este proyecto está el afianzar conocimientos en cuanto al trabajo en equipo, desarrollar una API usando microservicios y recordar conocimientos pasados como el uso de requerimientos y el modelado de la APl.
 
 Descripción
 ----------
PSBapp es una app WEB desarrollada para funcionar en cualquier navegador actualizado en sus versiones más recientes, Este aplicativo WEB ha sido elaborado para brindar una solución al problema de basureros satélites en la ciudad de Cartagena, Esta aplicación será desarrollada con las herramientas Angular para el desarrollo del front-end, Flask para el desarrollo del backend, MongoDB que será utilizado en el motor de base de datos y RabbitMQ quien será el encargado de la comunicación de los microservicios.
 

## Captura de Requerimientos ##

### 1. Requerimientos Funcionales
  
  
  #### 1.1) Requerimientos de usuario: 
  
  * El usuario NO necesita crear una cuenta para poder interactuar con el servicio.
  
  * El usuario debe ubicar las coordenadas del por medio de un mapa interactivo o ingresar la dirección del lugar a denunciar.
  
  * El usuario tendrá la opción anexar una fotografía actual del basurero a denunciar.
  
  * El usuario podrá observar los Puntos Satélite de Basura (PSB) dentro del mapa, arrojando los datos correspondientes al mismo.
  
  
  #### 1.2) Requerimientos del Sistema:

  * El sistema debe contar con dos opciones para registrar los PSB, uno mediante la localización actual del dispositivo que está interactuando con este y el segundo mediante un mapa interactivo colocando la dirección.

  * El sistema debe contar con una base de datos donde sean almacenadas las imágenes y los datos que caractericen cada uno de los PSB y debe ser capaz de mostrarlas si el usuario las solicita.

  * El sistema debe verificar si los nuevos PSB ingresados por otros usuarios ya existen actualmente. (Verificar su complejidad y si es posible realizarlo dentro del tiempo estimado de entrega).

  * El sistema debe enviar una notificación por mail al usuario indicando si el reporte enviado fue recibido con éxito o si falló. (Verificar su complejidad y si es posible realizarlo dentro del tiempo estimado de entrega.

  * El sistema debe ser capaz de proporcionar datos estadísticos al usuario partir de los datos registrados de los PSB si este lo requiere.


#### 2.Requerimientos No funcionales

##### 2.1 Eficiencia

  * Cualquier navegador de uso actual en sus versiones más recientes
  Un equipo de cómputo con especificaciones técnicas promedio


##### 2.2 Usabilidad
  
  * El servicio debe contar con un FAQ en caso de tener una sugerencia, inquietud o necesitar ayuda respecto al uso del servicio.



          Diagrama de la arquitectura 
![Diagrama de la acquitectura](https://github.com/skilletComatose/PSBapp/blob/master/Arquitectura.jpg)
