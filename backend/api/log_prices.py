import csv
from pathlib import Path
from .schemas import Item

LOG_FILE = Path("items_log.csv")

def log_item(item: Item):
    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists: #only write the header once
            writer.writerow(["item_name", "quantity", "unit"])

        writer.writerow([item.name, item.quantity, item.unit])

