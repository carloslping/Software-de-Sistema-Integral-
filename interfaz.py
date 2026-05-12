import tkinter as tk
from tkinter import ttk, messagebox
from sistema import *
from datetime import datetime

# ======================================
# SISTEMA PRINCIPAL
# ======================================
sistema = SistemaGestion()
# ======================================
# RELOJ EN TIEMPO REAL
# ======================================
def actualizar_hora():

    hora_actual = datetime.now().strftime(
        "%d/%m/%Y  %I:%M:%S %p"
    )

    label_hora.config(
        text=hora_actual
    )

    ventana.after(
        1000,
        actualizar_hora
    )



# ======================================
# MOSTRAR MODULOS
# ======================================
def mostrar_modulo(nombre):

    modulo_clientes.pack_forget()

    modulo_reservas.pack_forget()

    modulo_reportes.pack_forget()

    frame_eventos.pack_forget()

    # =========================
    # CLIENTES
    # =========================
    if nombre == "clientes":

        modulo_clientes.pack(

            side="left",

            fill="y",

            padx=15
        )

    # =========================
    # RESERVAS
    # =========================
    elif nombre == "reservas":

        modulo_reservas.pack(

            side="left",

            fill="y",

            padx=15
        )

    # =========================
    # REPORTES
    # =========================
    elif nombre == "reportes":

        label_total_clientes.config(

            text=f"Total Clientes: {len(sistema.clientes)}"
        )

        label_total_reservas.config(

            text=f"Total Reservas: {len(tabla_reservas.get_children())}"
        )

        modulo_reportes.pack(

            side="left",

            fill="both",

            expand=True,

            padx=15
        )

    # =========================
    # EVENTOS
    # =========================
    elif nombre == "eventos":

        frame_eventos.pack(

            fill="both",

            expand=True,

            pady=10
        )

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
# MOSTRAR / OCULTAR EVENTOS
# ======================================
def toggle_eventos():

    global eventos_visibles

    if eventos_visibles:

        frame_eventos.pack_forget()

        eventos_visibles = False

    else:

        frame_eventos.pack(

            fill="both",

            expand=True,

            pady=10
        )

        eventos_visibles = True
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
# RELOJ SUPERIOR
# ======================================
label_hora = tk.Label(

    ventana,

    font=("Arial", 11, "bold"),

    bg="#1E1E2E",

    fg="#00FFAA"

)

label_hora.place(
    x=20,
    y=20
)

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
# CONTENEDOR CENTRAL
# ======================================
contenedor = tk.Frame(

    frame,

    bg="#1E1E2E"
)

contenedor.pack(

    side="left",

    fill="both",

    expand=True,

    padx=10,

    pady=10
)

# ======================================
# SIDEBAR
# ======================================
sidebar = tk.Frame(

    frame,

    bg="#111827",

    width=220

)

sidebar.pack(

    side="left",

    fill="y"
)

sidebar.pack_propagate(False)

# ======================================
# LOGO / TITULO
# ======================================
tk.Label(

    sidebar,

    text="SOFTWARE FJ",

    font=("Arial", 18, "bold"),

    bg="#111827",

    fg="white"

).pack(pady=20)

# ======================================
# BOTONES MENU
# ======================================

btn_clientes = tk.Button(

    sidebar,

    text="🧑 Clientes",

    font=("Arial", 11),

    bg="#1F2937",

    fg="white",

    relief="flat",

    width=20,

    pady=10,

    command=lambda: mostrar_modulo("clientes")

)

btn_clientes.pack(pady=5)

btn_reservas = tk.Button(

    sidebar,

    text="📅 Reservas",

    font=("Arial", 11),

    bg="#1F2937",

    fg="white",

    relief="flat",

    width=20,

    pady=10,

    command=lambda: mostrar_modulo("reservas")

)

btn_reservas.pack(pady=5)

btn_reportes = tk.Button(

    sidebar,

    text="📊 Reportes",

    font=("Arial", 11),

    bg="#1F2937",

    fg="white",

    relief="flat",

    width=20,

    pady=10,

    command=lambda: mostrar_modulo("reportes")

)

btn_reportes.pack(pady=5)

btn_eventos = tk.Button(

    sidebar,

    text="⚙ Eventos",

    font=("Arial", 11),

    bg="#1F2937",

    fg="white",

    relief="flat",

    width=20,

    pady=10,

    command=lambda: mostrar_modulo("eventos")

)

btn_eventos.pack(pady=5)

btn_salir = tk.Button(

    sidebar,

    text="🚪 Salir",

    font=("Arial", 11),

    bg="#DC2626",

    fg="white",

    relief="flat",

    width=20,

    pady=10,

    command=ventana.destroy

)

btn_salir.pack(

    side="bottom",

    pady=20
)


# ======================================
# CONTENEDOR MODULOS
# ======================================
# ======================================
# MODULO CLIENTES
# ======================================
modulo_clientes = tk.Frame(

    contenedor,

    bg="#2C2F48",

    padx=10,

    pady=10
)

# ======================================
# MODULO RESERVAS
# ======================================
modulo_reservas = tk.Frame(

    contenedor,

    bg="#2C2F48",

    padx=10,

    pady=10
)

