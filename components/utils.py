import json
import os
import numpy 


def get_patterns():
    return {
        'C1': 'vs {EN}',
        'C2': '{EN} vs',
        'C3': 'or {EN}',
        'C4': '{EN} or',
        'H1': 'such as {EN} * or OR and',
        'H2': 'especially {EN},',
        'H3': 'including {EN},',
    }



def json_file_to_dict(filename):
    with open(file=filename, mode='r', encoding='utf-8') as json_file:
        dict_ = json.load(json_file)
        return dict_



def data_to_file(data, folder, file, mode_="w"):
    print(f"[DATA TO FILE] data/{folder}/{file}")
    try:
        os.makedirs(f"data/{folder}")
    except FileExistsError:
         pass
    with open(file=f"data/{folder}/{file}", mode=mode_, encoding='utf-8') as outfile:
        outfile.write(data)


def create_unique_list(list_):
    return list(set(list(numpy.concatenate(
        list(list_.values())))))


def is_word(word):
    if(len(word) > 17): # sometimes there is some trash
        return False
    return word.isalpha() 



# Filtering the phrase that is entity or competitor name
def has_intersection(phrase, competitors_list, entity_name):
    entity_name = entity_name.lower()
    phrase = phrase.lower()
    if entity_name in phrase or phrase in entity_name:
        return True
    for competitor in competitors_list:
        if len(competitor) > 2 and competitor.lower() in phrase.lower():
            return True
        if len(phrase) > 2 and phrase.lower() in competitor.lower():
            return True
    return False


# minimum distance between w1 and w2 in s
def distance(s, w1, w2):
    s, w1, w2 = [item.lower() for item in [s, w1, w2]]
    if w1 == w2:
        return 0
    words = s.split()
    min_dist = len(words) + 1
    for index in range(len(words)):
        if words[index] == w1:
            for search in range(len(words)):
                if words[search] == w2:
                    curr = abs(index - search) - 1
                    if curr < min_dist:
                        min_dist = curr
    return min_dist

