import requests
import json
from components.utils import data_to_file





def get_search_res(entity, pattern_code, query):
    print(f"[GET] Search results of query: {query} ")
    pages_res = []
    for page_num in range(1, 5):
        r = requests.get(f'https://searx.roughs.ru/search?q={query}&language=en&pageno={page_num}&format=json')
        pages_res = pages_res + r.json()['results']

    list_of_results = []
    for res in pages_res:
        _dict = dict()
        if 'title' in res:
            _dict['title'] = res['title']
        if 'content' in res:
            _dict['content'] = res['content']
        list_of_results.append(_dict)

    data_json = json.dumps(list_of_results, ensure_ascii=False, indent=4)
    data_to_file(data_json, folder=entity, file=pattern_code+'.json')










