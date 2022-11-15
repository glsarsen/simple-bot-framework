import csv
import json


with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

with open("questions.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(("tag", "responses", "answer", "patterns"))
    for element in data["intents"]:
        row = (element["tag"], element["responses"], "", *element["patterns"])
        writer.writerow(row)
