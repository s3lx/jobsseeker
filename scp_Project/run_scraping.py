import os, sys
from django.db import DatabaseError
from django.contrib.auth import get_user_model
import asyncio
import datetime as dt

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django
django.setup()

from scraping.parsers import get_parse
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = ((get_parse,'get_parse'),)
jobs, errors = [], []

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['language_id'],) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['language_id'],): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['language'] = pair[0]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls

async def main(value):
    func, url, language = value
    job, err =  await loop.run_in_executor(None, func, url, language)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['language'])
            for data in url_list
            for func, key in parsers]

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors':errors})
        err.save()
    else:
        er = Error(data=f'errors{errors}').save()

ten_days_ago = dt.date.today() - dt.timedelta(10)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()