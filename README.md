# Generador de Plan de Dieta para Atletas

Esta aplicación genera planes de dieta personalizados para atletas utilizando IA (Groq API con el modelo llama3-8b-8192).

## Estructura del Proyecto

- `backend/`: API FastAPI que se comunica con Groq para generar planes de dieta
- `frontend/`: Interfaz de usuario Streamlit para recopilar datos y mostrar resultados
- `run.py`: Script para ejecutar tanto el backend como el frontend

## Requisitos

- Python 3.7+
- Paquetes: fastapi, uvicorn, streamlit, groq

## Cómo Ejecutar la Aplicación

1. Asegúrate de tener Python instalado
2. Ejecuta el script `run.py`:

```bash
python run.py
```

Este script:
- Instalará las dependencias necesarias si no están presentes
- Iniciará el servidor backend (FastAPI)
- Iniciará la aplicación frontend (Streamlit)
- Abrirá automáticamente la aplicación en tu navegador

## Solución de Problemas

Si experimentas problemas con la generación de dietas, verifica lo siguiente:

1. **Conexión entre Frontend y Backend**: Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000
2. **API Key de Groq**: Verifica que la API key en `backend/config.py` sea válida
3. **Formato de Respuesta**: La aplicación ahora maneja varios formatos de respuesta de la API de Groq


