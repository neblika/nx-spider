from bs4 import BeautifulSoup
from browser import Browser
import json

print("======================")
print("=== Spider Project ===")
print("======================")


browser = Browser()


with open("urls.json", "r") as rFile:
  pages = json.load(rFile)


for page in pages:
  node = page.get("node")
  browser.win.get(page["url"])
  html = browser.win.page_source

  if node:
    soup = BeautifulSoup(html)
    nodeAttr = node.split("=")
    nodeMatches = soup.find_all(attrs={nodeAttr[0]: nodeAttr[1]})
    node_target = nodeMatches[0]
    print(node_target.get_text())
  else:
    soup = BeautifulSoup(html)
    print(soup.get_text())

  browser.quit()
