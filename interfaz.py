import tkinter as tk
from tkinter import ttk, messagebox
from sistema import *

# ======================================
# SISTEMA PRINCIPAL
# ======================================
sistema = SistemaGestion()

# ======================================
# FUNCIONES
# ======================================

def actualizar_tabla_clientes():

    for item in tabla_clientes.get_children():
        tabla_clientes.delete(item)

    for i, cliente in enumerate(sistema.clientes):

        tabla_clientes.insert(

            "",

            tk.END,

            iid=i,

            values=(

                cliente.get_tipo_documento(),

                cliente.get_numero_documento(),

                cliente.get_nombre(),

                cliente.get_correo(),

                cliente.get_celular(),
            )
        )

# ======================================
# REGISTRAR CLIENTE
# ======================================
def registrar_cliente():

    try:

        cliente = Cliente(

            combo_tipo_documento.get(),

            entry_documento.get(),

            entry_nombre.get(),

            entry_correo.get(),

            entry_celular.get(),

        )

        sistema.agregar_cliente(cliente)

        actualizar_tabla_clientes()

        mostrar_resultado(
            "Cliente registrado correctamente"
        )

        limpiar_campos()

    except Exception as e:

        mostrar_resultado(str(e))

# ======================================
# SELECCIONAR CLIENTE
# ======================================
def seleccionar_cliente(event):

    try:

        seleccionado = tabla_clientes.selection()[0]

        valores = tabla_clientes.item(
            seleccionado,
            "values"
        )

        combo_tipo_documento.set(valores[0])

        entry_documento.delete(0, tk.END)
        entry_documento.insert(0, valores[1])

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[2])

        entry_correo.delete(0, tk.END)
        entry_correo.insert(0, valores[3])

        entry_celular.delete(0, tk.END)
        entry_celular.insert(0, valores[4])



    except:
        pass

# ======================================
# EDITAR CLIENTE
# ======================================
def editar_cliente():

    try:

        seleccionado = tabla_clientes.selection()[0]

        sistema.editar_cliente(

            int(seleccionado),

            combo_tipo_documento.get(),

            entry_documento.get(),

            entry_nombre.get(),

            entry_correo.get(),

            entry_celular.get(),

        )

        actualizar_tabla_clientes()

        mostrar_resultado(
            "Cliente editado correctamente"
        )

        limpiar_campos()

    except Exception as e:

        mostrar_resultado(str(e))

# ======================================
# ELIMINAR CLIENTE
# ======================================
def eliminar_cliente():

    try:

        seleccionado = tabla_clientes.selection()[0]

        confirmar = messagebox.askyesno(

            "Confirmar",

            "¿Desea eliminar el cliente?"

        )

        if confirmar:

            sistema.eliminar_cliente(
                int(seleccionado)
            )

            actualizar_tabla_clientes()

            mostrar_resultado(
                "Cliente eliminado"
            )

            limpiar_campos()

    except Exception as e:

        mostrar_resultado(str(e))

# ======================================
# CREAR RESERVA
# ======================================
def crear_reserva():

    try:

        if len(sistema.clientes) == 0:

            raise ReservaError(
                "No hay clientes registrados"
            )

        seleccionado = tabla_clientes.selection()[0]

        cliente = sistema.clientes[
            int(seleccionado)
        ]

        tipo = combo_servicio.get()

        # =========================
        # SERVICIO SALA
        # =========================
        if tipo == "Sala":

            servicio = ReservaSala(
                "Sala VIP",
                50000
            )

            costo = servicio.calcular_costo(
                horas=2
            )

        # =========================
        # SERVICIO EQUIPO
        # =========================
        elif tipo == "Equipo":

            servicio = AlquilerEquipo(
                "Laptop",
                50000
            )

            costo = servicio.calcular_costo(
                dias=2
            )

        # =========================
        # SERVICIO ASESORIA
        # =========================
        elif tipo == "Asesoría":

            servicio = Asesoria(
                "IA",
                120000
            )

            costo = servicio.calcular_costo(

                horas=2,

                descuento=0.1
            )

        else:

            raise ServicioError(
                "Seleccione un servicio"
            )

        sistema.agregar_servicio(servicio)

        reserva = Reserva(

            cliente,

            servicio,

            2

        )

        reserva.procesar()

        tabla_reservas.insert(

            "",

            tk.END,

            values=(

                cliente.get_nombre(),

                servicio.nombre,

                reserva.estado,

                formato_cop(costo)

            )
        )

        mostrar_resultado(

            f"Reserva creada exitosamente | "

            f"Valor: {formato_cop(costo)}"

            )

    except Exception as e:

        mostrar_resultado(str(e))

