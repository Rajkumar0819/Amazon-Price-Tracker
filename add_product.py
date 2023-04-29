import requests
from bs4 import BeautifulSoup
import csv
import os


def add_data(code, price, discounted_price):
    if os.path.isfile("data.csv"):
        data = [str(code), price, discounted_price]
        file = open("data.csv", mode="a", newline="")
        writer = csv.writer(file)
        writer.writerow(data)

    else:
        data = [
            ["ProductCode", "ActualPrice", "DiscountedPrice"],
            [str(code), price, discounted_price]
        ]
        file = open("data.csv", mode="w", newline="")
        writer = csv.writer(file)
        writer.writerows(data)

    print("Data added successfully you'll get a mail once the product has discounts")


# getting the url
url = str(input("Enter the Amazon Product Url: "))
code_value = url.index("B0")
code_value = url[code_value:(code_value + 10)]

# getting the price of the product using WebScraping
header = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=header)
website_data = response.text

soup_data = BeautifulSoup(website_data, "lxml")

product_price = soup_data.find(class_="a-price-whole").text
product_price = int(product_price.replace(",", "").split(".")[0])
print(f"Product Price is: {product_price}")

# getting the Discounted amount the user wants it to go to receive a notification
amount = int(input("Enter the amount at which we can send a notification mail:"))

add_data(code_value, product_price, amount)
