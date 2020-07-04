import requests
import time
from bs4 import BeautifulSoup
import json

def getAllSiteUrls(start_url, link_class, flag):
	"""function to get all Urls of Sites with Recipes from provided Start_url and provided link class
		only to update if flag is true"""
	if flag == True:
		linkDICT = {}
		try:
			r = requests.get(start_url)
			if r.status_code == 200:
				print("got start site : %s"%(start_url))
				soup = BeautifulSoup(r.text, 'html.parser')
				links = soup.find_all("a" ,{"class": link_class})
				for link in links:
					linkDICT[link.decode_contents()] = link.get("href")
			else:
				print("error while getting start site: %s"%(r.status_code))
		except requests.exceptions.MissingSchema as error:
			print("++++++++++++++++")
			print(error)
			print("++++++++++++++++")
		except requests.exceptions.ConnectionError as error:
			print("++++++++++++++++")
			print(error)
			print("++++++++++++++++")
		finally:
			with open('links.json', 'w', encoding='utf-8') as f:
				json.dump(linkDICT, f, ensure_ascii=False, indent=4)
			return linkDICT
	else:
		print("getting links from links.json")
		with open("links.json") as links_file:
			linkDICT = json.load(links_file)
		return linkDICT


if __name__ == "__main__":
	with open("config.json") as config_file:
		CONFIG = json.load(config_file)
	linkDICT = getAllSiteUrls(CONFIG["start_url"], CONFIG["link_class"], CONFIG["update_links_flag"])
