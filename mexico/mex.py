#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import gzip
from io import BytesIO
import asyncio
from aiohttp import ClientSession, TCPConnector, ClientTimeout
import time
import re
import os
import numpy as np

""" Bot who gets the booking hotels from Mexico formating their outputs for
English characters. """

""" Api Urls and empty lists for data """
apartah = ["https://www.booking.com/sitembk-themed-city-gostinicy-index.xml",
"https://www.booking.com/sitembk-themed-city-guest_house-index.xml",
"https://www.booking.com/sitembk-themed-city-hanting_express-index.xml",
"https://www.booking.com/sitembk-themed-city-hilton-index.xml",
"https://www.booking.com/sitembk-themed-city-holidayhomes-index.xml",
"https://www.booking.com/sitembk-themed-city-holidayinn-index.xml",
"https://www.booking.com/sitembk-themed-city-holidaypark-index.xml",
"https://www.booking.com/sitembk-themed-city-home_inn-index.xml",
"https://www.booking.com/sitembk-themed-city-home_stay-index.xml",
"https://www.booking.com/sitembk-themed-city-hostels-index.xml",
"https://www.booking.com/sitembk-themed-city-ibis-index.xml",
"https://www.booking.com/sitembk-themed-city-inn-index.xml",
"https://www.booking.com/sitembk-themed-city-jacuzzi-index.xml",
"https://www.booking.com/sitembk-themed-city-lodge-index.xml",
"https://www.booking.com/sitembk-themed-city-love_hotel-index.xml",
"https://www.booking.com/sitembk-themed-city-luxury-index.xml",
"https://www.booking.com/sitembk-themed-city-marriott-index.xml",
"https://www.booking.com/sitembk-themed-city-mercure-index.xml"]

apartahotels_list, reviews, links, themes, descriptions, titles, locations, hotels_scrap, final_links, formated_links = [], [], [], [], [], [], [], [], [], []
argentina = re.compile(r"/mx/")
argentina_sitemap = re.compile(r"-mx")
params = {
    'lang': 'en-gb',
    'sb_price_type': 'total',
    'type': 'total',
    'lang_click': 'other',
    'lang_changed': '1',
}

def get_soup(url):
    """ Get the soup object for urls """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_hotel_data(hotel_lists):
    """ Get hotels links and append to lists """
    response = requests.Session().get(url=hotel_lists, params=params).text
    soup = BeautifulSoup(response, 'lxml')
    try:
        link_find = soup.find_all('header', {'class': 'bui-spacer--medium'})
        for ad_link in link_find:
            ad_link = ad_link.a['href']
            if ad_link.startswith('/hotel') and not None:
                f_link = "https://www.booking.com" + ad_link
                formated_links.append(f_link)
            else:
                continue
    except:
        pass

def extract_selectors(soup, selector):
    """ Avoid NoneType object don't have attribute failure """
    try:
        return soup.find(selector)
    except:
        return None


def get_each_hotel_data(link, url):
    """ Get hotels data and append to lists """
    soup = BeautifulSoup(link, 'lxml')
    try:
        description = soup.find(id="property_description_content").text
        title = soup.find(id="hp_hotel_name").h2.text
        theme = soup.find(id="hp_hotel_name").div.text
        description = re.sub(r"You're eligible for a Genius discount.*all you have to do is sign in.", '', description)
        if (description and title and theme and url) != None:
            if 'ñ' not in description:
                descriptions.append(description)
            else:
                descriptions.append(np.nan)
            if 'ñ' not in title:
                titles.append(title)
            else:
                titles.append(np.nan)
            if 'ñ' not in theme:
                themes.append(theme)
            else:
                themes.append(np.nan)
            final_links.append(url)
        else:
            pass
    except:
        pass

def make_df():
    """ Make pandas dataframe to manipulate data """
    df = pd.DataFrame({'Themes': themes,'Listing_url': final_links, 'Description': descriptions, 'Title': titles
    })
    return df

def make_excel(df):
    """ Make excel file from dataframe """
    if os.path.exists('mexico_first_step.xlsx'):
        df_source = pd.read_excel('mexico_first_step.xlsx')
        vertical_concat = pd.concat([df_source, df], axis=0)
        vertical_concat.drop_duplicates(keep='first')
        vertical_concat.to_excel("mexico_first_step.xlsx", index=False)
    else:
        df.to_excel('mexico_first_step.xlsx', index=False)

def get_links(xml):
    """ Get the links from the page """
    format_links = []
    soup = BeautifulSoup(xml, features='xml')
    links = soup.find_all('loc')
    for link in links:
        if argentina.findall(str(link)):
            link = link.text
            format_links.append(link)
        else:
            continue
    return format_links

def get_sitemap(site_url):
    """ Get sitemap to obtain later the links. """
    resp = requests.get(site_url)
    return resp.content

def descompress_sitemap(site_response):
    """ Get a byte object and decompress to read the links """
    with BytesIO(site_response) as file:
        with gzip.open(file, 'rb') as f:
            file_data = f.read()
            return file_data

def fetch_async_1(urls):
    """ Function who coordinates the coroutines for data """
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all_1(urls))
    loop.run_until_complete(future)

async def fetch_all_1(urls):
    """ Function who make task pool """
    tasks = []
    connector = TCPConnector(force_close=True, limit_per_host=10)
    async with ClientSession(connector=connector) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch_1(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)

async def fetch_1(url, session):
    """ Function to return response object from url to fill the tasks """
    if url != None:
        try:
            async with session.get(url=url, params=params) as response:
                r = await response.text()
                return get_each_hotel_data(r, url)
        except:
            pass

def themed_country(site_list):
    start = 0
    apartahotel = get_soup(str(site_list)).loc
    for regions in apartahotel:
        sitemap_response = get_sitemap(regions)
        final_regions = descompress_sitemap(sitemap_response)
        links_to_regions = get_links(final_regions)
        if links_to_regions:
            for first in links_to_regions:
                get_hotel_data(first)
                time.sleep(8) # with 20 works
        format_1 = formated_links[:int(len(formated_links)/5)]
        number = len(format_1)
        format_2 = formated_links[int(number):(int(number*2))]
        format_3 = formated_links[int(len(format_1*2)):int(len(format_1*3))]
        format_4 = formated_links[int(len(format_1*3)):int(len(format_1*4))]
        format_5 = formated_links[int(len(format_1*4)):]
        fetch_async_1(format_2)
        df = make_df()
        df_droped = df.drop_duplicates().dropna()
        make_excel(df_droped)
        print("first_part_done")
        time.sleep(15)
        fetch_async_1(format_3)
        df = make_df()
        df_droped = df.drop_duplicates().dropna()
        make_excel(df_droped)
        print("second_part_done")
        time.sleep(16)
        fetch_async_1(format_4)
        df = make_df()
        df_droped = df.drop_duplicates().dropna()
        make_excel(df_droped)
        print("third_part_done")
        time.sleep(18)
        fetch_async_1(format_5)
        df = make_df()
        df_droped = df.drop_duplicates().dropna()
        make_excel(df_droped)
        print("fourth_part_done")
        time.sleep(14)
        fetch_async_1(format_1)
        df = make_df()
        df_droped = df.drop_duplicates().dropna()
        make_excel(df_droped)
        print("fifth_part_done")
        time.sleep(20)

if __name__=='__main__':
    for i in apartah:
        time.sleep(22)
        print(i)
        themed_country(i)
