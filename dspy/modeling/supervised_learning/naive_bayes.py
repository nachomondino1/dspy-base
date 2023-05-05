# Importo librerias
import pandas as pd

def train_naive_bayes(df, var_resp):
    """
    Entrena un modelo de Naive Bayes determinando las probibilades correspondientes.
    :param df: Dataframe train. Columnas: cualquier numero de variables dependientes y con la variable respuesta
    :param var_resp: String. Nombre de la variable respuesta
    :return: Dataframe. Columnas: la variable respuesta y cada variable dependiente por cada valor que toma. Index:
    valores de la variable respuesta. Celdas: probabilidades de que tal variable dependiente valga tal valor dado que
    la variable respuesta es tal valor.
    """
    # Definicion de variables
    d = {}  # Diccionario donde cargare las columnas para el dataset df_prob
    l_atrib = list(df.drop(var_resp, axis=1).columns)
    l_clases = df[var_resp].unique()  # Valores de la variable respuesta (debe ser categorica)
    k = len(l_clases)  # Cantidad de valores de la variable respuesta (utilizado en correccion de Laplace)

    # Paso 1: Obtener estimacion de P(vj) (en este caso, P(escoces) y P(ingles)
    d[var_resp] = [len(df[df[var_resp] == clase]) / len(df) for clase in l_clases]

    # Paso 2: Por cada valor de cada atributo (e.g. atrib scones toma valor 0 o 1), calcular P(ai/vj)
    # Por atributo (sin incluir la variable respuesta)
    for atributo in l_atrib:
        print(f'Atributo: {atributo}')

        # Por valor del atributo
        for valor_atr in df[atributo].unique():

            print(f'\t Valor del atributo: {valor_atr}', end='. ')
            l = []

            # Por clase (valor de la variable respuesta)
            for clase in l_clases:

                # Calculo P(valor atrib / clase)
                numerador = len(df[(df[atributo] == valor_atr) & (df[var_resp] == clase)]) + 1  # el +1 es por la correccion de Laplace
                denominador = len(df[df[var_resp] == clase]) + k  # el +k es por la correccion de Laplace
                l.append(numerador/denominador)
                print(f'\t Probabilidad para la clase {clase}: {numerador/denominador}')

            # Agrego la columna
            d[f'{atributo}={valor_atr}'] = l

    # Concateno columnas del
    df_prob = pd.DataFrame(d, index=l_clases)  # Convierto diccionario en Dataframe (asi evito error de Highly fragmented)
    return df_prob

def predict_naive_bayes(df_prob, df_test, var_resp, con_prob=False):
    """
    Predice la clase de cada nuevo registro usando el modelo entrenado de Naive Bayes.
    :param df_prob: Dataframe. Columnas: la variable respuesta y cada variable dependiente por cada valor que toma.
    Index: valores de la variable respuesta. Celdas: probabilidades de que tal variable dependiente valga tal valor dado
    que la variable respuesta es tal valor.
    :param df_test: Dataframe test. Columnas: cualquier numero de variables dependientes y, necesiaramente al final, la
    variable respuesta.
    :param var_resp: String. Nombre de la variable respuesta
    :return: Dataframe test mas una columna con la clase predicha por el modelo
    """
    l_atrib = list(df_test.drop(var_resp, axis=1).columns)

    # Por registro a predecir
    for i in range(len(df_test)):

        # Defino variables
        d = {}  # Reinicio diccionario por cada nuevo registro
        prob_den = 0  # Reinicio prob_den por cada nuevo registro

        # Paso 3: Multiplicar P(ai/vj) y P(vj)
        # Por clase (valor de la variable respuesta)
        for clase in list(df_prob.index):

            # Definicion de variables
            prob = df_prob.loc[clase, var_resp]  # Inicializo variable. Probabilidad de que sea de una clase dados ciertos atributos

            # Por atributo
            for atrib in l_atrib:

                valor_atr = df_test.loc[i, atrib]
                col_name = f'{atrib}={valor_atr}'
                try:
                    prob *= df_prob.loc[clase, col_name]
                    print(f"P({col_name}/{clase}) = {df_prob.loc[clase, col_name]}")
                except KeyError:
                    print(f"Fallo la extraccion de la probabilidad {col_name}")

            # Guardo probabilidad de que pertenezca a la clase
            d[clase] = prob
            print(f"Prob que sea clase {clase}: {prob}")

            # Calculo prob del denominador para poder calcular la prob de una clase dado ciertos atrib
            prob_den += prob
            print("Prob denominador: ", prob_den)

        # Guardo resultados
        prob_max = max(d.values())
        for clase, prob in d.items():

            # Si la clase tiene la mayor probabilidad
            if prob == prob_max:
                # Guardo la clase predicha
                df_test.loc[i, 'y_pred'] = clase
                print("Dados los atributos, se infiere que es {} con una prob de {:.0f}%".format(clase, prob))

            if con_prob:
                # Guardo probabilidad de la clase (de todas las clases)
                df_test.loc[i, f'prob_{clase}'] = prob / prob_den * 100
    return df_test