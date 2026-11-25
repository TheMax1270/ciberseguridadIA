# Asistente de validación de respaldos — IaaS/PaaS/SaaS

## Descripción

Aplicación desarrollada para validar evidencias de copias de respaldo y pruebas de restauración en servicios de infraestructura, plataforma y software en la nube.



El sistema combina reglas deterministas con inteligencia artificial local para identificar hallazgos, establecer prioridades, interpretar evidencias y generar recomendaciones orientadas a la gestión de riesgos y la recuperación de servicios.

## Integrantes

- Max Daniel Pérez Quintero
- David Gómez Agudelo
- Sebastián Flórez Jaramillo

**Universidad de Antioquia**



Curso: Introducción a la Ciberseguridad



Docente: Beatriz Chaverra



2026-2

## Tecnologías utilizadas

- Python: lógica de negocio y validación mediante reglas.
- Streamlit: interfaz de usuario.
- Ollama: ejecución local del modelo de inteligencia artificial.
- Llama 3.2 (3B): interpretación de resultados y generación de recomendaciones.
- JSON y CSV: almacenamiento, exportación y evaluación de resultados.
- Unittest: pruebas automatizadas.

## Instalación y ejecución

### Requisitos

- Python.
- Git.
- Ollama instalado y en ejecución.

### 1. Clonar el repositorio
```bash
git clone https://github.com/TheMax1270/ciberseguridadIA.git
cd ciberseguridadIA
```

### 2. Crear el entorno virtual e instalar las dependencias

Desde PowerShell en Windows:
```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Descargar el modelo de inteligencia artificial
```
ollama pull llama3.2:3b
```

### 4. Ejecutar la aplicación
```
.\.venv\Scripts\python.exe -m streamlit run app.py
```

La aplicación estará disponible en:



`http://localhost:8501`

## Funcionamiento

La aplicación permite seleccionar casos de laboratorio o ingresar datos manualmente. El motor de reglas valida el estado, completitud y antigüedad del respaldo, así como las evidencias y tiempos de restauración.



El modelo de inteligencia artificial interpreta los resultados y genera recomendaciones complementarias. La aplicación permite comparar ambos análisis y exportar los resultados en formato JSON.



La decisión final corresponde al administrador o auditor responsable.

## Pruebas automatizadas

El proyecto incluye 78 pruebas automatizadas y 20 casos de laboratorio distribuidos en ocho casos problemáticos, ocho legítimos y cuatro ambiguos.



Para ejecutar las pruebas automatizadas:
```
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Para ejecutar la evaluación del modelo local:
```
.\.venv\Scripts\python.exe evaluar_modelo.py --salida resultados_evaluacion_nueva
```

## Seguridad

El modelo funciona localmente mediante Ollama. Las recomendaciones no se ejecutan automáticamente sobre infraestructura y los resultados requieren revisión humana.
