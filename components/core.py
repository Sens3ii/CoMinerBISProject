from components.utils import get_patterns, json_file_to_dict
from components.search_api import get_search_res

from components.competitor_discovery import get_competitor_list
from components.domain_mining import get_domain_list
patterns = get_patterns()


def start(entity):

    # COMPETITOR DISCOVERY

    # Getting query results
    # for key, value in patterns.items():
    #     get_search_res(entity, key, value.replace("{EN}", entity))
    
    # Results
    competitor_list = get_competitor_list(entity)
    print(f"[COMPETITORS]\nEntity: {entity}")
    for i in list(competitor_list.keys())[0:6]:
        print(i, competitor_list[i])


    # DOMAIN DISCOVERY

    # Getting query results
    # for competitor in list(competitor_list)[:6]:
    #     get_search_res(entity, competitor, f'{entity} {competitor}')

    # Results
    domain_list = get_domain_list(entity, list(competitor_list)[:6])
    for i in list(domain_list.keys())[0:12]:
        print(i, domain_list[i])
