# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas
import re
import time


def fetch_model(link_description):
    if link_description is not None:
        for model in models:
            if model in link_description:
                return model
    else:
        return None


def has_sequence(link_text):
    pos = 0
    numbers = []
    number = ""
    while pos != len(link_text):
        if link_text[pos] != " ":
            try:
                val = int(link_text[pos])
                number = number + str(val)
            except ValueError:
                pos += 1
                number = ""
                continue
        elif number != "":
            numbers.append(number)
            number = ""
        else:
            pass

        pos += 1

    return numbers


base_url = "https://www.nairaland.com/autos"
site_url = base_url
records = []
matches = ["toyota", "toks", "tokunbo", "auction"]
models = ["toyota", "honda", "bmw", "lexus", "kia", "peugeot", "mercedes",
          "chevrolet", "range rover", "suzuki", "dodge", "ford", "nissan",
          "benz", "hyundai", "volks", "audi", "infiniti", "rolls royce",
          "mazda", "land rover", "infinity"]

for page in range(1, 4, 1):
    request = requests.get(site_url,
                           headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux '
                                                  'x86_64;rv:61.0) Gecko/20100101 '
                                                  'Firefox/61.0'})
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    main_table = soup.find("table", {"id": None})
    table_rows = main_table.find_all("tr")

    for row in table_rows:
        link = row.find_all("a")
        main_link = link[1]
        name_link = link[0]

        price = 0

        """if any(x in main_link.text.lower() for x in matches):
            print(name_link.get("name"), " -- ", main_link.text, matches) """

        identified_make = fetch_model(main_link.text.lower())
        link_numbers = has_sequence(main_link.text + " ")
        year = None
        phone_number = None
        for numb in link_numbers:
            if len(numb) == 4:
                year = numb
            elif len(numb) >= 11:
                phone_number = numb

        price_list = re.findall("\d+\.\d+", main_link.text)
        if len(price_list) > 0:
            price = price_list[0]

        if link[0].get("name"):
            data_row = {"record_id": link[0].get("name"), "make": identified_make, "model": " ",
                        "year": year, "description": main_link.text.lower(), "price": price,
                        "phone_number": phone_number}
            records.append(data_row)
        site_url = base_url + "/" + str(page)  # ensures we will be navigating to the next page on our next iteration

date_now = time.strftime("%m_%d_%Y_%H%M%S", time.localtime())
data_frame = pandas.DataFrame(records)
# print(data_frame)
data_frame.to_csv("~/Documents/scraped_data/scrape_" + date_now + "_output.csv")
