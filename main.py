#==============================================================================================================================================================
# Estructura del proyecto
#==============================================================================================================================================================
# 1. Juego (Juego)
# 2. Circuito de juego (MAQUETA)(Programacion de Thonny)
# 3. Conexiones (CONECTAR)(leds, botones, scroll, Pantalla (opcional))
# 4. Pruebas (TESTEAR)
# 5. Documentacion (Cronograma, materiales, codigo, fotos, video)
#==============================================================================================================================================================
# Desarrollo del juego FIFA89
#==============================================================================================================================================================

# Importamos las librerias necesarias para el desarrollo del juego
import tkinter as Tk
from tkinter import messagebox
import variables
from itertools import cycle
from PIL import Image, ImageTk
import pygame

#==============================================================================================================================================================

# Configuracion del sonido de fondo del juego
pygame.mixer.init()
pygame.mixer.music.load("Candy.mp3")
pygame.mixer.music.play(-1)  # Reproducir en bucle infinito

#==============================================================================================================================================================
# Configuracion de la ventana principal del juego
root = Tk.Tk()
root.withdraw()
#==============================================================================================================================================================
# Crear ventana principal con sus propiedades y caracteristicas
ventana = Tk.Toplevel()
ventana.title("FIFA89")
ventana.geometry(f"{variables.ancho}x{variables.alto}")
ventana.configure(bg="black", cursor="spider", relief="groove", bd=20)
ventana.resizable(False, False)
ventana.iconbitmap("icono.ico")
ventana.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("Salir", "Para salir del juego, por favor presiona el boton de 'Salir' en la interfaz."))  

#==============================================================================================================================================================

# Cargar el GIF animado y redimensionar los frames al tamaño de la ventana
gif_path = "1.gif"
frame_gif = 30  # Cambia 30 por el número de frames de tu GIF
gif_frames = []

for i in range(frame_gif):
    frame = Image.open(gif_path)
    frame.seek(i)
    resized = frame.resize((variables.ancho, variables.alto), Image.LANCZOS)
    gif_frames.append(ImageTk.PhotoImage(resized))
frames = cycle(gif_frames)

def actualizar_fondo():
    frame = next(frames)
    fondo_label.config(image=frame)
    fondo_label.image = frame  # Evita que el frame se elimine por el recolector de basura
    ventana.after(100, actualizar_fondo)

fondo_label = Tk.Label(ventana)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
actualizar_fondo()

#==============================================================================================================================================================
# Creación de un frame para centrar los botones y ocultar el fondo GIF detrás de ellos
botones_frame = Tk.Frame(ventana, bg="black", bd=12, relief="ridge")
botones_frame.place(relx=0.5, rely=0.5, anchor="center")

#==============================================================================================================================================================
# Animación de botones al pasar el mouse

def animar_boton(event, boton, color_hover, color_fg_hover):
    boton.config(bg=color_hover, fg=color_fg_hover)

def restaurar_boton(event, boton, color_normal, color_fg_normal):
    boton.config(bg=color_normal, fg=color_fg_normal)

#==============================================================================================================================================================
# BOTON 1 - SALIR
buton1 = Tk.Button(
    botones_frame,
    text="Salir",
    command=ventana.destroy,
    bg="black",
    fg="white",
    font=("Arial Black", 18, "bold"),
    bd=8,
    width=12,
    height=2,
    cursor="hand2",
    activebackground="#b71c1c",
    relief="flat"
)
buton1.pack(pady=10)
buton1.bind("<Enter>", lambda e: animar_boton(e, buton1, "#d32f2f", "#fff176"))
buton1.bind("<Leave>", lambda e: restaurar_boton(e, buton1, "black", "white"))

