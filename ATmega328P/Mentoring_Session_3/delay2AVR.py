#INPUT: Frecuencia de tu reloj = 1MHz
#INPUT: El delay deseado = 1Segundo
#OUTPUT: El valor de los registros Rexterno, RintermediO, Rinterno

def calcular_retardo_max_10_nops(FrecuenciaReloj, delayDeseado):
    T_ciclo = 1 / FrecuenciaReloj
    max_nops = 4 #10
    max_reg = 256  # registros de 8 bits

    mejor_error = float('inf')
    mejor_config = None
    ##
    ciclos_nece = delayDeseado/(T_ciclo)
    ##
    for nops in range(3, max_nops + 1):
        ciclos_necesarios = delayDeseado / (T_ciclo * nops)
        
        # Buscar todas las combinaciones de 2 o más registros cuyo producto se aproxime a ciclos_necesarios
        for R1 in range(1, max_reg):
            if ciclos_necesarios % R1 != 0:
                continue
            resto = ciclos_necesarios / R1
            if resto <= max_reg:
                R2 = int(resto)
                delay_real = T_ciclo * nops * R1 * R2
                error = abs(delay_real - delayDeseado)
                if error < mejor_error:
                    mejor_error = error
                    mejor_config = {
                        'Registros': [R1, R2],
                        'NOPs_internos': nops,
                        'Delay_real': delay_real,
                        'Error': error
                    }

            # Si deseas más registros anidados (como 3), agrega lógica adicional:
            for R2 in range(1, max_reg):
                if resto % R2 != 0:
                    continue
                R3 = int(resto / R2)
                if R3 <= max_reg:
                    delay_real = T_ciclo * nops * R1 * R2 * R3
                    error = abs(delay_real - delayDeseado)
                    if error < mejor_error:
                        mejor_error = error
                        mejor_config = {
                            'Registros': [R1, R2, R3],
                            'NOPs_internos': nops,
                            'Delay_real': delay_real,
                            'Error': error
                        }

    if mejor_config:
        print(f"Delay deseado: {delayDeseado*1e6:.2f} us")
        print(f"Delay real:    {mejor_config['Delay_real']*1e6:.2f} us")
        print(f"Error:         {mejor_config['Error']*1e6:.2f} us")
        print(f"Ciclos necesarios: {ciclos_nece}")
        return mejor_config
    else:
        print("No se encontró una configuración válida con NOPs ≤ 10.")
        return None


resultado = calcular_retardo_max_10_nops(1000000, 0.000100)  # f=1MHz,  delaydeseado= 1 segundo
print(resultado)