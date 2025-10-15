#==============================================================================================================================================================
# Estructura del proyecto FIFA89 - Juego de Penales con Paletas
#==============================================================================================================================================================

import tkinter as Tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import pygame

#==============================================================================================================================================================
# Variables globales del juego
ancho = 800
alto = 600

#==============================================================================================================================================================
# Configuracion del sonido de fondo del juego
pygame.mixer.init()
try:
    pygame.mixer.music.load("Candy.mp3")
    pygame.mixer.music.play(-1)
except:
    pass

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
try:
    ventana.iconbitmap("icono.ico")
except:
    pass
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
# JUEGO DE PENALES CON PALETAS
#==============================================================================================================================================================

class JuegoPenales:
    def __init__(self, ventana_padre):
        self.ventana = Tk.Toplevel(ventana_padre)
        self.ventana.title("FIFA89 - Penales con Paletas")
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
        self.porteria_x = 200
        self.porteria_y = 100
        self.porteria_ancho = 500
        self.porteria_alto = 250
        
        # Sistema de paletas (6 paletas) - DEFINIR ANTES DE DIBUJAR
        self.paletas = []
        self.paletas_labels = []
        self.paletas_estado = []  # True = arriba (no deja pasar), False = abajo (deja pasar)
        self.ancho_paleta = self.porteria_ancho // 6
        self.alto_paleta = 80
        
        # Ahora sí dibujar la portería
        self.dibujar_porteria()
        
        # Crear las 6 paletas
        for i in range(6):
            x_inicio = self.porteria_x + (i * self.ancho_paleta)
            y_centro = self.porteria_y + self.porteria_alto // 2
            
            # Estado inicial aleatorio
            estado = random.choice([True, False])
            self.paletas_estado.append(estado)
            
            y_pos = y_centro - self.alto_paleta // 2 if estado else y_centro + 40
            
            # Crear paleta
            paleta = self.canvas.create_rectangle(
                x_inicio + 5,
                y_pos,
                x_inicio + self.ancho_paleta - 5,
                y_pos + self.alto_paleta,
                fill="#ff6f00",
                outline="#e65100",
                width=3
            )
            self.paletas.append(paleta)
            
            # Número de la paleta
            label = self.canvas.create_text(
                x_inicio + self.ancho_paleta // 2,
                y_pos + self.alto_paleta // 2,
                text=str(i + 1),
                font=("Arial Black", 24, "bold"),
                fill="white"
            )
            self.paletas_labels.append(label)
        
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
        self.zona_disparo = 0  # Zona 1-6 donde se dispara
        
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
            text="Teclas 1-6: Elegir zona | ESPACIO: Disparar",
            font=("Arial", 12),
            bg="#1b5e20",
            fg="white"
        )
        self.label_instrucciones.pack(side="right", padx=10)
        
        # Indicador de zona seleccionada
        self.zona_seleccionada = 0
        self.indicador_zona = None
        
        # Controles
        for i in range(1, 7):
            self.ventana.bind(str(i), lambda e, zona=i: self.seleccionar_zona(zona))
        self.ventana.bind("<space>", self.disparar)
        
        # Iniciar animación de paletas
        self.animar_paletas()
    
    def dibujar_campo(self):
        # Líneas del campo
        self.canvas.create_line(0, 400, 900, 400, fill="white", width=3)
        
        # Área de penal
        self.canvas.create_rectangle(150, 80, 750, 370, outline="white", width=3)
        
        # Punto de penal
        self.canvas.create_oval(440, 490, 460, 510, fill="white", outline="white")
        
    def dibujar_porteria(self):
        # Marco de la portería
        # Poste izquierdo
        self.canvas.create_rectangle(
            self.porteria_x - 10,
            self.porteria_y,
            self.porteria_x,
            self.porteria_y + self.porteria_alto,
            fill="#e0e0e0", outline="#757575", width=3
        )
        # Poste derecho
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
        
        # Divisiones de zonas (líneas verticales para separar las 6 zonas)
        for i in range(1, 6):
            x = self.porteria_x + (i * self.ancho_paleta)
            self.canvas.create_line(
                x, self.porteria_y,
                x, self.porteria_y + self.porteria_alto,
                fill="#9e9e9e", width=2, dash=(5, 5)
            )
    
    def seleccionar_zona(self, zona):
        if not self.puede_disparar or self.disparando:
            return
        
        self.zona_seleccionada = zona
        
        # Borrar indicador anterior
        if self.indicador_zona:
            self.canvas.delete(self.indicador_zona)
        
        # Crear nuevo indicador
        x_zona = self.porteria_x + ((zona - 1) * self.ancho_paleta)
        self.indicador_zona = self.canvas.create_rectangle(
            x_zona + 2,
            self.porteria_y + 2,
            x_zona + self.ancho_paleta - 2,
            self.porteria_y + self.porteria_alto - 2,
            outline="#ffeb3b",
            width=4,
            dash=(10, 5)
        )
    
    def animar_paletas(self):
        # Mover paletas aleatoriamente
        for i in range(6):
            # Cada cierto tiempo, cambiar estado de manera aleatoria
            if random.random() < 0.05:  # 5% de probabilidad en cada frame
                self.paletas_estado[i] = not self.paletas_estado[i]
                self.actualizar_posicion_paleta(i)
        
        # Continuar animación
        self.ventana.after(100, self.animar_paletas)
    
    def actualizar_posicion_paleta(self, indice):
        x_inicio = self.porteria_x + (indice * self.ancho_paleta)
        y_centro = self.porteria_y + self.porteria_alto // 2
        
        if self.paletas_estado[indice]:  # Arriba (bloqueando)
            y_pos = y_centro - self.alto_paleta // 2
        else:  # Abajo (dejando pasar)
            y_pos = y_centro + 40
        
        # Actualizar paleta
        self.canvas.coords(
            self.paletas[indice],
            x_inicio + 5,
            y_pos,
            x_inicio + self.ancho_paleta - 5,
            y_pos + self.alto_paleta
        )
        
        # Actualizar número
        self.canvas.coords(
            self.paletas_labels[indice],
            x_inicio + self.ancho_paleta // 2,
            y_pos + self.alto_paleta // 2
        )
    
    def disparar(self, event):
        if not self.puede_disparar or self.disparando or self.zona_seleccionada == 0:
            return
        
        # Borrar indicador
        if self.indicador_zona:
            self.canvas.delete(self.indicador_zona)
            self.indicador_zona = None
        
        # Calcular objetivo según la zona seleccionada
        zona_index = self.zona_seleccionada - 1
        x_zona = self.porteria_x + (zona_index * self.ancho_paleta)
        
        self.objetivo_x = x_zona + self.ancho_paleta // 2 + random.randint(-20, 20)
        self.objetivo_y = self.porteria_y + self.porteria_alto // 2 + random.randint(-30, 30)
        self.zona_disparo = self.zona_seleccionada
        
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
        # Verificar si la paleta de esa zona está bloqueando o dejando pasar
        zona_index = self.zona_disparo - 1
        
        if self.paletas_estado[zona_index]:  # Paleta arriba = bloquea
            # Atajada
            self.atajadas += 1
            self.mostrar_mensaje(f"¡ATAJADA EN ZONA {self.zona_disparo}!", "#f44336")
        else:  # Paleta abajo = deja pasar
            # Gol
            self.goles += 1
            self.mostrar_mensaje(f"¡GOOOL EN ZONA {self.zona_disparo}!", "#ffeb3b")
        
        self.total_tiros += 1
        self.actualizar_marcador()
        self.zona_seleccionada = 0
        self.ventana.after(1500, self.reiniciar_balon)
    
    def mostrar_mensaje(self, texto, color):
        mensaje = self.canvas.create_text(
            450, 450,
            text=texto,
            font=("Arial Black", 36, "bold"),
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
        "Jose Sandi Arrieta\n"
        "Proyecto: Futbolín con Paletas\n"
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