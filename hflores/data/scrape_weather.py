#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Enforce path
sys.path.insert(0, os.getcwd())
sys.path.insert(1, os.path.join(os.path.pardir, os.getcwd()))

YESTERDAY = datetime.date.today() - datetime.timedelta(days=1)
NOW = '{:%Y-%m-%d-%H:%M:%S}'.format(datetime.datetime.now())
LOGDIR = path.join('data/jpn_weather/', NOW)


STATES = ['Ibaraki',
          'Tochigi',
          'Gumma',
          'Saitama',
          'Chiba',
          'Tokyo',
          'Kanagawa',
          'Yamanashi',
          'Shizuoka']


def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    coord = dms2dd(parts[0], parts[1], parts[2], parts[3])
    return coord


def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_states(url):
    soup = get_soup(url)
    hrefs = {state: state.parent['href'] for state in soup(text=STATES)}

    # Strip unnecessary './' from map link
    for state, link in hrefs.items():
        hrefs[state] = re.sub(r'./', '', link)

    # Append state map link to root url
    for state, link in hrefs.items():
        hrefs[state] = re.sub(r'index.html', link, url)
    return hrefs


def get_areas(url):
    soup = get_soup(url)
    hrefs = {a['alt']: a['href'] for a in soup.findAll('area')}

    # Get yesterdays data for full 24 hour
    for area, link in hrefs.items():
        hrefs[area] = re.sub(r'today', 'yesterday', link)

    # Append area link to root url
    for area, link in hrefs.items():
        hrefs[area] = re.sub(r'map.+', link, url)
    return hrefs


def get_coords(cline):
    cline = re.sub(r'\s+', '', cline[0]).split(';')
    cline = [re.sub(r'.*:', '', c) for c in cline]
    cline[-1] = re.sub(r'm', '', cline[-1])
    return (parse_dms(cline[0]), parse_dms(cline[1]), cline[-1])


# TODO: refactor and more robust to states/cities that have different fields
def get_data(url, state, city):
    soup = get_soup(url)

    # Get lat, lon, and altitude from page
    cline = soup(text=re.compile(r'Latitude'))
    lat, lon, alt = get_coords(cline)

    # Extract table
    table = soup.find('table', id='tbl_list')
    rows = [row for row in table if row != '\n']

    # Create data from rows
    has_temp = False
    data = []
    for hr, r in enumerate(rows):
        if hr == 0:  # Check for temp field
            field = r.findAll(class_='block')[0]
            has_temp = field.get_text() == 'Temperature'
        elif hr == 1:
            continue
        else:  # Collect data
            stamp = '{} {}:00:00'.format(YESTERDAY, str(hr - 1))
            cols = [state, city, lat, lon, alt, stamp]

            if not has_temp:
                val = r.findAll(class_='block')[0].get_text()
                cols += ['NaN', val, 'NaN', 'NaN', 'NaN']
            else:
                for b in r.findAll(class_='block'):
                    val = b.get_text()
                    cols += [val] if val != '\xa0' else ['NaN']
            data.append(cols)
    return data


if __name__ == '__main__':
    url = 'http://www.jma.go.jp/en/amedas_h/index.html'
    states_hrefs = get_states(url)
    areas_hrefs = [(p, get_areas(h)) for p, h in states_hrefs.items()]
    data = [get_data(url, state, city)
            for state, cities in areas_hrefs for city, url in cities.items()]

    flattened_data = [city for state in data for city in state]
    df = pd.DataFrame(flattened_data)

    columns = ['state', 'city', 'latitude', 'longitude', 'altitude', 'time',
               'temperature', 'precipitation', 'wind_direction', 'wind_speed',
               'sunshine_duration', 'humidity', 'pressure']
    df.columns = columns
    df.to_csv(LOGDIR, index=False)
