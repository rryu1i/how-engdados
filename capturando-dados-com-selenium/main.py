
from selenium import webdriver
import sys
import time

cep =  sys.argv[1]

if cep:
    driver  = webdriver.Chrome('./src/chromedriver')
    time.sleep(5)
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    elem_cep = driver.find_element('name','endereco')
    elem_cep.clear()
    elem_cep.send_keys(f'{cep}')
    elem_cmb = driver.find_element('name','tipoCEP')
    elem_cmb.click()
    driver.find_element('xpath',
        '/html/body/main/form/div[1]/div[1]/div/section/div[2]/div/div[2]/select/optgroup/option[1]').click()
    driver.find_element('id','btn_pesquisar').click()

    time.sleep(5)
    logradouro = driver.find_element('xpath',
        '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[1]').text
    bairro = driver.find_element('xpath',
        '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[2]').text
    localidade = driver.find_element('xpath',
        '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[3]').text

    driver.close()

    print("""
    Para o CEP {} temos:
    Endereço: {}
    Bairro: {}
    Localidade: {}
    """.format(
    cep,
    logradouro.split(' - ')[0],
    bairro,
    localidade
    ))
