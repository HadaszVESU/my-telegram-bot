import requests
from bs4 import BeautifulSoup
import telegram
import schedule
import time
import logging

# Ustawienie logowania
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Twój token bota z Telegrama
TOKEN = '7636796167:AAGKR_CnqQKul9wS7V1No05hCs5aJWgkUws'
CHAT_ID = '6255040286'  # Twój chat_id z userinfobot

# URL-e stron, które będziemy monitorować
URLS = [
    'https://www.euro.com.pl/karty-graficzne,stan-outlet-doskonaly:outlet-dobry.bhtml',
    'https://www.oleole.pl/karty-graficzne,stan-outlet-doskonaly:outlet-dobry.bhtml'
]

# Inicjalizacja bota Telegrama
bot = telegram.Bot(token=TOKEN)

# Funkcja do sprawdzania stron
def check_outlet():
    for url in URLS:
        logging.info(f'Rozpoczynam monitorowanie strony: {url}')
        response = requests.get(url)
        
        # Sprawdzamy, czy odpowiedź z serwera jest poprawna
        if response.status_code != 200:
            logging.error(f'Błąd podczas pobierania strony {url}. Kod odpowiedzi: {response.status_code}')
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Przykład, jak znaleźć karty graficzne (możesz dostosować selektory CSS do strony)
        items = soup.find_all('div', class_='product-item')  # To może się różnić w zależności od struktury strony
        
        if not items:
            logging.info(f'Brak nowych produktów na stronie {url}.')
        
        for item in items:
            name = item.find('a', class_='product-name').get_text(strip=True)
            link = item.find('a', class_='product-name')['href']
            
            # Jeśli znajdziesz produkt, wyślij powiadomienie
            message = f'Nowa karta graficzna: {name}\nLink: {link}'
            logging.info(f'Wysyłam powiadomienie: {message}')
            bot.send_message(chat_id=CHAT_ID, text=message)

# Funkcja, która uruchamia sprawdzanie co jakiś czas
def job():
    check_outlet()

# Funkcja wysyłająca powiadomienie, że bot działa
def send_status():
    test_message = "Bot działa poprawnie i monitoruje strony!"
    logging.info(f'Wysyłam testową wiadomość: {test_message}')
    bot.send_message(chat_id=CHAT_ID, text=test_message)

# Zaplanuj, aby funkcja `job` była uruchamiana co 10 minut
schedule.every(10).minutes.do(job)

# Zaplanuj, aby funkcja `send_status` była uruchamiana co 29 minut
schedule.every(29).minutes.do(send_status)

# Pętla, która uruchamia bota
logging.info('Bot uruchomiony i działa 24/7.')
while True:
    schedule.run_pending()
    time.sleep(1)
