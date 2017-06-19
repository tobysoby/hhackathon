import json
import pandas as pd
import numpy as np
import spacy
import re
import requests
import json
from pprint import pprint
from datetime import date
from datetime import datetime
from datetime import timedelta

nlp = spacy.load('en')

import sys
from collections import Counter
import argparse
from geotext import GeoText
import pycountry


def get_data(page_id, token):
    '''


    :param page_id: page id of the facebook feed
    :param token: token for the facebook Graph Api

    return: list of facebook posts containing the relevant information
    '''
    feed = requests.get(
        'https://graph.facebook.com/v2.9/' + page_id + '/posts?access_token=' + token + '&limit=100&fields=message,id,from,type,picture,link,created_time,updated_time')

    posts = []
    ninety_days = timedelta(days=90)
    start_date = date.today() - ninety_days
    feed_json = feed.json()
    # print feed_json['paging']['next']



    posts = feed_json['data']
    # start_date needs a time also
    start_date = datetime.combine(start_date, datetime.min.time())
    pprint(start_date)
    pprint(feed_json['data'][-1]['created_time'])
    pprint(datetime.parse(posts['data'][-1]['created_time']))

    last_date = datetime.combine(date.today(), datetime.min.time())
    while (last_date > start_date):
        last_date = datetime.strptime(feed_json['data'][-1]['created_time'][:-5], "%Y-%m-%dT%H:%M:%S")
        pprint(last_date)
        feed = requests.get(feed_json['paging']['next'])
        feed_json = feed.json()
        posts += feed_json['data']
    return posts


def preprocess_text(text):
    '''

    :param text: text to clean
    :return: cleaned text
    '''
    out = text
    try:
        out = text.replace(u"'s", u"")
        out = out.replace(u"-", u" ")
    except:
        pass
    return out


def get_named_entities(text):
    '''

    :param text
    :return: named entities given by the spacy model
    '''
    out = []
    try:
        doc = nlp(text)
        out = [{'label':ent.label_, 'text':ent.text} for ent in doc.ents]
    except:
        pass
    return out

def countries_from_nes(ne_list):
    cities = []
    countries = []
    for ne in ne_list:
        if ne['label'] in ['NORP', 'LOC', 'GPE']:
            places = GeoText(ne['text'])
            cities = cities + places.cities
            countries = countries + places.country_mentions.keys()
    return cities, countries

def alpha2_to_alpha3(old_key):
    if old_key == "XK":
        new_key = "RKS"
        name = 'Kosovo'
    else:
        country = pycountry.countries.get(alpha_2=old_key)
        new_key = country.alpha_3
        name = country.name
    return new_key, name

def a3_to_name(a3):
    if a3 == "RKS":
        name = 'Kosovo'
    else:
        country = pycountry.countries.get(alpha_3=a3)
        name = country.name
    return name


def build_data(posts):
    '''


    :param posts: post data returned by the Graph Api
    :return: relevant dataframes
    '''
    df = pd.DataFrame(posts)
    df['time'] = pd.to_datetime(df.created_time) # get datetime
    df['cleaned_text'] = df.message.apply(preprocess_text) # clean text
    df['named_entities'] = df.cleaned_text.apply(get_named_entities) # get named entities
    df['Persons'] = df.named_entities.apply(lambda x: [ne['text'] for ne in x if ne['label'] == 'PERSON']) # get persons

    cities = []
    countries = []
    for ne in df.named_entities:
        cities_plus, countries_plus = countries_from_nes(ne)
        cities = cities + cities_plus
        countries = countries + countries_plus

    countries_new = []
    country_names = []
    for c in countries:
        a3, name = alpha2_to_alpha3(c)
        countries_new.append(a3)
        country_names.append(name)

    df_countries = pd.DataFrame(Counter(countries_new).most_common())
    df_countries.columns = ['a3', 'number']
    df_countries['log_number'] = np.log(df_countries.number)
    df_countries['country'] = df_countries.a3.apply(a3_to_name)

    df_cities = pd.DataFrame(Counter(cities).most_common())
    df_cities.columns = ['city', 'number']

    df_cities.drop_duplicates(inplace=True)

    return df, df_countries, df_cities

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pageid', metavar='pageid', type=int,
                        help='the facebook page id')
    parser.add_argument('-t', '--token', metavar='token', type=int,
                        help='the facebook Graph Api token')
    token = parser.parse_args().token
    page_id = parser.parse_args().pageid

    posts = get_data(page_id=page_id, token=token)
    df, df_countries, df_cities = build_data(posts=posts)
    df_countries.to_csv('countries_log.csv', encoding='utf-8', index=False)