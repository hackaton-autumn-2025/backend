from datetime import datetime
from random import randint


def get_traffic_level_by_time() -> int:
    hour = datetime.now().time().hour
    return randint(
        (8 if 7 <= hour < 10 else
         7 if 17 <= hour < 20 else
         5 if 12 <= hour < 14 else
         1 if 23 <= hour or hour < 6 else 4),
        (10 if 7 <= hour < 10 else
         9 if 17 <= hour < 20 else
         7 if 12 <= hour < 14 else
         3 if 23 <= hour or hour < 6 else 6)
    )
