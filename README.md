# Scrapy Mercado Livre

## Tutorial

[Webscraping com python e scrapy tutorial! 10000 itens do mercadolivre em 2 minutos!](https://www.youtube.com/watch?v=7le4AGwtH94)

## Create Project

```bash
scrapy startproject mcz_scrapy_mercadolivre
```

## Create Spider

```bash
scrapy genspider ml mercadolivre.com
```

## Run Scrapy Crawl

```bash
scrapy crawl ml
```

## Run Scrapy Crawl And Create Json File

```bash
scrapy crawl ml -o pagination.json
```

## Get Your User Agent

Digit on google search __my user agent__ and get your agent, for example:

```bash
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15
```
