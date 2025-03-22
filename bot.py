import requests
from bs4 import BeautifulSoup
import telegram
import schedule
import time

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
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Przykład, jak znaleźć karty graficzne (możesz dostosować selektory CSS do strony)
        items = soup.find_all('div', class_='product-item')  # To może się różnić w zależności od struktury strony
        
        for item in items:
            name = item.find('a', class_='product-name').get_text(strip=True)
            link = item.find('a', class_='product-name')['href']
            
            # Jeśli znajdziesz produkt, wyślij powiadomienie
            bot.send_message(chat_id=CHAT_ID, text=f'Nowa karta graficzna: {name}\nLink: {link}')

# Funkcja, która uruchamia sprawdzanie co jakiś czas
def job():
    check_outlet()

# Zaplanuj, aby funkcja `job` była uruchamiana co 10 minut
schedule.every(10).minutes.do(job)

# Pętla, która uruchamia bota
while True:
    schedule.run_pending()
    time.sleep(1)
