#==============================================================================================================================================================
# Estructura del proyecto FIFA89 - Juego de Penales
#==============================================================================================================================================================

# Importamos las librerias necesarias para el desarrollo del juego
import tkinter as Tk
from tkinter import messagebox
import random
from itertools import cycle
from PIL import Image, ImageTk
import pygame

#==============================================================================================================================================================
# Variables globales del juego
ancho = 800
alto = 600

#==============================================================================================================================================================
# Configuracion del sonido de fondo del juego

pygame.mixer.init()
pygame.mixer.music.load("Candy.mp3")
pygame.mixer.music.play(-1)  # Reproducir en bucle infinito (comentado si no tienes el archivo)

#==============================================================================================================================================================
# Configuracion de la ventana principal del juego
root = Tk.Tk()
root.withdraw()

#==============================================================================================================================================================
# Crear ventana principal con sus propiedades y caracteristicas
ventana = Tk.Toplevel()
ventana.title("FIFA89")
ventana.geometry(f"{ancho}x{alto}")
ventana.configure(bg="black", cursor="spider", relief="groove", bd=20)
ventana.resizable(False, False)
ventana.iconbitmap("icono.ico")  # Comentado si no tienes el archivo
ventana.protocol("WM_DELETE_WINDOW", lambda: messagebox.showinfo("Salir", "Para salir del juego, por favor presiona el boton de 'Salir' en la interfaz."))  

#==============================================================================================================================================================
# Fondo de la ventana principal
fondo_label = Tk.Label(ventana, bg="#0d47a1")
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

#==============================================================================================================================================================
# Creación de un frame para centrar los botones
botones_frame = Tk.Frame(ventana, bg="black", bd=12, relief="ridge")
botones_frame.place(relx=0.5, rely=0.5, anchor="center")

#==============================================================================================================================================================
# Animación de botones al pasar el mouse

def animar_boton(event, boton, color_hover, color_fg_hover):
    boton.config(bg=color_hover, fg=color_fg_hover)

def restaurar_boton(event, boton, color_normal, color_fg_normal):
    boton.config(bg=color_normal, fg=color_fg_normal)

#==============================================================================================================================================================
# JUEGO DE PENALES
#==============================================================================================================================================================

