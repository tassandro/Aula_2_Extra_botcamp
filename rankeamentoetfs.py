from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

url = "https://www.etf.com/etfanalytics/etf-finder"

driver.get(url)

time.sleep(5)

botao_100 = driver.find_element("xpath", '''html/body/div[5]/section/div/div[3]/section/div
                                                /div/div/div/div[2]/
                                section[2]/div[2]/section[2]/div[1]/div/div[4]/button/label/span''')

driver.execute_script("arguments[0].click();", botao_100)

numero_paginas = driver.find_element("xpath", '''/html/body/div[5]/section/div/div[3]/
section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[2]/div/label[2]''')

numero_paginas = numero_paginas.text.replace("of ", "")

numero_paginas = int(numero_paginas)

lista_de_tabela_por_pagina = []

for pagina in range(0, numero_paginas):
    
    tabela = driver.find_element("xpath", '''/html/body/div[5]/section/div/div[3]/section/div/
                                    div/div/div/div[2]/section[2]/div[2]/div/table''')
    html_tabela = tabela.get_attribute("outerHTML")

    tabela_final = pd.read_html(html_tabela)[0]
    
    lista_de_tabela_por_pagina.append(tabela_final)
    
    botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
    
    driver.execute_script("arguments[0].click();", botao_avancar_pagina
    
    
base_de_dados_completa = pd.concat(lista_de_tabela_por_pagina)

botao_aba = driver.find_element("xpath", ''' /html/body/div[5]/section/div/div[3]/section/div/div/div/div/
div[2]/section[2]/div[2]/ul/li[2]/span''')

driver.execute_script("arguments[0].click();", botao_aba)

#voltando a 1 página

for pagina in range(0, numero_paginas):
    
    botao_voltar_pagina = driver.find_element("xpath", '//*[@id="previousPage"]')
    
    driver.execute_script("arguments[0].click();", botao_voltar_pagina)
    
    
lista_de_tabela_por_pagina = []

for pagina in range(0, numero_paginas):
    
    tabela = driver.find_element("xpath", '''/html/body/div[5]/section/div/div[3]/section/div/
                                    div/div/div/div[2]/section[2]/div[2]/div/table''')

    html_tabela = tabela.get_attribute("outerHTML")

    tabela_final = pd.read_html(html_tabela)[0]
    
    lista_de_tabela_por_pagina.append(tabela_final)
    
    botao_avancar_pagina = driver.find_element("xpath", '//*[@id="nextPage"]')
    
    driver.execute_script("arguments[0].click();", botao_avancar_pagina)
    

base_de_dados_performance = pd.concat(lista_de_tabela_por_pagina)

driver.quit()

base_de_dados_completa = base_de_dados_completa.set_index('Ticker')
base_de_dados_performance = base_de_dados_performance.set_index("Ticker")

base_de_dados_performance

base_de_dados_performance = base_de_dados_performance[['3 Years', '5 Years', '10 Years']]

base_de_dados_performance

base_de_dados_performance = base_de_dados_performance.replace("--", pd.NA)

base_de_dados_performance

base_de_dados_performance = base_de_dados_performance.dropna()

base_de_dados_performance

base_de_dados_performance['3 Years'] = (base_de_dados_performance['3 Years'].
                                        str.rstrip('%').astype(float)/100)

base_de_dados_performance['5 Years'] = (base_de_dados_performance['5 Years'].
                                        str.rstrip('%').astype(float)/100)

base_de_dados_performance['10 Years'] = (base_de_dados_performance['10 Years'].
                                        str.rstrip('%').astype(float)/100)

base_de_dados_performance

base_de_dados_final = base_de_dados_completa.join(base_de_dados_performance, how = "inner")

base_de_dados_final

base_de_dados_final = base_de_dados_final[~base_de_dados_final['Segment'].str.contains("Leveraged")]

base_de_dados_final

base_de_dados_final['rank_3_anos'] = base_de_dados_final['3 Years'].rank(ascending = False)
base_de_dados_final['rank_5_anos'] = base_de_dados_final['5 Years'].rank(ascending = False)
base_de_dados_final['rank_10_anos'] = base_de_dados_final['10 Years'].rank(ascending = False)

base_de_dados_final

base_de_dados_final['rank_final'] =  (base_de_dados_final['rank_3_anos'] + 
                                      base_de_dados_final['rank_5_anos'] + 
                                      base_de_dados_final['rank_10_anos'])

base_de_dados_final

melhores_etfs = base_de_dados_final.sort_values(by = "rank_final")

melhores_etfs

melhores_etfs.head(10)
