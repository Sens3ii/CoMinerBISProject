import requests
import json
from bs4 import BeautifulSoup
from const import __queries
from search_api import get_data


def get_hearst_queries(entity, domain=""):
    queries = [item.replace("{EN}", entity) for item in __queries]
    return queries


def competitor_discovery(entity, domain=""):
    print("[DISCOVERY] Competitor discovery")
    competitor_list = []
    candidate_extraction(entity, domain)
    return competitor_list


def candidate_extraction(entity, domain=""):
    print("[EXTRACTION] Candidate extraction")
    # queries = get_hearst_queries(entity, domain)
    # for q in queries:
    #     get_data(q, entity)
    

competitor_discovery("Toyota")
