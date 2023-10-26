import datetime as dt
from random import randint

N_ROWS = 10_000_000

Q1_DATA = [
    {
        "ship_date": dt.datetime(1995 + randint(0, 10), 9, 2),
        "quantity": i,
        "extended_price": 0.1 * i,
        "discount": 1 - (0.1 * i),
        "tax": (1 - (0.1 * i)),
        "line_status": "shipped" if i < N_ROWS / 3 else "pending",
        "returned": not i < N_ROWS / 2,
    }
    for i in range(N_ROWS)
]

if __name__ == "__main__":
    data = Q1_DATA
