import scrapy
import os

# Atributo global para controle visual das páginas raspadas
position = 1

def get_position():
    global position
    return position

def set_position(new_value):
    global position
    position += new_value

def print_position():
    global position
    print(f'posisiton: {position}')

# Atributo global para informar a uri base do site
base_uri = 'https://www.mercadolivre.com.br'

def get_base_uri():
    global base_uri
    return base_uri

def set_base_url(new_value):
    global base_uri
    base_uri = new_value

class MlSpider(scrapy.Spider):
    name = 'ml'
    
    # Informa a url da primeira página que será raspada
    start_urls = [f'{get_base_uri()}/ofertas?page=1']

    # Apaga o arquivo caso exista, para evitar sobreposição
    if os.path.exists("pagination.json"):
        os.remove("pagination.json")

    def parse(self, response):

        #Print da posição atual
        print_position()

        # Realiza a raspagem da página de ofertas de produtos
        for i in response.xpath('//li[@class="promotion-item default"]'):
            price_original = i.xpath('normalize-space(.//span[@class="promotion-item__oldprice"]//text())').get()
            price = i.xpath('normalize-space(.//span[@class="promotion-item__price"]//text())').get()
            price_sup = i.xpath('normalize-space(.//span[@class="promotion-item__price"]/sup//text())').get()
            title = i.xpath('normalize-space(.//p[@class="promotion-item__title"]/text())').get()
            link = i.xpath('normalize-space(./a/@href)').get()

            # Ajusta o preço do produto incluindo as casas decimais caso as mesmas existam
            if price_sup:
                price = f'{price},{price_sup}'

            # Monta dicionário que será inserido na chamada da função parse_detail
            fields = {
                'price_original': price_original,
                'price': price,
                'title': title,
                'link': link
            }

            # Realiza a raspagem da página de detalhes do produto
            yield scrapy.Request(url=f'{link}', callback=self.parse_detail, cb_kwargs=fields)

        # Controle da quantidade de páginas que serão raspadas, o mesmo está sendo utilizado devido ao caráter didático da solução
        if get_position() <= 3:

            # Set da próxima posição
            set_position(1)

            # Realiza a chamada da função para raspagem da próxima página de ofertas
            next_page = response.xpath('//a[contains(@title, "Próxima")]/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response, **kwargs):
        
        details = {}
        index = 1
        
        # Captura a imagem principal do produto
        image = response.xpath('//figure[@class="ui-pdp-gallery__figure"]/img/@src').get()

        # Captura os detalhes da descrição do produto
        for i in response.xpath('//p[@class="ui-pdp-description__content"]//text()'):
            details[f'detail_{index}'] = (f'{i.get()}').replace("\n","")
            index += 1

        # Captura as informações do vendedor
        for i in response.xpath('//div[@class="ui-seller-info"]'):
            seller = i.xpath('.//div[@class="ui-pdp-seller__header__title"]//text()').get()
            seller_subtitle = i.xpath('.//p[contains(@class, "ui-pdp-seller__header__subtitle")]//text()').get()
            seller_status = i.xpath('.//p[contains(@class, "ui-pdp-seller__status-title")]//text()').get()

        # Junção dos dados (produto + detalhes do produto) que serão exportados para o arquivo pagination.json
        yield {
            'price_original': kwargs.get('price_original'),
            'price': kwargs.get('price'),
            'title': kwargs.get('title'),
            'link': kwargs.get('link'),
            'image': image,
            'seller': seller,
            'seller_subtitle': seller_subtitle,
            'seller_status': seller_status,
            'details': details
        }