import base64
from openai import OpenAI
import os
import json
import uuid
import time
from dotenv import load_dotenv
import glob
import csv

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuración de directorios
# Obtener directorio base donde se encuentra este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_DIR = os.path.join(BASE_DIR, "FOTOS estudiantes")
OUTPUT_DIR = os.path.join(BASE_DIR, "static/generated")
LOGO_PATH = os.path.join(BASE_DIR, "Images/logo.png")

# Asegurarse de que el directorio de salida exista
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Función para leer los datos del estudiante desde un archivo CSV o JSON si existe
def get_student_data(student_folder):
    # Buscar archivos JSON o CSV en la carpeta del estudiante
    json_files = glob.glob(os.path.join(student_folder, "*.json"))
    csv_files = glob.glob(os.path.join(student_folder, "*.csv"))
    
    if json_files:
        # Leer datos desde el primer archivo JSON encontrado
        with open(json_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('name', ''), data.get('career', ''), data.get('gender', 'male')
    
    elif csv_files:
        # Leer datos desde el primer archivo CSV encontrado
        with open(csv_files[0], 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    return row[0], row[1], row[2]
                elif len(row) >= 2:
                    return row[0], row[1], 'male'
                else:
                    return row[0] if row else '', '', 'male'
    
    # Si no se encuentra información, usar el nombre de la carpeta
    folder_name = os.path.basename(student_folder)
    return folder_name, "Ingeniería", "male"  # Valores por defecto

# Función para generar el prompt según el género
def generate_prompt(name, career, gender):
    if gender.lower() == 'female':
        return f"""
        Edit the image, based on the reference. The image is of me in the picture smiling while holding my graduation diploma with the logo that i provide to you and the name "{name}", additionally two signatures in the bottom right corner and left corner. I am standing in a well-kept garden in front of a circular water fountain. Behind me is a modern multi-story building with large windows, likely a university campus. I am 5 years older dressed elegantly in a formal dress with subtle details, looking professional and confident for my graduation ceremony.

        The diploma I am holding shows that I graduated as a "{career}" from the Escuela Colombiana de Ingeniería Julio Garavito in Colombia. My name, visible on the diploma, is {name}.

        In the background, there are flowering bushes, which, together with the modern building, create a solemn and pleasant atmosphere—perfect for a graduation ceremony. My posture, elegant attire, and the way I proudly hold the diploma reflect my happiness and pride in this academic achievement.
        """
    else:  # 'male' u otras opciones
        return f"""
        Edit the image, based on the reference. The image is of me in the picture smiling while holding my graduation diploma with the logo that i provide to you and the name "{name}", additionally two signatures in the bottom right corner and left corner. I am standing in a well-kept garden in front of a circular water fountain. Behind me is a modern multi-story building with large windows, likely a university campus. I am 5 years older dressed formally in a white dress shirt with small dark dots, a blue tie with white dots, a dark blue suit jacket, and matching pants.

        The diploma I am holding shows that I graduated as a "{career}" from the Escuela Colombiana de Ingeniería Julio Garavito in Colombia. My name, visible on the diploma, is {name}.

        In the background, there are flowering bushes, which, together with the modern building, create a solemn and pleasant atmosphere—perfect for a graduation ceremony. My posture, formal attire, and the way I proudly hold the diploma reflect my happiness and pride in this academic achievement.
        """

# Función para procesar una imagen
def process_image(image_path, name, career, gender):
    print(f"Procesando imagen para {name}...")
    
    # Generar el prompt según el género
    prompt = generate_prompt(name, career, gender)
    
    try:
        # Generar la imagen con el método images.edit de la API de OpenAI
        result = client.images.edit(
            model="gpt-image-1",
            image=open(image_path, "rb"),
            mask=open(LOGO_PATH, "rb"),
            prompt=prompt
        )
        
        # Obtener la imagen generada en formato base64
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        
        # Generar nombre único para la imagen
        output_filename = f"graduacion_{name.replace(' ', '_')}_{uuid.uuid4()}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Guardar la imagen generada
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        
        print(f"✅ Imagen guardada en: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error al procesar la imagen para {name}: {str(e)}")
        return None

def main():
    print("==================================================")
    print("VENTANA AL FUTURO - PROCESADOR DE IMÁGENES POR LOTES")
    print("==================================================")
    
    # Verificar si existe el directorio de estudiantes
    if not os.path.exists(STUDENTS_DIR):
        print(f"❌ Error: El directorio {STUDENTS_DIR} no existe.")
        return
    
    # Obtener todas las subcarpetas de estudiantes
    student_folders = [f.path for f in os.scandir(STUDENTS_DIR) if f.is_dir()]
    
    if not student_folders:
        print(f"❌ No se encontraron subcarpetas en {STUDENTS_DIR}.")
        return
    
    print(f"Se encontraron {len(student_folders)} carpetas de estudiantes.")
    
    # Procesar cada carpeta de estudiante
    for student_folder in student_folders:
        # Obtener nombre, carrera y género del estudiante
        name, career, gender = get_student_data(student_folder)
        
        # Buscar imágenes en la carpeta del estudiante
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(glob.glob(os.path.join(student_folder, ext)))
        
        if not image_files:
            print(f"⚠️ No se encontraron imágenes en la carpeta de {name}.")
            continue
        
        # Procesar cada imagen encontrada
        for image_path in image_files:
            output_path = process_image(image_path, name, career, gender)
            
            # Esperar un poco entre solicitudes para no sobrecargar la API
            time.sleep(1)
    
    print("==================================================")
    print("Procesamiento completado.")
    print("==================================================")

if __name__ == "__main__":
    main()