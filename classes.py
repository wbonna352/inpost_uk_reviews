import time
import requests
from bs4 import BeautifulSoup

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
        return self._section.find('p', {'data-service-review-text-typography': 'true'}).text

    @property
    def date_of_experience(self):
        return self._section.find('p', {'data-service-review-date-of-experience-typography': 'true'}).text[20:]

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

    
if __name__ == '__main__':

    URL = 'https://uk.trustpilot.com/review/inpost.co.uk?languages=all'

    page = requests.get(URL).content
    soup = BeautifulSoup(page)

    for i in soup.find_all('div', {'class': 'styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ'}):
    
        r = Review(i)
        print(r.date_of_experience)
    
        break