import requests
from bs4 import BeautifulSoup
import re

# Amazon no permite webScrapping

amazon = 'https://www.amazon.com.mx/Apple-Audifonos-Inalambricos-AirPods-Estuche/dp/B07RK58K76/ref=sr_1_3?crid=1UWV89KRWIZ5E&keywords=airpods&qid=1657215150&refinements=p_89%3AApple&rnid=11790855011&s=electronics&sprefix=ai%2Caps%2C104&sr=1-3&ufe=app_do%3Aamzn1.fos.713a5ea8-28c8-4756-9a04-20c241c6dc4c'

ishop_mixup = 'https://www.ishopmixup.com/airpods-estuche-carga/p'
liverpool = 'https://www.liverpool.com.mx/tienda/pdp/Apple-AirPods-con-estuche-de-carga/1082662576?skuId=1082662576'
sears = 'https://www.sears.com.mx/producto/190133/airpods-con-estuche-de-carga/'
palacio_hierro = 'https://www.elpalaciodehierro.com/apple-apple-airpods-con-estuche-de-carga-40044132.html'
sanborns = 'https://www.sanborns.com.mx/producto/65189/audifonos-airpods-apple/'


# fuentes = [mercado_libre, amazon, apple, ishop_mixup, liverpool, sears, palacio_hierro, sanborns]

# Función que genera la solicitud de la pagina web y retorna un objeto soup
def request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    page_request = requests.get(url, headers=headers)
    if page_request.status_code != 200:
        return "error"

    print(f'status code: {page_request.status_code}')
    soup = BeautifulSoup(page_request.text, 'html.parser')  # Genera un objeto soup
    return soup


# Función que retorna el precio en mercado libre
def precio_ml():  # Funcion que obtiene el precio en mercado libre

    url_mercado_libre = 'https://www.mercadolibre.com.mx/apple-airpods-con-estuche-de-carga-blanco/p/MLM15914456?hide_psmb=true#reco_item_pos=0&reco_backend=best-seller&reco_backend_type=low_level&reco_client=highlights-rankings&reco_id=0f8a0e0d-0157-4194-8c5a-403f14435d7c&tendency_print_id=74bbbcf3-df2c-4a1c-a28b-ed6777faa694'

    request_ml = request(url_mercado_libre)  # Llamamos a la función request para realizar la consulta de mercado libre

    search_in_soup = request_ml.find('span', attrs={
        'class': 'andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact'}).find(
        'span', attrs={'class': 'andes-visually-hidden'})

    s_precio = search_in_soup.get_text()  # Devuelve el texto dentro del objeto p (bs4Soup)
    precio = float(re.findall('\d+', s_precio)[0])  # Obtiene el precio como un flotante
    print(f'El precio en mercado libre es de: ${precio}')
    return precio


def precio_apple():
    url_apple = 'https://www.apple.com/mx/shop/product/MV7N2BE/A/airpods-con-estuche-de-carga'
    request_apple = request(url_apple)  # Llamamos a la función request para realizar la consulta de la página de apple

    search_in_soup = request_apple.find('script', attrs={'type': 'application/ld+json'}).get_text()
    # Hacemos la búsqueda con expresiones regulares, ya que el precio no se encuentra dentro de una etiqueta html, sino en un script json
    patron = re.compile(r'\bprice":\b')  # Busca la el texto "price"
    s_search_in_soup = str(search_in_soup)
    inicio = patron.search(s_search_in_soup).end()
    precio = float(s_search_in_soup[inicio:inicio + 7])
    print(f'El precio en la página oficial de Apple es de: ${precio}')
    return precio


def run():
    precio_ml()
    precio_apple()


if __name__ == '__main__':
    run()
