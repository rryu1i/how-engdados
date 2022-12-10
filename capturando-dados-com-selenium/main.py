#%%
import selenium
from selenium import webdriver

#%%
driver = webdriver.Chrome('/home/roger/How/EngDados/how-engdados/capturando-dados-com-selenium/src/chromedriver')

#%%
driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
elem_cep = driver.find_element("name", "endereco")

#%%/src/chromedriver