# ======================================
# CANCELAR RESERVA
# ======================================
def cancelar_reserva():

    try:

        seleccionado = tabla_reservas.selection()[0]

        valores = tabla_reservas.item(
            seleccionado,
            "values"
        )

        tabla_reservas.item(

            seleccionado,

            values=(

                valores[0],

                valores[1],

                "Cancelada",

                valores[3]

            )
        )

        mostrar_resultado(
            "Reserva cancelada"
        )

    except Exception as e:

        mostrar_resultado(str(e))


# ======================================
# FORMATO MONEDA COP
# ======================================
def formato_cop(valor):

    return f"$ {valor:,.2f} COP"
# ======================================
# MOSTRAR RESULTADOS
# ======================================
def mostrar_resultado(mensaje):

    area_resultados.config(state="normal")

    area_resultados.insert(

        tk.END,

        f"{mensaje}\n"

    )

    area_resultados.config(state="disabled")

# ======================================
# LIMPIAR CAMPOS
# ======================================
def limpiar_campos():

    combo_tipo_documento.set("")

    entry_documento.delete(0, tk.END)

    entry_nombre.delete(0, tk.END)

    entry_correo.delete(0, tk.END)

    entry_celular.delete(0, tk.END)



# ======================================
# VENTANA PRINCIPAL
# ======================================
ventana = tk.Tk()

ventana.title(
    "Sistema Software FJ"
)

ventana.geometry("1200x700")

ventana.config(bg="#1E1E2E")

# ======================================
# TÍTULO
# ======================================
titulo = tk.Label(

    ventana,

    text="SISTEMA SOFTWARE FJ",

    font=("Arial", 22, "bold"),

    bg="#1E1E2E",

    fg="white"

)

titulo.pack(pady=15)

# ======================================
# FRAME PRINCIPAL
# ======================================
frame = tk.Frame(

    ventana,

    bg="#1E1E2E"

)

frame.pack(

    fill="both",

    expand=True

)

# ======================================
# PANEL IZQUIERDO
# ======================================
panel = tk.Frame(

    frame,

    bg="#2A2A40",

    padx=15,

    pady=15

)

panel.pack(

    side="left",

    fill="y",

    padx=10

)

# ======================================
# FORMULARIO CLIENTES
# ======================================
tk.Label(

    panel,

    text="FORMULARIO CLIENTES",

    font=("Arial", 14, "bold"),

    bg="#2A2A40",

    fg="white"

).pack(pady=10)

# ======================================
# TIPO DOCUMENTO
# ======================================
tk.Label(

    panel,

    text="Tipo Documento",

    bg="#2A2A40",

    fg="white"

).pack()

combo_tipo_documento = ttk.Combobox(

    panel,

    values=[

        "Cédula de Ciudadanía",

        "PPT",

        "Pasaporte",

        "Cédula Extranjería"

    ],

    width=27

)

combo_tipo_documento.pack(pady=5)

# ======================================
# DOCUMENTO
# ======================================
tk.Label(

    panel,

    text="Número Documento",

    bg="#2A2A40",

    fg="white"

).pack()

entry_documento = tk.Entry(
    panel,
    width=30
)

entry_documento.pack(pady=5)

# ======================================
# NOMBRE
# ======================================
tk.Label(

    panel,

    text="Nombre y Apellido",

    bg="#2A2A40",

    fg="white"

).pack()

entry_nombre = tk.Entry(
    panel,
    width=30
)

entry_nombre.pack(pady=5)

# ======================================
# CORREO
# ======================================
tk.Label(

    panel,

    text="Correo Electrónico",

    bg="#2A2A40",

    fg="white"

).pack()

entry_correo = tk.Entry(
    panel,
    width=30
)

