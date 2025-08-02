# 🎓 Ventana al Futuro - Generador de Imágenes AI

[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-412991.svg)](https://openai.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Este proyecto utiliza inteligencia artificial (OpenAI) para transformar fotos de estudiantes de primer semestre en retratos profesionales de graduación. Creado para la Escuela Colombiana de Ingeniería Julio Garavito.

![Ejemplo de transformación](https://i.imgur.com/placeholder.png)

## ✨ Características

- 🖼️ Procesa imágenes de estudiantes desde directorios específicos
- 👩‍🎓👨‍🎓 Genera prompts personalizados según el género del estudiante
- 🤖 Utiliza la API de OpenAI (gpt-image-1) para editar imágenes
- 💾 Guarda las imágenes generadas con nombres únicos
- 📄 Lee datos de estudiantes desde archivos JSON o CSV
- 🚀 Procesamiento por lotes para múltiples estudiantes

## 📁 Estructura de Directorios

```
ImageMakerOpenAI/
├── GPT_GEN_IMG.py       # 🚀 Script principal
├── .env                 # 🔑 Variables de entorno (API key)
├── requirements.txt     # 📋 Dependencias
├── Images/
│   └── logo.png         # 🏫 Logo de la institución (usado como máscara)
├── FOTOS estudiantes/   # 📸 Carpeta con fotos de estudiantes
│   ├── Estudiante1/     # 👩‍🎓 Una subcarpeta por estudiante
│   │   ├── foto.jpg     # 📷 Foto(s) del estudiante
│   │   └── info.json    # 📝 Opcional: datos del estudiante
│   └── Estudiante2/     # 👨‍🎓 Otro estudiante
│       ├── foto.png     # 📷 Foto del estudiante
│       └── datos.csv    # 📊 Opcional: datos en CSV
└── static/
    └── generated/       # 🖼️ Aquí se guardarán las imágenes generadas
```

## 📊 Formato de Datos del Estudiante

### Archivo JSON (ejemplo)
```json
{
    "name": "Nombre Estudiante",
    "career": "Ingeniería de Sistemas",
    "gender": "male"  // o "female"
}
```

### Archivo CSV (ejemplo)
```
Nombre Estudiante,Ingeniería de Sistemas,male
```

> **Nota**: Si no se proporciona un archivo de datos, el script utilizará el nombre de la carpeta como nombre del estudiante, "Ingeniería" como carrera y "male" como género predeterminado.

## 🚀 Instalación

1. **Clona este repositorio:**
```bash
git clone https://github.com/Juan-Rpenuela/ImageMakerOpenAI.git
cd ImageMakerOpenAI
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configura tu API key:**
   - Crea un archivo `.env` basado en el archivo `.env.example`
   - Añade tu API key de OpenAI:
```
OPENAI_API_KEY=tu_clave_api_aqui
```

## 📋 Uso

1. **Prepara las imágenes:**
   - Coloca las fotos de los estudiantes en subcarpetas dentro de `FOTOS estudiantes/`
   - Opcionalmente, añade archivos JSON o CSV con los datos de cada estudiante

2. **Ejecuta el script:**
```bash
python GPT_GEN_IMG.py
```

3. **Revisa los resultados:**
   - Las imágenes generadas se guardarán en la carpeta `static/generated/`

## 💡 Consejos y Notas

- 🖼️ Usa fotos claras y frontales del rostro del estudiante para mejores resultados
- ⏱️ El script pausa brevemente entre solicitudes para evitar límites de la API
- 📝 Los prompts están optimizados para generar imágenes de graduación profesionales
- 🎭 El sistema detecta automáticamente el género para personalizar la vestimenta
- 📋 Puedes personalizar los prompts editando la función `generate_prompt`

## 🔧 Requisitos Técnicos

- Python 3.8 o superior
- Cuenta de OpenAI con acceso a la API gpt-image-1
- Conexión a internet para las llamadas a la API
## 🌟 Ventana al Futuro - Escuela Colombiana de Ingeniería

Este proyecto fue desarrollado para la Escuela Colombiana de Ingeniería Julio Garavito para ofrecer a los nuevos estudiantes una "ventana al futuro", mostrándoles cómo podrían verse el día de su graduación.
