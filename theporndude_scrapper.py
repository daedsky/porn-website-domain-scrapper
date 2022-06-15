from bs4 import BeautifulSoup
import requests


def get_webpage(url):
    webpage = requests.get(url,
                           proxies={
                               'http': 'http://163.172.98.25:80'
                           }).content.decode('utf-8')
    return webpage


def get_sites_list(webpage):
    soup = BeautifulSoup(webpage, 'lxml')

    a_tags = soup.findAll('a', {'class': 'link'})

    sites_list = []
    for a_tag in a_tags:
        if 'data-site-link' in str(a_tag):
            site = a_tag['data-site-link']
            sites_list.append(site)

    return sites_list


def remove_http(sites_list):
    # remove https or https form their prefix
    porn_sites = []
    for site in sites_list:
        if 'https://' in site:
            site = site.removeprefix('https://')
        elif 'http://' in site:
            site = site.removeprefix('http://')
        if '/' == site[-1]:
            site = site.removesuffix('/')

        porn_sites.append(site)

    return porn_sites


def remove_www(porn_sites):
    ps = []
    for site in porn_sites:
        if 'www.' in site:
            site = site.removeprefix('www.')
        ps.append(site)

    return ps


def remove_url_after_slash(ps):
    # remove things after slash
    _porn_sites = []
    for site in ps:
        if '/' in site:
            site = site[:site.index('/')]
        _porn_sites.append(site)
    return _porn_sites


def main():
    # webpage should be the category. eg: https://theporndude.com/category_url
    webpage = get_webpage('https://theporndude.com/best-escort-sites')
    sites_list = get_sites_list(webpage)
    without_http = remove_http(sites_list)
    without_www = remove_www(without_http)
    porn_sites = remove_url_after_slash(without_www)

    final_porn_sites = list(set(porn_sites))

    print(final_porn_sites)
    print(len(final_porn_sites))


if __name__ == '__main__':
    main()
