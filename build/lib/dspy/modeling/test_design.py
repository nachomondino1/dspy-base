def separate_train_and_test(df, porc_corte=0.8):
    """
    Separa un dataframe en train y test segun el porcentaje de corte indicado
    :param df: Dataframe.
    :param porc_corte: Float entre 0 y 1. Porcentaje de registros en el df_train
    :return: Dataframe train y Dataframe test.
    """
    # Shuffle dataframe
    df = df.sample(frac=1).reset_index(drop=True)

    # Separo conjunto de datos en train y test
    corte = int(porc_corte * len(df))
    df_train, df_test = df.loc[:corte].reset_index(drop=True), df.loc[corte:].reset_index(drop=True)
    return df_train, df_test

def cross_validation():
    pass

def boostrap():
    pass