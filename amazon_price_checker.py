import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib


def send_mail(url, actual_price, product_price):
    my_email = "your email"
    my_password = "sample password"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="to email",
                            msg=f"Subject:LIVE!!!!!This Product has a Discount Now!!\n\n"
                                f"PRODUCT LINK:{url}\nORIGINAL PRICE: Rs{actual_price}\n"
                                f"OFFER PRICE: Rs{product_price}")


def check_existing_product():
    data = pd.read_csv("data.csv")
    df = pd.DataFrame(data)

    header = {
        "Accept-Language": "en-GB,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    for index, row in df.iterrows():
        actual_price = int(row["ActualPrice"])
        price_user_want = int(row["DiscountedPrice"])

        url = f"https://www.amazon.in/dp/{row['ProductCode']}"
        response = requests.get(url, headers=header)
        website_data = response.text
        data = BeautifulSoup(website_data, "lxml")
        product_price = data.find(class_="a-price-whole").text
        product_price = int(product_price.replace(",", "").split(".")[0])

        if product_price <= price_user_want:
            send_mail(url, actual_price, product_price)


check_existing_product()
