import requests
from bs4 import BeautifulSoup
import os

class Page:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup(url)

    def get_html(self, url):
        res = requests.get(url)
        html = res.text
        return html

    def get_soup(self, url):
        html = self.get_html(url)
        return BeautifulSoup(html, features='lxml')
    
    def select(self, query):
        return self.soup.select(query)

class Chapter:
    def __init__(self, url, title = '', images_urls = []):
        self.url = url
        self.title = title
        self.images_urls = images_urls
        self.page = None

    def get_page(self):
        return Page(self.url)

    def set_page(self):
        if self.page is None:
            self.page = self.get_page()

    def get_title(self):
        self.set_page()
        return self.page.select('.container.comicName')[0].text
    
    def set_title(self):
        self.set_page()
        self.title = self.get_title()

    def get_images_urls(self):
        self.set_page()
        images_elems = self.page.select('#lightgallery img')
        images_urls = [elem['src'] for elem in images_elems]
        return images_urls

    def set_images_urls(self):
        self.set_page()
        self.images_urls = self.get_images_urls()

class Comic:
    def __init__(self, url, title = '', chapters = []):
        self.url = url
        self.title = title
        self.chapters = chapters
        self.page = None

    def get_page(self):
        return Page(self.url)
    
    def set_page(self):
        if self.page is None:
            self.page = self.get_page()

    def get_title(self):
        self.set_page()
        title = self.page.select('.detailComic .preface .detail h4')[0].text
        return title
    
    def set_title(self):
        self.title = self.get_title()
    
    def get_chapters(self):
        self.set_page()
        chapters_urls_elems = self.page.select('.chapters .list a')
        chapters_names_elems = self.page.select('.chapters .list .name .titleComic')
        chapters = []
        for url_elem, name_elem in zip(chapters_urls_elems, chapters_names_elems):
            name = name_elem.text.strip()
            url = url_elem['href']
            chapter = Chapter(url, name, [])
            chapters.append(chapter)
        return chapters
    
    def set_chapters(self):
        self.chapters = self.get_chapters()
    
class Downloader:
    def download(self, chapter, path):
        chapter_dir = os.path.join(path, chapter.title)
        if not os.path.isdir(chapter_dir):
            os.mkdir(chapter_dir)
        if len(chapter.images_urls) <= 0:
            chapter.set_images_urls()
        for i, image_url in enumerate(chapter.images_urls):
            image = requests.get(image_url).content
            image_path = os.path.join(chapter_dir, str(i) + '.jpg')
            with open(image_path, 'wb') as f:
                f.write(image)
    

