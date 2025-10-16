# TaskManager

Pequeña aplicación de consola para gestionar tareas (añadir, listar, completar, eliminar) con persistencia en JSON.

## Contenido del repositorio

- `main.py` - Interfaz de consola para usar `TaskManager`.
- `task_manager.py` - Lógica principal: clases `Task` y `TaskManager` (serialización a `tasks.json`).
- `ai_service.py` - Integración opcional con APIs de IA (OpenAI / GenAI). Usa variables de entorno para las claves.
- `borrar.py` - Script de ejemplo que usa la API de Google Generative AI (si existe).
- `tests/` - Tests de pytest (ej.: `tests/test_task_manager.py`).
- `requirements.txt` - Dependencias (nota: algunas entradas pueden ser específicas de conda).

## Requisitos

- Python 3.10+ (se recomienda 3.12/3.13 según tu entorno).
- pip o conda para instalar dependencias.

Recomendado: crear un entorno virtual o conda para evitar colisiones de paquetes.

Conda (recomendado):

```powershell
conda create -n taskenv python=3.12 -y
conda activate taskenv
python -m pip install -r requirements.txt
```

Virtualenv / pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si tu `requirements.txt` contiene entradas específicas de conda o `file:///`, revisa y adapta (ver nota más abajo).

## Ejecutar la aplicación

Desde la raíz del proyecto, con el intérprete activo:

```powershell
# Si prefieres llamar al python absoluto (ejemplo usado en este proyecto):
& C:/Python313/python.exe C:/MASTER_DESARROLLO_CON_IA_BIGSEO/TaskManager/main.py

# O desde el entorno activo:
python main.py
```

El menú de `main.py` permite:
- 1: Añadir tarea
- 2: Listar tareas
- 3: Completar tarea
- 4: Eliminar tarea
- 5: Eliminar todas las tareas
- 6: Salir

## Archivo de datos

Las tareas se escriben en `tasks.json` en la carpeta del proyecto. `TaskManager` serializa objetos `Task` a dict y los persiste en ese fichero.

## Variables de entorno y claves de API (ai_service / borrar)

Los scripts que usan APIs externas (ej. `ai_service.py`, `borrar.py`) esperan claves en variables de entorno:

- OpenAI: `OPENAI_API_KEY`
- Google GenAI: `GOOGLE_API_KEY` o `GENAI_API_KEY`

Ejemplos en PowerShell (sesión actual):

```powershell
$env:OPENAI_API_KEY = 'tu_api_key_aqui'
$env:GOOGLE_API_KEY = 'tu_api_key_aqui'
& C:/Python313/python.exe C:/MASTER_DESARROLLO_CON_IA_BIGSEO/TaskManager/ai_service.py
```

Para persistir la variable (persistente en Windows):

```powershell
setx OPENAI_API_KEY "tu_api_key_aqui"
```

También puedes usar un archivo `.env` en la raíz y la librería `python-dotenv` (no hagas commit del `.env`):

```.env
OPENAI_API_KEY=tu_api_key_aqui
GOOGLE_API_KEY=tu_api_key_aqui
```

Asegúrate de añadir `.env` a `.gitignore` y de no publicar las claves. Si una clave se filtra, rótala/elimínala inmediatamente desde la consola del proveedor.

### Notas sobre Google GenAI

Si usas la librería `google-genai`, el cliente puede inicializarse con `api_key` (API pública) o con credenciales de Google Cloud (Vertex AI). Habilita la API `generativelanguage.googleapis.com` y activa facturación si usas la API de pago.

## Ejecutar tests

Se usan tests con pytest. Para ejecutar (ejemplo usando el python absoluto que usamos en este proyecto):

```powershell
& C:/Python313/python.exe -m pytest -q
```

Los tests usan `tmp_path` para aislar el archivo `tasks.json` y `capsys` para capturar la salida por consola.

Si `pytest` no está instalado en el intérprete que usas, instálalo así:

```powershell
& C:/Python313/python.exe -m pip install pytest
```

## API pública del módulo `task_manager`

Clases y métodos principales (resumen):

- class `Task`:
	- `Task(id, description, completed=False)` — constructor
	- `to_dict()` — serializa a diccionario
	- `from_dict(d)` — (si está implementado) crea Task desde dict

- class `TaskManager`:
	- `FILENAME` — ruta a `tasks.json` (puede sobrescribirse para tests)
	- `add_task(description)` — añade y persiste
	- `list_tasks()` — imprime tareas en consola
	- `complete_task(task_id)` — marca completada y persiste
	- `delete_task(task_id)` — elimina y persiste
	- `delete_all_tasks()` — borra todas las tareas y reinicia ids
	- `load_tasks()` / `save_tasks()` — carga/guarda desde/para `FILENAME`

Usa `TaskManager.FILENAME = str(tmp_path / 'tasks.json')` dentro de tests para aislar la persistencia en disco.

## Problemas comunes y soluciones rápidas

- `ModuleNotFoundError: No module named 'openai'` o `dotenv` — asegúrate de instalar las dependencias en el intérprete correcto: `& C:/Python313/python.exe -m pip install openai python-dotenv`
- `Permission denied (publickey)` al hacer git push — problema con la clave SSH; usa HTTPS o configura tu clave SSH correctamente.
- `API key not valid` — la clave es inválida, está restringida o la API no está habilitada. Rota la clave y activa la API/facturación.

## Contribuir

1. Crea un fork.
2. Crea una rama feature/bugfix.
3. Añade tests si cambias lógica.
4. Envía PR y espera revisión.

## CI sugerido

Configura GitHub Actions para ejecutar `pytest` en cada push/PR. Un `workflow` básico ejecuta:

- setup-python
- instalar dependencias (pip install -r requirements.txt)
- ejecutar `pytest -q`

Si quieres, puedo crear el `workflow` y un `requirements_pip.txt` reducido (pip-only) para simplificar CI.

## Licencia

Por defecto no se incluye una licencia. Añade `LICENSE` si quieres publicar bajo una licencia concreta.

---

Si quieres que genere también el `.gitignore`, un `.env.example` o el workflow de GitHub Actions, dime y lo creo.
