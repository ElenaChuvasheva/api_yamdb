import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

CSV_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')

filename = 'users.csv'
filepath = os.path.join(CSV_DIR, filename)

with open(filepath, 'r') as f:
    reader = list(csv.reader(f))
    reader.pop(0)
    for row in reader:
        print(f'{row[0]} {row[1]} {row[2]}')
        User.objects.create(pk=int(row[0]), username=row[1], email=row[2])
