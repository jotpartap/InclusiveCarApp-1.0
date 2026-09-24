# *InclusiveCarApp*, Versión: 1.0

**InclusiveCarApp** es una aplicación web potenciada con IA que busca lograr que el coche automático sea más inclusivo para todo tipo de gente. 

- ## [M, O, V] y Canales de adaptación:
  - ### Vector [M, O, V]:
    Definimos el vector M, O, V como un conjunto de 3 variables cuyo valor puede variar según las necesidades del usuario:

    - 0: en caso de que el usuario no tenga, tenga frágil... la variable. Por ejemplo, un 0 en vista significa que el pasajero es ciego, ve borroso...
    - 1: significa que la persona, no tiene ningun problema en el aspecto. Por ejemplo, un 1 en oido, significa que el usuario puede oir sin problemas y no requiere ayuda en ello.
    - 2: cuando el pasajero del coche tiene sensibilidad, hipercapacidad... en una de las tres variables. Por ejemplo, alquien con TDAH tendria un 2 en movilidad.

  - ### Los 4 Canales de Adaptación:
    Los 4 canales de adaptación, son diferentes configuraciones que considero que el cohe automático deberia de tener para más inclusividad y son los siguientes:

    1\. canal auditivo: asistencia de voz automática al pasajero.

    2\. canal visual: ayuda con comunicacion visual al usuario.

    3\. canal háptico: integración de sistemas que usen el tacto, por ejemplo, Braile.

    4\. Canal gestual/motriz: una rampa para ayudar en la mobilidad, entendimiento de gestos...

  - ### Tabla VOM/Canales:
    Al final, se adjunta un documento sobre como creo que deberia de reaccionar cada Canal a diferentes pasajeros según su vector [V, O, M]. Se pone OFF en caso de que se deberia de apagar para ahorro energetico, MÁXIMO si se deberia de dar la mayor importancia posible a ese canal...
  
- ## La Aplicación:
  - ### Idea y diseño:
  InclusiveCarApp busca comunicar como deberia de reaccionar cada canal del coche automático según el vector [V, O, M] de alguien. 

  La app cuenta con dos modos:

  1\: Modo IA: Considero que la IA és una tecnologia inovadora que se deberia de utilizar para lograr propositos comunes como la inclusividad. En este modo, el usuario puede ingresar en un recuadro de texto su información para que un modelo de IA interprete el mismo el vector [V, O, M] y analice la que deberia de ser la respuesta de cada canal para esa persona. Ademñas de eso, también puede activar el boton confianza para saber con que tanta confianza dice el modelo su predicción, que es muy útil al momento de experimentarlo y evaluarlo.

  2\: Modo deslizador: Entendiendo que haya personas que no quieran hablar sobre sus caracteristicas por diferentes razones. Aunque el modo IA no usa los datos del usuario ni guarda nada, como podeis ver en los codigos dejados en el repositorio, la app cuenta con esta sección en la que el usuario puede él mismo insertar el mismo su vector [M, O, V] deslizando valores si eso le genera más confianza.

  - ### Organización de Archivos:
    - #### requirements.txt
    Contiene las librerias de python usadas para la aplicación.
    - #### gen.py
    Contiene el codigo para generar un dataset de un poco mas de 5000 lineas con las expresiones que se le marcan en un diccionario.
    - #### dataset.csv
    Es el dataset del que se entrena el modelo de IA y que fue generado con el antes mencionado gen.py. Contiene 5003 lineas y 4 columnas: texto, movilidad, oido y vista.
    - #### web.py:
    Es el archivo principal y el nucleo de la app que lo organizamos en 3 partes: el diccionario con las tablas de la adaptación de los 4 canales, el modelo de IA y el desarollo web.
  - ### modelo de IA:
    El modelo de ML utiliza tecnicas de NLP, en especial Transformers/Embeddings. El Transformer que usamos es uno multilingue: 'distiluse-base-multilingual-cased-v2', y luego a partir de los embeddings usamos una regresion logistica para predecir cada elemento del vector [V, O, M].
  - ### Desarollo Web:
    La app tiene como titulo InclusiveCarApp y dos pestañas: 'Modo Deslizador' y 'Modo IA' para cada modo. En el Modo Deslizador, hay 3 deslizadores que se pueden colocar en el valor que la queramos dar a cada elemento del vector y al clicar el boton 'Submit', nos devuelve en vector [V, O, M] y la reacción de cada canal según el diccionario 'CANALES'. En el Modo IA, hay una celda para escribir texto y, semejantemente al Modo Deslizador, al  clicar el boton Submit se nos devuelve la adaptación de cada canal de coche. La diferencia es que en este caso es el modelo de IA el que interpreta cual es el vector [V, O, M].

- ## Conclusiones:
  Considero que la IA y todas las tecnologias deberian de ser una herramienta para lograr bienes comunes: la inclusivida, sostenibilidad... InclusiveCarApp, aunque no deja de ser a nivel tecnico una app minimalista, lo que busca es expressar eso, el buen uso de la tecnologia actual. Por eso considero que deberia de ser Open Source, al alcance de todas las personas. Muchas gracias por leer esto.

- ## Autor:
  Me llamo Jotpartap Singh, o simplemente Jot. Tengo 13 años y soy estudiante de ESO, pero, en especial, soy un freekie de las matematicas y de las tecnologias, en especial del fenómeno de la IA y los modelos de ML. 

- ## Agradecimientos:
  Agradezco a Capgemini por organizar el Hackhaton Digital: Flow to the Future.
  Agradezco a todo mi equipo en esta hackathon: Lex, Hector, Rita, Jon... por ser tan buen compañeros y apoyarme, a parte de aportar tan buenas ideas e opiniones.
