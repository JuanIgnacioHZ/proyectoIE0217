#!/usr/local/Cellar/python@3.9/3.9.0_1/bin/python3.9
# Curso: IE0217 II Semestre, 2020
# Profesor: Juan Carlos Coto Ulate
# Estudiante: Juan Ignacio Hernández Zamora (B93826)
# Última edición 14-12-20 11:34 p.m.
from pdb import set_trace
from os import system, popen


class ÁrbolDeHuffman:
    def __init__(self, texto):
        self.elementos = list(reversed((Procesar_Texto(texto)).items()))
        self.árbol_de_Huffman = Generar_Árbol(self.elementos)
        self.dict_codificación = (self.Obtener_Codif())[0]
        self.long_máx_caract = (self.Obtener_Codif())[1]

    def __iter__(self):
        return self

    def __next__(self):
        '''
            Esta recorre a profundidad el árbol que se generó al principio
        y en cada iteración devuelve el elemento siguiente.
        '''

        if len(self.elementos) > 2:
            if ('None' in str(type(self.nodo_actual))):
                self.nodos_recorridos = []
                raise StopIteration
        else:
            if ((('int' in str(type(self.nodo_actual.valor))) and
                 (len(self.nodos_recorridos) == len(self.elementos)))):
                raise StopIteration

        if (('tuple' in str(type(self.nodo_actual.valor)))):
            salida = [self.nodo_actual.valor[0], self.código_temp]
            self.código_temp = ''
            if (((self.nodo_padre is not None) and
                 (self.nodo_padre.Cantidad_Hijos == 1))):
                if not(self.nodo_padre in self.nodos_recorridos):
                    self.nodos_recorridos.append(self.nodo_padre)
            if self.nodo_actual not in self.nodos_recorridos:
                self.nodos_recorridos.append(self.nodo_actual)
            self.nodo_actual = self.árbol_de_Huffman[self.llave_primer_elem]
            self.nodo_padre = []
            return salida

        elif ('int' in str(type(self.nodo_actual.valor))):
            if ((('None' not in str(type(self.nodo_actual.izq))) and
                 (self.nodo_actual.izq not in self.nodos_recorridos))):
                self.nodo_actual = self.nodo_actual.izq
                self.código_temp += '0'
                self.nodo_padre = self.nodo_actual.padre
                return self.__next__()

            elif (('None' not in str(type(self.nodo_actual.der))) and
                  (self.nodo_actual.der not in self.nodos_recorridos)):
                self.nodo_actual = self.nodo_actual.der
                self.código_temp += '1'
                self.nodo_padre = self.nodo_actual.padre
                return self.__next__()

            else:
                if ('None' not in str(type(self.nodo_padre.padre))):
                    self.nodo_padre = self.nodo_padre.padre
                self.nodos_recorridos.append(self.nodo_actual)
                self.nodo_actual = self.nodo_actual.padre
                return self.__next__()

    def Obtener_Codif(self):
        '''
            Esta funció se encarga de ir añadiendo a la salida la codificación
        de cada elemento, con él incluido, de manera que al terminar de
        recorrer el árbol se tenga todo codificado y en ordenado de manera
        creciente respecto al número de bits  que toma el elemento codificado.
        '''
        self.llave_primer_elem = [int(i)
                                  for i in iter(self.árbol_de_Huffman)][0]
        self.nodo_actual = self.árbol_de_Huffman[self.llave_primer_elem]
        self.nodos_recorridos = []
        self.código_temp = ''
        salida_temp = {}
        salida = {}
        for i in self:
            salida_temp[i[0]] = i[1]
        del self.llave_primer_elem
        del self.nodo_actual
        del self.nodos_recorridos
        del self.código_temp
        longitudes = []
        for i in salida_temp:
            longitudes.append([i, len(salida_temp[i])])
        while True:
            # Sí, yo sé que esto es vergonzosamente ineficiente
            entrada_temporal = []
            contador = 0
            for i in range(len(longitudes)):
                try:
                    if longitudes[i][1] > longitudes[i+1][1]:
                        entrada_temporal = longitudes[i]
                        longitudes[i] = longitudes[i+1]
                        longitudes[i+1] = entrada_temporal
                except IndexError:
                    continue
            if entrada_temporal == []:
                for i in range(len(longitudes)):
                    salida[longitudes[i][0]] = salida_temp[longitudes[i][0]]
                    if i == (len(longitudes) - 1):
                        contador = len(salida_temp[longitudes[i][0]])
                break
        salida = [salida, contador]
        return salida

    def Codificar(self, entrada):
        '''
            Esta recibe una tira de caracteres, evalúa que todos sean
        codificables y, de serlo, devuelve en una sola tira el código asignado
        a cada caracter.
        '''
        salida = ''
        try:
            for i in entrada:
                if not(i in self.elementos):
                    raise ValueError
        except ValueError:
            system('clean')
        for i in entrada:
            salida += (self.dict_codificación[i])
        return salida

    def Decodificar(self, entrada):
        '''
            Esta función recibe una tira binaria y la corresponde los
        elementos con su codificación respectiva.
        '''
        salida = ''
        dict_temporal = {}
        lista_temporal = []
        for i in self.dict_codificación:
            dict_temporal[self.dict_codificación[i]] = i

        for i in entrada:
            lista_temporal.append(i)

        while lista_temporal != []:
            código_temporal = ''
            for i in range(self.long_máx_caract):
                try:
                    código_temporal += lista_temporal[i]
                    if código_temporal in dict_temporal:
                        salida += dict_temporal[código_temporal]
                        for j in range(i+1):
                            lista_temporal.pop(0)
                except IndexError:
                    pass
                except TypeError:
                    break
        return salida

    def Devolver_Clave(self):
        salida = ''
        salida += ''
        for i in self.dict_codificación:
            elemento = (i + (' ' * self.long_máx_caract) + '|' +
                        str(self.dict_codificación[i]) + '\n')
            salida += elemento
        return salida


