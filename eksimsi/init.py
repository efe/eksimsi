from constants import MIN_ENTRY_ID, MAX_ENTRY_ID
from models import Entry

for i in range(MIN_ENTRY_ID, MAX_ENTRY_ID):
    print(i)
    Entry.create(eksi_id=i)
