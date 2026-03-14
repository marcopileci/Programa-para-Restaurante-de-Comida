import time
def verificar_nombre(nombre):
    while True:
        if nombre.isalpha():
            nombre= str(nombre)
            return nombre
            break
        else:
            print("Por favor, ingrese un nombre de manera valida.")
            nombre= input("Ingresa el nombre: ")

def verificar_numero(numero):
    while True:
            if numero.isdigit(): 
                return int(numero)
                break
            else:
                print("Por favor, ingrese un numero de manera valida.")
                numero= input("Ingrese un numero para el pedido: ")

def cambio_de_turno(empleado):
    empleado = input("Ingrese el nombre del encargado: ")
    return empleado

def registro_ingreso(empleado):
    hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    registro= f"IN {hora} - {empleado} ha Ingresado.\n"
    with open("registro.txt", "a") as f:
        f.write(registro)

def registro_salida(empleado, ventas):
    hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    registro= f"OUT {hora} - {empleado} se ha retidado. Ventas: ${ventas}\n"
    with open("registro.txt", "a") as f:
        f.write(registro)
###ventas##
ventas_totales_encargado_actual= 0

encargado = input("Ingrese el nombre del encargado: ")
encargado= verificar_nombre(encargado)
registro_ingreso(encargado)

while True:
    print(f"Welcome back {encargado} to Los Pollos Hermanos Family")
    print("1. Ingresa Nuevo pedido")
    print("2. Cambio de turno")
    print("3. Apagar Sistema")
    opcion = input(">>> ")
    match opcion:
        case "1":
            #########################
            # Ingresar nuevo pedido #
            #########################
            nombre= input("Ingrese el nombre del cliente: ")
            nombre= verificar_nombre(nombre)
            combo1 = verificar_numero(input("Ingrese cantidad de Combo 1: "))
            combo2 = verificar_numero(input("Ingrese cantidad de Combo 2: "))
            combo3 = verificar_numero(input("Ingrese cantidad de Combo 3: "))
            postre = verificar_numero(input("Ingrese cantidad de Postre: "))
            PrecioCombo1 = 7
            PrecioCombo2 = 3
            PrecioCombo3 = 5
            PrecioPostre = 4
            totalCostoCombo1 = PrecioCombo1 * combo1
            totalCostoCombo2 = PrecioCombo2 * combo2
            totalCostoCombo3 = PrecioCombo3 * combo3
            totalCostoPostre = PrecioPostre * postre
            total= totalCostoCombo1 + totalCostoCombo2 + totalCostoCombo3 + totalCostoPostre
            print("El precio total del pedido es de $" , total)
            while True:
                paga= verificar_numero(input("Abona con $"))
                if paga < total:
                    print("No se puede continuar con el pedido si se abona con un monto menor al total.")
                else:
                    break    
            vuelto= paga - total
            print("El vuelto para el cliente es de $",vuelto)
            while True:
                FinPedido=  input("¿Confirma pedido? Y/N : ").lower()
                match FinPedido:
                    case "y":
                        ventas_totales_encargado_actual= ventas_totales_encargado_actual + total
                        hora= time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
                        ventas= f"{nombre} , {hora} , {combo1} , {combo2}, {combo3}, {postre}, ${total}\n"
                        with open("ventas.txt", "a") as f:
                            f.write(ventas)
                        print("¡Pedido Guardado!")
                        break 
                    case "n":
                        print("¡Pedido Eliminado!")
                        break
                    case _:
                        print("Confirme el pedido presionando ""Y""(Si) o ""N""(No).")
        case "2":
            # Cambio de turno
            registro_salida(encargado, ventas_totales_encargado_actual)
            ventas_totales_encargado_actual= 0
            encargado= cambio_de_turno(encargado)
            encargado= verificar_nombre(encargado)
            registro_ingreso(encargado)
        case "3":
            registro_salida(encargado, ventas_totales_encargado_actual)
            print("Gracias por Trabajar en Los Pollos Hermanos!")
            break
        case _:
            print("Opcion Invalida.")