def Generar_Árbol(caracteres):
    '''
        Aquí es donde se forma el árbol, primero se toma un diccionario como
    una matriz de tamaño 2xn, donde cada vector 2x1 tiene la forma
    (carcater(str), frecuencia(int)), así, se toman los dos últimos, se les
    asigna un nodo, y se forma otro nodo con la suma de sus frecuencias, esto
    se repite hasta llegar de manera recursva al final de la lista.
        Nota, esta función no genera árboles genéricos, está hacha para árboles
    de Huffman.
    '''
    caract = {}  # Aquí van los caracteres que van a ser las hojas
    nudos = {}   # Como los nudos de un árbol, aquí va la suma de las
    # frecuencias de cada dos hojas
    try:
        # Aquí se procesan los caracteres y se empieza a formar el árbol
        for i in range(0, len(caracteres), 2):
            # Esto se recorre de dos en dos para armar el árbol de abajo
            # hacia arriba y poder tener el mismo tipo de referencia a lo
            # largo de todo el ciclo
            # Se crean los nodos
            caract[caracteres[i][0]] = Nodo(caracteres[i])
            caract[caracteres[i+1][0]] = Nodo(caracteres[i+1])
            nudos[i] = Nodo(caracteres[i][1] + caracteres[i+1][1])

            # Se asignan los parentescos, esto sirve, no arreglarlo
            Argregar_Parentesco(nudos[i],
                                caract[caracteres[i][0]],
                                caract[caracteres[i+1][0]])
    except IndexError:
        caract[caracteres[i][0]] = Nodo(caracteres[i])
        nudos[i] = Nodo(caracteres[i][1])
        nudos[i].Establecer(2, caract[caracteres[i][0]])

    while len(nudos) > 1:
        nudos = Recalcular_Nudos(nudos)
    return nudos


def Recalcular_Nudos(entrada):
    '''
        Esta función se ancarga de revisar los dos primeros de la lista que se
    le ingrese, de manera que se establezca un nodo entre ellos que tenga como
    valor la suma de sus frecuencias y ambos nodos como hijos donde el de mayor
    valor va hacia la derecha y el de menor valor hacia la izquierda.
    Los nodos calculados se agregan al final de la lista y se eliminan los dos
    primeros para porder ejecutar la función de manera recursiva.
    '''
    contador = 0
    nudo_ant = {}
    try:
        for i in entrada:
            if contador == 0:
                contador = 1
                nudo_ant = i
            elif ((contador == 1) and (nudo_ant != {})):
                pos_dic = entrada[nudo_ant].valor + entrada[i].valor

                entrada[pos_dic] = Nodo(pos_dic)
                Argregar_Parentesco(entrada[pos_dic],
                                    entrada[nudo_ant],
                                    entrada[i])
                contador = 0
                del entrada[i]
                del entrada[nudo_ant]
                nudo_ant = {}
                break
    except KeyError:
        entrada[pos_dic] = Nodo(pos_dic)
        Argregar_Parentesco(entrada[pos_dic],
                            entrada[nudo_ant])
        del entrada[nudo_ant]
    return entrada


def Argregar_Parentesco(padre, hijo1, hijo2=None):
    '''
        Esta función toma un padre y dos hijos, establece el hijo con el
    mayor valor a la derecha y el del menor a la izquierda, se presupone
    que si un hijo es None, es que no existe y se le da un valor de cero.
    Lo mismo, esto sirve, no arreglarlo.
    '''
    if hijo2 is None:
        hijo1.Establecer(0, padre)
        padre.Establecer(2, hijo1)
    else:
        hijo1.Establecer(0, padre)
        hijo2.Establecer(0, padre)
        if (hijo1.valor >= hijo2.valor):
            padre.Establecer(2, hijo1)
            padre.Establecer(1, hijo2)
        else:
            padre.Establecer(2, hijo2)
            padre.Establecer(1, hijo1)


