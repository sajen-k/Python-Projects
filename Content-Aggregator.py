import json
import notify2
import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize

def alert(info):
	notify2.init('content aggr')
        notif = notify2.Notification('content', info)
	# notif.set_urgency(notify2.URGENCY_CRITICAL)
        notif.show()
        notif.set_timeout(10)

with open('ca_cfgs.json', 'r') as reader:
	cfgs = reader.read()

def get_content():
	url = json.loads(cfgs)['source']

	# Retrieve page
	page = requests.get(url).text

	# Tbs object
	soup = BeautifulSoup(page, 'html.parser')

	# headline
	headline = soup.find('h1').get_text()

	# <p> tags text
	p_tags = soup.find_all('p’)
	p_tags_text = [tag.get_text().strip() for tag in p_tags] # @ 'p' & strip

	# Filter out sentences filter; chars '\n', no '.'
	sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
	sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

	# Combine items list
	article = ' '.join(sentence_list)
	summary = summarize(article_text, ratio = 0.3)

	return summary

alert(get_content())