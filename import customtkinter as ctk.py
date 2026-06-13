import customtkinter as ctk
from sympy import symbols, sympify, oo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Variable para que SymPy entienda que la 'x' es una letra matemática y no un número
x = symbols("x")
def aproximar_limite(funcion, h):
    # Si tiende a infinito, evaluamos la función en un número gigante
    if h == oo:
      # .subs() reemplaza la 'x' por el número, y .evalf() lo calcula y entrega el resultado como decimal  
        return funcion.subs(x, 100000).evalf()
    if h == -oo:
        return funcion.subs(x, -100000).evalf()
      # Si es un número normal, nos acercamos un poco por la izquierda y la derecha para promediar
      # Usamos un delta minúsculo para simular el concepto de límite: acercarse sin tocar el punto
    delta = 0.000001
    izquierda = funcion.subs(
        x, float(h) - delta).evalf()
    derecha = funcion.subs(
        x, float(h) + delta).evalf()
    return (izquierda + derecha) / 2
def calcular():
    try:
        # Rescatamos los textos de la app y los pasamos a formato matemático
        funcion_texto = entrada_funcion.get()
        h_texto = entrada_h.get()
        # sympify convierte el texto ingresado (ej: "x**2") en una expresión que SymPy puede operar matemáticamente
        funcion = sympify(funcion_texto)
        h = sympify(h_texto)
        # Llamamos a la función de arriba para calcular el resultado numérico
        resultado = aproximar_limite(
            funcion, h)
        etiqueta_resultado.configure(
            text=f"Límite ≈ {resultado}")
        # Borramos el gráfico viejo para que no se superpongan las líneas
        # winfo_children() busca todos los elementos dibujados en el frame y destroy() los elimina de la memoria
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        # Definimos desde qué número hasta qué número del eje X vamos a dibujar la función
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
                # is_real filtra los resultados, evitando guardar números imaginarios que harían caer el gráfico 2D
                if y.is_real:
                    xs.append(valor)
                    ys.append(float(y))
            except:
                pass #Ignoramos el error si la función se indefine (ej. división por cero)
            valor += 0.1
        # Armamos el gráfico con Matplotlib uniendo los puntos (x, y) calculados
        figura, ax = plt.subplots(
            figsize=(6, 4))
        ax.plot(
            xs, ys)
        # Línea vertical en h
        if h != oo and h != -oo:
           # axvline dibuja una línea punteada (--) indicando el punto exacto donde estamos calculando el límite 
            ax.axvline(
                float(h), linestyle="--")
        ax.set_title(
            "Gráfica de la Función")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        # Activa la cuadrícula de fondo para que se lea mejor la escala como en un cuaderno de matemáticas
        ax.grid(True)
        # FigureCanvasTkAgg es el "puente" que permite incrustar un gráfico de Matplotlib dentro de la interfaz gráfica
        canvas = FigureCanvasTkAgg(
            figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both", expand=True)
    except Exception as e:
        # Si se escribe mal la función, mostramos el error en vez de que la app se caiga
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
# pady=15 da un margen vertical para que los elementos respiren y no queden pegados unos con otros
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
# fill="both" y expand=True obligan a que el cuadro del gráfico se estire si el usuario agranda la ventana
frame_grafico.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20)
# EJECUTAR APP
# mainloop() mantiene el programa vivo en un ciclo infinito, escuchando si el usuario hace clics o escribe 
app.mainloop()