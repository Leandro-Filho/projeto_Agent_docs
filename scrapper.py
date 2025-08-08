#importamos as duas bibliotecas que usaremos para fazer a pesquisa em uma url

# Será responsável por facilitar o recebimento de dados e informações vinda da internet
import requests 

#responsável por pegar os dados da url da melhor forma possível
from bs4 import BeautifulSoup

#essa função irá apenas acessar a url e extrair o texto por inteiro do site
def get_all_text_from_url(url):
    response = requests.get(url)

#apenas verifica se a busca na url deu certo
    if response.status_code == 200:
        soup =BeautifulSoup(response.content, "html.parser")

#remove tudo que não é o texto que queremos, ou seja, os scripts e styles do site 
        for scripts_or_styles in soup("script", "style"):
            scripts_or_styles.decompose()

#pega apenas o texto da pagina
        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chuncks = (phrase.strip() for line in lines for phrase in line.split())
        text = "\n ".join(chunk for chunk in chuncks if chunk)

        return text
    
    else:
        return("erro ao tentar acessar o site: {response.status_code}")