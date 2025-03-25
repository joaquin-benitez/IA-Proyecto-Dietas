import os
import json
import groq
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from config import GROQ_API_KEY  # Importación corregida

app = FastAPI()

# Configurar el cliente de Groq con la API Key
client = groq.Client(api_key=GROQ_API_KEY)

@app.get("/")
def read_root():
    return {"message": "API de generación de dietas para atletas"}

class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    sport: str
    goal: str  # e.g., "muscle gain", "weight loss"
    dietary_restrictions: List[str] = []

class DietPlan(BaseModel):
    name: str
    meals: List[dict]
    macros: dict

def generate_diet_with_groq(request: DietRequest):
    prompt = f"""
    Eres un nutricionista experto en planes de alimentación para atletas.
    Genera dos planes de dieta personalizados basados en los siguientes datos:
    
    - Edad: {request.age} años
    - Peso: {request.weight} kg
    - Altura: {request.height} cm
    - Deporte: {request.sport}
    - Objetivo: {request.goal}
    - Restricciones alimenticias: {", ".join(request.dietary_restrictions) if request.dietary_restrictions else "Ninguna"}
    
    Devuelve la respuesta en formato JSON con la siguiente estructura:
    {{
        "plans": [
            {{
                "name": "Plan 1",
                "meals": [
                    {{"name": "Desayuno", "description": "..."}},
                    {{"name": "Almuerzo", "description": "..."}},
                    {{"name": "Cena", "description": "..."}},
                    {{"name": "Snack 1", "description": "..."}},
                    {{"name": "Snack 2", "description": "..."}}
                ],
                "macros": {{
                    "calories": "XXXX kcal",
                    "proteins": "XX g",
                    "carbs": "XX g",
                    "fats": "XX g"
                }}
            }},
            {{
                "name": "Plan 2",
                "meals": [ ... ],
                "macros": {{ ... }}
            }}
        ]
    }}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "Eres un nutricionista experto en dietas."},
                  {"role": "user", "content": prompt}],
        max_tokens=800
    )

    try:
        # Intentar parsear la respuesta como JSON
        content = response.choices[0].message.content
        
        # Verificar si la respuesta ya es un JSON válido
        try:
            diet_response = json.loads(content)
        except json.JSONDecodeError:
            # Si no es un JSON válido, intentar extraer un bloque JSON de la respuesta
            import re
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```|({[\s\S]*})', content)
            if json_match:
                json_str = json_match.group(1) or json_match.group(2)
                try:
                    diet_response = json.loads(json_str)
                except json.JSONDecodeError:
                    return {"error": "No se pudo extraer un JSON válido de la respuesta."}
            else:
                return {"error": "La respuesta no contiene un formato JSON reconocible."}
        
        # Verificar que la estructura sea correcta o adaptarla
        if "plans" not in diet_response:
            # Si no tiene la estructura esperada, intentar adaptarla
            if isinstance(diet_response, dict):
                # Buscar alguna clave que pueda contener los planes
                for key in diet_response:
                    if isinstance(diet_response[key], list) and len(diet_response[key]) > 0:
                        return {"plans": diet_response[key]}
                
                # Si no encontramos una lista, envolver la respuesta
                return {"plans": [diet_response]}
            elif isinstance(diet_response, list):
                # Si es una lista, asumimos que son los planes
                return {"plans": diet_response}
            else:
                # Crear una estructura básica con la respuesta como texto
                return {"plans": [{"name": "Plan generado", "meals": [{"name": "Comidas", "description": str(diet_response)}], "macros": {}}]}
        
        return diet_response
        
    except Exception as e:
        return {"error": f"Error al procesar la respuesta: {str(e)}"}

@app.post("/generate-diet", response_model=dict)
def generate_diet(request: DietRequest):
    return generate_diet_with_groq(request)
