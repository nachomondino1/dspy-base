import pandas as pd
import datetime

def get_date_from_actual(delta_days, date_format="%d/%m/%Y"):
    """
    Obtiene una fecha unos dias posterior a partir de la fecha actual
    :param delta_days: Integer, numero de dias posteriores a la fecha actual
    :return: Datetime fecha. Delta dias respecto de la fecha actual.
    """
    # Obtengo fecha actual
    fecha_act = datetime.datetime.today()

    # Obtencion de siguiente fecha a partir de la actual
    next_fecha = fecha_act + datetime.timedelta(days=delta_days)

    # Formateo siguiente fecha tal que sea igual que en el XPATH de la pagina web
    next_fecha = next_fecha.strftime(date_format)
    return next_fecha







def format_date(df):  # Aun no la probe pues deberia hice el format de la fecha junto con la extraccion pero bueno
    """
    Convierte fecha del formato "14.02.2023 00:00" a formato "dd/mm/yyyy hh:mm", es decir, "14/02/2023 20:00"
    :param df: Dataframe. Fecha en formato "14.02.2023 20:00"
    :return: String. Fecha y hora con formato "dd/mm/yyyy", por ejemplo, "14/02/2023 20:00"
    """
    # Por registro (partido)
    for i in range(len(df)):

        # PASO 1: SPLIT FECHA (STRING) EN ELEMENTOS (DIA, MES, AÑO, HORA Y MIN)
        n_dia, n_mes, n_año, hora, min = re.split(r':|.', df.loc[i, 'fecha'])

        # Paso 2: convierto string a datetime
        fecha_datetime = datetime.datetime(int(n_año), int(n_mes), int(n_dia), int(hora), int(min))  # Convierto variable de clase 'str' a clase 'datetime.datetime'
        fecha_form = fecha_datetime.strftime("%Y/%m/%d %H:%M")  # Convierto el formato de datetime del default al formato deseado

        # Guardo fecha formateada
        df.loc[i, 'Fecha'] = fecha_form

    return df


def convert_fecha_to_datetime(df):
    # Ordeno dataframe por fecha (de mas reciente a mas viejo)
    print(type(df.fecha[0]))

    # convert to date
    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)

    # verify datatype
    print(type(df.fecha[0]))
    return df


# Utils formatting que tenia en web_scraping_projects...
def format_date(fecha_string, hora_string):
    """
    Convierte fecha del formato "Jan 14" y hora "8:00 PM" a formato "dd/mm/yyyy hh:mm", es decir,
    "14/01/2023 19:30"
    :param fecha_string: String. Fecha en formato "Jan 14"
    :param hora_string: String. Hora en formato "8:00 PM"
    :return: String. Fecha y hora con formato "dd/mm/yyyy hh:mm", por ejemplo, "14/01/2023 20:00"
    """
    # PASO 1: SPLIT FECHA (STRING) EN ELEMENTOS (DIA, MES, AÑO, HORA Y MIN)
    hora, min = split_hour_string(hora_string)  # Paso de string a un integer para la hora y otro para el min
    n_año, n_mes, n_dia = split_date_string(fecha_string)  # Paso de string a un integer para el mes y otro para el dia

    # PASO 2: FORMATEO FECHA
    # Si la fecha tiene hora o minutos
    try:
        fecha_datetime = datetime.datetime(n_año, n_mes, n_dia, hora, min) # Convierto variable de clase 'str' a clase 'datetime.datetime'
        return fecha_datetime.strftime("%d/%m/%Y %H:%M")  # Convierto el formato de datetime del default al formato deseado
    # Si la fecha no tiene hora o minutos
    except:
        fecha_datetime = datetime.datetime(n_año, n_mes, n_dia)  # Convierto variable de clase 'str' a clase 'datetime.datetime'
        return fecha_datetime.strftime("%d/%m/%Y")  # Convierto el formato de datetime del default al formato deseado

# Funciones auxiliares de format_date()
def convert_hour_AM_PM_to_24hs(hora_string):
    """
    Transforma la hora desde AM/PM (e.g. 08:30 PM) a 24 hs (e.g. 20:30)
    :param hora_string: String. Hora en formato AM/PM (e.g. 08:30 PM)
    :return: String. Hora en formato 24 hs (e.g. 20:30), o bien, mensaje de aviso
    """
    try:
        in_time = datetime.datetime.strptime(hora_string, "%I:%M %p")  # Formato hh:mm AM/PM
        out_time = datetime.datetime.strftime(in_time, "%H:%M")  # Convierto hora de AM/PM a 24 hs
        return out_time
    except:
        print("\t No se pudo convertir la hora {} de AM/PM a 24 hs. Es posible que la hora ya es en formato 24 hs".format(hora_string))
        return hora_string

def split_date_string(fecha_string):
    """
    A partir de fecha en formato string, se obtiene los elementos (dia, mes y año) de la fecha por separado en formato
    entero
    :param fecha_string: String. Fecha en formato "Jan 14"
    :return: Integer & Integer & Integer. Dia, mes y año.
    """
    # Definicion de variables
    d = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, 'nov': 11, 'dec': 12}
    deduct_year = lambda mes, dia: datetime.datetime.today().year if datetime.datetime.today() <= datetime.datetime(datetime.datetime.today().year, mes, dia, 23, 59) else datetime.datetime.today().year+1

    # intento extraer dia, mes y año de string
    try:
        mes, n_dia = fecha_string.split()  # Separo string original segun espacios para obtener elementos (mes y dia)
        n_mes, n_dia = d[mes.lower()], int(n_dia)  # Convierto strings a integer
        n_año = deduct_year(n_mes, n_dia)  # Deduzco año de la fecha segun mes y dia
        return n_año, n_mes, n_dia
    # Si falla extraccion de dia, mes y año de string
    except:
        print("Fallo la conversion de la fecha {} de string a integer".format(fecha_string))  # Mensaje de aviso
        return None, None, None

def split_hour_string(hora_string):
    """
    A partir de la hora en string (e.g. 08:30 AM, 20:30), se obtiene hora y minuto (por separado) en formato entero
    :param hora_string: String. Hora en formato (e.g. 08:30 AM, 15:50, ecc)
    :return: Integer & Integer. Hora y minuto en formato entero. En caso de que falla la obtencion, None & None
    """
    # Transforma (solo si es necesario) la hora desde AM/PM (e.g. 08:30 PM) a 24 hs (e.g. 20:30)
    hora_string = convert_hour_AM_PM_to_24hs(hora_string)

    # Intento extraer hora y minuto del string
    try:
        hora, min = hora_string.split(":")  # Obtengo hora y min por separado
        return int(hora), int(min)
    # Si falla la extraccion de hora y minuto del string
    except:
        print("La hora {} no tiene el formato %I:%M".format(hora_string))
        return None, None




def convert_hour_into_min(hora_string):  # Funcion auxiliar de get_duracion()
    """
    Calcula cantidad de minutos equivalentes a una hora en formato hh:mm. Por ejemplo, 05:30 es equivalente a 330
    minutos (5h * 60min/1h + 30 min = 330 min)
    :param hora_string: String. Hora en formato hh:mm
    :return: Integer. Hora pasada como parametro en minutos
    """
    # Descompongo hora en cantidad de horas y cantidad de minutos
    n_horas, n_min = hora_string.split(".")

    # Calculo cantidad de minutos sabiendo que 1 hora = 60 min
    n_min_total = int(n_horas) * 60 + int(n_min)
    return n_min_total

