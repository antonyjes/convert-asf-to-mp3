import os
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configurar la ruta de FFmpeg y ffprobe
ffmpeg_path = os.getenv('FFMPEG_PATH')
ffprobe_path = os.getenv('FFPROBE_PATH')
AudioSegment.converter = ffmpeg_path

# Ruta principal obtenida del archivo .env
root_directory = os.getenv("ROOT_DIRECTORY")

def detect_format(file_path):
    """
    Detecta el formato del archivo usando ffprobe.
    """
    try:
        command = [
            ffprobe_path, 
            "-v", "error", 
            "-show_entries", "format=format_name", 
            "-of", "default=nw=1:nk=1", 
            file_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()  # Devuelve el formato detectado (ej. "wma", "mp3")
    except Exception as e:
        print(f"Error al detectar el formato de {file_path}: {e}")
        return None

def convert_to_mp3(file_path, output_path):
    """
    Convierte un archivo de audio a MP3.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        audio.export(output_path, format="mp3")
        print(f"Archivo convertido: {file_path} -> {output_path}")
    except Exception as e:
        print(f"Error al convertir {file_path}: {e}")

def process_audio_files(root_directory):
    """
    Procesa todos los archivos en la carpeta raíz y subcarpetas.
    """
    for foldername, subfolders, filenames in os.walk(root_directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            output_path = os.path.join(foldername, filename.rsplit(".", 1)[0] + ".mp3")

            # Detectar el formato del archivo
            detected_format = detect_format(file_path)
            if detected_format == "asf":  # Solo convierte si es un archivo asf (WMA)
                print(f"\nArchivo encontrado: {file_path} (Formato detectado: {detected_format})")
                if not os.path.exists(output_path):  # Evita duplicados
                    convert_to_mp3(file_path, output_path)
                    os.remove(file_path)  # Elimina el archivo original
                    print(f"Archivo original eliminado: {file_path}")
                else:
                    print(f"El archivo convertido ya existe: {output_path}")
            else:
                print(f"Formato no compatible o no necesario: {file_path} (Detectado: {detected_format})")

if __name__ == "__main__":
    if not root_directory:
        print("Error: ROOT_DIRECTORY no está definido en el archivo .env.")
    elif not os.path.exists(root_directory):
        print(f"Error: La ruta especificada no existe: {root_directory}")
    else:
        process_audio_files(root_directory)
