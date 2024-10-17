from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import datetime
import json


def getText(linea):
    """Toma un elemento de beautiful soup y le extra el campo de texto

    Args:
        linea (bs4.element.Tag): linea de la cual queremos sacra el texto

    Returns:
        str: texto que hemos extraido
    """
    dato = linea.text
    return dato.strip()

def get_columnas(columnas, max, dias):
    max_final=max+1+((dias+1)*3)
    lista_aux=columnas[max+1:max_final]
    return max_final, lista_aux


def df_datos_mes(sopa):
    table = sopa.findAll("table", {"class":"days ng-star-inserted"})
    columnas = table[0].findAll("td")

    with open('../datos/dias_mes.json', 'r') as archivo_json:
        dias_mes = json.load(archivo_json)[0]
    with open('../datos/dias_mes.json', 'r') as archivo_json:
        meses = json.load(archivo_json)[1]

    mes_hoy = datetime.datetime.now().month
    mes_actual = columnas[8].text.strip()
    if meses[str(mes_hoy)]==mes_actual:
        dias = datetime.datetime.now().day
    else:
        dias = dias_mes[mes_actual]


    encabezados=columnas[:7]
    encabezados_limpio = list(map(getText,encabezados))

    listas = []
    df = pd.DataFrame()

    # dias
    max1=8+1+dias
    mes=columnas[8:max1]
    listas.append(mes)

    maxi = max1
    for i in range(5):
        maxi, lista_aux = get_columnas(columnas, maxi, dias)
        listas.append(lista_aux)


    # #temperatura
    # max2, temperaturas = get_columnas(columnas, max1, dias)
    # listas.append(temperaturas)

    # #rocío
    # max3, rocio = get_columnas(columnas, max2, dias)
    # listas.append(rocio)

    # #humedad
    # max4, humedad = get_columnas(columnas, max3, dias)
    # listas.append(humedad)

    # #viento
    # max5, viento = get_columnas(columnas, max4, dias)
    # listas.append(viento)

    # #presion
    # max6, presion = get_columnas(columnas, max5, dias)
    # listas.append(presion)

    #precipitacion
    max7=maxi+1+dias+1
    precipitacion = columnas[maxi+1:max7]
    listas.append(precipitacion)

    i=0
    for lista in listas:
        lista_limpia = list(map(getText,lista))
        if i!=0 and i!=6:
            df_aux=pd.DataFrame(np.reshape(lista_limpia,(dias+1,3)))
        else:
            df_aux=pd.DataFrame(lista_limpia)
        df = pd.concat([df, df_aux], axis=1)
        i+=1

    #Metemos el mes, renombramos las columnas, rehacemos el indice y que quitamos la columna indice
    df.insert(0,"mes", mes_actual)
    df.columns = ["mes","dia", "max_temp", "avg_temp", "min_temp", "max_rocio", "avg_rocio", "min_rocio",
                "max_humedad", "avg_humedad", "min_humedad", "max_viento", "avg_viento",
                "min_viento", "max_presion", "avg_presion", "min_presion", "lluvia"]
    df = df.drop(index=0)
    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)

    return df


