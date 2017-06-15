import urllib.request
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

try:
    url='http://music.163.com/playlist?id=563880089'
    response=urllib.request.urlopen(url)
    soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
    links=soup.find_all('a',href=re.compile('/song\?id=[0-9]'))

    all_song_urls=set()
    for link in links:
        new_url=link['href']
        new_full_url=urljoin('http://music.163.com',new_url)
        all_song_urls.add(new_full_url)

    all_mv_urls=set()
    for url in all_song_urls:
        response=urllib.request.urlopen(url)
        soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
        link=soup.find('a',title=re.compile('播放mv'))
        new_url=link['href']
        new_full_url=urljoin('http://music.163.com',new_url)
        all_mv_urls.add(new_full_url)


    fout=open('output.html','w',encoding='utf-8')
    fout.write("<html>")
    fout.write("<body>")
    fout.write("<table>")
    for i in all_mv_urls:
        fout.write("<tr>")
        fout.write("<td><a href=%s>%s</a></td>"%(i,i))
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")

except:
    print('error')
