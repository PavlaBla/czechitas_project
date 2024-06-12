import pandas as pd
import csv


data = []
with open("all_in_one.csv", mode="r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        data.append(line)

# nacte soubor do seznamu 'data'

headers = data[0]
data = data[1:]
df = pd.DataFrame(data, columns=headers)

# vytvori dataframe a oddeli hlavicku od dat

cities = [
    "Praha",
    "Brno",
    "Ostrava",
    "Plzeň",
    "Liberec",
    "Olomouc",
    "České Budějovice",
    "Hradec Králové",
    "Pardubice",
    "Ústí nad Labem",
    "Karlovy Vary",
    "Jihlava",
    "Zlín",
]

arrangements = ["1+0", "1+kk", "1+1", "2+kk", "2+1", "3+kk", "3+1", "4+1", "4+kk"]

# seznamy mest a dispozici, ktere nas zajimaji

filtered_data = []
for index, row in df.iterrows():
    condition_1 = "idnes" not in row["data_url"]
    condition_2 = "apartment" in row["data_type"]
    condition_3 = "auction" not in row["data_offerType"]
    condition_4 = any(city.lower() in row["data_address"].lower() for city in cities)
    condition_5 = row["data_arrangement"] in arrangements
    if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
        filtered_data.append(row)

filtered_df = pd.DataFrame(filtered_data)

# filtruje data podle zadanych podminek a ulozi je do noveho dataframe

columns = [
    "createdAt",
    "data_priceTotal",
    "data_price",
    "data_priceType",
    "data_arrangement",
    "data_livingArea",
    "data_address",
    "data_energyClass",
    "id",
    "data_city",
    "data_buildingType",
    "data_district",
    "data_offerType",
    "data_equipment",
    "data_ownership",
    "data_propertyState",
    "data_type",
    "data_url",
    "isLive",
    "markAsDeadAt",
]
all_in_one_df = filtered_df[columns]

# ulozi jen vypsane sloupce


def extract_realitka(url):
    parts = url.split(".")
    if len(parts) > 1:
        return parts[1]
    return None


all_in_one_df["realitka"] = all_in_one_df["data_url"].apply(extract_realitka)

# extrahuje nazev realitniho webu z URL

new_columns = [
    col[5:] if col.startswith("data_") else col for col in all_in_one_df.columns
]
all_in_one_df.columns = new_columns

# odstrani prefix 'data_' z nazvu sloupcu


def determine_city(row):
    address = str(row["address"])
    parts = address.split(",")
    for city in cities:
        if address.lower().startswith(city.lower()) and len(address.split()[0]) == len(
            city
        ):
            return city
        if city.lower() in parts[0].lower():
            return city
        if len(parts) > 1 and city.lower() in parts[1].lower():
            if not parts[1].lower().lstrip().startswith("okres"):
                return city


all_in_one_df["city"] = all_in_one_df.apply(determine_city, axis=1)

# urci mesto podle sloupce adresy a zalozi novy sloupce 'city'

cleaned_data = all_in_one_df.dropna(subset=["city", "price"])

cleaned_data = cleaned_data.drop(columns=["address", "url"])

# odstrani radky s prazdnymi hodnotami a prebytecne sloupce

cleaned_data.to_csv("all_in_one_output.csv", index=False)

# ulozi vycisteny dataframe do csv

with open("all_in_one_output.csv", mode="r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        data.append(line)

# nacte vysledny soubor pro provedeni kontroly
