from imap_tools import MailBox, AND
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv("EMAIL")
password_app = os.getenv("PASS_APP")
netflix_password = os.getenv("PWD")

print(f'Avvio in corso... {datetime.now().ctime()}',end='\r')

def get_url():
    with MailBox('imap.gmail.com').login(email, password_app) as mailbox:
        # Fetch delle email con il soggetto specificato e ordina in modo che l'ultima email sia la prima della lista
        for msg in mailbox.fetch(AND(subject='Importante: come aggiornare il tuo Nucleo domestico Netflix'), reverse=True):
            html = msg.html
            # Utilizzo di BeautifulSoup per estrarre l'URL dalla pagina HTML dell'email
            page = bs(html, 'html5lib')
            url_tag = page.find('a', {'class': 'h5'})
            if url_tag:
                return url_tag.get('href')
    return None

def accept(url):
    try:
        driver.get(url)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="appMountPoint"]/div/div/div/div/div[2]/div/div/div/div[4]/button').click()
        pass
    except:
        pass

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')  # Aggiungere questo per evitare l'errore di sandboxing su Colab
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

old_url = ''
while True:
    time.sleep(2)
    url = get_url()
    if url != old_url:
        # go to the site
        driver.get('https://www.netflix.com/browse')
        time.sleep(5)
        # accept cookies
        try:
            driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            pass
        time.sleep(1)
        # login into netflix
        driver.find_element(By.ID, ":r0:").send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, ':r3:').send_keys(netflix_password)
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="appMountPoint"]/div/div/div/div/div[2]/div/form/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/div/div[2]/button').click()
        time.sleep(1)
        print(f'Richiesta ricevuta... {datetime.now().ctime()}',end='\r')
        accept(url)
        print(f'Richiesta accettata. {datetime.now().ctime()}',end='\r')
        
    else:
        print(f'Nessuna nuova richiesta... {datetime.now().ctime()}',end='\r')
        pass
    old_url = url
