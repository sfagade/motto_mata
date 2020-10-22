# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas
import re
import time
from app_util import fetch_vehicle_make, load_properties, fetch_vehicle_model


def start_processing():
    prop_json = load_properties()

    site_url = prop_json['sites']['auto']
    records = []

    for page in range(1, 10, 1):
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

            price = '0'

            """if any(x in main_link.text.lower() for x in matches):
                print(name_link.get("name"), " -- ", main_link.text, matches) """

            identified_make = fetch_vehicle_make(main_link.text.lower())
            identified_model = fetch_vehicle_model(main_link.text.lower())
            # link_numbers = has_sequence(main_link.text + " ")
            link_numbers = re.findall(r"(?:[\d\.\,]{1,})", main_link.text)
            print("checking: ", main_link.text)
            print('Found: ', link_numbers)
            year = None
            phone_number = None
            for numb in link_numbers:
                if len(numb) == 4 and numb.startswith('20'):  # most of the time four digit numbers are the vehicle year
                    year = numb
                elif len(numb) == 11 and numb.startswith("0"):
                    phone_number = numb
                elif '.' in numb and '..' not in numb or ',' in numb:  # this is either float amount of currency amount
                    price = numb
                else:
                    print("Did not find use for numbers")

            if price == '0' or price == '.':
                price_list = re.findall('\d+\.\d+', main_link.text)  # find all number with dot in-between them
                if len(price_list) > 0:
                    price = price_list[0]
            if price == '0' or price == '.':
                # find every amount that ends with m indicating million
                price_list = re.search(r'\d{1,4}[m]', main_link.text.replace('matic', '').replace('month',''))
                if price_list:
                    print("trying to pick: ", price_list)
                    price = price_list[0].replace('m', '')

            if link[0].get("name") and identified_make and year:
                data_row = {"record_id": link[0].get("name"), "make": identified_make, "model": identified_model,
                            "year": year, "description": main_link.text.lower(), "price": price,
                            "phone_number": phone_number}
                records.append(data_row)
            # ensures we will be navigating to the next page on our next iteration
            site_url = prop_json['sites']['auto'] + "/" + str(page)

    date_now = time.strftime("%m_%d_%Y_%H%M%S", time.localtime())
    data_frame = pandas.DataFrame(records)
    # print(data_frame)
    data_frame.to_csv("~/Documents/scraped_data/scrape_" + date_now + "_output.csv")
