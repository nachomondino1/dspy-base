import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def k_means(df):
    """
    Aplica modelo de K-means a los datos pasados por parametro. Previamente, selecciono automaticamente el k ideal.
    :param df_clustering: Dataframe. Unidad de análisis: alternativa del producto. Columnas: id_alternativa y atributos
    del producto. Celdas: sentiment que toma el atributo (sin NaN)
    :return: Dataframe. Unidad de análisis: alternativa del producto. Columnas: id_alternativa, una por atributo del
    producto y la columna "label" con el cluster al que pertenece. Celdas: sentiment que toma el atributo
    """
    # Defino variables
    X = np.array(df[df.columns])  #por ahi teenga que sacar algunas columnas..
    sc_X = StandardScaler() # inicializo objeto de clase StandardScaler()
    print("Las {} columnas a clusterizar: {}".format(len(df.columns), list(df.columns)))

    # Escalo datos para determinar k  # estoy en duda si hay que hacerlo pero por los rdos diria que si
    scaled_data = sc_X.fit_transform(X)

    # Eleccion automatica de k
    k = chooseBestKforKMeans(scaled_data, range(2,20))

    # Ejecutamos K-means
    kmeans = KMeans(n_clusters=k).fit(X)

    # Agrego columna de cluster al que pertenece cada alternativa
    df["label"] = kmeans.labels_
    return df

def chooseBestKforKMeans(scaled_data, k_range):
    """
    Choose best k for some data
    :param scaled_data: Data que debe estar normalizada
    :param k_range: Slice. Rango de valores que puede tomar k
    :return: Integer. Best k
    """
    # Defino variable
    ans = []

    # Por posible valor de k
    for k in k_range:

        # Creo modelo de K-means
        scaled_inertia = kMeansRes(scaled_data, k)

        # Guardo resultados del modelo
        ans.append((k, scaled_inertia))

    # Creo dataframe para mostrar los resultados
    df = pd.DataFrame(ans, columns=['k', 'Scaled Inertia']).set_index('k')
    print(df)

    # Elijo el mejor k (minimiza scaled inertia)
    best_k = df.idxmin()[0]
    return best_k

def kMeansRes(scaled_data, k, alpha_k=0.06):  #lo subi de 0.02 a 0.06 para tener menos clusters...
    """
    Entrena modelo de K-means con k pasada como parametro y calcula metrica "scaled inertia"
    :param scaled_data: rows are samples and columns are features for clustering
    :param k: Integer. Current k for applying KMeans
    :param alpha_k: Float. Manually tuned factor that gives penalty to the number of clusters
    :return: Float. Scaled inertia value for current k
    """
    # Calculo inertia para k=1 donde todos los datos pertenecen a un solo grupo
    inertia_o = np.square((scaled_data - scaled_data.mean(axis=0))).sum()

    # Entreno Modelo de K-means buscando k clusters
    kmeans = KMeans(n_clusters=k, random_state=0).fit(scaled_data)

    # Evaluo el modelo con metrica "scaled inertia" (formula de scaled inertia)
    scaled_inertia = kmeans.inertia_ / inertia_o + alpha_k * k
    return scaled_inertia