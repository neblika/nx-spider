from bs4 import BeautifulSoup
from modifier import Modifier
from browser import Browser
from copy import deepcopy
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
    self._scanning = True
    self.links = []
    self.scanned_links = []
    self._load_urls_list()


  @property
  def scanning(self):
    return self._scanning


  def _load_urls_list(self):
    with open("urls.json", "r") as rFile:
      self.links = json.load(rFile)


  def start(self):
    while self._scanning:
      for link in self.links:
        if link in self.scanned_links:
          print(f"link was already scanned: {link}")
          continue

        self.scanned_links.append(link)
        print(f"searching: {link}")
        rootLink, domain = self.get_domain(link)
        nodeAttr = self.modifier.node_target(link)
        self.browser.win.get(link)

        html = self.browser.win.page_source
        html_links = self.extract_links(html, rootLink)
        # print("html_links", html_links)

        for html_link in html_links:
          if html_link not in self.links:
            self.links.append(html_link)

        node_target = self.get_node(html, search=nodeAttr)
        print(self.extract_texts(
          soup=node_target,
          excludes=["nav", "aside", "header", "footer"]
        ))

    self.browser.quit()


  def get_node(self, html, search=None):
    soup = BeautifulSoup(html)
    if search:
      nodeAttr = search.split("=")
      nodeMatches = soup.find_all(attrs={nodeAttr[0]: nodeAttr[1]})
      node_target = nodeMatches[0] if len(nodeMatches) else soup 
      return node_target
    return soup


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
    return set(links)


  def decompose_nodes(self, soup, nodes):
    """ delete nodes from soup """
    if not soup or not nodes: return
    elements = soup.find_all(nodes)
    for element in elements:
      element.decompose()


  def extract_texts(self, soup, excludes=None):
    """ return a text (content) from soup """
    self.decompose_nodes(
      soup=soup,
      nodes=excludes
    )
    elements = soup.find_all(['p', "h1", "h2", "h3", "h4", "li"])
    content = ""
    for element in elements:
      text = element.get_text()
      if element.name in ["h1" , "h2", "h3", "h4"]: text += "\n"
      text = re.sub(r'\n+', '\n', text)
      text = re.sub(r' +', ' ', text)
      if len(text) < 2: continue
      content += text + " "
    return content


  def get_domain(self, link):
    """ returns (root link, domain) """
    matches = re.findall(r"(https?:\/\/(([a-zA-Z0-9]\.?-?_?)*))", link)
    return matches[0][0], matches[0][1]


if __name__ == '__main__':
  spider = Spider()
  spider.start()
