import csv
import os

from django.conf import settings

from users.models import CustomUser

CSV_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


def read_to_DB(filename, DBclass):
    filepath = os.path.join(CSV_DIR, filename)
    with open(filepath, 'r') as f:
        reader = list(csv.reader(f))
        reader.pop(0)
        for row in reader:
            print(f'{row[0]} {row[1]} {row[2]} {row[3]}')
            howto_create(DBclass, row)


def howto_create(DBclass, row):
    if DBclass == CustomUser:
        kwargs = {'pk': int(row[0]), 'username': row[1], 'email': row[2],
                  'role': row[3]}
    DBclass.objects.create(**kwargs)


read_to_DB('users.csv', CustomUser)
