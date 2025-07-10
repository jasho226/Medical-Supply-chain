
from datetime import date

date1 = date(2024, 3, 20)
date2 = date(2024, 3, 16)

if date1 < date2:
    print("date1 comes before date2")
elif date1 > date2:
    print("date1 comes after date2")
else:
    print("date1 and date2 are the same")