entry_correo.pack(pady=5)

# ======================================
# CELULAR
# ======================================
tk.Label(

    panel,

    text="Celular",

    bg="#2A2A40",

    fg="white"

).pack()

entry_celular = tk.Entry(
    panel,
    width=30
)

entry_celular.pack(pady=5)


# ======================================
# BOTONES
# ======================================
tk.Button(

    panel,

    text="Registrar Cliente",

    width=25,

    bg="#4CAF50",

    fg="white",

    command=registrar_cliente

).pack(pady=5)

tk.Button(

    panel,

    text="Editar Cliente",

    width=25,

    bg="#FFC107",

    command=editar_cliente

).pack(pady=5)

tk.Button(

    panel,

    text="Eliminar Cliente",

    width=25,

    bg="#F44336",

    fg="white",

    command=eliminar_cliente

).pack(pady=5)

# ======================================
# SERVICIOS
# ======================================
tk.Label(

    panel,

    text="Tipo Servicio",

    bg="#2A2A40",

    fg="white"

).pack(pady=10)

combo_servicio = ttk.Combobox(

    panel,

    values=[

        "Sala",

        "Equipo",

        "Asesoría"

    ],

    width=27

)

combo_servicio.pack()

# ======================================
# BOTONES RESERVA
# ======================================
tk.Button(

    panel,

    text="Crear Reserva",

    width=25,

    bg="#2196F3",

    fg="white",

    command=crear_reserva

).pack(pady=10)

tk.Button(

    panel,

    text="Cancelar Reserva",

    width=25,

    bg="#9C27B0",

    fg="white",

    command=cancelar_reserva

).pack(pady=5)

# ======================================
# PANEL DERECHO
# ======================================
derecha = tk.Frame(

    frame,

    bg="#1E1E2E"

)

derecha.pack(

    side="right",

    fill="both",

    expand=True,

    padx=10

)

# ======================================
# TABLA CLIENTES
# ======================================
tk.Label(

    derecha,

    text="CLIENTES",

    font=("Arial", 13, "bold"),

    bg="#1E1E2E",

    fg="white"

).pack()

tabla_clientes = ttk.Treeview(

    derecha,

    columns=(

        "Tipo Doc",

        "Documento",

        "Nombre",

        "Correo",

        "Celular",


    ),

    show="headings",

    height=7

)

tabla_clientes.heading(
    "Tipo Doc",
    text="Tipo Doc"
)

tabla_clientes.heading(
    "Documento",
    text="Documento"
)

tabla_clientes.heading(
    "Nombre",
    text="Nombre"
)

tabla_clientes.heading(
    "Correo",
    text="Correo"
)

tabla_clientes.heading(
    "Celular",
    text="Celular"
)


tabla_clientes.pack(
    fill="x",
    pady=10
)

tabla_clientes.bind(
    "<<TreeviewSelect>>",
    seleccionar_cliente
)

# ======================================
# TABLA RESERVAS
# ======================================
tk.Label(

    derecha,

    text="RESERVAS",

    font=("Arial", 13, "bold"),

    bg="#1E1E2E",

    fg="white"

).pack()

tabla_reservas = ttk.Treeview(

    derecha,

    columns=(

        "Cliente",

        "Servicio",

        "Estado",

        "Costo"

    ),

    show="headings",

    height=8

)

tabla_reservas.heading(
    "Cliente",
    text="Cliente"
)

tabla_reservas.heading(
    "Servicio",
    text="Servicio"
)

tabla_reservas.heading(
    "Estado",
    text="Estado"
)

tabla_reservas.heading(
    "Costo",
    text="Costo"
)

tabla_reservas.pack(
    fill="x",
    pady=10
)

# ======================================
# EVENTOS DEL SISTEMA
# ======================================
tk.Label(

    derecha,

    text="EVENTOS DEL SISTEMA",

    font=("Arial", 13, "bold"),

    bg="#1E1E2E",

    fg="white"

).pack()

area_resultados = tk.Text(

    derecha,

    height=8,

    bg="#2A2A40",

    fg="white"

)

area_resultados.pack(

    fill="both",

    expand=True

)

# ======================================
# EJECUTAR SISTEMA
# ======================================
ventana.mainloop()