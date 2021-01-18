import matplotlib.pyplot as plt
from hatesonar import Sonar

import os
from image import HateImage
import re

# from emot.emo_unicode import UNICODE_EMO, EMOTICONS
from hatecrawler import HateCrawler


class HateRater:
    def __init__(self, post=""):
        """
        Class constructor which takes in a string parameter, defaults to "" if not specified.
        This string represents the post that a user has posted
        """
        self.post = post

    def __makeGraph(self, hs, ol, nr):
        """
        Creates a bar chart based on the values from hate speech, offensive language, and neutral language
        Saves the bar chart as a .jpg file in the directory of the file running this function
        """
        this_dir = os.path.dirname(os.path.realpath(__file__))
        cur_dir = os.getcwd()
        os.chdir(this_dir)
        # plotting 3 confidence levels and producing graph image file
        left = [1, 2, 3]
        height = [hs, ol, nr]
        tick_label = ["Hate Speech", "Offensive Language", "Neither"]
        plt.bar(left, height, tick_label=tick_label, width=0.8, color=["blue"])
        plt.title("Post Analysis")
        plt.savefig("post_analysis.jpg")
        plt.clf()
        plt.close()
        os.chdir(cur_dir)

    # May be implemented at a later time
    # Idea is to convert text to emoji's

    # def convert_emoticons(text):
    #     for emot in EMOTICONS:
    #         text = re.sub(
    #             u"(" + emot + ")",
    #             "_".join(EMOTICONS[emot].replace(",", "").split()),
    #             text,
    #         )
    #     return text

    # def convert_emojis(text):
    #     for emot in UNICODE_EMO:
    #         text = text.replace(
    #             emot,
    #             "_".join(UNICODE_EMO[emot].replace(",", "").replace(":", "").split()),
    #         )
    #     text = convert_emoticons(text)
    #     return text

    def getScoresFromPost(self, graph=False):
        """
        Takes an optional argument of graph which is False by default
        Gets the score from the post for if it is hate speech, offensive speech, or neutral speech.  Checks if it has an link and passes through that.
        If graph is true, then a graph is made and put into a jpg file.
        """
        (hate_speech, offensive_language, neither) = self.handle_url(self.post)
        (ths, tol, tnl) = self.__getScoresFromText(self.post)
        if not (hate_speech == 0 and offensive_language == 0 and neither == 0):
            hate_speech += ths
            offensive_language += tol
            neither += tnl
            hate_speech /= 2
            offensive_language /= 2
            neither /= 2
        else:
            hate_speech = ths
            offensive_language = tol
            neither = tnl

        if graph:
            self.__makeGraph(hate_speech, offensive_language, neither)
        return (hate_speech, offensive_language, neither)

    def __getScoresFromText(self, text):
        """
        Takes in text which is a string uses HateSonar to get the values of hate_speech, offensive_language and neither.
        Each value representing a percentage of which type of speech HateSonar thinks it is
        Returns confidence levels of 3 metrics
        """
        if text is None:
            return 0, 0, 0
        # text = convert_emojis(text)

        data = Sonar().ping(text)
        hate_speech = data["classes"][0]["confidence"]
        offensive_language = data["classes"][1]["confidence"]
        neither = data["classes"][2]["confidence"]

        return (hate_speech, offensive_language, neither)

    def __getScoresFromImg(self, image_file):
        """
        Takes in image_file, routes to image.py for word processing from image 
        Returns output from score analysis on resulting text 
        """
        text = HateImage(image_file).get_text()
        return self.__getScoresFromText(text)

    def handle_url(self, text):
        """
        Takes in text which is a string.  Checks through the text to see if there are any links to images, gifs or html files.
        If so they are handled accordingly.  Returns the average values from all the links.
        """
        urls = re.findall(
            "(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?",
            text,
        )
        img_types = [".png", ".jpg", ".jpeg", ".png", ".gif", ".tiff", ".webp"]
        text = ""
        ths, tol, tnl = 0, 0, 0
        for u in urls:
            t1, t2, t3 = 0, 0, 0
            is_img = any(img in u for img in img_types)
            if is_img:
                t1, t2, t3 = self.__getScoresFromImg(u)
            else:
                data = self.__get_text_from_html(u)
                t1, t2, t3 = self.__getScoresFromText(data)
            ths += t1
            tol += t2
            tnl += t3
        num_urls = len(urls)
        if not num_urls == 0:
            ths /= num_urls
            tol /= num_urls
            tnl /= num_urls
        return (ths, tol, tnl)

    def __get_text_from_html(self, html):
        """
        Takes in html input and routes args to hatecrawler.py for processing of link content
        Returns relevant text from site for further use by confidence level functions 
        """
        ws = HateCrawler(html)
        data = ws.data
        return data

