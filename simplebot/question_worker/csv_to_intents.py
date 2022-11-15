import csv
import json
import os

data = {
    "intents": [],
}

with open("questions.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    _ = next(reader)
    for tag, responses, *patterns in reader:
        patterns = [elem for elem in patterns if elem]
        data["intents"].append(
            {"tag": tag, "responses": responses, "patterns": patterns}
        )

for i in range(100):
    try:
        os.rename(
            "intents.json", os.path.join("static", "intents", f"intents_old_{i}.json")
        )
        break
    except FileExistsError:
        continue
    except FileNotFoundError:
        break

with open("intents.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)
