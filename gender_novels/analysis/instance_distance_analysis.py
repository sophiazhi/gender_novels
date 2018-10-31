from gender_novels.corpus import Corpus
from statistics import median, mean

import numpy as np
import matplotlib.pyplot as plt
from gender_novels.analysis.analysis import male_instance_dist, female_instance_dist, pronoun_instance_dist
from gender_novels import common
#import seaborn as sns
#sns.set()

#def process_medians(lst1 ,lst2):
 #   return

#TO-DO - get medians, means, max and min instance distances per novel per gender


def run_distance_analysis(corpus):
    """
    Takes in a corpus of novels. Return a dictionary with each novel mapped to an array of 3 lists:
     - median, mean, min, and max distances between male pronoun instances
     - median, mean, min, and max distances between female pronoun instances
     - for each of the above stats, the difference between male and female values. (male stat- female stat for all stats)
        POSITIVE DIFFERENCE VALUES mean there is a LARGER DISTANCE BETWEEN MALE PRONOUNS and therefore
        HIGHER FEMALE FREQUENCY.
    dict order: [male, female]

    :param corpus:
    :return:dictionary where the key is a novel and the value is the results of distance analysis
    """
    results = {}
    for novel in corpus:
        print(novel.title, novel.author)
        male_results = male_instance_dist(novel)
        female_results = female_instance_dist(novel)

        male_stats = get_stats(male_results)
        female_stats = get_stats(female_results)

        diffs = {}
        for stat in range(0, 4):
            stat_diff = list(male_stats.values())[stat] - list(female_stats.values())[stat]
            diffs[list(male_stats.keys())[stat]] = stat_diff

        novel.text = ""
        novel._word_counts_counter = None
        results[novel] = {'male': male_stats, 'female': female_stats, 'difference': diffs}

    return results


def store_raw_results(results, corpus_name):
    try:
        common.load_pickle("instance_distance_raw_analysis_" + corpus_name)
        x = input("results already stored. overwrite previous analysis? (y/n)")
        if x == 'y':
            common.store_pickle(results, "instance_distance_raw_analysis_" + corpus_name)
        else:
            pass
    except IOError:
        common.store_pickle(results, "instance_distance_raw_analysis_" + corpus_name)


def get_stats(distance_results):
    """
    list order: median, mean, min, max
    :param distance_results:
    :return: dictionary of stats
    """
    if len(distance_results) == 0:
        return {'median': 0, 'mean': 0, 'min': 0, 'max': 0}
    else:
        return {'median': median(distance_results), 'mean': mean(distance_results), 'min': min(distance_results),
                'max': max(distance_results)}

