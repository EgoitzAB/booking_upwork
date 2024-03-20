import unittest
import gzip
import argparse

from unittest.mock import patch, Mock
from bs4 import BeautifulSoup

# Import your script here
import src.mex as mex
URL = 'https://www.booking.com/hotel/ar/centro1555.es.html?aid=2311236&label=es-es-booking-desktop-onknyt5TBrS8m9RnGd%2A6fgS652829001115%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1005527%3Ali%3Adec%3Adm&sid=727fda0a735e543940f7410002cd685e&all_sr_blocks=914573005_370419051_0_0_0;checkin=2024-03-20;checkout=2024-04-02;dest_id=-979186;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=914573005_370419051_0_0_0;hpos=1;matching_block_id=914573005_370419051_0_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=914573005_370419051_0_0_0__42455;srepoch=1710957094;srpvid=52e27d8f85d1016c;type=total;ucfs=1&#hotelTmpl'

class TestMex(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup('<html><body><div id="property_description_content">description</div><div id="hp_hotel_name"><h2>title</h2><div>theme</div></div></body></html>', 'lxml')

    @patch('src.mex.requests.get')
    def test_get_soup(self, mock_get):
        mock_get.return_value.text = '<html></html>'
        soup = mex.get_soup(URL)
        self.assertEqual(str(soup), '<html></html>')

    @patch('src.mex.requests.Session')
    def test_get_hotel_data(self, mock_session):
        mock_session.return_value.get.return_value.text = '<html><body><header class="bui-spacer--medium"><a href="/hotel"></a></header></body></html>'
        mex.get_hotel_data(URL)
        self.assertEqual(mex.formated_links, ['https://www.booking.com/hotel'])

    def test_extract_selectors(self):
        result = mex.extract_selectors(self.soup, 'div')
        self.assertEqual(result.text, 'description')

    def test_get_each_hotel_data(self):
        mex.get_each_hotel_data(str(self.soup), URL)
        self.assertEqual(mex.descriptions, ['description'])
        self.assertEqual(mex.titles, ['title'])
        self.assertEqual(mex.themes, ['theme'])
        self.assertEqual(mex.final_links, [URL])

    def test_make_df(self):
        mex.descriptions = ['description']
        mex.titles = ['title']
        mex.themes = ['theme']
        mex.final_links = ['URL']
        df = mex.make_df()
        self.assertEqual(df['Description'].tolist(), ['description'])
        self.assertEqual(df['Title'].tolist(), ['title'])
        self.assertEqual(df['Themes'].tolist(), ['theme'])
        self.assertEqual(df['Listing_url'].tolist(), ['URL'])

    @patch('src.mex.requests.get')
    def test_get_sitemap(self, mock_get):
        mock_get.return_value.content = b'<xml></xml>'
        sitemap = mex.get_sitemap('URL')
        self.assertEqual(sitemap, b'<xml></xml>')

    def test_descompress_sitemap(self):
        sitemap = mex.descompress_sitemap(gzip.compress(b'<xml></xml>'))
        self.assertEqual(sitemap, b'<xml></xml>')

if __name__ == '__main__':
    unittest.main()
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg', help='Argumento para las pruebas')
    args = parser.parse_args()

    # Aquí puedes usar args.arg en tus pruebas
    mex.arg = args.arg

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMex)
    unittest.TextTestRunner().run(suite)