def get_municipios():
    """Devuelve la lista de municipios de Madrid

    Returns:
        list: lista de los municipios
    """
    lista_municipios = ['acebeda-la', 'ajalvir', 'alameda-del-valle', 'alamo-el', 'alcala-de-henares', 'alcobendas', 'alcorcon', 'aldea-del-fresno', 'algete', 'alpedrete', 'ambite', 'anchuelo', 'aranjuez', 'arganda-del-rey', 'arroyomolinos', 'atazar-el', 'batres', 'becerril-de-la-sierra', 'belmonte-de-tajo', 'berrueco-el', 'berzosa-del-lozoya', 'boadilla-del-monte', 'boalo-el', 'braojos', 'brea-de-tajo', 'brunete', 'buitrago-del-lozoya', 'bustarviejo', 'cabanillas-de-la-sierra', 'cabrera-la', 'cadalso-de-los-vidrios', 'camarma-de-esteruelas', 'campo-real', 'canencia', 'carabana', 'casarrubuelos', 'cenicientos', 'cercedilla', 'cervera-de-buitrago', 'chapineria', 'chinchon', 'ciempozuelos', 'cobena', 'collado-mediano', 'collado-villalba', 'colmenar-del-arroyo', 'colmenar-de-oreja', 'colmenarejo', 'colmenar-viejo', 'corpa', 'coslada', 'cubas-de-la-sagra', 'daganzo-de-arriba', 'escorial-el', 'estremera', 'fresnedillas-de-la-oliva', 'fresno-de-torote', 'fuenlabrada', 'fuente-el-saz-de-jarama', 'fuentiduena-de-tajo', 'galapagar', 'garganta-de-los-montes', 'gargantilla-del-lozoya-y-pinilla-de-buitrago', 'gascones', 'getafe', 'grinon', 'guadalix-de-la-sierra', 'guadarrama', 'hiruela-la', 'horcajo-de-la-sierra-aoslos', 'horcajuelo-de-la-sierra', 'hoyo-de-manzanares', 'humanes-de-madrid', 'leganes', 'loeches', 'lozoya', 'lozoyuela-navas-sieteiglesias', 'madarcos', 'madrid', 'majadahonda', 'manzanares-el-real', 'meco', 'mejorada-del-campo', 'miraflores-de-la-sierra', 'molar-el', 'molinos-los', 'montejo-de-la-sierra', 'moraleja-de-enmedio', 'moralzarzal', 'morata-de-tajuna', 'mostoles', 'navacerrada', 'navalafuente', 'navalagamella', 'navalcarnero', 'navarredonda-y-san-mames', 'navas-del-rey', 'nuevo-baztan', 'olmeda-de-las-fuentes', 'orusco-de-tajuna', 'paracuellos-de-jarama', 'parla', 'patones', 'pedrezuela', 'pelayos-de-la-presa', 'perales-de-tajuna', 'pezuela-de-las-torres', 'pinilla-del-valle', 'pinto', 'pinuecar-gandullas', 'pozuelo-de-alarcon', 'pozuelo-del-rey', 'pradena-del-rincon', 'puebla-de-la-sierra', 'puentes-viejas-manjiron', 'quijorna', 'rascafria', 'reduena', 'ribatejada', 'rivas-vaciamadrid', 'robledillo-de-la-jara', 'robledo-de-chavela', 'robregordo', 'rozas-de-madrid-las', 'rozas-de-puerto-real', 'san-agustin-del-guadalix', 'san-fernando-de-henares', 'san-lorenzo-de-el-escorial', 'san-martin-de-la-vega', 'san-martin-de-valdeiglesias', 'san-sebastian-de-los-reyes', 'santa-maria-de-la-alameda', 'santorcaz', 'santos-de-la-humosa-los', 'serna-del-monte-la', 'serranillos-del-valle', 'sevilla-la-nueva', 'somosierra', 'soto-del-real', 'talamanca-de-jarama', 'tielmes', 'titulcia', 'torrejon-de-ardoz', 'torrejon-de-la-calzada', 'torrejon-de-velasco', 'torrelaguna', 'torrelodones', 'torremocha-de-jarama', 'torres-de-la-alameda', 'tres-cantos', 'valdaracete', 'valdeavero', 'valdelaguna', 'valdemanco', 'valdemaqueda', 'valdemorillo', 'valdemoro', 'valdeolmos-alalpardo', 'valdepielagos', 'valdetorres-de-jarama', 'valdilecha', 'valverde-de-alcala', 'velilla-de-san-antonio', 'vellon-el', 'venturada', 'villaconejos', 'villa-del-prado', 'villalbilla', 'villamanrique-de-tajo', 'villamanta', 'villamantilla', 'villanueva-de-la-canada', 'villanueva-del-pardillo', 'villanueva-de-perales', 'villar-del-olmo', 'villarejo-de-salvanes', 'villaviciosa-de-odon', 'villavieja-del-lozoya', 'zarzalejo']
    return lista_municipios