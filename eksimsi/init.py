import sys

from constants import MIN_ENTRY_ID, MAX_ENTRY_ID
from models import Entry

arg = int(sys.argv[1])

MIN = MIN_ENTRY_ID
MAX = arg if arg else MIN_ENTRY_ID

for i in range(MIN, MAX):
    print(i)
    Entry.create(eksi_id=i)
