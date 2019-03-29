import requests


def main():
    url = input('URL:')
    response = requests.get('http://' + url)
    status_code = response.status_code
    cabecalho = response.headers
    tamanho_resposta = response.headers['Content-Length']
    corpo = response.text
    print('status_code = ', status_code, '\nCabeçalho = ', cabecalho, '\nTamanho Resposta = ', tamanho_resposta,
          '\nCorpo = ', corpo)


if __name__ == '__main__':
    main()
