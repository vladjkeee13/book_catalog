import sys
from datetime import datetime
from slugify import slugify
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from requests_html import HTMLSession
from django.core.management.base import BaseCommand

from catalog.models import *


locker = Lock()


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text

    slug = slugify(name)

    description = response.html.xpath('//div[@id="description"]/span[2]')[0].text
    description = '\n'.join(['<p>{}</p>'.format(p) for p in description.split('\n') if p])

    img_source = response.html.xpath('//img[@id="coverImage"]/@src')[0]

    try:

        with HTMLSession() as session2:
            img_resp = session2.get(img_source)

        image_name = 'books_images/' + slug + img_source[-4:]

        with open('media/{}'.format(image_name), 'wb') as imgf:
            imgf.write(img_resp.content)

        del img_resp

    except Exception as e:
        print(e, type(e), sys.exc_info()[-1].tb_lineno)
        image_name = 'default.jpg'

    author = response.html.xpath('//a[@class="authorName"]/span/text()')[0]

    pages = response.html.xpath('//span[@itemprop="numberOfPages"]/text()')[0]
    pages = int(pages.split()[0])

    chars = []

    isbn, language = '', ''

    rows = response.html.xpath('//div[@class="clearFloats"]')
    for row in rows:
        key = row.xpath('//div[@class="infoBoxRowTitle"]')[0].text
        if key == 'ISBN':
            isbn = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
        elif key == 'Edition Language':
            language = row.xpath('//div[@class="infoBoxRowItem"]')[0].text
        elif key == 'Characters':
            for link in row.xpath('//div[@class="infoBoxRowItem"]/a'):
                chars.append(link.text)
        del key

    published = response.html.xpath('//div[@id="details"]/div[@class="row"][2]')[0]
    published = ' '.join(published.text.split()[1:4])
    published = datetime.strptime(published, '%B %dth %Y')

    categs = response.html.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()')

    book = {
        'name': name,
        'slug': slug,
        'img_source': img_source,
        'book_source': url,
        'description': description,
        'author': author,
        'pages': pages,
        'isbn': isbn,
        'language': language,
        'published': published,
        'img': image_name,
    }

    try:
        with locker:
            book = Book.objects.create(**book)
    except Exception as e:
        print(type(e), e)
        return

    for char in chars:
        with locker:
            char, created = Character.objects.get_or_create(name=char)
        book.char.add(char)

    for cat in categs:
        cat = {'name': cat, 'slug': slugify(cat), 'description': ''}
        with locker:
            cat, created = Category.objects.get_or_create(**cat)
        book.cat.add(cat)

    print('Success:', url)


def urls_generator(start, end, task):
    for i in range(start, end):
        url = 'https://www.goodreads.com/book/show/{}.Harry'.format(i)
        with locker:
            task.status = 'scrape id: {}'.format(i)
            task.save()
        yield url


def run_crawler(start, end, task):
    task.status = 'start parsing'
    task.save()
    url_gen = urls_generator(start, end, task)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(crawler, url_gen)
    task.status = 'finished'
    task.end_time = datetime.now()
    task.save()


class Command(BaseCommand):
    help = 'Running books scraper'

    def handle(self, *args, **options):
        from task.models import Task

        task = Task.objects.create(name='run_scraper')
        run_crawler(300, 500, task)
