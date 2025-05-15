import datetime
from .storage import get_latest_serial_with_prefix, save_record_to_db, init_db

MONTH_LETTER_MAP = {
    1: 'A', 2: 'B', 3: 'C', 4: 'D',
    5: 'E', 6: 'F', 7: 'G', 8: 'H',
    9: 'I', 10: 'J', 11: 'K', 12: 'L'
}

init_db()


def generate_pack_serial(bms_serial, capacity_code="14"):
    now = datetime.datetime.now()
    year = str(now.year)[-2:]
    month_letter = MONTH_LETTER_MAP.get(now.month, 'X')
    prefix = f"{year}{month_letter}{capacity_code}"

    latest_serial = get_latest_serial_with_prefix(prefix)

    if latest_serial:
        seq_num = int(latest_serial[-3:]) + 1
    else:
        seq_num = 1

    new_serial = f"{prefix}{seq_num:03d}"

    save_record_to_db(new_serial, bms_serial)

    return new_serial
