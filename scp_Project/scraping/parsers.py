from random import randint

import requests
import codecs
from bs4 import BeautifulSoup as BS

__all__ = ('get_parse',)

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           ]

def get_parse(url, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0,2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'inner-right search-results-items'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-list-item'})
                # a = 1
                for div in div_lst:
                    link = div.find('div', attrs={'class': 'inner-left company-logo-wrap'})
                    href = link.a['href']
                    company_name =  link.span.text
                    link_two = div.find('div', attrs={'class': 'inner-right listing-content-wrap'})
                    sub_link_two = div.find('div', attrs={'class': 'title-date-wrap'})
                    title = sub_link_two.h6.text
                    content = sub_link_two.h6.text
                    jobs.append({'title': title, 'url': href,
                                 'description': content, 'company': company_name,
                                 'language_id': language})
            else:
                errors.append({'url': url, 'title': " Div does not exists "})

        else:
            errors.append({'url': url, 'title': "Page doesn't response "})

        return jobs, errors


if __name__ == '__main__':
    url = 'https://dev.bg/?s=python&post_type=job_listing'
    jobs, errors = get_parse(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
