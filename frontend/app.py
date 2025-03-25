import streamlit as st
import requests
import json
from streamlit.components.v1 import html

# Configurar la URL del backend
API_URL = "http://127.0.0.1:8000/generate-diet"

# Estado del modo oscuro
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# Aplicar estilos dinámicos según el modo oscuro
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
            body, .stApp, .sidebar .sidebar-content { background-color: #3C3C3C;  color: black; }
            .stTextInput, .stNumberInput, .stSelectbox, .stMultiselect { background-color: #555555 !important; color: white !important; }
            .stButton>button { background-color: #777777 !important; color: white !important; }
            .footer {position: fixed; bottom: 10px; width: 100%; text-align: center; color: white;}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            body, .stApp, .sidebar .sidebar-content { background-color: #E0E0E0; color: black; }
            .footer {position: fixed; bottom: 10px; width: 100%; text-align: center; color: black;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Botón para cambiar el modo oscuro
if st.sidebar.button("🌙 / ☀️ Cambiar Tema"):
    toggle_theme()

# Título de la aplicación
st.title("🥗 Generador de Plan de Dieta para Atletas")

# Descripción y pasos de uso en la barra lateral
st.sidebar.subheader("ℹ️ Información")
st.sidebar.write(
    "Crea un plan de alimentación personalizado según tu perfil y objetivos nutricionales."
)
st.sidebar.subheader("📌 Cómo Funciona")
st.sidebar.write(
    "1️⃣ **Completa tus datos.**\n"
    "2️⃣ **Selecciona tu deporte y meta.**\n"
    "3️⃣ **Añade restricciones alimentarias si es necesario.**\n"
    "4️⃣ **Presiona 'Generar Plan de Dieta'.**\n"
    "5️⃣ **Consulta los planes y su contenido nutricional.**"
)

# Formulario para ingresar datos
st.header("📋 Tus Datos Personales")
age = st.number_input("🧑 Edad", min_value=10, max_value=100, value=25, step=1)
weight = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
height = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=175, step=1)
sport = st.selectbox("⚽ Deporte", ["Fútbol", "Natación", "Ciclismo", "Running", "Gimnasio", "Otro"])
goal = st.selectbox("🎯 Objetivo", ["Aumento de masa muscular", "Pérdida de peso", "Mantenimiento"])
dietary_restrictions = st.multiselect("🚫 Restricciones Alimenticias", ["Sin lactosa", "Vegetariano", "Vegano", "Sin gluten", "Ninguna"])

if st.button("🍽️ Generar Plan de Dieta"):
    st.info("⏳ Procesando solicitud...")
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "sport": sport,
        "goal": goal,
        "dietary_restrictions": dietary_restrictions
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        diet_plans = response.json()
        if isinstance(diet_plans, dict) and "plans" in diet_plans:
            for i, plan in enumerate(diet_plans["plans"]):
                st.subheader(f"🍽️ Plan {i+1}")
                for meal in plan.get("meals", []):
                    st.write(f"🍽️ **{meal['name']}**: {meal['description']}")
                if "macros" in plan:
                    st.subheader("📊 Información Nutricional")
                    macros = plan["macros"]
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("🔥 Calorías", macros.get("calories", "N/A"))
                    with col2:
                        st.metric("💪 Proteínas", macros.get("proteins", "N/A"))
                    with col3:
                        st.metric("🍞 Carbohidratos", macros.get("carbs", "N/A"))
                    with col4:
                        st.metric("🫒 Grasas", macros.get("fats", "N/A"))
                st.divider()
    else:
        st.error(f"🚨 Error en la API: {response.status_code}")

# Footer con enlace a GitHub
st.markdown(
    """
    <div class='footer'>
        <a href='https://github.com/joaquin-benitez/proyectopy' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/25/25231.png' width='30'>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
