import requests
from bs4.element import Comment
from bs4 import BeautifulSoup


ACCEPTED_CODES = [200, 201, 202, 203, 205, 206, 207, 208, 226]


class HateCrawler:
    def __init__(self, url=""):
        """
        Takes in a string parameter which is supposed to be a URL
        Initializes the webscraper with setting default values to data, soup, and url
        """
        self.data = ""
        self.soup = None
        if url.strip() is not "":
            self.set_url(url)

    def set_url(self, url):
        """
        Sets the URL of the webscrapper and initializes the data
        """
        self.url = url
        self.__init_data()

    def __init_data(self):
        """
        From the initialized class variables, the html page is webscraped from the url
        Returns all visible text from the HTML page
        """
        if self.url == "":
            return None
        rq = requests.get(self.url)
        if not rq.status_code in ACCEPTED_CODES:
            return None
        self.soup = BeautifulSoup(rq.content, "html.parser")
        text = self.soup.findAll(text=True)
        vis_text = filter(self.__tag_visible, text)
        self.data = u"".join(t.strip() for t in vis_text)

    def __tag_visible(self, element):
        """
        Checks the element and returns if a tag is visible or not on the HTML page
        """
        if element.parent.name in [
            "style",
            "script",
            "head",
            "title",
            "meta",
            "[document]",
        ]:
            return False
        if isinstance(element, Comment):
            return False
        return True

