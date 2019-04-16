from bs4 import BeautifulSoup
import requests
import requests_cache
import re
from operator import itemgetter
requests_cache.install_cache('demo_cache')
resultados = []


def verificar_rank(keyword, text, url):
    rank = 0
    if keyword.upper() in url.upper():
        rank += 1
    if text.count(keyword) >= 10:
        rank += 5
    elif 5 < text.count(keyword) < 10:
        rank += 3
    elif text.count(keyword) < 5:
        rank += 1

    return rank


def verificar_camada(keyword,links, cm, cm2):
    if cm > 0:

        for link in links:
            try:
                if re.search('\\bhttp\\b', link['href'], re.IGNORECASE) or re.search('\\bhttps\\b', link['href'], re.IGNORECASE):
                    buscador(keyword, link['href'], cm - 1, cm2 + 1)
            except KeyError:
                ''


def buscador(keyword, url, cm, cm2=0):
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html5lib')
    links = html.find_all('a')
    text = html.body.get_text().split()
    print("Visitando a url: %s" % url)

    if keyword in text:
        rank = verificar_rank(keyword,text,url)
        posicao = text.index(keyword)
        antes = '[...]' + text[posicao - 3] + ' ' + text[posicao - 2] + ' ' + text[posicao - 1] + ' '
        depois = ' ' + text[posicao + 1] + ' ' + text[posicao + 2] + ' ' + text[posicao + 3] + '[...]'
        aux = str(antes + keyword + depois)
        resultados.append({"url": url, "texto": aux, "rank": rank, "camada": cm2})

    verificar_camada(keyword, links, cm, cm2)


print("\t\tIniciando Busca")
buscador('buriti', 'https://pt.wikipedia.org/wiki/Buriti', 1)
sorted_results = sorted(resultados, key=itemgetter(str('rank')), reverse=True)
print('Resultados:')
for resultado in sorted_results:
    print("URL--> " + str(resultado['url']))
    print("Rank--> " + str(resultado['rank']))
    print("Camada--> %s" % str(resultado["camada"]))
    print(resultado["texto"])
    print("\n\n")
resultados.clear()