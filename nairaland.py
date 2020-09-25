# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas
import re


def fetch_model(link_description):
    if link_description is not None:
        for model in models:
            if model in link_description:
                return model
    else:
        return None


base_url = "https://www.nairaland.com/autos"
site_url = base_url
records = []
matches = ["toyota", "toks", "tokunbo", "auction"]
models = ["toyota", "honda", "bmw", "lexus", "kia", "peugeot", "mercedes", "chevrolet", "range rover"]

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

        identified_model = fetch_model(main_link.text.lower())
        price_list = re.findall("\d+\.\d+", main_link.text.lower())
        if len(price_list) > 0:
            price = price_list[0]

        data_row = {"record_id": link[0].get("name"), "model": identified_model,
                    "description": main_link.text.lower(), "price": price}
        records.append(data_row)
        site_url = base_url + "/" + str(page)

data_frame = pandas.DataFrame(records)
data_frame.to_csv("test_output.csv")
