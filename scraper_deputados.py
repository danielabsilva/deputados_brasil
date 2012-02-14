# -*- coding: utf-8 -*-
from lxml.html.soupparser import fromstring
import urllib
import BeautifulSoup
from webstore.client import Database
import json

def get_url():
	anos = range(41,54)
	for ano in anos:
		url_busca = "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura=" + str(ano) + "&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem="
		html_busca = urllib.urlopen(url_busca).read()
		soup = fromstring(html_busca)
		urls_deputados = soup.cssselect("#content a")
		for url in urls_deputados:
			get_data(url.get("href"), ano)
		
def get_data(url, ano):
	html = urllib.urlopen(url).read()
	soup = fromstring(html)
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
	
	#prints
	print data["legislatura"]	
	print data["id"]
	print data["nome"]
	print data["partido"]
	print data["estado"]
	print data["nascimento"]
	print data["naturalidade"]
	print data["profissoes"]
	print data["filiacao"]
	print data["imagem"]
	print data["outros"]
	
	#save
	table.writerow(data, unique_columns=['id'])

#connect
database = Database('webstore.thedatahub.org', 'danielabsilva', 'deputados_brazil', http_apikey='f2476977-c91e-49cb-a9c3-ab9ad7d34730')
table = database['deputados_bio']

get_url()