def results_by_author_gender(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary that maps
    'male' (male author) and 'female' (female author) to a list of difference values from novels written by an author of
    that gender. The dictionary bins difference values from one of the stats (median, mean, min, max) depending on which
    metric is specified in parameters
    :param results dictionary, a metric ('median', 'mean', 'min', 'max')
    :return: list of dictionaries, each with two keys: 'male' (male author) or 'female' (female author). Each key maps
    a list of difference stats for each novel.
    """
    data = {'male': [], "female": []}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")
    for novel in list(results.keys()):
        if novel.author_gender == "male":
            data['male'].append(results[novel]['difference'][metric])
        else:
            data['female'].append(results[novel]['difference'][metric])
    return data

def results_by_date(results, metric):
    """
    takes in a dictionary of results and a specified metric from run_distance_analysis, returns a dictionary that maps
    different time periods to a list of difference values from novels written by an author of
    that gender. The dictionary bins difference values from one of the stats (median, mean, min, max) depending on which
    metric is specified in parameters
    :param results:
    :param metric: either 'median', 'mean', 'min', or 'max'
    :return: dictionary
    """
    data = {}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")

    date_to_1810 = []
    date_1810_to_1819 = []
    date_1820_to_1829 = []
    date_1830_to_1839 = []
    date_1840_to_1849 = []
    date_1850_to_1859 = []
    date_1860_to_1869 = []
    date_1870_to_1879 = []
    date_1880_to_1889 = []
    date_1890_to_1899 = []
    date_1900_on = []

    for k in list(results.keys()):
        if k.date < 1810:
            date_to_1810.append(results[k]['difference'][metric])
        elif k.date < 1820:
            date_1810_to_1819.append(results[k]['difference'][metric])
        elif k.date < 1830:
            date_1820_to_1829.append(results[k]['difference'][metric])
        elif k.date < 1840:
            date_1830_to_1839.append(results[k]['difference'][metric])
        elif k.date < 1850:
            date_1840_to_1849.append(results[k]['difference'][metric])
        elif k.date < 1860:
            date_1850_to_1859.append(results[k]['difference'][metric])
        elif k.date < 1870:
            date_1860_to_1869.append(results[k]['difference'][metric])
        elif k.date < 1880:
            date_1870_to_1879.append(results[k]['difference'][metric])
        elif k.date < 1890:
            date_1880_to_1889.append(results[k]['difference'][metric])
        elif k.date < 1900:
            date_1890_to_1899.append(results[k]['difference'][metric])
        else:
            date_1900_on.append(results[k]['difference'][metric])

    data['date_to_1810'] = date_to_1810
    data['date_1810_to_1819'] = date_1810_to_1819
    data['date_1820_to_1829'] = date_1820_to_1829
    data['date_1830_to_1839'] = date_1830_to_1839
    data['date_1840_to_1849'] = date_1840_to_1849
    data['date_1850_to_1859'] = date_1850_to_1859
    data['date_1860_to_1869'] = date_1860_to_1869
    data['date_1870_to_1879'] = date_1870_to_1879
    data['date_1880_to_1889'] = date_1880_to_1889
    data['date_1890_to_1899'] = date_1890_to_1899
    data['date_1900_on'] = date_1900_on

    return data


def results_by_location(results, metric):
    """

    :param results:
    :param metric:
    :return:
    """
    data = {}
    metric_indexes = {"median": 0, "mean": 2, "min": 3, "max": 4}
    try:
        stat = metric_indexes[metric]
    except:
        print("Not valid metric name. Valid names: 'median', 'mean', 'min', 'max'")

    location_UK = []
    location_US = []
    location_other = []

    for k in list(results.keys()):
        if k.country_publication in ["United Kingdom", "England", "Scotland", "Wales"]:
            location_UK.append(results[k]['difference'][metric])
        elif k.country_publication == 'United States':
            location_US.append(results[k]['difference'][metric])
        else:
            location_other.append(results[k]['difference'][metric])

    data = {}

    data['location_UK'] = location_UK
    data['location_US'] = location_US
    data['location_other'] = location_other

    return data


def run_analysis(corpus_name):
    print("loading corpus")
    corpus = Corpus(corpus_name)
    novels = corpus.novels

    print("running analysis")
    results = run_distance_analysis(novels)

    print("storing results")
    store_raw_results(results, corpus_name)


def analyze_raw_results(corpus_name):
    try:
        raw_results = common.load_pickle("instance_distance_raw_analysis_" + corpus_name)
    except IOError:
        print("No raw results available for this corpus")
    #ANALYSIS STUFF


if __name__ == '__main__':
    run_analysis("gutenberg")
    r = common.load_pickle("instance_distance_raw_analysis_gutenberg")
    r2 = results_by_location(r, "mean")
    r3 = results_by_author_gender(r, "mean")
    r4 = results_by_date(r, "median")
    r5 = results_by_location(r, "median")
    r6 = results_by_author_gender(r, "median")
    r7 = results_by_date(r, "median")

    common.store_pickle(r2, "instance_distance_mean_differences_by_location")
    common.store_pickle(r3, "instance_distance_mean_differences_by_author_gender")
    common.store_pickle(r4, "instance_distance_mean_differences_by_date")

    common.store_pickle(r5, "instance_distance_median_differences_by_location")
    common.store_pickle(r6, "instance_distance_median_differences_by_author_gender")
    common.store_pickle(r7, "instance_distance_median_differences_by_date")

