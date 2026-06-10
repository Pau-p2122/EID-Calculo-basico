import customtkinter as ctk
from sympy import symbols, sympify, oo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Variable simbólica
x = symbols("x")
def aproximar_limite(funcion, h):
    # Límites al infinito
    if h == oo:
        return funcion.subs(x, 100000).evalf()
    if h == -oo:
        return funcion.subs(x, -100000).evalf()
    # Aproximación por ambos lados
    delta = 0.000001
    izquierda = funcion.subs(
        x, float(h) - delta).evalf()
    derecha = funcion.subs(
        x, float(h) + delta).evalf()
    return (izquierda + derecha) / 2
def calcular():
    try:
        # Obtener datos ingresados
        funcion_texto = entrada_funcion.get()
        h_texto = entrada_h.get()
        funcion = sympify(funcion_texto)
        h = sympify(h_texto)
        # Calcular límite mediante aproximación
        resultado = aproximar_limite(
            funcion, h)
        etiqueta_resultado.configure(
            text=f"Límite ≈ {resultado}")
        # Limpiar gráfico anterior
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        # Rango de la gráfica
        if h == oo or h == -oo:
            if h == oo:
                inicio = 1
                fin = 50
            else:
                inicio = -50
                fin = -1
        else:
            inicio = float(h) - 5
            fin = float(h) + 5
        xs = []
        ys = []
        valor = inicio
        while valor <= fin:
            try:
                y = funcion.subs(
                    x, valor).evalf()
                if y.is_real:
                    xs.append(valor)
                    ys.append(float(y))
            except:
                pass
            valor += 0.1
        # Crear gráfico
        figura, ax = plt.subplots(
            figsize=(6, 4))
        ax.plot(
            xs, ys)
        # Línea vertical en h
        if h != oo and h != -oo:
            ax.axvline(
                float(h), linestyle="--")
        ax.set_title(
            "Gráfica de la Función")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        canvas = FigureCanvasTkAgg(
            figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True)
    except Exception as e:
        etiqueta_resultado.configure(
            text=f"Error: {e}")
# CONFIGURACIÓN DE LA APP
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title(
    "Analizador y Visualizador de Límites")
app.geometry(
    "850x650")
# TÍTULO
titulo = ctk.CTkLabel(
    app, text="Analizador y Visualizador de Límites", font=("Arial", 22, "bold"))
titulo.pack(
    pady=15)
# ENTRADA FUNCIÓN
entrada_funcion = ctk.CTkEntry(
    app, width=450, placeholder_text="Ejemplo: (x**2-1)/(x-1)")
entrada_funcion.pack(
    pady=10)
# ENTRADA h
entrada_h = ctk.CTkEntry(
    app, width=200, placeholder_text="Ingrese h (1, 2, oo, -oo)")
entrada_h.pack(
    pady=10)
# BOTÓN
boton = ctk.CTkButton(
    app, text="Calcular", command=calcular)
boton.pack(
    pady=10)
# RESULTADO
etiqueta_resultado = ctk.CTkLabel(
    app, text="Resultado del límite")
etiqueta_resultado.pack(
    pady=10)
# ÁREA DE GRÁFICA
frame_grafico = ctk.CTkFrame(app)
frame_grafico.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20)
# EJECUTAR APP
app.mainloop()