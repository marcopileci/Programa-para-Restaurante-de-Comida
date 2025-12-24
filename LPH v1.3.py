import time
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
from tkinter import messagebox

ventana= tk.Tk()
ventana.title("Los Pollos Hermanos")
ventana.geometry("600x700")
ventana.resizable(0,0)
#**** PAD ****#
PAD_Y= 15
PAD_X=10
PAD_ALL=10

#####################################
#          Funciones                #
#####################################

def restablecer_valores():
    global cantidad_combo_1, cantidad_combo_2, cantidad_combo_3, canditad_postre, canditad_precio_final, cantidad_vuelto
    cantidad_combo_1 = 0
    cantidad_combo_2 = 0
    cantidad_combo_3 = 0
    canditad_postre = 0
    canditad_precio_final = 0
    cantidad_vuelto = 0

    label_combo1.config(text=cantidad_combo_1)
    label_combo2.config(text=cantidad_combo_2)
    label_combo3.config(text=cantidad_combo_3)
    label_combo_postre.config(text=canditad_postre)
    label_precio_final.config(text=f"${canditad_precio_final}")
    label_vuelto.config(text=f"${cantidad_vuelto}", fg="black") 
    textbox_cliente.delete(0, tk.END)
    textbox_paga.delete(0, tk.END)

def registrar_nombre():
    global empleado_ingresado, etiqueta_sesion 
    nombre = textbox_empleado.get()
    if nombre.strip() == "":
        messagebox.showerror("Error", "El nombre del empleado no puede estar vacío.")
        return
    elif nombre.isdigit():
        messagebox.showerror("Error", "Introduzca un nombre valido para el empleado.")
        return
    empleado_ingresado = True
    messagebox.showinfo("Éxito", f"Bienvenido {nombre}")
    encargado_Actual= textbox_empleado.get()
    conn=  sqlite3.connect("registro.sqlite")
    cursor = conn.cursor()
    hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    registro= (encargado_Actual, hora, "IN", "0.0")
    cursor.execute("CREATE TABLE IF NOT EXISTS Registro (Encargado TEXT, Fecha TEXT, Evento TEXT, Caja REAL)"    
    )
    cursor.execute("INSERT INTO Registro VALUES (?,?,?,?)", registro)
    conn.commit()
    conn.close()
    #Si ya existe la etiqueta, la destruira.
    #try:
    #    etiqueta_sesion.destroy()
    #except NameError:
    #    pass
    
    etiqueta_sesion = tk.Label(
        frame_botones,
        text=f"SESION INICIADA COMO: {textbox_empleado.get()}",
        anchor="center",
        width=45,
        wraplength=400
    )
    etiqueta_sesion.grid(row=1, column=0, columnspan= 3, padx=PAD_X, pady=15, sticky="s")
def registrar_salida():
    global empleado_ingresado
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    global ventas_totales_encargado_actual
    encargado_Actual= textbox_empleado.get()
    conn=  sqlite3.connect("registro.sqlite")
    cursor = conn.cursor()
    hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    registro= (encargado_Actual, hora, "OUT", ventas_totales_encargado_actual)
    cursor.execute("INSERT INTO Registro VALUES (?,?,?,?)", registro)
    ventas_totales_encargado_actual= 0
    conn.commit()
    conn.close()
    restablecer_valores()
    empleado_ingresado= False
    messagebox.showinfo("Salir","Sesion cerrada con exito.")
    textbox_empleado.delete(0, tk.END)
    etiqueta_sesion.destroy()

def ventas():
    global cliente_ingresado
    nombre_cliente= textbox_cliente.get()
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    if canditad_precio_final == 0:
        messagebox.showerror("Error", "No se puede procesar una venta vacia.")
        return
    elif nombre_cliente.strip() == "":
        messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
        return
    elif nombre_cliente.isdigit():
        messagebox.showerror("Error", "Introduzca un nombre valido para el cliente.")
        return
    
    cliente_ingresado= True
    global ventas_totales_encargado_actual
    conn= sqlite3.connect("ventas.sqlite")
    cursor = conn.cursor()
    ventas_totales_encargado_actual= ventas_totales_encargado_actual + canditad_precio_final
    hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    ventas_cliente= (textbox_cliente.get(), hora , cantidad_combo_1, cantidad_combo_2, cantidad_combo_3, canditad_postre, canditad_precio_final)
    cursor.execute("CREATE TABLE IF NOT EXISTS Ventas (Cliente TEXT, Fecha TEXT, [Combo 1] INTEGER, [Combo 2] INTEGER, [Combo 3] INTEGER, Postre INTEGER, Total INTEGER)"    
    )
    cursor.execute("INSERT INTO Ventas VALUES (?,?,?,?,?,?,?)", ventas_cliente)
    conn.commit()
    conn.close()
    messagebox.showinfo("Venta", "¡Venta registrada con exito!")
    restablecer_valores()
    cliente_ingresado= False
    return ventas_totales_encargado_actual

def cancelar_pedido():
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    restablecer_valores()
    messagebox.showinfo("Venta", "Venta cancelada.")

