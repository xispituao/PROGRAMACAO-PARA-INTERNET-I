import requests
from bs4 import BeautifulSoup
def main():
    site_url = requests.get(input('Url da imagem: '))
    soup = BeautifulSoup(site_url.content, 'html.parser')
    links = soup.find_all('a')
    open('C:/Users/natan/Desktop/links.txt', 'w').write(str(links))
    # for link in links:
    #     open('C:/Users/natan/Desktop/links.txt', 'w').write(str(link + '\n'))



if __name__ == '__main__':
    main()
