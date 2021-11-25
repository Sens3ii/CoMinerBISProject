import requests
import json
from bs4 import BeautifulSoup
import urllib.request
from inscriptis import get_text


def data_to_file(data, path, mode_="w"):
    print(f"[DATA TO FILE] data/{path}")
    with open(file=f"data/{path}", mode=mode_, encoding='utf-8') as outfile:
        outfile.write(data)


def get_search_res(query):
    print(f"[GET] Search results {query} ")
    r = requests.get(f'https://searx.roughs.ru/search?q={query}&format=json')
    data_json = json.dumps(r.json(), ensure_ascii=False, indent=4)
    data_to_file(data_json, "search_page.json")


def get_urls_from_search_page():
    print(f"[GET] URLs from search results")
    search_page_dict = json_file_to_dict("data/search_page.json")
    urls = [res['url'] for res in search_page_dict["results"]]
    data_json = json.dumps(urls, ensure_ascii=False, indent=4)
    data_to_file(data_json, "urls.json")


def json_file_to_dict(filename):
    print(f"[CONVERT] JSON file to dict {filename}")
    with open(file=filename, mode='r', encoding='utf-8') as json_file:
        dict_ = json.load(json_file)
        return dict_


def get_data_from_url():
    print(f"[GET] Data from URLs")
    urls_dict = json_file_to_dict("data/urls.json")
    data_list = []
    for url in urls_dict:
        print(f"[GET] Data from URL: {url}")
        try:
            html = urllib.request.urlopen(url).read().decode('utf-8')
            text = get_text(html)
            text = ' '.join(text.split())
            data_to_file(text, "data.txt", "a")
        except:
            print(f"[ERROR] Data from URL: {url}")


# get_search_res(query="Toyota")
# get_urls_from_search_page()
get_data_from_url()
