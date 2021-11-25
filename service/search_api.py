import requests
import json
from bs4 import BeautifulSoup


def save_to_json(data, filename="data/data.json", mode="w"):
    with open(file=filename, mode=mode, encoding='utf-8') as outfile:
        outfile.write(data)


def save_query_results(filename="data/data.json", query=""):
    r = requests.get(
        f'https://searx.roughs.ru/search?q={query}&format=json')
    data_json = json.dumps(r.json(), ensure_ascii=False, indent=4)
    save_to_json(data_json)


def get_dict(filename="data/data.json"):
    with open(file=filename, mode='r', encoding='utf-8') as json_file:
        json_dict = json.load(json_file)
        return json_dict


def save_urls(filename="data/data.json"):
    json_dict = get_dict(filename="data/data.json")
    urls = [res['url'] for res in json_dict["results"]]
    json_string = json.dumps(urls, ensure_ascii=False, indent=4)
    save_to_json(json_string, filename="data/urls.json")


def get_data_from_url(urls_path="data/urls.json"):
    json_dict = get_dict(urls_path)
    data_list = []
    for url in json_dict:
        print(url)
        r = requests.get(url).text
        formatted = BeautifulSoup(r, 'html.parser').get_text()
        data_list.append(formatted)
    json_string = json.dumps(data_list, ensure_ascii=False, indent=4)
    save_to_json(json_string, filename="data/pages.json")


# save_query_results(query="Toyota")
# save_urls()
get_data_from_url()
