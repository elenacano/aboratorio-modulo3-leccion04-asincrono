import asyncio
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep
import time

from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 

import funciones_auxiliares as fa

#---------------------------------------------------------------------------------------------------


async def pag_mes(munici):
    """Accede al tiempo de los últimos 10 meses y guarda los datos de cada día en un dataframe.

    Args:
        munici (str): municipio del cual queremos buscar el tiempo

    Returns:
        DataFrame: DataFrame con todos los parametros del municipio.
    """
    #Abrimos el driver y accedemos a la página principal
    driver = webdriver.Chrome()
    url_wunder = "https://www.wunderground.com/history"
    driver.get(url_wunder)
    driver.maximize_window()
    sleep(1)
    #Denegamos las cookies
    iframe_cookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", '//*[@id="sp_message_iframe_1165301"]')))
    driver.switch_to.frame(iframe_cookies)

    sleep(3)
    try:
        driver.find_element("css selector", "#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column").click()
    except:
        print("No encuentro el boton de las cookies")

    driver.switch_to.default_content()

    # Introduce el municipio en la página principal
    sleep(3)
    driver.find_element("css selector", "#historySearch").send_keys(f"{munici}, Spain", Keys.ENTER)

    # Damos click en view
    sleep(3)
    driver.find_element("css selector", "#dateSubmit").click()
    driver.find_element("css selector", "#dateSubmit").click()

    # Pinchar en monthly de la página del municipio
    sleep(2)
    driver.find_element("css selector", "#inner-content > div.region-content-main > div.row > div:nth-child(1) > div:nth-child(1) > div > lib-link-selector > div > div > div > a:nth-child(3)").click()

    # Gogemos la url de la web
    sleep(3)
    url_mes = driver.find_element("xpath", "/html/head/link[51]").get_attribute("href")
    url_mes_base= url_mes[:-2]
    print(url_mes_base)
   
    df_final=pd.DataFrame()

    # Iteramos para cada mes
    for i in range(1,11):
        url_mes = url_mes_base + f"{i}"
        driver.get(url_mes)
        sleep(3)

        # Cogemos el html de la pagina actual
        html_table_page = driver.page_source

        # Hacemos la sopa y extraemos los datos que queremos
        sopa = BeautifulSoup(html_table_page, "html.parser")
        df=fa.df_datos_mes(sopa)
        df_final = pd.concat([df_final, df])

    return df_final


async def main():
    """Función principal que itera por municipios y guarda el dataframe con todos los datos de todos los municipios.
    """
    inicio = time.time()
    
    municipios = fa.get_municipios()
    lista_tareas = []
    municipios = ["alcobendas", "leganes", "alcorcon", "alpedrete"]
    for munici in municipios:
        lista_tareas.append(pag_mes(munici))

    lista_df_muni = await asyncio.gather(*lista_tareas)
    df_final = pd.concat(lista_df_muni)
    print(df_final.shape)
    
    df_final.reset_index(inplace=True)
    df_final.to_csv("../datos/df_asinc.csv")

    fin = time.time()
    tiempo_total = np.round(((fin - inicio)/60), 2)
    print(f"El tiempo total es {tiempo_total} min")


if __name__ == "__main__":
    asyncio.run(main())

