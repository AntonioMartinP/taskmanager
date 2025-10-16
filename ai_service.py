import os
import sys
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ModuleNotFoundError:
    print("Falta el paquete 'openai'. Instálalo con:")
    print(r"& 'C:/Python313/python.exe' -m pip install openai")
    sys.exit(1)

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None

def _fallback_split(description: str):
    parts = [p.strip() for p in description.split('.') if p.strip()]
    return parts if parts else [description.strip()]

def _extract_text_from_response(resp):
    # Varias versiones del SDK retornan formatos distintos; intentamos varias rutas.
    try:
        # estilo: resp.choices[0].message.content
        return resp.choices[0].message.content
    except Exception:
        pass
    try:
        # estilo: resp.choices[0].text
        return resp.choices[0].text
    except Exception:
        pass
    try:
        # si es stringifyable
        return str(resp)
    except Exception:
        return ""

def create_simple_tasks(description: str):
    """
    Devuelve una lista de subtareas extraídas de `description`.
    Si no hay clave o la llamada falla, devuelve un fallback local.
    """
    if not description:
        return []

    if not client:
        return ["WARNING: OPENAI_API_KEY no configurada."] + _fallback_split(description)

    prompt = (
        "Desglosa la siguiente tarea en subtareas simples y numeradas, responde solo con cada subtarea en una línea empezando por '-':\n\n"
        f"Tarea: {description}\n\n"
        "Formato de respuesta:\n"
        "- Subtarea 1\n"
        "- Subtarea 2\n"
        "- Subtarea 3\n"
    )

    params = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en gestión de tareas que divide tareas en subtareas claras y accionables."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
        # "n": 1,  # opcional
    }

    try:
        response = client.chat.completions.create(**params)
        content = _extract_text_from_response(response) or ""
        # parsear líneas con guion o numeradas
        subtasks = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            # guion inicial
            if line.startswith("-"):
                candidate = line[1:].strip()
                if candidate:
                    subtasks.append(candidate)
                continue
            # numeración "1." o "1)"
            if line[0].isdigit():
                # eliminar prefijo numérico
                candidate = line.lstrip("0123456789. )\t").strip()
                if candidate:
                    subtasks.append(candidate)
                continue
            # si no cumple, aceptar la línea tal cual
            subtasks.append(line)
        return subtasks if subtasks else _fallback_split(description)
    except Exception as e:
        return [f"Error: no se pudo conectar a la API de OpenAI: {e}"] + _fallback_split(description)