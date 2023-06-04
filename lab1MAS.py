import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.editor import VideoClip

# Variables globales para almacenar los datos del movimiento
velocidad = 0.0
aceleracion = 0.0
angulo = 0.0
altura = 0.0

# Función para detectar el objeto en movimiento y obtener sus medidas
def obtener_medidas(frame):
    # Preprocesamiento de la imagen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detección de bordes con Canny
    edges = cv2.Canny(gray, 50, 150)

    # Detección de contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Buscar el contorno más grande (objeto en movimiento)
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # Obtener el centro del contorno
    if max_contour is not None:
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Calcular las medidas en función del centro del objeto
            global velocidad, aceleracion, angulo, altura
            velocidad = cx * 0.1
            aceleracion = cx * 0.05
            angulo = cx * 0.45
            altura = cy * 0.1

    # Dibujar el contorno y el centro en la imagen original
    if max_contour is not None:
        cv2.drawContours(frame, [max_contour], 0, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    return frame

# Función para superponer los datos del movimiento en el video
def procesar_video(t):
    global velocidad, aceleracion, angulo, altura

    # Cargar el fotograma correspondiente al tiempo t
    frame = frames[int(t * fps)]

    # Realizar detección de objeto en movimiento y obtener las medidas
    frame = obtener_medidas(frame)

    # Actualizar las medidas del movimiento
    # (puedes ajustar la lógica de cálculo según tus necesidades)
    velocidad = t * 10.0
    aceleracion = t * 5.0
    angulo = t * 45.0
    altura = t * 100.0

    # Agregar datos del movimiento en el video
    # (puedes ajustar el formato y la posición según tus necesidades)
    text1 = f"Velocidad: {velocidad:.2f} m/s  Aceleracion: {aceleracion:.2f} m/s²"
    text2 = f"Angulo: {angulo:.2f}°  Altura: {altura:.2f} m"

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text1, (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, text2, (50, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame

# Cargar el video
video_path = r"C:\Video\PENDULO2.mp4"
video = cv2.VideoCapture(video_path)

# Obtener las dimensiones del video
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Leer y almacenar todos los fotogramas del video
frames = []
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    frames.append(frame)

video.release()

# Crear el clip de video procesado
processed_clip = VideoClip(procesar_video, duration=total_frames / fps)

# Mostrar el video con las medidas superpuestas en tiempo real
processed_clip.preview(fps=fps)

# Cerrar la ventana al finalizar
cv2.destroyAllWindows()