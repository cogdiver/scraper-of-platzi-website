import requests
import lxml.html as html
from timeit import default_timer

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


def parse_course(link, idCourse):
  global fileCourses
  global modulesCourses

  try:
    response = requests.get(link)
    if response.status_code == 200:
      curso = response.content.decode('utf-8')
      parsed = html.fromstring(curso)
      Modules = parsed.xpath(XPATH_MODULES)
      
      modulesCourses[idCourse]=[]

      for i in range(len(Modules)):
        try:
          nameModule = parsed.xpath(NAMES_MODULES.replace('{index}',str(i+1)))[0]
        except IndexError:
          nameModule = ''
          
        nameClassModule = parsed.xpath(NAME_CLASS_MODULES.replace('{index}',str(i+1)))
        modulesCourses[idCourse].append([nameModule, nameClassModule])

      fileCourses[idCourse].append(modulesCourses[idCourse])
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve, ' - ',link)


def parse_courses():
  global fileCourses
  
  for idCourse in fileCourses:
    parse_course(HOME_URL+'/cursos/'+idCourse,idCourse)


def parse_route(link, idRoute, idCategory):
  global filePaths
  global fileCourses

  global namesRoutes
  global imagesRoutes
  global descrsRoutes

  global levelsPaths

  try:
    response = requests.get(link)

    if response.status_code == 200:
      route = response.content.decode('utf-8')
      parsed = html.fromstring(route)

      namesRoutes[idRoute] = parsed.xpath(NAMES_ROUTES)[0]
      imagesRoutes[idRoute] = parsed.xpath(IMAGES_ROUTES)[0]
      descrsRoutes[idRoute] = parsed.xpath(DESCRS_ROUTES)[0]
      
      levelsPath = parsed.xpath(XPATH_LEVELS)

      levelsPaths[idRoute]=[]
      for i in range(len(levelsPath)):
        tittleLevel = parsed.xpath(TITTLE_LEVEL.replace('{index}',str(i+1)))[0]
        namesLevel = parsed.xpath(NAMES_LEVEL.replace('{index}',str(i+1)))[0]
        
        imgCourses = parsed.xpath(IMAGES_COURSES.replace('{index}',str(i+1)))
        nameCourses = parsed.xpath(NAMES_COURSES.replace('{index}',str(i+1)))
        linkCourses = parsed.xpath(LINKS_TO_COURSES.replace('{index}',str(i+1)))

        idCourses = [link.replace('/cursos/','').replace('/','') for link in linkCourses]

        for index in range(len(idCourses)):
          idCourse = idCourses[index]
          url = linkCourses[index]
          name = nameCourses[index]
          img = imgCourses[index]

          try:
            x = fileCourses[idCourse]
          except KeyError:
            fileCourses[idCourse]=[]
            fileCourses[idCourse].append(url)
            fileCourses[idCourse].append(name)
            fileCourses[idCourse].append(img)
            
          if len(fileCourses[idCourse])==3:
            fileCourses[idCourse].append([idRoute])
          else:
            if idRoute not in fileCourses[idCourse][3]:
              fileCourses[idCourse][3].append(idRoute)


          try:
            proyectLevel = parsed.xpath(PROYECTS_LEVEL.replace('{index}',str(i+1)))[0]
          except:
            proyectLevel = False

        levelsPaths[idRoute].append([tittleLevel, namesLevel, idCourses, proyectLevel])


      url = link.replace('https://platzi.com','')
      filePaths[idRoute]=[url, namesRoutes[idRoute], imagesRoutes[idRoute], idCategory, descrsRoutes[idRoute], levelsPaths[idRoute]]
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve, ' - ',link)


def parse_link_routes(link, idCategory):
  global linksRoutes

  try:
    response = requests.get(link)
    
    if response.status_code == 200:
      category = response.content.decode('utf-8')
      parsed = html.fromstring(category)
      linksRoutes[idCategory] = parsed.xpath(LINKS_TO_ROUTES)
      
      paths = []
      for url in linksRoutes[idCategory]:
        idRoute = url.replace('/','')
        paths.append(idRoute)
        parse_route(HOME_URL+url, idRoute, idCategory)

      return paths
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve, ' - ',link)


def parse_home():
  global fileCategorys
  
  global linksCategorys
  global namesCategorys

  try:
    response = requests.get(HOME_URL)
    if response.status_code == 200:
      home = response.content.decode('utf-8')
      parsed = html.fromstring(home)
      linksCategorys = parsed.xpath(XPATH_LINK_TO_CATEGORYS)
      namesCategorys = parsed.xpath(XPATH_NAME_CATEGORYS)
      
      for index in range(len(linksCategorys)):
        url = linksCategorys[index]
        idCategory = url.replace('/categorias/','').replace('/','')
        name = namesCategorys[index]

        paths = parse_link_routes(HOME_URL+url, idCategory)
        fileCategorys[idCategory]=[url, name, paths]
    else:
      raise ValueError(f'Error: {response.status_code}')
  except ValueError as ve:
    print(ve, ' - ',HOME_URL)


def run():
  parse_home()
  parse_courses()


def scraper():
  run()


if __name__ == '__main__':
  inicio = default_timer()
  scraper()
  fin = default_timer()
  time = fin - inicio
  print('Timer ___________________________________________________________________')
  print(time)
  print('\n')
  print('File of Categorys ___________________________________________________________________')
  print(fileCategorys)
  print('\n')
  print('File of Paths ___________________________________________________________________')
  print(filePaths)
  print('\n')
  print('File of Courses ___________________________________________________________________')
  print(fileCourses)
