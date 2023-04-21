# Importo librerias
import pandas as pd

def train_naive_bayes(df):  # PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
    """
    Entrena un modelo de Naive Bayes determinando las probibilades correspondientes.
    :param df: Dataframe train. Columnas: cualquier numero de variables dependientes y, necesiaramente al final, la
    variable respuesta.
    :return: Dataframe. Columnas: la variable respuesta y cada variable dependiente por cada valor que toma. Index:
    valores de la variable respuesta. Celdas: probabilidades de que tal variable dependiente valga tal valor dado que
    la variable respuesta es tal valor.
    """
    # Definicion de variables
    var_resp = df.columns[-1]  # Nombre de la variable respuesta
    l_clases = df.iloc[:, -1].unique()  # Valores de la variable respuesta (debe ser categorica)
    k = len(l_clases)  # Cantidad de valores de la variable respuesta (utilizado en correccion de Laplace)
    df_prob = pd.DataFrame(index=l_clases)  # Dataframe de probabilidades

    # Paso 1: Obtener estimacion de P(vj) (en este caso, P(escoces) y P(ingles)
    for clase in l_clases:

        df_prob.loc[clase, var_resp] = len(df[df.iloc[:, -1] == clase]) / len(df)

    # Paso 2: Por cada valor de cada atributo (e.g. atrib scones toma valor 0 o 1), calcular P(ai/vj)
    # Por atributo (sin incluir la variable respuesta)
    for atributo in list(df.columns)[:-1]:

        # Por valor del atributo
        for valor in df[atributo].unique():

            # Defino nombre de columna
            col_name = '{}={}'.format(atributo, str(valor))

            # Por clase (valor de la variable respuesta)
            for clase in l_clases:

                # Calculo P(valor atrib / clase)
                numerador = len(df[(df[atributo] == valor) & (df.iloc[:, -1] == clase)]) + 1  # el +1 es por la correccion de Laplace
                denominador = len(df[df.iloc[:, -1] == clase]) + k  # el +k es por la correccion de Laplace
                df_prob[clase, col_name] = numerador / denominador

    return df_prob

def predict_naive_bayes(df_prob, df_test, col_prob_clase=False):  # PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
    """
    Predice la clase de cada nuevo registro usando el modelo entrenado de Naive Bayes.
    :param df_prob: Dataframe. Columnas: la variable respuesta y cada variable dependiente por cada valor que toma.
    Index: valores de la variable respuesta. Celdas: probabilidades de que tal variable dependiente valga tal valor dado
    que la variable respuesta es tal valor.
    :param df_test: Dataframe test. Columnas: cualquier numero de variables dependientes y, necesiaramente al final, la
    variable respuesta.
    :return: Dataframe test mas una columna con la clase predicha por el modelo
    """
    # Definicion de variables
    l_atrib, var_resp = df_test.columns[:-1], df_test.columns[-1]
    l_clases = list(df_prob.index)  # Valores que puede tomar la variable respuesta

    # Por registro a predecir
    for i in range(len(df_test)):

        # Reinicio variables
        prob_max, prob_den = 0, 0

        # Paso 3: Multiplicar P(ai/vj) y P(vj)
        # Por clase (valor de la variable respuesta)
        for clase in l_clases:

            # Definicion de variables
            prob = df_prob.loc[clase, var_resp]  # Inicializo variable. Probabilidad de que sea de una clase dados ciertos atributos

            # Por atributo
            for atrib in l_atrib:

                col_name = '{}={}'.format(atrib, df_test.loc[i, atrib])
                prob *= df_prob.loc[clase, col_name]
                # print("P({}/{}) = {}}".format(atrib+str(valor), clase, df_prob[col_name]))

            # Guardo probabilidad de que pertenezca a la clase
            # print("Prob que sea clase {}: {}".format(clase, prob))
            if prob > prob_max:
                prob_max = prob
                clase_max = clase

            # Calculo prob del denominador para poder calcular la prob de una clase dado ciertos atrib
            prob_den += prob
            # print("Prob denominador: ", prob_den)

        # Guardo resultados
        prob_clase = prob_max / prob_den * 100
        df_test.loc[i, 'y_pred'] = clase_max
        # print("Dados los atributos, se infiere que es {} con una prob de {:.0f}%".format(clase_max, prob_clase))

        # Si el usuario quiere la probabilidad de la clase predicha
        if col_prob_clase:
            # Guardo probabilidad de la clase predicha
            df_test.loc[i, 'y_pred_prob'] = prob_clase

    return df_test