from bs4 import BeautifulSoup
from modifier import Modifier
from browser import Browser
import json
import re


print("======================")
print("=== Spider Project ===")
print("======================")



class Spider:
  def __init__(self):
    super(Spider, self).__init__()
    self.browser = Browser()
    self.modifier = Modifier()
    self.links = []
    self._load_urls_list()


  def _load_urls_list(self):
    with open("urls.json", "r") as rFile:
      self.links = json.load(rFile)


  def start(self):
    for link in self.links:
      print(f"searching: {link}")
      rootLink, domain = self.get_domain(link)
      nodeAttr = self.modifier.node_target(link)
      self.browser.win.get(link)
      html = self.browser.win.page_source
      html_links = self.extract_links(html, rootLink)

      print("html_links", html_links)

      if nodeAttr:
        node_target = self.get_node(html, search=nodeAttr)
        print(self.extract_texts(soup=node_target))
      else:
        soup = BeautifulSoup(html)
        print(self.extract_texts(soup=soup))   

    self.browser.quit()


  def get_node(self, html, search):
    soup = BeautifulSoup(html)
    nodeAttr = search.split("=")
    nodeMatches = soup.find_all(attrs={nodeAttr[0]: nodeAttr[1]})
    node_target = nodeMatches[0]
    return node_target


  def extract_links(self, html, rootLink):
    soup = BeautifulSoup(html)
    nodeMatches = soup.find_all(href=True)
    links = []
    for element in nodeMatches:
      link = element["href"]
      if not link.startswith("http"):
        links.append(rootLink + link)
      else:
        links.append(link)
    return links


  def extract_texts(self, soup):
    elements = soup.find_all(['p', "h1", "h2", "h3", "h4"]) # li
    content = ""
    for element in elements:
      # print(element.name)
      text = element.get_text()
      text = re.sub(r'\n+', '\n', text)
      text = re.sub(r'\s+', ' ', text)
      if len(text) < 2: continue
      # print(">>> ", text)
      content += element.get_text() + " "
    return content


  def get_domain(self, link):
    """ returns (root link, domain) """
    matches = re.findall(r"(https?:\/\/(([a-zA-Z0-9]\.?-?_?)*))", link)
    return matches[0][0], matches[0][1]


if __name__ == '__main__':
  spider = Spider()
  spider.start()
