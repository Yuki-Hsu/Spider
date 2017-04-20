import urllib.request
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

try:
    url='http://list.youku.com/albumlist/show/id_27543808.html?sf=10200&spm=a2h0k.8191403.0.0'
    response=urllib.request.urlopen(url)
    soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
    links=soup.find_all('a',title=re.compile('没有黄段子的无聊世界'))
    new_urls=set()
    for link in links:
        new_url=link['href']
        new_full_url=urljoin('http:',new_url)
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

except:
    print('error')
