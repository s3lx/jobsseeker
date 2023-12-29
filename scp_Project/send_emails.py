import os, sys
import django
import datetime
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth import get_user_model

from config.settings import EMAIL_HOST_USER

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

django.setup()
from scraping.models import Vacancy, Error, Url

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f"Job's newsletter for {today}"
text_content = f"'Job's newsletter {today}"
from_email = EMAIL_HOST_USER
empty = '<h2> Unfortunately there is no news for today </h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('language', 'email')
users_dct = {}

for i in qs:
    users_dct.setdefault((i['language'],),[])
    users_dct[(i['language'],)].append(i['email'])

if users_dct:
    params = {'language_id__in': []}
    for pair in users_dct.keys():
        params['language_id__in'].append(pair[0])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['language_id'],),[])
        vacancies[(i['language_id'],)].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


qs = Error.objects.filter(timestamp=today)
subject = ''
ext_content = ''
to = ADMIN_USER
_html = ""

if qs.exists():
    error = qs.first()
    data = error.data['errors']
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject += f"Scraping error{today}"
    text_content += "Scraping error"
    data = error.data['user_data']
    if data:
        _html += '<hr>'
        _html += '<hr2> User request</hr2>'
        for i in data:
            _html += f'<p"> Language: {i["language"]}  and Email:{i["email"]}</p><br>'
        subject += f"User request{today}"
        text_content += "User request"


qs = Url.objects.all().values('language',)
urls_dct = {(i['language'],): True for i in qs}
urls_err = ''

for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0]:
            urls_err += f'<p"> For language {keys[0]} there is no url</p><br>'

if urls_err:
    subject += 'Missing urls'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()