modulo_clientes = tk.Frame(

    contenedor,

    bg="#2C2F48",

    padx=10,

    pady=10
)



# ======================================
# FORMULARIO CLIENTES
# ======================================
tk.Label(

    modulo_clientes,

    text="FORMULARIO CLIENTES",

    font=("Arial", 14, "bold"),

    bg="#2A2A40",

    fg="white"

).pack(pady=10)

# ======================================
# TIPO DOCUMENTO
# ======================================
tk.Label(

    modulo_clientes,

    text="Tipo Documento",

    bg="#2A2A40",

    fg="white"

).pack()

combo_tipo_documento = ttk.Combobox(

    modulo_clientes,

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

    modulo_clientes,

    text="Número Documento",

    bg="#2A2A40",

    fg="white"

).pack()

entry_documento = tk.Entry(
    modulo_clientes,
    width=30
)

entry_documento.pack(pady=5)

# ======================================
# NOMBRE
# ======================================
tk.Label(

    modulo_clientes,

    text="Nombre y Apellido",

    bg="#2A2A40",

    fg="white"

).pack()

entry_nombre = tk.Entry(
    modulo_clientes,
    width=30
)

entry_nombre.pack(pady=5)

# ======================================
# CORREO
# ======================================
tk.Label(

    modulo_clientes,

    text="Correo Electrónico",

    bg="#2A2A40",

    fg="white"

).pack()

entry_correo = tk.Entry(
    modulo_clientes,
    width=30
)

entry_correo.pack(pady=5)

# ======================================
# CELULAR
# ======================================
tk.Label(

    modulo_clientes,

    text="Celular",

    bg="#2A2A40",

    fg="white"

).pack()

entry_celular = tk.Entry(
    modulo_clientes,
    width=30
)

entry_celular.pack(pady=5)


# ======================================
# BOTONES
# ======================================
tk.Button(

    modulo_clientes,

    text="Registrar Cliente",

    width=25,

    bg="#4CAF50",

    fg="white",

    command=registrar_cliente

).pack(pady=5)

tk.Button(

    modulo_clientes,

    text="Editar Cliente",

    width=25,

    bg="#FFC107",

    command=editar_cliente

).pack(pady=5)

tk.Button(

    modulo_clientes,

    text="Eliminar Cliente",

    width=25,

    bg="#F44336",

    fg="white",

    command=eliminar_cliente

).pack(pady=5)

# ======================================
# CONTROL EVENTOS
# ======================================
eventos_visibles = False

# ======================================
# modulo_clientes DERECHO
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
# MODULO RESERVAS
# ======================================
# ======================================
# MODULO REPORTES
# ======================================
modulo_reportes = tk.Frame(

    contenedor,

    bg="#2C2F48",

    padx=10,

    pady=10
)
# ======================================
# TITULO REPORTES
# ======================================
tk.Label(

    modulo_reportes,

    text="REPORTES DEL SISTEMA",

    font=("Arial", 16, "bold"),

    bg="#2C2F48",

    fg="white"

).pack(pady=20)

# ======================================
# REPORTE CLIENTES
# ======================================
label_total_clientes = tk.Label(

    modulo_reportes,

    text="Total Clientes: 0",

    font=("Arial", 12),

    bg="#2C2F48",

    fg="white"

)

label_total_clientes.pack(pady=10)

# ======================================
# REPORTE RESERVAS
# ======================================
label_total_reservas = tk.Label(

    modulo_reportes,

    text="Total Reservas: 0",

    font=("Arial", 12),

    bg="#2C2F48",

    fg="white"

)

label_total_reservas.pack(pady=10)

modulo_reservas = tk.Frame(

    contenedor,

    bg="#2C2F48",

    padx=10,

    pady=10
)
modulo_reservas.pack_forget()

# ======================================
# SERVICIOS
# ======================================
tk.Label(

    modulo_reservas,

    text="Tipo Servicio",

    bg="#2A2A40",

    fg="white"

).pack(pady=10)

combo_servicio = ttk.Combobox(

    modulo_reservas,

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

    modulo_reservas,

    text="Crear Reserva",

    width=25,

    bg="#2196F3",

    fg="white",

    command=crear_reserva

).pack(pady=10)

tk.Button(

    modulo_reservas,

    text="Cancelar Reserva",

    width=25,

    bg="#9C27B0",

    fg="white",

    command=cancelar_reserva

).pack(pady=5)

tk.Button(

    modulo_reservas,

    text="Ver Eventos",

    width=25,

    bg="#607D8B",

    fg="white",

    command=lambda: mostrar_modulo("eventos")

).pack(pady=10)

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
frame_eventos = tk.Frame(

    derecha,

    bg="#1E1E2E"
)
tk.Label(

    derecha,

    text="EVENTOS DEL SISTEMA",

    font=("Arial", 13, "bold"),

    bg="#1E1E2E",

    fg="white"

).pack(in_=frame_eventos)

area_resultados = tk.Text(

    derecha,

    height=8,

    bg="#2A2A40",

    fg="white"

)

area_resultados.pack(

    in_=frame_eventos,

    fill="both",

    expand=True

)

# ======================================
# EJECUTAR SISTEMA
# ======================================
actualizar_hora()

mostrar_modulo("clientes")

ventana.mainloop()