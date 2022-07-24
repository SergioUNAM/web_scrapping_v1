import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


# Función que escribe en un archivo html el resultado de la consulta para poder visualizarlo
def archivo(soup):
    f = open('soup.html', 'w')
    f.write(str(soup.prettify()))
    f.close()


# Función que genera la solicitud de la página web y retorna un objeto soup
def request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    page_request = requests.get(url, headers=headers)
    if page_request.status_code != 200:
        print(page_request.status_code)
        return "error"

    # print(f'status code: {page_request.status_code}')
    soup = BeautifulSoup(page_request.text, 'html.parser')  # Genera un objeto soup
    return soup


# Función que retorna el precio en mercado libre
def precio_ml():  # Funcion que obtiene el precio en mercado libre

    url_mercado_libre = 'https://www.mercadolibre.com.mx/apple-airpods-con-estuche-de-carga-blanco/p/MLM15914456?hide_psmb=true#reco_item_pos=0&reco_backend=best-seller&reco_backend_type=low_level&reco_client=highlights-rankings&reco_id=0f8a0e0d-0157-4194-8c5a-403f14435d7c&tendency_print_id=74bbbcf3-df2c-4a1c-a28b-ed6777faa694'

    request_ml = request(url_mercado_libre)  # Llamamos a la función request para realizar la consulta de mercado libre

    search_in_soup = str(request_ml.find('span', attrs={
        'class': 'andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact'}).find(
        'span', attrs={'class': 'andes-visually-hidden'}).get_text())
    # Devuelve el texto dentro del objeto p (bs4Soup)
    precio = float(re.findall('\d+', search_in_soup)[0])  # Obtiene el precio como un flotante
    # print(f'El precio en mercado libre es de: ${precio}')
    return precio


# Función que retorna el precio de la página oficial de apple
def precio_apple():
    url_apple = 'https://www.apple.com/mx/shop/product/MV7N2BE/A/airpods-con-estuche-de-carga'
    request_apple = request(url_apple)  # Llamamos a la función request para realizar la consulta de la página de apple

    search_in_soup = str(request_apple.find('script', attrs={
        'type': 'application/ld+json'}).get_text())  # Guarda la busqueda y la transforma de un objeto bs4 a un str
    # Hacemos la búsqueda con expresiones regulares, ya que el precio no se encuentra dentro de una etiqueta html, sino en un script json
    patron = re.compile(r'\bprice":\b')  # Genera el patron que se desea buscar
    inicio = patron.search(
        search_in_soup).end()  # Retorna la posicion final donde localiza el patrón generado dentro de la cadena s_search_in_soup
    precio = float(search_in_soup[inicio:inicio + 5])
    # print(f'El precio en la página oficial de Apple es de: ${precio}')
    return precio


# Función que retorna el precio de ishopmixup.com
def precio_ishop():
    url_ishop = 'https://www.ishopmixup.com/airpods-estuche-carga/p'
    request_ishop = request(url_ishop)

    # Iniciamos la búsqueda particular
    search_in_soup = str(request_ishop.find('script', attrs={
        'type': 'application/ld+json'}).get_text())  # Guarda la busqueda y la transforma de un objeto bs4 a un str
    # Utilizamos expresiones regulares, ya que el precio se encuentra dentro de un script json y no dentro de una etiqueta html
    patron = re.compile(r'\bprice":\b')  # Genera el patron que se desea buscar
    inicio = patron.search(search_in_soup).end()
    precio = float(search_in_soup[inicio:inicio + 4])
    # print(f"El precio en ishop es de: ${precio}")
    return precio


def precio_ph():
    url_ph = 'https://www.elpalaciodehierro.com/apple-apple-airpods-con-estuche-de-carga-40044132.html'
    request_ph = request(url_ph)
    search_in_soup = str(request_ph.find("span", attrs={"class": "b-product_price-value"}).get_text())
    patron_numero = re.compile('\d+')
    l_precio = re.findall(patron_numero, search_in_soup)
    precio = ""
    for p in l_precio[0:2]:
        precio = precio + p
    precio = float(precio)
    # print(f"El precio en Palacio de Hierro es de: ${precio}")
    return precio


def escritura_archivo_precios():
    mercado_libre = precio_ml()
    apple = precio_apple()
    ishop = precio_ishop()
    palacio_hierro = precio_ph()

    fh_consulta = datetime.now()  # fecha y hora de consulta
    fecha = str(fh_consulta.date())
    hora = str(fh_consulta.strftime("%H:%M:%S"))
    # print(f"fecha: {fecha} y hora: {hora}")

    lista_precios = [fecha, ", ", hora, ", ", mercado_libre, ", ", ", ", ishop, ", ", palacio_hierro, "\n"]

    for dato in lista_precios:
        with open("/Users/sergiocastelarfernandez/Documents/scripts varios python/track_precios.txt", "a") as file:
            file.write(str(dato))


def run():
    escritura_archivo_precios()


if __name__ == '__main__':
    run()
