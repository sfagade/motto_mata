# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas
import re
import time
from app_util import fetch_vehicle_make, load_properties, fetch_vehicle_model
from data_connection import check_record_exist, save_new_record


def start_processing():
    prop_json = load_properties()

    site_url = prop_json['sites']['auto']
    records = []
    created_at = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
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
            ref_link = link[1].get("href")

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
                price_list = re.search(r'\d{1,4}[m]', main_link.text.replace('matic', '').replace('month', ''))
                if price_list:
                    print("trying to pick: ", price_list)
                    price = price_list[0].replace('m', '')

            data_row = {}

            if link[0].get("name") and identified_make and year:
                views_tag = row.find("span", {"class": "s"}).find_all("b")[2]
                post_by = row.find("span", {"class": "s"}).find("b").find("a").text
                if not check_record_exist(link[0].get("name")):
                    data_row = {"record_id": link[0].get("name"), "make": identified_make, "model": identified_model,
                                "year": year, "price": price, "description": main_link.text.lower(), "url": ref_link,
                                "views": views_tag.text, "posted_by": post_by, "phone_number": phone_number,
                                "created_at": created_at}
                    save_new_record(data_row)
                else:
                    print("Record exist in our database")

                records.append(data_row)
            # ensures we will be navigating to the next page on our next iteration
            site_url = prop_json['sites']['auto'] + "/" + str(page)

    data_frame = pandas.DataFrame(records)
    date_now = time.strftime("%m_%d_%Y_%H%M%S", time.localtime())
    data_frame.to_csv("~/Documents/scraped_data/scrape_" + date_now + "_output.csv")
    print("Total records: ", len(records))
