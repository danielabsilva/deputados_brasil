# -*- coding: utf-8 -*-
from lxml.html.soupparser import fromstring
import urllib
import BeautifulSoup
from webstore.client import Database
import json
import scraper_deputados_api

def get_url(ano):
	return "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura=" + str(ano) + "&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem="

			
def get_data(url, ano):
	soup = parser(url)
	data = {}
	#dicionario
	data["nome"] = ""
	data["partido"] = ""
	data["estado"] = ""
	data["nascimento"] = ""
	data["naturalidade"] = ""
	data["profissoes"] = ""
	data["filiacao"] = ""
	data["imagem"] = ""
	data["outros"] = ""
	
	#id
	data["legislatura"] = ano
	data["id"] = url.split("=")[1]
	data["url"] = url
	
	#bioNomParlamentrPartido
	try:
		data["nome"] = soup.cssselect(".bioNomParlamentrPartido")[0].text.split("-")[0].strip()
		data["partido"] = soup.cssselect(".bioNomParlamentrPartido")[0].text.split("-")[1].split("/")[0].strip()
		data["estado"] = soup.cssselect(".bioNomParlamentrPartido")[0].text.split("-")[1].split("/")[1].strip()
	except:
		data["nome"] = soup.cssselect(".bioNomParlamentrPartido")[0].text
	
	#bioDetalhes
	detalhes = soup.cssselect(".bioDetalhes span")
	for detalhe in detalhes:
		if detalhe.text == u"Nascimento: ":
			data["nascimento"] = detalhe.getnext().text
		elif detalhe.text == u"Naturalidade: ":
			data["naturalidade"] = detalhe.getnext().text
		elif detalhe.text == u"Profissões: ":
			data["profissoes"] = detalhe.getnext().text
		elif detalhe.text == u"Filiação: ":
			data["filiacao"] = detalhe.getnext().text
		else:
			print "yousuck " + str(detalhe.getnext())
			
	#bioFoto
	data["imagem"] = "http://www2.camara.gov.br/deputados/pesquisa/" + soup.cssselect(".bioFoto img")[0].get("src")
	
	#bioOutrosTexto
	titulos = soup.cssselect(".bioOutrosTitulo")
	data["outros"] = []
	for titulo in titulos:
		informacao = {}
		informacao["titulo"] = titulo.text.strip(":")
		informacao["conteudo"] = titulo.getnext().text
		data["outros"].append(informacao)
	data["outros"] = json.dumps(data["outros"])
	
	#save
	table.writerow(data, unique_columns=['id'])

def parser(url):
	html = urllib.urlopen(url).read()
	return fromstring(html)

#connect
database = Database('webstore.thedatahub.org', 'danielabsilva', 'deputados_brazil', http_apikey=apikey)
table = database['deputados_bio']
erros = database['erros']

anos = range(41,54)
for ano in anos:
	url_busca = get_url(ano)
	soup = parser(url_busca)
	urls_deputados = soup.cssselect("#content a")
	for url in urls_deputados:
		try:
			print "baixando " + url.get("href")
			get_data(url.get("href"), ano)
		except:
			print "erro em " + url.get("href")
			erros.writerow({"url" : url.get("href")})