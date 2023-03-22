from selenium import webdriver
from bs4 import BeautifulSoup
from googletrans import Translator
import re
import time
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_cloud_api_myservice.json"

# Chrome tarayıcısı ile sürücüyü başlat
driver = webdriver.Chrome()

# Web sayfasını yükle
driver.get("https://www.classcentral.com/")

# Tam sayfayı getir
html = driver.execute_script("return document.documentElement.outerHTML")

# Soupla HTML'i parse et
soup = BeautifulSoup(html, "html.parser")

translator = Translator()

html_text = str(soup)


def translate_text(target, text):
    import six
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]


def extractInnerTags(data):
    tags = ['a', 'p', 'h2', 'h3', 'strong', 'button']
    finaltext = data.text.strip()
    for t in tags:
        inner_tags = data.find_all(t)
        for inner_tag in inner_tags:
            finaltext = finaltext.replace(inner_tag.text.strip(), "")
    return finaltext.strip()


tags = ['a', 'p', 'h2', 'h3', 'strong', 'button']

for tag in tags:
    print(tag+" tag processing..")
    datas = soup.find_all(str(tag))  # get tag elements
    for data in datas:
        text = (extractInnerTags(data))
        if not (text == ""):
            translated_text = translate_text("hi", text)  # translate text
            # create a new tag with the translated text
            new_tag = soup.new_tag(tag)
            for attr in data.attrs:
                new_tag[attr] = data[attr]
            new_tag.string = translated_text
            # replace the old tag with the new tag
            data.replace_with(new_tag)

# update the HTML text with the translated tags
html_text = str(soup)

with open("output.html", "w") as file:
    file.write(html_text)

# Sürücüyü kapat
driver.quit()
