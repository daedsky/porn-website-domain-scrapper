from bs4 import BeautifulSoup
import requests
import re


def allpronsites_dot_net():
    source = requests.get('https://allpornsite.net/').content

    soup = BeautifulSoup(source, 'lxml')
    divs = soup.find_all('div', attrs={'class': 'link-list'})

    all_sites = []
    for div in divs:
        lists = div.find_all('li')
        for li in lists:
            site = li.find('a', attrs={'class': 'site-link'}).attrs['href']
            all_sites.append(site)

    return all_sites


def remove_https_and_beautify():
    sites = allpronsites_dot_net()

    result = []

    for site in sites:
        site = site.strip()
        if site.startswith('https://') and 'www.' not in site:
            res = site.replace('https://', 'www.').strip().removesuffix('/').strip()
        elif site.startswith('https://') and 'www.' in site:
            res = site.replace('https://', '').strip().removesuffix('/').strip()

        elif site.startswith('http://') and 'www.' not in site:
            res = site.replace('http://', 'www.').strip().removesuffix('/').strip()
        elif site.startswith('http://') and 'www.' in site:
            res = site.replace('http://', '').strip().removesuffix('/').strip()

        else:
            res = site

        if '/' in res:
            slash_idx = res.index('/')
            _res = res[:slash_idx]
        else:
            _res = res

        result.append(_res)

    return result


def confirm():  # confirm that they are websites
    sites = remove_https_and_beautify()

    pattern = 'w{3}\..+\..'

    result = []

    for site in sites:
        if re.match(pattern, site):
            result.append(site)

    return result


if __name__ == '__main__':
    sites = confirm()
    print(sites)
