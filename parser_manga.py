from bs4 import BeautifulSoup
import bs4 as bs
import lxml
import requests
from fake_useragent import UserAgent
from datetime import datetime
import json
import codecs

class Parser:
    url = "https://readmanga.io"
    ua = UserAgent()

    def get_request(self) -> str:
        
        header = {"User-Agent": self.ua.random}
        r = requests.get(self.url, headers=header)
        
        return r.text

    def find_manga_on_index(self):
        html = self.get_request()
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find_all(name='div', class_='simple-tile')
        self.generate_json_from_index(items)

    def generate_json_from_index(self, arrayManga: bs.element.ResultSet):
        now = datetime.today().strftime('%Y-%m-%d')
        collections = []
        all_manga = []
        for item in arrayManga:
            allA = item.findAll('a')
            url_manga = ""
            tags = []
            image_url = ""
            title = ""
            description = ""

            img = item.find('img', class_="img-fluid")
            if img is not None:
                image_url = img.get('data-original')
                title = img.get('title')

            descr = item.find('div', class_="manga-description")
            if descr is not None:
                description = descr.string

            isCollection = False

            for a in allA:
                if "list" in a.get("href"):
                    tag = {"url": f'{self.url}{a.get("href")}', "name": a.string}
                    tags.append(tag)
                elif "collection" in a.get("href"):
                    isCollection = True
                    titleCollection = item.find('div', class_="strong title")
                    collection = {"url": f'{self.url}{a.get("href")}', "name": titleCollection.string.replace('\n', ''), "image": image_url}
                    collections.append(collection)
                else:
                    url_manga = a.get("href")

            if not isCollection:
                manga = {"title": title, "url": f'{self.url}{url_manga}', "image": image_url, "description": description.replace('\n', '', 1), "tags": tags}
                all_manga.append(manga)
        
        with codecs.open(f'index_{now}.json', 'w', 'utf-8') as manga_file:
            json.dump(all_manga, manga_file, ensure_ascii=False)
            manga_file.close()

        with codecs.open(f'index_collection_{now}.json', 'w', 'utf-8') as collectionFile:
            json.dump(collections, collectionFile, ensure_ascii=False)
            collectionFile.close()

    def generate_json_from_manga_page(self):
        end_url = ''
        url = f'{self.url}/moi_sempai_razdrajaet_/vol9/179?tran=83821'

        if 'vol' in url:
            splitted_url = url.split('/')
            for temp_url in splitted_url:
                if 'vol' not in temp_url:
                    end_url = f'{end_url}/{temp_url}'
                else:
                    break

        end_url = end_url[1:]

        header = {"User-Agent": self.ua.random}
        r = requests.get(end_url, headers=header)

        with open('manga.html', 'w') as file:
            file.write(r.text)

def test():
    parser = Parser()
    parser.generate_json_from_manga_page()

if __name__ == "__main__":
    test()