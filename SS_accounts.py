import requests
import re
import urllib.request

url_1 = 'http://gdmi.weebly.com/31185233981997832593.html'
r_1 = requests.get(url_1)
a_1 = re.findall(r'a href="ss://.*?"', r_1.text)

url_2 = 'https://doub.io/sszhfx/'
r_2 = requests.get(url_2)
a_2 = re.findall(r'ss://.*?"', r_2.text)

fout=open('output.html','w',encoding='utf-8')
for x in range(len(a_1)):
	fout.write(a_1[x]+'\n')
for x in range(len(a_2)):
	fout.write(a_2[x]+'\n')