#==============================================================================================================================================================
# BOTON 2 - ACERCA DE
def acerca_de():
    acerca_ventana = Tk.Toplevel(ventana)
    acerca_ventana.title("Acerca de FIFA89")
    acerca_ventana.geometry("800x600")
    acerca_ventana.configure(bg="#e3f2fd")
    acerca_ventana.resizable(False, False)

    # Frame centrado para la portada
    portada_frame = Tk.Frame(acerca_ventana, bg="#e3f2fd")
    portada_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título principal
    titulo = Tk.Label(
        portada_frame,
        text="FIFA89",
        font=("Arial Black", 36, "bold"),
        bg="#e3f2fd",
        fg="#1565c0",
        justify="center"
    )
    titulo.pack(pady=(0, 20))

    # Texto centrado tipo portada
    portada_texto = (
        "Instituto Tecnológico de Costa Rica\n"
        "Fundamentos de sistemas computacionales\n"
        "Profesor: Luis Alonso Barboza Artavia\n"
        "Estudiante: Joshua Morales Guzmán\n"
        "Proyecto: Futbolín\n"
        "Año: 2025"
    )
    acerca_label = Tk.Label(
        portada_frame,
        text=portada_texto,
        font=("Arial Black", 14),
        bg="#e3f2fd",
        fg="#263238",
        justify="center"
    )
    acerca_label.pack(pady=10)

    cerrar_btn = Tk.Button(
        portada_frame,
        text="Cerrar",
        command=acerca_ventana.destroy,
        font=("Arial", 12),
        bg="#2b95e1",
        fg="white",
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )
    cerrar_btn.pack(pady=20)

button2 = Tk.Button(
    botones_frame,
    text="Acerca de",
    command=acerca_de,
    bg="black",
    fg="white",
    font=("Arial Black", 18, "bold"),
    bd=8,
    width=12,
    height=2,
    cursor="hand2",
    activebackground="#1b5e20",
    relief="flat"
)
button2.pack(pady=10)
button2.bind("<Enter>", lambda e: animar_boton(e, button2, "#388e3c", "#fff176"))
button2.bind("<Leave>", lambda e: restaurar_boton(e, button2, "black", "white"))

#==============================================================================================================================================================
# BOTON 3 - CONFIGURACION INICIAL
def mostrar_configuracion_inicial():
    config_ventana = Tk.Toplevel(ventana)
    config_ventana.title("Configuración Inicial")
    config_ventana.geometry("400x300")
    config_ventana.configure(bg="#f9fbe7")
    config_ventana.resizable(False, False)

    # Frame centrado para la configuración
    config_frame = Tk.Frame(config_ventana, bg="#f9fbe7")
    config_frame.place(relx=0.5, rely=0.5, anchor="center")

    label = Tk.Label(
        config_frame,
        text="Opciones de configuración",
        font=("Arial Black", 18, "bold"),
        bg="#f9fbe7",
        fg="#263238",
        justify="center"
    )
    label.pack(pady=(0, 20))

    # Scroll de volumen-------------------------------------------------------------------------------------------------------------------
    volumen_label = Tk.Label(
        config_frame,
        text="Volumen",
        font=("Arial", 14),
        bg="#f9fbe7",
        fg="#263238",
        justify="center"
    )
    volumen_label.pack(pady=(0, 10))

    volumen_var = Tk.DoubleVar(value=pygame.mixer.music.get_volume() * 100)

    def cambiar_volumen(valor):
        pygame.mixer.music.set_volume(float(valor) / 100)

    volumen_scroll = Tk.Scale(
        config_frame,
        from_=0,
        to=100,
        orient="horizontal",
        variable=volumen_var,
        command=cambiar_volumen,
        length=200,
        bg="#f9fbe7",
        fg="#263238",
        troughcolor="#fbc02d",
        highlightthickness=0,
        font=("Arial", 12)
    )
    volumen_scroll.pack(pady=(0, 20))

    cerrar_btn = Tk.Button(
        config_frame,
        text="Cerrar",
        command=config_ventana.destroy,
        font=("Arial", 12),
        bg="#fbc02d",
        fg="black",
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )
    cerrar_btn.pack(pady=10)

buton3 = Tk.Button(
    botones_frame,
    text="Configuración Inicial",
    command=mostrar_configuracion_inicial,
    bg="black",
    fg="white",
    font=("Arial Black", 18, "bold"),
    bd=8,
    width=12,
    height=2,
    cursor="hand2",
    activebackground="#f9a825",
    relief="flat"
)
buton3.pack(pady=10)
buton3.bind("<Enter>", lambda e: animar_boton(e, buton3, "#fbc02d", "#388e3c"))
buton3.bind("<Leave>", lambda e: restaurar_boton(e, buton3, "black", "white"))

#==============================================================================================================================================================
# Cierre de la ventana principal del juego
ventana.mainloop()
#==============================================================================================================================================================