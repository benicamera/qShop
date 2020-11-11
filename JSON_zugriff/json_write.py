import json

i = 0xe900
i = int(i)
i = str(i)

j = 0xe901
j = int(j)
j = str(j)

with open("data.json", "w") as obj:

    data = {
        "tomate": i,
        "apfel": j
    }
    json.dump(data, obj, indent=4)

with open("data.json", "r") as obj:
    data = json.load(obj)

    for g in data:
        alt_i = data[g]
        alt_i = int(alt_i)
        alt_i = hex(alt_i)
        print(alt_i)
