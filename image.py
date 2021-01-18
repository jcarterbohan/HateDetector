# Import required packages
import pytesseract
import os
from PIL import Image
import requests


ACCEPTED_CODES = [200, 201, 202, 203, 205, 206, 207, 208, 226]


class HateImage:
    # Class constructor which takes in a variable representing the URL of the image posted
    def __init__(self, img_url):
        self.img = img_url

    def get_text(self):
        """
        Uses pytesseract to retrieve the text from an image, currently only works on black text

        If the file is a gif, gifhandler will take over
        todo: other colored text
        """
        this_dir = os.path.dirname(os.path.realpath(__file__))
        cur_dir = os.getcwd()

        os.chdir(this_dir)

        extension = dl_img_from_url(self.img)
        if extension == "":
            return
        if extension == ".gif":
            return self.__gifhandler(cur_dir)
        else:
            text = pytesseract.image_to_string("image.png")
            os.chdir(cur_dir)

    def __gifhandler(self, dir):
        """
        The function below splits the frames of the GIF into individual images, so they can all be analyzed for hate speech separately
        However, it stops duplicate text that also appears on another image from going on the output string.
        """
        gif = Image.open("image.gif")
        gif_frames = gif.n_frames
        gif_text = ""

        for frame in range(0, gif_frames):
            gif.seek(frame)
            grbimg = gif.convert("RGBA")
            text = pytesseract.image_to_string(grbimg)
            if text not in gif_text:
                gif_text.append(f"{text}\n")
        os.chdir(dir)
        return gif_text.strip()


def dl_img_from_url(url):
    """
    Downloads images from any url which may be posted by a user 
    """
    extension = ".png" if not ".gif" in url else ".gif"
    f = open(f"image{extension}", "wb")
    rq = requests.get(url)
    if not rq.status_code in ACCEPTED_CODES:
        return ""
    f.write(requests.get(url).content)
    f.close()
    return extension