class JuegoPenales:
    def __init__(self, ventana_padre):
        self.ventana = Tk.Toplevel(ventana_padre)
        self.ventana.title("FIFA89 - Penales")
        self.ventana.geometry("900x700")
        self.ventana.configure(bg="#1b5e20")
        self.ventana.resizable(False, False)
        
        # Variables del juego
        self.goles = 0
        self.atajadas = 0
        self.total_tiros = 0
        self.puede_disparar = True
        
        # Canvas del juego
        self.canvas = Tk.Canvas(self.ventana, width=900, height=600, bg="#2e7d32", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Dibujar campo
        self.dibujar_campo()
        
        # Portería
        self.porteria_x = 250
        self.porteria_y = 100
        self.porteria_ancho = 400
        self.porteria_alto = 200
        self.dibujar_porteria()
        
        # Portero
        self.portero_x = 450
        self.portero_y = 250
        self.portero_ancho = 80
        self.portero_alto = 100
        self.portero_velocidad = 25
        self.portero = self.canvas.create_rectangle(
            self.portero_x - self.portero_ancho//2,
            self.portero_y - self.portero_alto//2,
            self.portero_x + self.portero_ancho//2,
            self.portero_y + self.portero_alto//2,
            fill="#ff6f00", outline="#e65100", width=3
        )
        
        # Cabeza del portero
        self.portero_cabeza = self.canvas.create_oval(
            self.portero_x - 25,
            self.portero_y - self.portero_alto//2 - 35,
            self.portero_x + 25,
            self.portero_y - self.portero_alto//2 + 15,
            fill="#ffab91", outline="#e65100", width=2
        )
        
        # Balón
        self.balon_x = 450
        self.balon_y = 500
        self.balon_radio = 15
        self.balon = self.canvas.create_oval(
            self.balon_x - self.balon_radio,
            self.balon_y - self.balon_radio,
            self.balon_x + self.balon_radio,
            self.balon_y + self.balon_radio,
            fill="white", outline="black", width=2
        )
        
        # Detalles del balón
        self.canvas.create_oval(
            self.balon_x - 8,
            self.balon_y - 8,
            self.balon_x + 8,
            self.balon_y + 8,
            outline="black", width=1
        )
        
        # Variables de disparo
        self.disparando = False
        self.objetivo_x = 0
        self.objetivo_y = 0
        
        # Panel de información
        self.info_frame = Tk.Frame(self.ventana, bg="#1b5e20")
        self.info_frame.pack(fill="x", padx=20)
        
        self.label_goles = Tk.Label(
            self.info_frame,
            text=f"Goles: {self.goles}",
            font=("Arial Black", 16),
            bg="#1b5e20",
            fg="#ffeb3b"
        )
        self.label_goles.pack(side="left", padx=10)
        
        self.label_atajadas = Tk.Label(
            self.info_frame,
            text=f"Atajadas: {self.atajadas}",
            font=("Arial Black", 16),
            bg="#1b5e20",
            fg="#f44336"
        )
        self.label_atajadas.pack(side="left", padx=10)
        
        self.label_instrucciones = Tk.Label(
            self.info_frame,
            text="Flechas: Mover portero | ESPACIO: Disparar",
            font=("Arial", 12),
            bg="#1b5e20",
            fg="white"
        )
        self.label_instrucciones.pack(side="right", padx=10)
        
        # Controles
        self.ventana.bind("<Left>", self.mover_portero_izquierda)
        self.ventana.bind("<Right>", self.mover_portero_derecha)
        self.ventana.bind("<space>", self.disparar)
        
    def dibujar_campo(self):
        # Líneas del campo
        self.canvas.create_line(0, 400, 900, 400, fill="white", width=3)
        
        # Área de penal
        self.canvas.create_rectangle(200, 80, 700, 350, outline="white", width=3)
        
        # Punto de penal
        self.canvas.create_oval(440, 490, 460, 510, fill="white", outline="white")
        
    def dibujar_porteria(self):
        # Postes
        self.canvas.create_rectangle(
            self.porteria_x - 10,
            self.porteria_y,
            self.porteria_x,
            self.porteria_y + self.porteria_alto,
            fill="#e0e0e0", outline="#757575", width=3
        )
        self.canvas.create_rectangle(
            self.porteria_x + self.porteria_ancho,
            self.porteria_y,
            self.porteria_x + self.porteria_ancho + 10,
            self.porteria_y + self.porteria_alto,
            fill="#e0e0e0", outline="#757575", width=3
        )
        # Travesaño
        self.canvas.create_rectangle(
            self.porteria_x,
            self.porteria_y - 10,
            self.porteria_x + self.porteria_ancho,
            self.porteria_y,
            fill="#e0e0e0", outline="#757575", width=3
        )
        
        # Red
        for i in range(self.porteria_x, self.porteria_x + self.porteria_ancho, 40):
            self.canvas.create_line(
                i, self.porteria_y,
                i, self.porteria_y + self.porteria_alto,
                fill="#bdbdbd", width=1
            )
        for j in range(self.porteria_y, self.porteria_y + self.porteria_alto, 40):
            self.canvas.create_line(
                self.porteria_x, j,
                self.porteria_x + self.porteria_ancho, j,
                fill="#bdbdbd", width=1
            )
    
    def mover_portero_izquierda(self, event):
        if self.portero_x - self.portero_velocidad > self.porteria_x + self.portero_ancho//2:
            self.portero_x -= self.portero_velocidad
            self.canvas.move(self.portero, -self.portero_velocidad, 0)
            self.canvas.move(self.portero_cabeza, -self.portero_velocidad, 0)
    
    def mover_portero_derecha(self, event):
        if self.portero_x + self.portero_velocidad < self.porteria_x + self.porteria_ancho - self.portero_ancho//2:
            self.portero_x += self.portero_velocidad
            self.canvas.move(self.portero, self.portero_velocidad, 0)
            self.canvas.move(self.portero_cabeza, self.portero_velocidad, 0)
    
    def disparar(self, event):
        if not self.puede_disparar or self.disparando:
            return
        
        # Elegir posición aleatoria en la portería
        self.objetivo_x = random.randint(
            self.porteria_x + 30,
            self.porteria_x + self.porteria_ancho - 30
        )
        self.objetivo_y = random.randint(
            self.porteria_y + 30,
            self.porteria_y + self.porteria_alto - 30
        )
        
        self.disparando = True
        self.puede_disparar = False
        self.animar_disparo()
    
    def animar_disparo(self):
        if not self.disparando:
            return
        
        # Calcular dirección
        dx = self.objetivo_x - self.balon_x
        dy = self.objetivo_y - self.balon_y
        distancia = (dx**2 + dy**2)**0.5
        
        if distancia > 20:
            # Mover balón hacia el objetivo
            velocidad = 20
            self.balon_x += (dx / distancia) * velocidad
            self.balon_y += (dy / distancia) * velocidad
            
            # Actualizar posición del balón
            self.canvas.coords(
                self.balon,
                self.balon_x - self.balon_radio,
                self.balon_y - self.balon_radio,
                self.balon_x + self.balon_radio,
                self.balon_y + self.balon_radio
            )
            
            self.ventana.after(30, self.animar_disparo)
        else:
            # El balón llegó al objetivo
            self.verificar_resultado()
    
    def verificar_resultado(self):
        # Verificar si el portero atajó
        portero_izq = self.portero_x - self.portero_ancho//2 - 30
        portero_der = self.portero_x + self.portero_ancho//2 + 30
        portero_arriba = self.portero_y - self.portero_alto//2 - 45
        portero_abajo = self.portero_y + self.portero_alto//2 + 15
        
        if (portero_izq <= self.balon_x <= portero_der and
            portero_arriba <= self.balon_y <= portero_abajo):
            # Atajada
            self.atajadas += 1
            self.mostrar_mensaje("¡ATAJADA!", "#f44336")
        else:
            # Gol
            self.goles += 1
            self.mostrar_mensaje("¡GOOOL!", "#ffeb3b")
        
        self.total_tiros += 1
        self.actualizar_marcador()
        self.ventana.after(1500, self.reiniciar_balon)
    
    def mostrar_mensaje(self, texto, color):
        mensaje = self.canvas.create_text(
            450, 450,
            text=texto,
            font=("Arial Black", 48, "bold"),
            fill=color,
            tags="mensaje"
        )
        self.ventana.after(1500, lambda: self.canvas.delete("mensaje"))
    
    def actualizar_marcador(self):
        self.label_goles.config(text=f"Goles: {self.goles}")
        self.label_atajadas.config(text=f"Atajadas: {self.atajadas}")
    
    def reiniciar_balon(self):
        # Reiniciar posición del balón
        self.balon_x = 450
        self.balon_y = 500
        self.canvas.coords(
            self.balon,
            self.balon_x - self.balon_radio,
            self.balon_y - self.balon_radio,
            self.balon_x + self.balon_radio,
            self.balon_y + self.balon_radio
        )
        self.disparando = False
        self.puede_disparar = True

def abrir_juego():
    JuegoPenales(ventana)

#==============================================================================================================================================================
# BOTON JUGAR
boton_jugar = Tk.Button(
    botones_frame,
    text="Jugar",
    command=abrir_juego,
    bg="black",
    fg="white",
    font=("Arial Black", 18, "bold"),
    bd=8,
    width=12,
    height=2,
    cursor="hand2",
    activebackground="#1565c0",
    relief="flat"
)
boton_jugar.pack(pady=10)
boton_jugar.bind("<Enter>", lambda e: animar_boton(e, boton_jugar, "#1976d2", "#ffeb3b"))
boton_jugar.bind("<Leave>", lambda e: restaurar_boton(e, boton_jugar, "black", "white"))

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

    portada_frame = Tk.Frame(acerca_ventana, bg="#e3f2fd")
    portada_frame.place(relx=0.5, rely=0.5, anchor="center")

    titulo = Tk.Label(
        portada_frame,
        text="FIFA89",
        font=("Arial Black", 36, "bold"),
        bg="#e3f2fd",
        fg="#1565c0",
        justify="center"
    )
    titulo.pack(pady=(0, 20))

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

    volumen_label = Tk.Label(
        config_frame,
        text="Volumen",
        font=("Arial", 14),
        bg="#f9fbe7",
        fg="#263238",
        justify="center"
    )
    volumen_label.pack(pady=(0, 10))

    volumen_var = Tk.DoubleVar(value=50)

    def cambiar_volumen(valor):
        try:
            pygame.mixer.music.set_volume(float(valor) / 100)
        except:
            pass

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
#================================================================================================================================================================
