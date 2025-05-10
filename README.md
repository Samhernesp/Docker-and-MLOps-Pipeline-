# MLOps Pipeline para Clasificación de Enfermedades

**Prototipo MLOps para diagnóstico médico con despliegue simplificado usando Docker Compose.**

---

## Requisitos Previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y en ejecución.
- Windows/macOS/Linux con WSL2 habilitado (para Windows).

---

## Instalación con Docker Compose

### 1. Clonar el repositorio
```bash
git clone https://github.com/Samhernesp/Docker-and-MLOps-Pipeline-.git
cd Docker-and-MLOps-Pipeline-
```

### 2. Construir y ejecutar
En el directorio del proyecto ejecutar el siguiente comando:
```bash
docker-compose up
```


### 3. Acceder a la aplicación
Accede en un navegador a la siguiente ruta:
```bash
http://localhost:8501
```
---
## Uso

- Interfaz de Usuario:
    - Ingresa los valores numéricos requeridos:

        - Edad (años)
          
        - Género
          
        - Tipo de sangre

        - Presión arterial sistólica (mm Hg)

        - Presión arterial diastólica (mm Hg)

        - Días de ejercicio al mes

- Resultados:
    - El sistema mostrará uno de estos estados con colores e iconos:

        - ✅ NO ENFERMO (Verde)

        - ⚠️ ENFERMEDAD LEVE (Amarillo)

        - 🚨 ENFERMEDAD AGUDA/CRÓNICA (Rojo)


## **Desarrollo**

### **Diseño**

#### **¿Qué restricciones y limitaciones existen?**

Del planteamiento inicial del problema, se puede identificar rápidamente una restricción que es la poca cantidad de datos que existen de las enfermedades huérfanas, por lo tanto, es imperativo que se tomen medidas con respecto a esta situación, ya que en el caso de entrenar un modelo con estas características va a tener una tendencia a identificar los casos de enfermedades huérfanas como casos de enfermedades comunes y por consiguiente a identificarlo con una de las clases con las que pueda coincidir mas pero de los datos mas representativos. Esto significa entonces que nuestro sistema estaría limitado en su mayoría a enfermedades comunes y tendría un rendimiento muy bajo para casos de enfermedades huérfanas.

Otra de las limitaciones que se puede identificar a profundidad en este contexto es la limitada capacidad que puede suponer metodologías y algoritmos de Machine Learning tradicional, ya que tienen una capacidad limitada frente a grandes fuentes de datos como se nos plantea en este caso. Debido a que algoritmos como SVM, Random Forest, etc, tienen limitadas escalabilidad computacional por su elevada complejidad temporal de alrededor de , y la limitada capacidad de memoria pues estos algoritmos requieren que los datos se encuentren en RAM.

De la misma manera, estos algoritmos tradicionales no están diseñados en su mayoría para trabajar con datos no estructurados, y en este caso, existe la posibilidad de que una de las características que se posea para entrenar el modelo sean textos sin procesar, que contengan todo el analisis que realiza por escrito un doctor sobre un paciente en específico, y por tanto esto se convierta en una de las materias primas para la construcción del modelo. Así, no es posible trabajar con este tipo de datos si se utilizan algoritmos tradicionales de Machine Learning, o no seria lo ideal para esto.

Por último, y de la mano con la segunda limitación ya comentada, en términos económicos y de eficiencia, no es correcto trabajar con algoritmos que no estén optimizados para trabajar con grandes cantidades de datos, es decir que no tengan la capacidad de tener un entrenamiento distribuido o paralelo. Debido a que esto derivaría en altos costes de energía y almacenamiento debido a los altos requerimientos de tiempo y memoria que pueden tener los algoritmos tradicionales frente a millones de datos.

#### **¿Qué tipos de datos se tienen?**

En este caso vamos a partir de la suposición de que se cuenta con una base de datos que cuenta con datos estructurados, por practicidad solo se van a tener como características la edad, el género, tipo de sangre, presión arterial, cantidad de ejercicio mensual. En este caso, contaríamos con 5 diferentes tipos de variables, de las cuales 3 son variables numéricas, que son la edad, la presión arterial, y la cantidad de ejercicio mensual, y 2 son variables categóricas.

