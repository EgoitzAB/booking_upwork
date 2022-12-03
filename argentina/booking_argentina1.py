import requests
from bs4 import BeautifulSoup
import asyncio
from aiohttp import ClientSession, TCPConnector, ClientTimeout
import pandas as pd
import time
params = {
    'lang': 'en-gb',
    'sb_price_type': 'total',
    'type': 'total',
    'lang_click': 'other',
    'lang_changed': '1',
}

all_urls, second_urls, main_urls, descriptions, themes, final_links, titles = [], [], [], [], [], [], []
mexico = "https://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggI46AdIM1gEaDqIAQGYAQq4ARnIAQ_YAQHoAQH4AQuIAgGoAgO4ArWs35sGwAIB0gIkOTdiNzg2YmUtZTFhZi00YjU1LTk2ZWYtNzRmNDM1MmQzZDc42AIG4AIB&sid=ce9848fa247d1a75778d6553de0a79d7&aid=304142&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.es.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaDqIAQGYAQq4ARnIAQ_YAQHoAQH4AQuIAgGoAgO4ArWs35sGwAIB0gIkOTdiNzg2YmUtZTFhZi00YjU1LTk2ZWYtNzRmNDM1MmQzZDc42AIG4AIB%26sid%3Dce9848fa247d1a75778d6553de0a79d7%26sb_price_type%3Dtotal%26%26&ss=M%C3%A9xico&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&efdco=1&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=mexico&ac_position=2&ac_langcode=es&ac_click_type=b&ac_meta=GhA4OTU3ODU5YWQ2ZTAwMDU4IAIoATICZXM6Bm1leGljb0AASgBQAA%3D%3D&dest_id=137&dest_type=country&place_id_lat=23.3446&place_id_lon=-102.188&search_pageview_id=8957859ad6e00058&search_selected=true&search_pageview_id=8957859ad6e00058&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0&offset=25"

def get_each_hotel_data(link, url):
    """ Get hotels data and append to lists """
    soup = BeautifulSoup(link, 'lxml')
    try:
        description = soup.find(id="property_description_content").text
        descriptions.append(description)
        title = soup.find(id="hp_hotel_name").h2.text
        titles.append(title)
        theme = soup.find(id="hp_hotel_name").div.text
        themes.append(theme)
        final_links.append(url)
    except:
        pass

def make_df():
    """ Make pandas dataframe to manipulate data """
    df = pd.DataFrame({'Themes': themes,'Listing_url': final_links,  'Title': titles, 'Description': descriptions,
    })
    return df

def make_excel(df):
    """ Make excel file from dataframe """
    excel_file = df.to_excel('0_2000_arg.xlsx', index=False)
    return excel_file

def fetch_async_1(urls):
    """ Function who coordinates the coroutines for data """
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all_1(urls))
    loop.run_until_complete(future)

async def fetch_all_1(urls):
    """ Function who make task pool """
    tasks = []
    connector = TCPConnector(limit_per_host=10)
    timeout = ClientTimeout(total=300)
    async with ClientSession(connector=connector, timeout=timeout) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch_1(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)

async def fetch_1(url, session):
    """ Function to return response object from url to fill the tasks """
    async with session.get(url=url, params=params) as response:
        try:
            r = await response.text()
            return get_each_hotel_data(r, url)
        except asyncio.TimeoutError:
            pass

for l in range(25, 275, 25):
    main_urls.append(f"https://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaDqIAQGYAQq4ARnIAQ_YAQHoAQH4AQyIAgGoAgO4AsO835sGwAIB0gIkOWNlY2M5YjEtYjZmMC00ZTMxLTljZGEtOTYxNDYwYzFmYjc52AIG4AIB&sid=db666b70a0c17aac91c4242d64e8ab5c&aid=304142&ss=Buenos+Aires%2C+Argentina&ssne=Argentina&ssne_untouched=Argentina&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-979186&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=225c8ca00aa3009f&ac_meta=GhAyMjVjOGNhMDBhYTMwMDlmIAAoATICZW46B2J1ZW5vcyBAAEoAUAA%3D&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure&offset={l}")
print(main_urls)
for all_urls in main_urls:
    try:
        time.sleep(3)
        response = requests.Session().post(all_urls)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find('div', id="bodyconstraint")
        link = links.find_all('a', {"class" : "bui-card__header_full_link_wrap"})
        for url in link:
            urls = "https://www.booking.com" + url['href']
            print(urls)
            second_urls.append(urls)
    except:
        pass
print(second_urls)
fetch_async_1(second_urls)
df = make_df()
df_droped = df.drop_duplicates()
make_excel(df_droped)
