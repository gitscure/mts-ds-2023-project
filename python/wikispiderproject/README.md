# Домашнее задание по Python 4

Парсер реализован, используя фреймворк [Scrapy](https://scrapy.org/).

Собирает следующую информацию по фильмам: название, жанр, режиссер, страна и год, используя [стартовую страницу](https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83).

Запуск:

```console
scrapy crawl wikispider -O output.csv
```