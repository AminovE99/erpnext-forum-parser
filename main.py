import json

import requests
import xmltodict as xmltodict
from bs4 import BeautifulSoup
import dicttoxml


def create_xml_by_list_with_data(list_with_data):
    xml_template = None
    with open('xml_template.xml', 'r') as file:
        xml = file.read()
        xml_template = xmltodict.parse(xml)
    i = 0
    for node in list_with_data:
        xml_template['documents']['document'][i]['@id'] = i
        xml_template['documents']['document'][i]['url'] = node['url']
        xml_template['documents']['document'][i]['title'] = node['title']
        xml_template['documents']['document'][i]['text'] = node['text']
        xml_template['documents']['document'][i]['keywords'] = node['category']
        i += 1

    xml_result = xmltodict.unparse(xml_template)
    with open('xml_result.xml', 'w') as file:
        file.write(xml_result)


def get_text_and_category_from_topic(link):
    res = requests.get(link + '.rss')
    xml = xmltodict.parse(res.text)
    text = xml['rss']['channel']['description']
    category = xml['rss']['channel']['category']
    return text, category


if __name__ == '__main__':
    rs = requests.get("https://discuss.erpnext.com/")
    soup = BeautifulSoup(rs.text)
    topics = soup.findAll('tr')
    list_with_content = []
    for topic in topics:
        if len(topic.text) > 25:
            link = topic.contents[1].contents[3].attrs['content']
            title = topic.contents[1].contents[5].attrs['content']
            # keywords = topic.contents[1].contents[9].contents[1].contents[0].attrs.contents[0]
            print(link)
            text, category = get_text_and_category_from_topic(link)
            list_with_content.append({'url': link, 'title': title, 'text': text, 'category': category})
    create_xml_by_list_with_data(list_with_content)