###################################
#    Variables los pedidos        #
###################################
cantidad_combo_1 = 0
cantidad_combo_2=0
cantidad_combo_3=0
canditad_postre=0
canditad_precio_final=0
cantidad_vuelto=0
empleado_ingresado = False
ventas_totales_encargado_actual= 0
#******** Precio de combos ********#

PrecioCombo1 = 7
PrecioCombo2 = 3
PrecioCombo3 = 5
PrecioPostre = 4
###################################################
#     Funciones pertenecientes a los botones      #
###################################################
def sumar():
    global cantidad_combo_1
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    cantidad_combo_1 += 1
    label_combo1.config(text=cantidad_combo_1)
    actualizar()

def restar():
    global cantidad_combo_1
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    if cantidad_combo_1 > 0:
        cantidad_combo_1 -= 1
    label_combo1.config(text=cantidad_combo_1)
    actualizar()
    
def sumar2():
    global cantidad_combo_2
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    cantidad_combo_2 = cantidad_combo_2 + 1
    label_combo2.config(text=cantidad_combo_2) 
    actualizar()
    
def restar2():
    global cantidad_combo_2
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    if cantidad_combo_2 > 0:
        cantidad_combo_2 -= 1
    label_combo2.config(text=cantidad_combo_2)
    actualizar()

def sumar3():
    global cantidad_combo_3
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    cantidad_combo_3 = cantidad_combo_3 + 1
    label_combo3.config(text=cantidad_combo_3) 
    actualizar()

def restar3():
    global cantidad_combo_3
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    if cantidad_combo_3 > 0:
        cantidad_combo_3 -= 1
    label_combo3.config(text=cantidad_combo_3)
    actualizar()

def sumar4():
    global canditad_postre
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    canditad_postre = canditad_postre + 1
    label_combo_postre.config(text=canditad_postre) 
    actualizar()
    
def restar4():
    global canditad_postre
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    if canditad_postre > 0:
        canditad_postre -= 1
    label_combo_postre.config(text=canditad_postre)
    actualizar()

def actualizar():
    global canditad_precio_final
    Total_Combo1= PrecioCombo1 * cantidad_combo_1
    Total_Combo2= PrecioCombo2 * cantidad_combo_2
    Total_Combo3= PrecioCombo3 * cantidad_combo_3
    Total_Postre= PrecioPostre * canditad_postre
    canditad_precio_final= Total_Combo1 + Total_Combo2 + Total_Combo3 + Total_Postre
    label_precio_final.config(text=f"${canditad_precio_final}")
    return canditad_precio_final

def mostrar_vuelto():
    if not empleado_ingresado:
        messagebox.showerror("Error", "Debes ingresar el nombre del empleado primero.")
        return
    global cantidad_vuelto
    global canditad_precio_final
    vuelto= textbox_paga.get()
    try:
        vuelto= int(vuelto)
    except ValueError:
        return
    vuelto= int(vuelto)
    canditad_precio_final= int(canditad_precio_final)
    cantidad_vuelto= vuelto - canditad_precio_final

    if cantidad_vuelto < 0:
        label_vuelto.config(text="Dinero insuficiente", fg="red")
    else:
        label_vuelto.config(text=f"${cantidad_vuelto}", fg= "green")
#####################################
#####################################

logo = Image.open("images\logo.png")
logo_tk = ImageTk.PhotoImage(logo)
labelImagen = tk.Label(ventana, image=logo_tk)
labelImagen.grid(row=0, column=0, columnspan=2, sticky="n")
###################################
#      Frame de la izquierda      #
###################################

frame_izquierdo= tk.Frame(ventana)
frame_izquierdo.grid(row=1, column=0, padx=10, sticky="n")
## ## ## ## ## ## ## ## ## ## ## ## 

etiqueta_encargado= tk.Label(frame_izquierdo, text="Nombre del encargado actual:")
etiqueta_encargado.grid(row=0, column=0, padx=PAD_X, pady=15, sticky="w")

etiqueta_combo1= tk.Label(frame_izquierdo, text="Combo 1", )
etiqueta_combo1.grid(row=1, column=0, padx=PAD_X, pady=15, sticky="w")

