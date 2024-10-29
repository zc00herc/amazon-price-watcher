from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

header = {
    "Accept-Language": "en-US",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

WEBSITE = "https://www.amazon.com/dp/B01NBKTPTS?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

response = requests.get(WEBSITE,headers=header)
response.raise_for_status()
html = response.text

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
FROM_NUM = os.getenv("FROM_NUM")
TO_NUM = os.getenv("TO_NUM")

client = Client(TWILIO_SID,TWILIO_AUTH)

soup = BeautifulSoup(html, "html.parser")
dollars = soup.find(class_="a-price-whole")
dollar_int = int(dollars.text.split(".")[0])
cents = soup.find(class_="a-price-fraction")
cents_int = int(cents.text)
price = float(f"{dollar_int}.{cents_int}")
print(price)
if price < 100:
    message = client.messages.create(
                body=f"Price of {price} is below set price of $100",
                from_= FROM_NUM,
                to= TO_NUM
            )