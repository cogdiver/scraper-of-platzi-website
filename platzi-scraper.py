import requests
import lxml.html as html
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')


#Constantes de xpath
HOME_URL = 'https://platzi.com'
XPATH_LINK_TO_CATEGORYS = '//div[@class="CategoriesSection"]/div/a/@href'
XPATH_NAME_CATEGORYS = '//div[@class="CategoriesSection"]/div/a/text()'

LINKS_TO_ROUTES = '//div[@class="LearningPathsList-content"]/a/@href'

NAMES_ROUTES = '//div[@class="Hero-route"]/div[@class="Hero-route-head"]//h1/text()'
IMAGES_ROUTES = '//div[@class="Hero-route"]/div[@class="Hero-route-head"]//img/@src'
DESCRS_ROUTES = '//div[@class="Hero-route"]/div[@class="Hero-route-desc"]/span/text()'

XPATH_LEVELS = '//div[@class="RoutesList"]'
TITTLE_LEVEL = '//div[@class="RoutesList"][{index}]/h3/text()'
NAMES_LEVEL = '//div[@class="RoutesList"][{index}]//div[@class="RoutesList-level"]/span/text()'
PROYECTS_LEVEL = '//div[@class="RoutesList"][{index}]//h4[@class="Projects-info-name"]/text()'

IMAGES_COURSES = '//div[@class="RoutesList"][{index}]//a[@class="RoutesList-item"]//img/@src'
NAMES_COURSES = '//div[@class="RoutesList"][{index}]//a[@class="RoutesList-item"]/h4/text()'
LINKS_TO_COURSES = '//div[@class="RoutesList"][{index}]//a[@class="RoutesList-item"]/@href'

XPATH_MODULES = '//div[@class="Content-wrapper u-wrapper"]//div[@class="ContentBlock"]'
NAMES_MODULES = '//div[@class="Content-wrapper u-wrapper"]//div[@class="ContentBlock"][{index}]//h3[@class="ContentBlock-head-title"]/text()'
NAME_CLASS_MODULES = '//div[@class="Content-wrapper u-wrapper"]//div[@class="ContentBlock"][{index}]//a//span/text()'

#Variables de contenido
linksCategorys = []
namesCategorys = []

linksRoutes = {}

namesRoutes = {}
imagesRoutes = {}
descrsRoutes = {}

levelsPaths = {}

modulesCourses = {}

#Variables de archivo
fileCategorys = {}
filePaths = {}
fileCourses = {}

def parse_course(link):
  pass

def parse_route(link):
  try:
    response = requests.get(link)
    if response.status_code == 200:
      route = response.content.decode('UTF-8')
      parsed = html.fromstring(route)

      imagesRoutes = parsed.xpath(IMAGES_ROUTES)
      namesRoutes = parsed.xpath(NAMES_ROUTES)
      descrsRoutes = parsed.xpath(DESCRS_ROUTES)

      descrsLevel = parsed.xpath(DESCRS_LEVEL)
      namesLevel = parsed.xpath(NAMES_LEVEL)
      proyectsLevel = parsed.xpath(PROYECTS_LEVEL)

      imagesCourses = parsed.xpath(IMAGES_COURSES)
      namesCourses = parsed.xpath(NAMES_COURSES)
      linksCourses = parsed.xpath(LINKS_TO_COURSES)

      for link in linksCourses:
        parse_course(HOME_URL+link)
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve)


def parse_link_routes(link):
  pass
  #print(link)
  #try:
  #  response = requests.get(link)
  #  if response.status_code == 200:
  #    category = response.content.decode('UTF-8')
  #    parsed = html.fromstring(category)
  #    linksRoutes = parsed.xpath(LINKS_TO_ROUTES)

  #    for link in linksRoutes:
  #      parse_route(HOME_URL+link)
  #  else:
  #    raise ValueError(f'Error: {response.status_code}')
  #except ValueError as ve:
  #  print(ve)


def parse_home():
  try:
    response = requests.get(HOME_URL)
    if response.status_code == 200:
      home = response.content.decode('utf-8')
      parsed = html.fromstring(home)

      global linksCategorys
      global namesCategorys
      linksCategorys = parsed.xpath(XPATH_LINK_TO_CATEGORYS)
      namesCategorys = parsed.xpath(XPATH_NAME_CATEGORYS)
      #if not os.path.isdir("data"):
      #  os.mkdir("data")
      
      #for link in linksCategorys:
      #  parse_link_routes(HOME_URL+link)

      print(linksCategorys)
      print(namesCategorys)

      for link in linksCategorys:
        index = linksCategorys.index(link)
        big_link=link
        link = link.replace('/categorias/','')
        link = link.replace('/','')

        name=namesCategorys[index]

        with open(f'data/{link}.txt','w',encoding='utf-8') as f:
          f.write(big_link)
          f.write('\n')
          f.write(link)
          f.write('\n')
          f.write(name)


    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve)

def run():
  parse_home()
  print('niña')


if __name__ == '__main__':
  run() 
