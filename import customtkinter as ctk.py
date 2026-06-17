import customtkinter as ctk
from sympy import symbols, sympify, oo, sin, cos, tan, sqrt, pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# Variable matemática
x = symbols("x")

# Corrige expresiones comunes
def limpiar_expresion(texto):

    texto = texto.lower()
    texto = texto.replace("sen", "sin")
    texto = texto.replace("^", "**")
    texto = texto.replace("∞", "oo")
    texto = texto.replace("infinito", "oo")

    for f in ("sin", "cos", "tan"):
        texto = texto.replace(f"{f}x", f"{f}(x)")
        texto = re.sub(fr"{f}(\d+)x", fr"{f}(\1*x)", texto)

    return texto

# Aproximación numérica del límite
def aproximar_limite(funcion, h):

    try:

        # Límite cuando x tiende a +∞
        if h == oo:

            a = funcion.subs(x, 100000).evalf()
            b = funcion.subs(x, 1000000).evalf()

            if abs(float(a - b)) < 0.01:
                return a, b, b, True

            return a, b, None, False

        # Límite cuando x tiende a -∞
        if h == -oo:

            a = funcion.subs(x, -100000).evalf()
            b = funcion.subs(x, -1000000).evalf()

            if abs(float(a - b)) < 0.01:
                return a, b, b, True

            return a, b, None, False

        # Límites normales
        for delta in [1e-2, 1e-4, 1e-6]:

            izquierda = funcion.subs(
                x,
                float(h) - delta
            ).evalf()

            derecha = funcion.subs(
                x,
                float(h) + delta
            ).evalf()

            if abs(float(izquierda - derecha)) < 0.001:

                return (
                    izquierda,
                    derecha,
                    (izquierda + derecha) / 2,
                    True
                )

        return izquierda, derecha, None, False

    except:

        return None, None, None, False

# Función principal
def calcular():

    try:

        texto = limpiar_expresion(
            entrada_funcion.get()
        )

        funcion = sympify(
            texto,
            locals={
                "x": x,
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "sqrt": sqrt,
                "pi": pi,
                "oo": oo,
            }
        )

        h = sympify(
            entrada_h.get()
        )

        izq, der, resultado, existe = aproximar_limite(
            funcion,
            h
        )

        if existe:

            procedimiento = (
                f"Límite izquierdo: {izq}\n"
                f"Límite derecho: {der}\n\n"
                "Ambos coinciden.\n"
                "El límite existe."
            )

        else:

            resultado = "No existe"

            procedimiento = (
                f"Límite izquierdo: {izq}\n"
                f"Límite derecho: {der}\n\n"
                "Los límites laterales son distintos o "
                "no pudieron aproximarse."
            )

        etiqueta_resultado.configure(
            text=f"Resultado: {resultado}"
        )

        caja_procedimiento.delete(
            "1.0",
            "end"
        )

        caja_procedimiento.insert(
            "1.0",
            procedimiento
        )

        # Eliminar gráfico anterior
        for widget in frame_grafico.winfo_children():
            widget.destroy()

        # Intervalo de dibujo
        if h == oo:

            inicio, fin = 1, 50

        elif h == -oo:

            inicio, fin = -50, -1

        else:

            inicio = float(h) - 5
            fin = float(h) + 5

        xs = []
        ys = []
        valor = inicio

        while valor <= fin:

            try:

                y = funcion.subs(
                    x,
                    valor
                ).evalf()

                if y.is_real and abs(float(y)) < 1000:

                    xs.append(valor)
                    ys.append(float(y))

            except:
                pass

            valor += 0.1

        figura, ax = plt.subplots(
            figsize=(6, 4)
        )

        ax.plot(xs, ys)

        if h not in (oo, -oo):

            ax.axvline(
                float(h),
                linestyle="--"
            )

        ax.set_title(
            "Gráfica de la Función"
        )

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(
            figura,
            master=frame_grafico
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    except Exception as e:

        etiqueta_resultado.configure(
            text=f"Error: {e}"
        )

# CONFIGURACIÓN DE LA APP

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title(
    "Analizador y Visualizador de Límites"
)

app.geometry("900x750")

# Título
ctk.CTkLabel(
    app,
    text="Analizador y Visualizador de Límites",
    font=("Arial", 22, "bold")
).pack(pady=15)

# Entrada función
entrada_funcion = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Ej: (x**2-1)/(x-1)"
)

entrada_funcion.pack(pady=10)

# Entrada h
entrada_h = ctk.CTkEntry(
    app,
    width=250,
    placeholder_text="Ingrese h (1, 2, oo, -oo)"
)

entrada_h.pack(pady=10)

# Botón
ctk.CTkButton(
    app,
    text="Calcular",
    command=calcular
).pack(pady=10)

# Resultado
etiqueta_resultado = ctk.CTkLabel(
    app,
    text="Resultado del límite"
)

etiqueta_resultado.pack(pady=10)

# Procedimiento
ctk.CTkLabel(
    app,
    text="Procedimiento"
).pack()

caja_procedimiento = ctk.CTkTextbox(
    app,
    height=120
)

caja_procedimiento.pack(
    fill="x",
    padx=20,
    pady=10
)

# Área gráfica
frame_grafico = ctk.CTkFrame(app)

frame_grafico.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# Ejecutar
app.mainloop()