import pandas as pd

def balance_dataset(df, var_resp):

    # Definicion de variables
    df_bal = pd.DataFrame(columns=df.columns)
    l_clases = list(df[var_resp].unique())

    # Random shuffle dataframe (por evitar mal balanceo en caso de que el df este ordenado por algun campo)
    df = df.sample(frac=1).reset_index(drop=True)

    # Paso 1: Identifico cuantos ejemplos deberia tener cada clase para que el dataset este balanceado
    n_ejs_clase_min = min([len(df[df[var_resp] == clase]) for clase in l_clases])
    print(f"Numero de ejemplos a dejar por clase: {n_ejs_clase_min}")

    # Paso 2: Efectuo el balanceo segun la cantidad que debe tener cada clase (n_ejs_clase_min)
    for clase in l_clases:

        # Obtengo registros de la clase segun n_ejs_clase_min
        df_clase_bal = df[df[var_resp] == clase][:n_ejs_clase_min]

        # Construyo nuevo dataset balanceado
        df_bal = pd.concat([df_bal, df_clase_bal])
        print(f"Clase: {clase}. Cantidad de valores inicial: {len(df[df[var_resp] == clase])}. Cantidad de valores final: {len(df_clase_bal)}")
    return df_bal

def categorize_numeric_columns(df):
    """
    Dado un dataframe, categoriza sus columnas numericas (las no numericas no porque al no haber una "distancia" entre
    strings, no puedo determinar cual se asemeja con cual) continuas (las discretas no pues ya estan categorizadas)
    :param df: Dataframe. Unidad de analisis: cualquiera. Columnas: cualquiera.
    :return: Dataframe. Unidad de analisis: cualquiera. Columnas: cualquiera. Todas sus columnas numericas continuas
    ahora son numericas discretas
    """
    # Defino variables
    # POR COLUMNA DEL DATAFRAME
    for columna in list(df.columns):
        print(columna.upper().center(120))

        # SI LA COLUMNA ES NUMERICA
        if (df[columna].dtype == 'float64') or (df[columna].dtype == 'int64'):

            # Defino variables
            n_clases = len(df[columna].unique())
            n_clases_opt = int(len(df[columna].dropna()) ** 0.5)

            # SI LA COLUMNA ES CONTINUA (toma muchos valores distintos, especificamente, mas que la cantidad optima)
            if n_clases > n_clases_opt:
                print("Sera categorizada pues tiene {} valores unicos cuando, en este caso, lo recomendado es {}.".format(n_clases, n_clases_opt))

                # OBTENGO VALORES MEDIOS Y MAXIMOS DE CADA CLASE
                d = create_classes(valores=df[columna], cant_clases=n_clases_opt)  # key=valor_max y val=valor_med

                # REEMPLAZO VALORES CONTINUOS POR LA MEDIA DE LA CLASE A LA QUE PERTENECE
                # Por valor del atributo
                for i in range(len(df[columna])):

                    # Por valor maximo de las clases
                    for valor_limite in list(d.keys()):

                        # Si el valor es menor al valor maximo de la clase
                        if df[columna].iloc[i] <= valor_limite:

                            # reemplazo valor por el valor medio de la clase
                            df.loc[i, columna] = d[valor_limite]

                            # dejo de comparar el valor con los valores maximos de las clases pues ya encontre su clase
                            break

            # SI LA COLUMNA ES DISCRETA (toma pocos valores distintos)
            else:
                # imprimo mensaje
                print("Es numerica pero discreta pues toma {} valores!".format(n_clases))

        # SI LA COLUMNA NO ES NUMERICA
        else:
            # imprimo mensaje
            print("No es numerica!")
    return df

def create_classes(valores, cant_clases):
    """
    Genera clases o categoria para un conjunto de valores numericos continuos
    :param valores: Lista de valores de una columna numerica continua
    :param cant_clases: Cantidad de clases a generar
    :return: Diccionario con valores maximos de cada clase como key y con valores medios de cada clase como value
    """
    # DEFINO VARIABLES
    valores_unicos = sorted(valores.dropna().unique())
    print("Valores unicos: ", valores_unicos)
    cant_clases_perc = int(round(0.1 * cant_clases, 0))  # cantidad de clases utilizando percentiles
    percentiles = 1 / cant_clases_perc  # percentil
    d = {}  # diccionario a retornar (con valores maximos y medios de cada clase)

    # CREO CLASES A PARTIR DE PERCENTILES
    # Por clase
    print("{:^10s}\t{:^10s}\t{:^10s}\t{:^10s}".format("Clase Nº", "Valor min", "Valor med", "Valor max"))
    for i in range(cant_clases_perc):

        # Obtengo indices de valor min y max para la clase
        idx_valor_min_clase = int(len(valores_unicos) * percentiles * i)  # valor min para estar en clase i
        idx_valor_max_clase = int(len(valores_unicos) * percentiles * (i + 1)) - 1  # valor min para estar en clase i. El -1 seria porque el idx de la lista arranca en 0

        # Obtengo valores min y max de la clase a partir de los indices
        valor_min_clase = valores_unicos[idx_valor_min_clase]
        valor_max_clase = valores_unicos[idx_valor_max_clase]
        valor_med_clase = (valor_max_clase + valor_min_clase) / 2  # valor medio de clase i

        # Guardo valor maximo y medio de la clase
        d[valor_max_clase] = valor_med_clase
        print("{:^10d}\t{:^10.1f}\t{:^10.1f}\t{:^10.1f}".format(i + 1, valor_min_clase, valor_med_clase, valor_max_clase))

    # Imprimo resultados de distribucion de valores en clases
    values_distribution_in_classes(d, valores_unicos)
    return d

def values_distribution_in_classes(dict, valores_unicos):
    """
    Obtiene la distribucion de los valores unicos en las clases, es decir, la cantidad de valores unicos por clase.
    :param dict: Diccionario con valores maximos de cada clase como key y con valores medios de cada clase como value
    :param valores_unicos: Lista de valores unicos de una columna numerica continua
    :return: Lista de cantidad de valores unicos por clase
    """
    # Inicializo diccionario a retornar
    d = {}
    for key in dict.keys():
        d[key] = 0

    # Por valor unico
    for valor in valores_unicos:

        # Por valor maximo de clase
        for valor_max_clase in list(dict.keys()):

            # si el valor es menor al valor maximo de clase
            if valor <= valor_max_clase:  # si el valor unico estaria en clase

                # sumo 1 a clase a la que pertenece el valor
                d[valor_max_clase] += 1

                break  # para no seguir comparando valor con otros valores maximos de clases

    print("Distribucion de valores unicos en clases: ", list(d.values()))
    return list(d.values())

def main():
    df = pd.read_excel('/Users/nachomondino/Desktop/df_prepared.xlsx')
    df_bal = balance_dataset(df, var_resp='equipo_ganador')

main()