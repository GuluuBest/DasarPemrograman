from datetime import datetime

tahun_ini = datetime(2025, 9, 13)
data = [
    {"name": "Nugraha", "birthdate": "1989-09-13"},
    {"name": "John", "birthdate": "1990-01-01"},
    {"name": "Jane", "birthdate": "1992-02-02"},
    {"name": "Doe", "birthdate": "1994-03-03"},
]

print(f"{'No':<5} {'Name':<10} {'Age':<5}")

for index, person in enumerate(data, start=1):
    birthdate = datetime.strptime(person["birthdate"], "%Y-%m-%d")
    age = tahun_ini.year - birthdate.year - ((tahun_ini.month, tahun_ini.day) < (birthdate.month, birthdate.day))
    print(f"{index:<5} | {person['name']:<10} | {age:<5}")