from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3

class Page:

    def __init__(self, url):
        self.url = url

    @property
    def _soup(self):
        page = requests.get(self.url).content
        return BeautifulSoup(page, 'html.parser')

    @property
    def _review_divs(self):
        return self._soup.find_all('div', {'class': 'styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ'})

    @property
    def reviews(self):
        return [self.Review(div) for div in self._review_divs]

    class Review:

        def __init__(self, div):
            self.div = div
            self.user = self.User(self._user_div)

        @property
        def _article(self):
            return self.div.find('article')

        @property
        def _user_div(self):
            return self._article.find('div', {'class': 'styles_consumerDetailsWrapper__p2wdr'})

        @property
        def _section(self):
            return self._article.find('section')

        @property
        def rate(self):
            return int(self._section.find('img')['alt'][6])

        @property
        def title(self):
            return self._section.find('a').text

        @property
        def url(self):
            return 'uk.trustpilot.com' + self._section.find('a').get('href')

        @property
        def description(self):
            # TODO AttributeError fix
            return self._section.find('p', {'data-service-review-text-typography': 'true'}).text

        @property
        def date_of_experience(self):
            date_string = self._section.find('p', {'data-service-review-date-of-experience-typography': 'true'}).text[20:]
            date_object = datetime.strptime(date_string, '%d %B %Y')
            return datetime.strftime(date_object, '%Y-%m-%d')

        class User:
            def __init__(self, div):
                self._div = div

            @property
            def url(self):
                return 'uk.trustpilot.com' + self._div.find('a').get('href')

            @property
            def name(self):
                return self._div.find('a').find('span').text

            @property
            def reviews_count(self):
                return self._div.find('div', {'class': 'styles_consumerExtraDetails__fxS4S'}).find('span').text.split(' ')[0]

            @property
            def location(self):
                return self._div.find('div', {'class': 'styles_consumerExtraDetails__fxS4S'}).find('div').text

        def insert_into_database(self, connection, table_name = 'reviews') -> None:
            values = {
                'url': self.url,
                'title': self.title,
                'description': self.description,
                'rate': self.rate,
                'date_of_experience': self.date_of_experience,
                'user_url': self.user.url,
                'user_name': self.user.name,
                'user_reviews_count': self.user.reviews_count,
                'user_location': self.user.location
            }

            cursor = connection.cursor()
            try:
                cursor.execute(f"""
                INSERT INTO {table_name} (url, title, description, rate, date_of_experience, user_url, user_name, user_reviews_count, user_location)
                VALUES (:url, :title, :description, :rate, :date_of_experience, :user_url, :user_name, :user_reviews_count, :user_location)
                """, values)
                connection.commit()
            except sqlite3.IntegrityError:
                print('RAW IS ALREADY IN DATABASE')
            cursor.close()

            print('ROW INSERTED')




if __name__ == '__main__':

    URL = 'https://uk.trustpilot.com/review/inpost.co.uk?languages=all&page=%s'

    # number_of_pages = 100
    # pages = {page_no: Page(URL % page_no) for page_no in range(1, number_of_pages+1)}

    test = Page(URL % 1)