En un analisis con un poco mas de profundidad de las variables podríamos darnos cuenta de varios puntos importantes, para el caso de la variable edad esta puede encontrarse entre valores de 0 a 100 aproximadamente, suponiendo que la edad se encuentra en años. La presión arterial, aunque se mide numéricamente generalmente se valora por medio de rangos, de la siguiente manera:

![image](https://github.com/user-attachments/assets/c6181c60-ff2d-49fa-84ca-2bde2e7b5f2d)


Fuente: American Heart Association

Como podemos ver en la tabla anterior, la presión arterial se evalúa con dos medidas diferentes es necesario contar con ambas medidas para dar valoraciones más exactas.

La característica del género cuenta con solamente dos categorías que son masculino y femenino. El tipo de sangre cuenta con solo 4 categorías, que son A, B, AB y O, por practicidad no se tendrá en consideración del factor Rh (Positivo - Negativo). Y por ultimo la variable cantidad de ejercicio mensual es una variable discreta, que representa el promedio de días que una persona realiza actividad física al mes.

### **Desarrollo**

#### **¿De qué fuentes provienen los datos y cómo se manejan?**

Inicialmente supondremos que los datos base del problema van a provenir de la entidad la cual está necesitando la construcción del modelo, en este caso vamos a suponer que es un hospital el que espera este modelo, y por tanto va a proveer información inicial con la cual se puede comenzar a experimentar y a definir las características de interés, es importante que los datos iniciales provengan de la entidad contratante ya que si se utilizan de entrada datos externos se corre el peligro que existan características que no sean recopiladas por la entidad y que por lo tanto no son datos reales que puedan ingresar los médicos a la hora de buscar predicciones del modelo.

Despues de la determinación de las características de interés, ahora si se procederá a extraer datos de terceros que tengan estas mismas características, pero que cuenten con clases distintas, como lo sería el caso de las enfermedades huérfanas, para ayudar a balancear la cantidad de datos que enfermedades huérfanas y enfermedades comunes.

Cuando ya se han recopilados los datos esperados y necesarios, es importante hacer un manejo correcto de estos, justo después de su recopilación es esencial su almacenamiento, por lo tanto, vamos a usar una base de datos que tenga la capacidad de almacenar grandes cantidades de datos del orden de millones o miles de millones, y que a su vez se pueda consultar eficientemente los datos cuando sean requeridos para el preprocesamiento y entrenamiento.

En el preprocesamiento de los datos es necesario tener en cuenta las particularidades de las características analizadas en el diseño para construir un conjunto de datos que sea útil para la construcción de un buen modelo. Por lo tanto, para las variables numéricas solo es necesario asegurar el que el tipo de variable corresponda a lo que describe la misma, en este caso las variables edad y cantidad de ejercicio mensual son variables discretas y por lo tanto se utiliza un tipo de dato entero. Despues es necesario normalizar o estandarizar de acuerdo con la distribución de los datos, no gaussiana o gaussiana respectivamente.

En este caso no se está teniendo en cuenta la variable presión arterial en cuenta para el procesamiento anterior ya que por su forma de analizar puede brindar más información clasificar los rangos anteriormente mostrados como categorías. De esta manera las dos variables de presión arterial se convierten en una sola variable categórica que cuenta con las clases normal, elevada, alta 1, alta 2 y crisis.

Finalmente, para las variables categóricas se realiza un único procedimiento conocido como el one-hot enconding, que convierte las categorías de cada característica categórica en una nueva característica binaria. Dando como resultado una base de datos con 13 características totalmente preprocesadas y listas para entrenar un modelo.

#### **¿Qué tipos de modelos de ML se puede usar?**

Para elegir un modelo adecuado para nuestra situación, lo primero que podemos resaltar es una de las limitaciones comentadas en el diseño, en cuanto a la gran cantidad de datos que se deben usar para entrenar un modelo y que por tanto ciertas arquitecturas o algoritmos tradicionales son descartados inicialmente. Con esto en mente, podemos filtrar los modelos por su capacidad de soportar paralelismo y computación distribuida. Además, suponiendo que el flujo de pacientes en el hospital no es lo suficientemente grande para aportar una cantidad considerable de datos diariamente ni semanalmente para considerar reentrenar el modelo con estas temporalidades, y si tambien consideramos que requiere cierto tiempo para que se pueda confirmar si la predicción dada es real o no, podemos considerar que el modelo debería estar actualizándose mensualmente con el batch de datos de este periodo.

Con estas características definidas ya podemos empezar a pensar algunas opciones de modelos como XGBoost, MLP tradicional, LightGBM.

#### **¿Cómo se van a validar/testear?**

Para validar y testear los modelos resultantes, vamos a dividir los datos desde un principio en tres datasets completamente diferentes que guarden cada uno las mismas proporciones y distribución de las clases de enfermedad (No Enfermo, Enfermo Leve, Enfermedad Aguda, Enfermedad Crónica ) así como el tipo de enfermedad (Enfermedad Común, Enfermedad Huerfana). Esto con el fin de que cada dataset represente lo más fielmente las condiciones normales de los datos.

La división del conjunto de datos tiene que ser una cantidad que sea estadísticamente significativa, por eso se realizan las verificaciones comentadas anteriormente, pero tambien se debe tener cuidado con las distribuciones de las variables de importancia así como con medias y varianzas. En este caso al tener un gran conjunto de datos se puede empezar con una distribución de 70, 15, 15, y posteriormente con las verificaciones dadas se puede llevar incluso a 80, 10, 10.

Con esto asegurado, se realizan las iteraciones necesarias del modelo, solo usando train y val para buscar maximizar las métricas necesarias para el dataset de validación. Y cuando ya se tengan un modelo definido como el mejor para la validación, si se puede proceder a realizar las pruebas con el conjunto de test. Esto se realiza para evitar que a través de las iteraciones de los modelos los hiperparametros puedan ir causando un posible sobreajuste en el conjunto de test.

### **Producción**

#### **¿Cómo se va a desplegar la solución?**

La solución se desplegará inicialmente en un entorno de nube escalable (ej: AWS o Azure) para garantizar acceso global y capacidad de procesamiento bajo demanda. Se integrará con los sistemas de historiales clínicos electrónicos (EHR) del hospital mediante APIs estándar como HL7 o FHIR, asegurando compatibilidad con plataformas como Epic o Cerner. Para facilitar el uso diario, se desarrollará una interfaz sencilla dentro del flujo de trabajo médico, donde los doctores ingresen síntomas y reciban predicciones en tiempo real.

#### **¿Se necesita algún tipo de monitoreo para esta aplicación?**

Sí, es crítico implementar dos tipos de monitoreo:

Rendimiento del modelo: Alertas si la precisión general o el recall de enfermedades huérfanas caen por debajo de un umbral predefinido (ej: <85% en F1-score para comunes, <70% en recall para huérfanas).

Calidad de datos: Detección de valores atípicos o formatos incorrectos en nuevas entradas (ej: presión arterial = 300/150, género = "Otro" si no está permitido).

Además, se incluirá un botón de "Retroalimentación" para que los médicos reporten predicciones erróneas, lo que activará una revisión manual.

#### **¿Pueden existir nuevos datos necesarios quizás para re-entrenar el modelo?**

Sí. Cada mes, se recolectarán nuevos casos confirmados (tanto comunes como huérfanas) para re-entrenar el modelo. Sin embargo, dado el costo computacional, solo se re-entrenará completamente cada 3 meses, aplicando actualizaciones incrementales mensuales con técnicas como fine-tuning en lotes pequeños. Para enfermedades huérfanas, se priorizará la incorporación inmediata de nuevos casos validados, incluso fuera del ciclo regular, usando active learning para ajustar el modelo con los ejemplos más informativos.

## **Diagrama del Pipeline de MLOps**

![image](https://github.com/user-attachments/assets/45e77671-ab49-46c4-a5f2-3dbbda7301df)


## **Data Input**  
La etapa de entrada de datos se centra en consolidar información clínica de múltiples fuentes para garantizar diversidad y representatividad. Los historiales electrónicos del hospital (EHR) proporcionan datos estructurados como edad, género y presión arterial, esenciales para capturar patrones de enfermedades comunes. Para abordar la escasez de datos en enfermedades huérfanas, se integran bases públicas como Orphanet y colaboraciones con centros especializados, que aportan casos raros validados clínicamente. Estos datos se almacenan en Amazon S3 o Redshift, elegidos por su capacidad para manejar grandes volúmenes y garantizar accesibilidad segura. La validación de esquemas asegura que todas las fuentes compartan la misma estructura como en el caso de la presión arterial como par sistólica/diastólica, evitando inconsistencias que afecten el entrenamiento. Esta etapa es la base para un modelo equilibrado, pues combina datos internos , que son abundantes pero sesgados hacia enfermedades comunes, con datos externos escasos pero críticos para rarezas, como las enfermedades huerfanas.

## **Preprocesamiento**  
El preprocesamiento transforma los datos en un formato usable para el modelo, priorizando la relevancia clínica. Las variables numéricas como edad y días de ejercicio mensual, se estandarizan para evitar sesgos por escalas dispares, mientras que las categóricas como género y tipo de sangre, se codifican con one-hot para preservar su naturaleza no ordinal. La presión arterial, inicialmente en valores numéricos, se convierte en categorías clínicas normal, elevada, etc. siguiendo los estándares de la American Heart Association, lo que permite al modelo interpretar rangos médicamente significativos. Para enfermedades huérfanas, se aplican técnicas como SMOTE o GANs para generar muestras sintéticas, equilibrando su representación sin alterar patrones reales. Este paso incluye también la depuración de anomalías como la presencia de valores imposibles como 300/150 en presión arterial, asegurando que el dataset refleje solo escenarios clínicos plausibles. El resultado es un conjunto de datos homogéneo, listo para alimentar algoritmos de ML.

## **Entrenamiento del Modelo**  
El entrenamiento utiliza un enfoque dual para abordar la disparidad de datos. Para enfermedades comunes, se implementan modelos escalables como XGBoost o LightGBM, optimizados mediante búsqueda de hiperparámetros y validación cruzada estratificada, lo que garantiza eficiencia incluso con millones de registros. En paralelo, las redes de Few-Shot Learning como Prototypical Networks se entrenan con embeddings preprocesados de enfermedades comunes, permitiéndoles generalizar a partir de pocos ejemplos de enfermedades huérfanas. La validación se realiza en tres conjuntos (70%-15%-15%), con métricas diferenciadas: F1-score para clases mayoritarias y Recall/AUC-PR para minoritarias, asegurando que el modelo no descarte casos raros por su escasez. Esta etapa prioriza la interoperabilidad, en donde los modelos para enfermedades comunes y huérfanas se ensamblan en un pipeline único, donde las predicciones se combinan jerárquicamente, priorizando señales de rareza, antes de entregar un diagnóstico integrado.

## **Despliegue del Modelo**  
El despliegue se realiza en una infraestructura híbrida diseñada para integración clínica fluida. Los modelos se encapsulan en contenedores Docker gestionados por Kubernetes, permitiendo escalabilidad automática durante picos de demanda en hospitales. Una API REST se integra con los sistemas EHR mediante estándares FHIR/HL7, facilitando predicciones en tiempo real dentro del flujo de trabajo médico como para alertas automáticas en historiales. Para casos sin integración directa, una interfaz Streamlit permite a los médicos ingresar datos manualmente, con validaciones en tiempo real como el bloqueo de valores fuera de rangos clínicos. La interpretabilidad se garantiza mediante reportes SHAP, que explican predicciones en términos médicos para conocer las variables que más influyeron en la predicción. Esta etapa prioriza la usabilidad: el modelo opera como un servicio silencioso en segundo plano para EHRs, pero está accesible como herramienta independiente para contextos sin automatización.

## **Monitoreo del Modelo**  
El monitoreo continuo asegura que el modelo se mantenga relevante ante cambios en patrones clínicos. Se implementan pruebas de drift estadístico (KS-test) para detectar desplazamientos en distribuciones de datos, un ejemplo de esto fue el aumento de pacientes con presión arterial elevada post-pandemia, lo que activa alertas para revisión. Un sistema de retroalimentación permite a los médicos reportar diagnósticos erróneos, almacenando estos casos en una base prioritaria para re-entrenamiento. Las actualizaciones siguen un ciclo dual: fine-tuning mensual con nuevos datos comunes y re-entrenamientos trimestrales que incorporan casos raros validados. Para enfermedades huérfanas, el Active Learning selecciona automáticamente los casos más informativos que puedan contener síntomas atípicos, maximizando el aprendizaje con mínimos datos. Los dashboards en Streamlit o Tableau visualizan métricas clave como la precisión por enfermedad o la tasa de drift, proporcionando transparencia total al equipo médico y de TI. Esta etapa cierra el ciclo de MLOps, transformando el modelo en un sistema adaptativo que evoluciona con la práctica clínica real.
