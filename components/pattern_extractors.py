import json
import re
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


# Filter array of words by nltk
def filter_stop_words(arr):
    ans = []
    for word in arr:
        if word.lower() not in stop_words:
            ans.append(word)
    return ans


def get_first_element(arr):
    return arr[0]


def get_second_element(arr):
    return arr[1]


def get_by_c1(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    results = re.findall(
        r'(\b[A-Z][a-zA-Z]*\b) (vs|VS|Vs|versus)\.? {}'.format(entity_name), dataset)
    ans = list(map(get_first_element, results))
    return filter_stop_words(ans)


def get_by_c2(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    results = re.findall(r'{} (vs|VS|Vs|versus)\.? (\b[A-Z][a-zA-Z]*\b)'.format(entity_name),
                         dataset)
    ans = list(map(get_second_element, results))
    return filter_stop_words(ans)


def get_by_c3(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    results = re.findall(
        r'{} or (\b[A-Z][a-zA-Z]*\b)'.format(entity_name), dataset)
    return filter_stop_words(results)


def get_by_c4(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    results = re.findall(
        r'(\b[A-Z][a-zA-Z]*\b) or {}'.format(entity_name), dataset)
    return filter_stop_words(results)


def get_by_h1(dataset_list, entity_name):
    dataset = " ".join(dataset_list)

    arr = re.findall(
        r'such as {},? (\b[A-Z][a-zA-Z]*\b \b[A-Z][a-zA-Z]*\b|\b[A-Z][a-zA-Z]*\b)'.format(entity_name), dataset)
    return filter_stop_words(arr)


def get_by_h2(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    arr = re.findall(
        r'especially {},? (\b[A-Z][a-zA-Z]+\b)'.format(entity_name), dataset)
    return filter_stop_words(arr)


def get_by_h3(dataset_list, entity_name):
    dataset = " ".join(dataset_list)
    arr = re.findall(
        r'including {},? (\b[A-Z][a-zA-Z]+\b)'.format(entity_name), dataset)
    return filter_stop_words(arr)


def get_pattern_extractors():
    pattern_extractors = {
        "C1": get_by_c1,
        "C2": get_by_c2,
        "C3": get_by_c3,
        "C4": get_by_c4,
        "H1": get_by_h1,
        "H2": get_by_h2,
        "H3": get_by_h3,
    }
    return pattern_extractors
