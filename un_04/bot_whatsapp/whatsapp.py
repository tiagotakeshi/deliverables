from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd

# links e xpaths
WPP_Link = "https://web.whatsapp.com/"
NEW_MSG_BUTTON = '//*[@id="side"]/header/div[2]/div/span/div[2]/div/span'
SEARCH_CONTACT_FIELD = '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[1]/div/label/div/div[2]'
FIRST_CONTACT = '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]'
TYPE_FIELD = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
SEND_BUTTON = '//*[@id="main"]/footer/div[1]/div[3]/button'

# abrindo o driver/whatsapp
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(WPP_Link)
    
# função de enviar mensagens
def message(nome,mensagem):
    new_msg_button = driver.find_element_by_xpath(NEW_MSG_BUTTON)
    new_msg_button.click()
    sleep(1)
    search_field = driver.find_element_by_xpath(SEARCH_CONTACT_FIELD)
    search_field.click()
    search_field.send_keys(nome)
    sleep(1)
    first_contact = driver.find_element_by_xpath(FIRST_CONTACT)
    first_contact.click()
    sleep(1)
    type_field = driver.find_element_by_xpath(TYPE_FIELD)
    type_field.click()
    type_field.send_keys("Olá, ", nome, "! O seu código é: ",mensagem)
    send_button = driver.find_element_by_xpath(SEND_BUTTON)
    send_button.click()
    sleep(1)

data = pd.read_excel("contatos.xlsx")

for i in range(len(data)):
    message(str(data['nome'][i]),str(data['código'][i]))