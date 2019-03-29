import requests;

def main():
    image_url = requests.get(input('Url da imagem: '))
    image = open(input('Nome do arquivo(com extensao)'), 'wb').write(image_url.content)


if __name__ == '__main__':
    main()