etiqueta_combo2= tk.Label(frame_izquierdo, text="Combo 2", )
etiqueta_combo2.grid(row=2, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_combo3= tk.Label(frame_izquierdo, text="Combo 3", )
etiqueta_combo3.grid(row=3, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_combo_postre= tk.Label(frame_izquierdo, text="Postre", )
etiqueta_combo_postre.grid(row=4, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_precio_final= tk.Label(frame_izquierdo, text="Precio Final a pagar", )
etiqueta_precio_final.grid(row=5, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_nombre_cliente= tk.Label(frame_izquierdo, text="Nombre del cliente", )
etiqueta_nombre_cliente.grid(row=6, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_cliente_paga= tk.Label(frame_izquierdo, text="El cliente paga con:", )
etiqueta_cliente_paga.grid(row=7, column=0, padx=PAD_X, pady=17.4, sticky="w")

etiqueta_vuelto= tk.Label(frame_izquierdo, text="Su vuelto es:")
etiqueta_vuelto.grid(row=8, column=0, padx=PAD_X, pady=17.4, sticky="w")
#####################################
#####################################

###################################
#      Frame de la derecha        #
###################################
frame_derecho = tk.Frame(ventana)
frame_derecho.grid(row=1, column=1, padx=10,sticky="n")
#**************************************************# 

# Empleado 
textbox_empleado = tk.Entry(frame_derecho)
textbox_empleado.grid(row=0, column=0, padx=PAD_X, pady=15)
                    #Fila ↑#Columna ↑
boton_ingresar= tk.Button(frame_derecho, text="Ingresar", bg="#feb81c", fg="black", command=registrar_nombre)
boton_ingresar.grid(row=0, column=2, pady=10)


# Combo 1 con botones
label_combo1 = tk.Label(frame_derecho, text=cantidad_combo_1, padx=PAD_X)
label_combo1.grid(row=1, column=0, padx=PAD_X, pady=15)
boton_sumar1 = tk.Button(frame_derecho, text="↑", bg="#feb81c", fg="black", command=sumar)
boton_sumar1.grid(row=1, column=1, pady=15)
boton_restar1 = tk.Button(frame_derecho, text="↓", bg="#feb81c", fg="black", command=restar)
boton_restar1.grid(row=1, column=2, pady=15)
                # Fila ↑ #Columna ↑

# Combo 2 con botones
label_combo2 = tk.Label(frame_derecho,text=cantidad_combo_2,)
label_combo2.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y)
boton_sumar2 = tk.Button(frame_derecho, text="↑", bg="#feb81c", fg="black",  command=sumar2)
boton_sumar2.grid(row=2, column=1, pady=PAD_Y)
boton_restar2 = tk.Button(frame_derecho, text="↓", bg="#feb81c", fg="black", command=restar2)
boton_restar2.grid(row=2, column=2, pady=PAD_Y)

# Combo 3 con botones
label_combo3 = tk.Label(frame_derecho, text=cantidad_combo_3,)
label_combo3.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y)
boton_sumar3 = tk.Button(frame_derecho, text="↑", bg="#feb81c", fg="black", command=sumar3)
boton_sumar3.grid(row=3, column=1, pady=PAD_Y)
boton_restar3 = tk.Button(frame_derecho, text="↓", bg="#feb81c", fg="black", command=restar3)
boton_restar3.grid(row=3, column=2, pady=PAD_Y)

# Postre con botones
label_combo_postre = tk.Label(frame_derecho, text= canditad_postre)
label_combo_postre.grid(row=4, column=0, padx=PAD_X, pady=PAD_Y)
boton_sumar4 = tk.Button(frame_derecho, text="↑", bg="#feb81c", fg="black", command=sumar4)
boton_sumar4.grid(row=4, column=1, pady=PAD_Y)
boton_restar4 = tk.Button(frame_derecho, text="↓", bg="#feb81c", fg="black", command=restar4)
boton_restar4.grid(row=4, column=2, pady=PAD_Y)

# Numero Precio Final
label_precio_final = tk.Label(frame_derecho, text=f"${canditad_precio_final}", )
label_precio_final.grid(row=5, column=0, padx=PAD_X, pady=PAD_Y)

# Cliente
textbox_cliente = tk.Entry(frame_derecho)
textbox_cliente.grid(row=6, column=0, padx=PAD_X, pady=PAD_Y)


# El cliente paga:
textbox_paga = tk.Entry(frame_derecho)
textbox_paga.grid(row=7, column=0, padx=PAD_X, pady=PAD_Y)

boton_actualizar_vuelto = tk.Button(frame_derecho, text="Calcular Vuelto", bg="#feb81c", fg="black", command=mostrar_vuelto)
boton_actualizar_vuelto.grid(row=7, column=2, pady=PAD_Y)

# Vuelto
label_vuelto = tk.Label(frame_derecho, text=f"${canditad_precio_final}", )
label_vuelto.grid(row=8, column=0, padx=PAD_X, pady=PAD_Y)


###################################
#     Frame Botones del final     #
###################################
frame_botones= tk.Frame(ventana)
frame_botones.grid (row=3,column=0, columnspan=2, pady=PAD_Y, sticky="s")

##Botones del frame ###
boton_hacer_pedido= tk.Button(frame_botones, text="Hacer pedido", command=ventas)
boton_hacer_pedido.grid(row=0, column= 0, padx= PAD_X, sticky="sw")

boton_cancelar_pedido= tk.Button(frame_botones, text="Cancelar pedido", command= cancelar_pedido)
boton_cancelar_pedido.grid(row= 0,column=1, padx= PAD_X, sticky="s")

boton_salir= tk.Button(frame_botones, text="Salir seguro", command= registrar_salida)
boton_salir.grid(row=0, column=2, padx=PAD_X, sticky="se")

#-------------------------------------------------------------------------------------------

##Mantener ventana abierta
ventana.mainloop()