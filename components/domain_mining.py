from components.utils import json_file_to_dict, is_word, has_intersection, distance
import nltk
import numpy
from nltk.corpus import wordnet
import re
import math


main_entity = ''
main_competitors = []



# for each pattern we get data
def get_data_of_competitor(entity, competitor):
    data = json_file_to_dict(f'data/{entity}/{competitor}.json')
    list_of_data = []
    for res in data:
        if 'title' in res:
            list_of_data.append(res['title'])
        if 'content' in res:
            list_of_data.append(res['content'])
    return list_of_data



def phrase_extract(description):
    global main_entity, main_competitors
    arr = nltk.pos_tag(nltk.word_tokenize(description))
    ans = []
    for i in range(len(arr)-1):
        first_word_info = list(arr[i])
        second_word_info = list(arr[i+1])
        first_word, first_word_pos = first_word_info
        second_word, second_word_pos = second_word_info
        first_word = first_word.lower()
        second_word = second_word.lower()
        if is_word(first_word) and not has_intersection(first_word, main_competitors, main_entity) :
            if first_word_pos in ['NN', 'NNP', 'VP'] and len(first_word) > 3:
                if first_word_pos in ['NNS', 'NNPS','NNP','VBZ'] and len(first_word) > 3 and (first_word[-1]=='s'):
                    first_word = first_word[0:len(first_word) - 1]
                ans.append(first_word)
            if first_word_pos in ['VBG', 'JJ', 'NN', 'NNP', 'VP'] and second_word_pos in ['NN', 'NNP', 'VP', 'NNS','NNPS']:
                if is_word(second_word) and not has_intersection(second_word, main_competitors, main_entity):
                    if second_word_pos in ['NNS', 'NNPS','NNP','VBZ'] and (second_word[-1]=='s'):
                        second_word = second_word[0:len(second_word)-1]
                    ans.append((f'{first_word} {second_word}'))
    return list(set(ans))


def get_phrase(descriptions):
    return list(numpy.concatenate(list(map(phrase_extract, descriptions))))


def get_phrases_list(competitors_data_list):
    return list(set(list(numpy.concatenate(list(map(get_phrase, competitors_data_list))))))



def get_descriptions_list(competitors_data_list):
    return list(numpy.concatenate(competitors_data_list))


def phrase_frequency(phrase, descriptions_list):
    data = ' '.join(descriptions_list)
    descriptions_word_array = nltk.word_tokenize(data.lower())
    return descriptions_word_array.count(phrase.lower())



def document_frequency(phrase, descriptions_list):
    cnt = 0
    for description in descriptions_list:
        description_word_array = nltk.word_tokenize(description.lower())
        if phrase.lower() in description_word_array:
            cnt += 1
    return cnt


def phrase_length(phrase):
    return len(phrase.lower().split(' '))


def average_distance(phrase, entity, competitors_and_data):
    sum = 0
    n = 0
    for c_name in competitors_and_data.keys():
        for description in competitors_and_data.get(c_name):
            description = description.lower()
            phrase = phrase.lower()
            try:
                if re.search(r'\W' + phrase + r'\W', description) != None:
                    if ' ' in phrase:
                        p_new = phrase.replace(" ", '')
                        description = description.replace(phrase, p_new)
                        phrase = p_new

                    sum += (distance(description, entity, phrase) + distance(description, c_name, phrase))
                    n += 1
            except:
                return 45454

    if n == 0:
        return 12345

    return sum/(2*n)

def phrase_independence(phrase, descriptions_list):
    appearment_list = []
    for description in descriptions_list:
        if(phrase in description):
            appearment_list.append(description)
    left_terms = set()
    right_terms = set()

    for description in appearment_list:
        description = description.lower()

        s = description.index(phrase)
        e = s + len(phrase)
        left_side = nltk.word_tokenize(description[0:s])
        right_side = nltk.word_tokenize(description[e:len(description)])

        for l in left_side:
            if(is_word(l)):
                left_terms.add(l)
        for r in right_side:
            if(is_word(r)):
                right_terms.add(r)
    PL, PR = 0, 0
    PF = len(appearment_list)
    left_terms = list(left_terms)
    right_terms = list(right_terms)
    for term in left_terms:
        F = len(re.findall(r'\b{}\b'.format(term), ' '.join(left_terms)))
        logga = 0
        if(PF !=0 and F!=0):
            logga = math.log2(F/ PF)
        PL += F/PF * logga
    for term in right_terms:
        F = len(re.findall(r'\b{}\b'.format(term), ' '.join(right_terms)))
        logga = 0
        if(PF !=0 and F!=0):
            logga = math.log2(F/ PF)
        PR += F/PF * logga
    return (PR+PF)/2



def get_domain_list(entity, competitors):
    print("[GET] Domain list")
    global main_entity, main_competitors

    main_entity = entity
    main_competitors = competitors

    competitors_and_data = dict()
    for competitor in competitors:
        competitors_and_data[competitor] = get_data_of_competitor(entity, competitor)
    
    competitors_data_list = list(competitors_and_data.values())
    phrases_list = get_phrases_list(competitors_data_list)
    descriptions_list = get_descriptions_list(competitors_data_list)
    
    dict_ = {}
    index_ = 0
    print(f"[STATS] Phrases count: {len(phrases_list)}")

    for phrase in phrases_list:
        index_ += 1
        print(f"[Analysis] {index_} - {phrase}", end="\r")
        dict_[phrase] = phrase_frequency(phrase, descriptions_list) * 0.14
        dict_[phrase] += document_frequency(phrase, descriptions_list) * 0.06
        dict_[phrase] += phrase_length(phrase) * 0.23
        dict_[phrase] += average_distance(phrase, entity, competitors_and_data) * (-0.075)
        dict_[phrase] += phrase_independence(phrase, descriptions_list) * 0.19

    domains_rating = dict(sorted(dict_.items(), key=lambda item: item[1], reverse=True))

    return domains_rating




    