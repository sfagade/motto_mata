import json


def load_properties():
    with open('properties.json') as prop_file:
        prop_json = json.load(prop_file)
        return prop_json


def fetch_model(link_description):
    """This function is used to fetch the vehicle make of the vehicle from the description string"""
    prop_json = load_properties()
    if link_description is not None:
        for model in prop_json['vehicle_makes']:
            if model in link_description:
                return model
    else:
        return None


def has_sequence(link_text):
    """This function is used to fetch numbers matching a sequence to fetch either the year of phone number"""
    print("Processing sequence for:\n ", link_text)
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
    print("found ", numbers)
    return numbers
