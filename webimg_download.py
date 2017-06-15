import urllib.request
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

try:
    urls=set()
    new_urls=set()
    roots=['https://www.jkforum.net/forum-535-1.html','https://www.jkforum.net/forum-535-2.html']

    proxy_support = urllib.request.ProxyHandler({'https': 'localhost:8087'})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    for root in roots:
        print('crawl',root)
        response=urllib.request.urlopen(root)
        soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
        links=soup.find_all('a',href=re.compile("^thread-"))
        for link in links:
            new_url=link['href']
            new_full_url=urljoin('https://www.jkforum.net/',new_url)
            print(new_full_url)
            urls.add(new_full_url)

    for url in urls:
        response=urllib.request.urlopen(url)
        soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
        links=soup.find_all('img',style="cursor:pointer")
        for link in links:
            new_url=link['file']
            new_full_url=urljoin('https://www.mymypic.net/',new_url)
            new_urls.add(new_full_url)

    fout=open('output.html','w',encoding='utf-8')
    fout.write("<html>")
    fout.write("<body>")
    fout.write("<table>")
    for i in new_urls:
        fout.write("<tr>")
        fout.write("<td><a href=%s>%s</a></td>"%(i,i))
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")


    i = 0
    j = 0
    for each in new_urls:
        print('downloading',each)
        try:
            pic= urllib.request.urlopen(each)
            string = 'pictures\\'+str(i) + '.jpg'
            fp=open(string,'wb') 
            fp.write(pic.read())
            fp.close()
        except:
            print('download error')
            j += 1
        i += 1
    print('sum pictures:',i)
    print('bad pictures:',j)


except:
    print('error')
