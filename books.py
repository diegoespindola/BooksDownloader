import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(prog='bookdl', description='descarga una cacha de libros')
parser.add_argument('-cat',  type=int, nargs='?', help='Categoria de libros numerica ej: security es categoria 199', default=199)
parser.add_argument('-lastpage', type=int, nargs='?', help='Cantidad maxima de paginas de la categoria', default=10)

parametros = parser.parse_args()
 
if not(parametros.cat) and  not(parametros.lastpage):
    parser.print_help()
home='https://es.ar1lib.org'
urlweb =home + '/category/' + str(parametros.cat) + '?page=' + str(1)
#print(urlweb)
cookies = {}
page = requests.get(url=urlweb, cookies=cookies)
 
cookies = page.cookies
if page.status_code==200:
    #print(page.text)
    soup = BeautifulSoup(page.content, 'html.parser')
    libros = soup.find_all('div', attrs={'itemtype':'http://schema.org/Book'})
  
    for libro in libros :   
        href = libro.find('h3').find('a')
 
        fileName = href.get_text().replace(" ","_")
        print(fileName)
        urlBook = home + href.get('href')
        print( '    urlBook: ' + urlBook)
        

        bookPage = requests.get(url=urlBook, cookies=cookies)
        cookies = bookPage.cookies
        if bookPage.status_code==200:
            bookSoup = BeautifulSoup(bookPage.content, 'html.parser')
            bookLink = bookSoup.find('a', attrs={'class':'btn btn-primary dlButton addDownloadedBook'})
            #Descargar (pdf, 10,87 MB)
            if(bookLink):
                bookUrlDownload = home + bookLink.get('href')
                print('    Link Descarga: ' +bookUrlDownload)
                bookfileresponse = requests.get(url=bookUrlDownload, cookies=cookies, allow_redirects=False)
                if(bookfileresponse.status_code==302):
                    finalURL =bookfileresponse.headers['Location']
                    print('finalURL :' + finalURL)
                    headers = {'Referer':home,
                                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
                                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                                'Accept-Encoding':'gzip, deflate, br'
                                }
                    r = requests.get(finalURL, allow_redirects=True, headers=headers)
                    extension = r.headers['content-type'].split('/',-1)[1]
                    print (extension)
                    open(fileName + '.' + extension, 'wb').write(r.content)
                    print(r)
                else:
                    print('bookfileresponse: ' + bookfileresponse.content)    
                    print('---')
                    print(bookfileresponse)
            else:
                print('    Sin Link de descarga')
        else:
            print(bookPage)

else:
    print(page)
