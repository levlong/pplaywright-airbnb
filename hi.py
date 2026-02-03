a = {"name": "Long", "age1": 12, "address": "no where"}

def ok(**z):
    print(z.pop("age", None))

ok(**a) 