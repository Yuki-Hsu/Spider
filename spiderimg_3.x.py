class UrlManager(object):
	def __init__(self):
		self.new_urls=set()
		self.old_urls=set()
	def add_new_url(self,url):
		if url is None:
			return
		if url not in self.new_urls and url not in self.old_urls:
			self.new_urls.add(url)
	def add_new_urls(self,urls):
		if urls is None or len(urls)==0:
			return
		for url in urls:
			self.add_new_url(url)
	def has_new_url(self):
		return len(self.new_urls)!=0
	def get_new_url(self):
		new_url=self.new_urls.pop()
		self.old_urls.add(new_url)
		return new_url

import urllib.request
#python 3.5.1**************************************************************
class HtmlDownloader(object):
	def download(self,url):
		if url is None:
			return None

		proxy_support = urllib.request.ProxyHandler({'http': 'localhost:8087'})
		opener = urllib.request.build_opener(proxy_support)
		urllib.request.install_opener(opener)

		response=urllib.request.urlopen(url)
		if response.getcode()!=200:
			return None	
		#print(response.read())
		return response.read()

from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
#python 3.5.1**************************************************************
class HtmlParser(object):
	def _get_new_urls(self,page_url,soup):
		new_urls=set()
		#links=soup.find_all('a',href=re.compile("/explore/zhenzhiwaitao/|/explore/banmiansheji/"))
		links=soup.find_all('a',href=re.compile("htm_data|thread0806"))
		for link in links:
			new_url=link['href']
			new_full_url=urljoin(page_url,new_url)
			new_urls.add(new_full_url)
		return new_urls
	def _get_new_data(self,page_url,soup):
		try:
			res_data={}
			res_data['url']=page_url
			title_node=soup.find("title")
			res_data['title']=title_node.get_text()
			print(res_data['title'])
			#summary_node=soup.find('div',class_="tpc_content do_not_catch")
			summary_node=soup.find('title',text=re.compile('千佳'))
			print(summary_node)
			if summary_node is None:
				return None
			res_data['summary']=title_node.get_text()
			#res_data['summary']=soup.find('div',class_="tpc_content do_not_catch").find('img')
			return res_data
		except:
			print ('	Did_not_get_new_data_from_this_URL')
			return None
	def parse(self,page_url,html_cont):
		if page_url is None or html_cont is None:
			return
		#soup=BeautifulSoup(html_cont,'html.parser',from_encoding="utf-8")
		soup=BeautifulSoup(html_cont,'html.parser',from_encoding="gb18030")
		#print(soup.prettify())
		new_urls=self._get_new_urls(page_url,soup)
		new_data=self._get_new_data(page_url,soup)
		return new_urls,new_data

class HtmlOutputer(object):
	def __init__(self):
		self.datas=[]
	def collect_data(self,data):
		if data is None:
			return
		self.datas.append(data)
	def output_html(self):
		fout=open('output.html','w',encoding='utf-8')
#python-windows OS***********************************************************
		fout.write("<html>")
		fout.write("<body>")
		#fout.write("<table>")
		for data in self.datas:
			#fout.write("<tr>")
			fout.write("<p>**********************************************************************************************************************************************************************</p>")
			fout.write("<a href=%s>%s</a>"%(data['url'],data['url']))
			fout.write("<p>%s</p>"%data['title'])
			fout.write("<div>%s</div>"%data['summary'])
			#fout.write("</tr>")
		#fout.write("</table>")
		fout.write("</body>")
		fout.write("</html>")
		
class SpiderMain(object):
	def __init__(self):
		self.urls=UrlManager()
		self.downloader=HtmlDownloader()
		self.parser=HtmlParser()
		self.outputer=HtmlOutputer()
	def craw(self,root_url):
		count=1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			try:
				new_url=self.urls.get_new_url()
				print (('craw %d : %s')%(count,new_url))
				html_cont=self.downloader.download(new_url)
				new_urls,new_data=self.parser.parse(new_url,html_cont)
				self.urls.add_new_urls(new_urls)
				self.outputer.collect_data(new_data)
				if count==1000:
					break
				count+=1
			except:
				print ('craw failed')
		self.outputer.output_html()
		
		
root_url="http://t66y.com/thread0806.php?fid=15"
#root_url="http://huaban.com/"
obj_spider=SpiderMain()
obj_spider.craw(root_url)
