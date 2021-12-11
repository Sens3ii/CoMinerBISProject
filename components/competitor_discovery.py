from components.utils import get_patterns, json_file_to_dict, create_unique_list
from components.pattern_extractors import get_pattern_extractors
import numpy
import re


# for each pattern we get data
def get_data_by_pattern(entity, pattern):
    data = json_file_to_dict(f'data/{entity}/{pattern}.json')
    list_of_data = []
    for res in data:
        if 'title' in res:
            list_of_data.append(res['title'])
        if 'content' in res:
            list_of_data.append(res['content'])
    return list_of_data


# for each pattern we get list of competitors
def get_competitors_by_pattern(entity, pattern, list_of_data):
    pattern_extractors = get_pattern_extractors()
    return pattern_extractors[pattern](list_of_data, entity)


# math count of competitor multyply by weight
def get_weight(competitors_by_pattern, pattern_weight, competitor):
    return pattern_weight * competitors_by_pattern.count(competitor)


# weight for each competitor (weights from the article)
def calculate_weights(patterns_and_competitors):
    unique_competitors = create_unique_list(patterns_and_competitors)
    competitor_and_weight = dict()
    for competitor in unique_competitors:
        competitor_and_weight[competitor] = get_weight(
            patterns_and_competitors['C1'], 5, competitor) 
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['C2'], 5, competitor)
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['C3'], 1, competitor)
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['C4'], 1, competitor)
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['H1'], 1, competitor)
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['H2'], 1, competitor)
        competitor_and_weight[competitor] += get_weight(
            patterns_and_competitors['H3'], 1, competitor)
    return competitor_and_weight

# Pointwise mutual info
def pmi(dataset, entity, competitor):
    search_data = " ".join(dataset)
    cnt = 0
    for sentence in dataset:
        cnt += len(re.findall(r' {entity} [a-z][a-z] {competitor}'.format(
            entity=entity, competitor=competitor), sentence))
        cnt += len(re.findall(r' {competitor} [a-z][a-z] {entity}'.format(
            entity=entity, competitor=competitor), sentence))
        cnt += len(re.findall(r' {competitor} [a-z][a-z] {entity}'.format(
            entity=entity, competitor=competitor), sentence))
        cnt += len(re.findall(r' {competitor} [a-z][a-z][a-z] {entity}'.format(
            entity=entity, competitor=competitor), sentence))
    hits_ce = cnt
    hits_c = len(re.findall(r'\b{}(\b)'.format(competitor), search_data))
    hits_e = len(re.findall(r'\b{}\b'.format(entity), search_data))
    return hits_ce / (hits_e * hits_c)


def candidate_confidence(dataset, competitor, patterns_and_competitors):
    search_data = " ".join(dataset)
    competitor_and_weights = calculate_weights(patterns_and_competitors)[competitor] 
    counter = len(
        re.findall(r'\b{}\b'.format(competitor), search_data))
    return competitor_and_weights / counter


def confidence_score(competitor, entity, patterns_and_competitors, patterns_and_data):
    dataset = numpy.concatenate(list(patterns_and_data.values()))
    r = calculate_weights(patterns_and_competitors)

    k1 = 0.2 * r.get(competitor)

    k2 = 0.6 * pmi(dataset, entity, competitor)

    k3 = 0.2 * candidate_confidence(dataset,
                                    competitor, patterns_and_competitors)

    return k1 + k2 + k3


def get_ranked_competitors(entity, patterns_and_data, patterns_and_competitors):
    unique_competitors = create_unique_list(patterns_and_competitors)
    competitors_and_score = {}
    for competitor in unique_competitors:
        competitors_and_score[competitor] = confidence_score(
            competitor, entity, patterns_and_competitors, patterns_and_data)
    # sort by score
    return dict(sorted(competitors_and_score.items(), key=lambda item: item[1], reverse=True))


def get_competitor_list(entity):
    print("[GET] Comptetitor list")
    patterns = get_patterns()

    patterns_and_data = dict()
    for key, value in patterns.items():
        patterns_and_data[key] = get_data_by_pattern(entity, key)

    patterns_and_competitors = dict()
    for key, value in patterns_and_data.items():
        patterns_and_competitors[key] = get_competitors_by_pattern(
            entity, key, value)

    ranked_competitors = get_ranked_competitors(
        entity, patterns_and_data, patterns_and_competitors)

    return ranked_competitors
