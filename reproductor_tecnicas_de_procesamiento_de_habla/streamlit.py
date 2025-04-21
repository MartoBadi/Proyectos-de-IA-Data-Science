import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os
from io import BytesIO

strings = ["FRECUENCIA FUNDAMENTAL (TONO): Relacionada con la vibración", "de las cuerdas vocales",
"TIMBRE Y RESONANCIA: Determinados por la forma del tracto vocal", "garganta, boca, nariz)",
"PRONUNCIACIÓN Y ACENTO: Factores conductuales que varían", "según el contexto cultural y social",
"DURACIÓN Y RITMO DEL HABLA", "forman patrones únicos de cada persona",
"SEGURIDAD Y AUTENTICACIÓN", "Autenticación en servicios bancarios o aplicaciones móviles",
"CONTROL DE ACCESO A SISTEMAS SENSIBLES",
"FORENSE: Identificación de personas a partir de grabaciones de voz", "en investigaciones criminales.",
"ASISTENTES VIRTUALES: Personalización de asistentes como Alexa, o Siri", "que pueden reconocer voces de diferentes usuarios",
"TELEMEDICINA Y BIENESTAR: Monitoreo de emociones y estados de salud mental", "a través del análisis de la voz",  
"es un mecanismo que permite asignar un valor de peso (relevancia)",
"a las palabras que componen un texto", "a fin de poder establecer la relación de esta con las demás",
"y poder determinar el contexto mediante otros algoritmos",
"Para obtener este valor", "se multiplica la cantidad de veces que se repite un término dentro del documento",
"por el logaritmo de la relación entre la cantidad de documentos", "dividido entre la cantidad de documentos que contienen la palabra en cuestión"]

# Generar los audios individuales
audios = []
for i, texto in enumerate(strings):
    tts = gTTS(text=texto, lang='es')  
# Generar el audio con gTTS
    filename = f"audio_{i + 1}.mp3"
    tts.save(filename)  # Guardar cada audio
    audios.append(filename)

# Función para calcular la duración en formato HH:MM:SS
def formato_duracion(ms):
    segundos = int(ms / 1000)
    minutos = segundos // 60
    horas = minutos // 60
    return f"{horas:02}:{minutos % 60:02}:{segundos % 60:02}"

# Cargar audios individuales y generar el audio largo
def cargar_audios(): 
   audio_largo = AudioSegment.empty()                                        
   duraciones = []                                                   
   nombres_audios = []

   for filename in sorted(os.listdir("/content")):  # Carpeta con los audios
      if filename.endswith(".mp3"):
                                                                                                                         
      audio = AudioSegment.from_file(os.path.join("/content", filename))                                                                              

      audio_largo += audio * 5  # Repetir        cada audio 5 veces
                                                                                            
      duraciones.append(len(audio) * 5)  
    # Duración total del audio repetido                                                                                                           nombres_audios.append(filename)

      return audio_largo, duraciones, nombres_audios                                                                                                                                                                                                                                                                    # Guardar el audio largo en un buffer     para reproducirlo                                                                                                               

def guardar_audio_largo(audio_largo):                                                                                                             
   buffer = BytesIO()                                                                                                                      
   audio_largo.export(buffer, format="mp3") 
   buffer.seek(0)                                                                                                                                                                                                                                         
   return buffer

                                                                                                                         # Configuración de la aplicación
                                                                                                                            st.title("Reproductor de Audios")

                                                                                                                            # Cargar los audios desde la carpeta "audios"
                                                                                                                            audio_largo, duraciones, nombres_audios = cargar_audios()
                                                                                                                            audio_largo_buffer = guardar_audio_largo(audio_largo)
                                                                                                                            # Duración total del audio largo
                                                                                                                            duracion_total = sum(duraciones)

                                                                                                                            # Mostrar las duraciones de los audios individuales
                                                                                                                            st.subheader("Duraciones de los Audios")
                                                                                                                            for i, (nombre, duracion) in enumerate(zip(nombres_audios, duraciones), 1):
                                                                                                                                st.write(f"{i}. **{nombre}**: {formato_duracion(duracion)}")

                                                                                                                                # Reproductor del audio largo
                                                                                                                                st.subheader("Reproductor del Audio Largo")
                                                                                                                                st.audio(audio_largo_buffer, format="audio/mp3")

                                                                                                                                # Botones para redirigir al inicio de cada audio
                                                                                                                                st.subheader("Ir al Inicio de los Audios")
                                                                                                                                duracion_acumulada = 0
                                                                                                                                for i, (nombre, duracion) in enumerate(zip(nombres_audios, duraciones)):
                                                                                                                                    # Calcular el tiempo acumulado para este audio
                                                                                                                                        inicio_audio = duracion_acumulada
                                                                                                                                            fin_audio = duracion_acumulada + duracion
                                                                                                                                                duracion_acumulada += duracion

                                                                                                                                                    # Crear un botón para redirigir al inicio del audio
                                                                                                                                                        if st.button(f"Ir a {nombre}", key=f"boton_{i}"):
                                                                                                                                                                st.session_state["audio_actual"] = i

                                                                                                                                                                    # Resaltar el botón si el audio actual está dentro de este rango
                                                                                                                                                                        if "audio_actual" in st.session_state and st.session_state["audio_actual"] == i:
                                                                                                                                                                                st.markdown(f"🎵 **Reproduciendo: {nombre}** 🎵")