class Nodo:
    '''
        Aquí se crean los nodos del árbol de Huffman
    '''
    def __init__(self, valor):
        self.valor = valor
        self.padre = None
        self.izq = None
        self.der = None

    def Establecer(self, tipo, valor):
        '''
        Esta función establece padre e hijos de un nodo
        tal que tipo 0 = padre, 1 = izquierda,  2 = derecha
        '''
        if tipo == 0:
            self.padre = valor
        elif tipo == 1:
            self.izq = valor
        elif tipo == 2:
            self.der = valor

    def Devolver(self, tipo):
        '''
        Esta función retorna padre e hijos de un nodo
        tal que tipo 0 = padre, 1 = izquierda,  2 = derecha
        '''
        if tipo == 0:
            return self.padre
        elif tipo == 1:
            return self.izq
        elif tipo == 2:
            return self.der

    def Cantidad_Hijos(self):
        if ((self.izq is None) and (self.der is None)):
            return 0
        elif ((self.izq is not None) and (self.der is not None)):
            return 2
        else:
            return 1


def Procesar_Texto(entrada: str):
    '''
        Esta función toma el texto ingresado, lo separa por caracteres y la
    la cantidad de los mismos, por último, los dordena de mayor a menor.
    '''
    dict_temporal = {}
    dict_de_salida = {}
    for i in entrada:
        if (i in dict_temporal):
            dict_temporal[i] += 1
            pass
        else:
            dict_temporal[i] = 1
    while dict_temporal != {}:
        lista_temp = ['', 0]
        for i in dict_temporal:
            if (dict_temporal[i] > lista_temp[1]):
                lista_temp[0] = i
                lista_temp[1] = dict_temporal[i]

        dict_de_salida[lista_temp[0]] = lista_temp[1]
        dict_temporal.pop(lista_temp[0])
    return dict_de_salida


def Terminal_Interactiva(entrada=None):
    '''
        Esto es un tipo de interfaz interactiva para el usuario.
    '''
    salida = Limpiar_Pantalla(2, ('1. Ingresar texto para crear árbol.\n' +
                                  '2. Mostrar clave.\n' +
                                  '3. Codificar texto.\n' +
                                  '4. Decodificar texto.\n' +
                                  '5. Salir.'))

    if salida == '1':
        texto = Limpiar_Pantalla(2, ('Ingrese el texto a partir del cuál ' +
                                     'desea crear el árbol.'))
        global árbol
        árbol = ÁrbolDeHuffman(str(texto))
        Limpiar_Pantalla(1, ('Árbol creado.\nClave:\n' +
                             (árbol.Devolver_Clave())))

        return True
    elif salida == '2':
        Limpiar_Pantalla(1, ('Clave:\n' +
                             (árbol.Devolver_Clave())))

        return True
    elif salida == '3':
        texto = Limpiar_Pantalla(2, ('Ingrese el texto que desea codificar.'))
        Limpiar_Pantalla(1, ('Texto codificado:\n' + árbol.Codificar(texto) +
                             '\n'))
        return True
    elif salida == '4':
        texto = Limpiar_Pantalla(2, ('Ingrese el texto que desea codificar.'))
        Limpiar_Pantalla(1, ('Texto decodificado:\n' +
                             árbol.Decodificar(texto) +
                             '\n'))
        return True
    elif salida == '5':
        return False
    else:
        Limpiar_Pantalla(1, ('Ingésó una opción inválida, ingrese una ' +
                             'de las dadas.'))
        return True


def Limpiar_Pantalla(tipo, mensaje=None):
    '''
        Esto limpia la pantalla y da un mensaje, el de tipo 1 no devuelve
    respuesta y el de tipo 2 sí
    '''

    system('clear')
    # El comando de abajo obtiene el ancho de la pantalla [filas, columnas][1]
    # esto, por lo que investigué, sólo funciona en Linux
    columnas = (popen('stty size', 'r').read().replace('\n', '').split(' '))[1]

    if tipo == 1:
        for i in range(0, (int(columnas)//2)-11):
            print('¯', end='')
        print('Proyecto final IE0217', end='')
        for i in range(0, (int(columnas)//2)-12):
            print('¯', end='')
        print()
        for i in range(0, (int(columnas)//2)-12):
            print('_', end='')
        print('Codificación de Huffman', end='')
        for i in range(0, (int(columnas)//2)-13):
            print('_', end='')
        print()
        mensaje += '\nPresione enter para volver.'
        input(mensaje)
        return None
    elif tipo == 2:
        for i in range(0, (int(columnas)//2)-11):
            print('¯', end='')
        print('Proyecto final IE0217', end='')
        for i in range(0, (int(columnas)//2)-12):
            print('¯', end='')
        print()
        for i in range(0, (int(columnas)//2)-12):
            print('_', end='')
        print('Codificación de Huffman', end='')
        for i in range(0, (int(columnas)//2)-13):
            print('_', end='')
        print()
        print(mensaje)
        print()
        for i in range(0, (int(columnas))):
            print('¯', end='')
        for i in range(0, (int(columnas))):
            print('_', end='')
        print()
        print()
        return (input('Selección ===> '))
    else:
        return None


# Inicio del programa
ciclo = True
while ciclo:
    ciclo = Terminal_Interactiva()

# Fin del programa
