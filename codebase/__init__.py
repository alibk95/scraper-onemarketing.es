from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    # https://dev.to/nazliander/using-selenium-within-a-docker-container-ghp
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options
# all links
#urls = ["https://onemarketingplace.es/busqueda/empresa/de/agencia-de-medios", "https://onemarketingplace.es/busqueda/empresa/de/agencias-digitales",
#        "https://onemarketingplace.es/busqueda/empresa/de/artes-graficas", "https://onemarketingplace.es/busqueda/empresa/de/asesorias-y-agencias",
#        "https://onemarketingplace.es/busqueda/empresa/de/asociaciones-de-marketing", "https://onemarketingplace.es/busqueda/empresa/de/bases-de-datos",
#        "https://onemarketingplace.es/busqueda/empresa/de/comunicacion-y-relaciones-publicas", "https://onemarketingplace.es/busqueda/empresa/de/consultoria-y-asesores",
#        "https://onemarketingplace.es/busqueda/empresa/de/desarrollo-web", "https://onemarketingplace.es/busqueda/empresa/de/ecommerce",
#        "https://onemarketingplace.es/busqueda/empresa/de/emailmarketing", "https://onemarketingplace.es/busqueda/empresa/de/eventos-y-congresos",
#        "https://onemarketingplace.es/busqueda/empresa/de/formacion-en-marketing", "https://onemarketingplace.es/busqueda/empresa/de/incentivos-y-merchandising",
#        "https://onemarketingplace.es/busqueda/empresa/de/incubadoras-de-negocio", "https://onemarketingplace.es/busqueda/empresa/de/investigacion-de-mercados",
#        "https://onemarketingplace.es/busqueda/empresa/de/marketing-movil", "https://onemarketingplace.es/busqueda/empresa/de/marketing-servicios",
#        "https://onemarketingplace.es/busqueda/empresa/de/marketing-de-contenidos", "https://onemarketingplace.es/busqueda/empresa/de/medios-y-soportes",
#        "https://onemarketingplace.es/busqueda/empresa/de/performance-marketing", "https://onemarketingplace.es/busqueda/empresa/de/produccion-multimedia",
#        "https://onemarketingplace.es/busqueda/empresa/de/redes-sociales", "https://onemarketingplace.es/busqueda/empresa/de/telemarketing"]

urls = ["https://onemarketingplace.es/busqueda/empresa/de/incubadoras-de-negocio", "https://onemarketingplace.es/busqueda/empresa/de/investigacion-de-mercados",
        "https://onemarketingplace.es/busqueda/empresa/de/marketing-movil", "https://onemarketingplace.es/busqueda/empresa/de/marketing-servicios",
        "https://onemarketingplace.es/busqueda/empresa/de/marketing-de-contenidos", "https://onemarketingplace.es/busqueda/empresa/de/medios-y-soportes",
        "https://onemarketingplace.es/busqueda/empresa/de/performance-marketing", "https://onemarketingplace.es/busqueda/empresa/de/produccion-multimedia",
        "https://onemarketingplace.es/busqueda/empresa/de/redes-sociales", "https://onemarketingplace.es/busqueda/empresa/de/telemarketing"]
# dataframe

# df = pd.DataFrame(columns=['address', 'business', 'category', 'company_description', 'company_name', 'company_url',
#                           'country', 'country_code', 'email', 'experience', 'facebook_url', 'first_name', 'found_at_url',
#                           'instagram_url', 'keywords', 'languages', 'last_name', 'linkedin_url', 'locality', 'middle_name',
#                           'number_of_ratings', 'other_emails', 'other_phones', 'other_urls', 'phone', 'premium', 'province',
#                           'rating', 'region', 'retrieved_timestamp', 'service', 'source', 'tags', 'twitter_url', 'verified',
#                           'working_hours', 'zip', 'service_slug', 'comment'])
base = "https://onemarketingplace.es"
for url in urls:
    df = pd.DataFrame(columns=['company_name', 'email', 'phone', 'address', 'review', 'company_url', 'service'])
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get(url)

    # Automatically scroll till the end of the page
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    # Give it a 10 second rest to load whatever left behind : )) and then close the browser.
    time.sleep(4)
    page = driver.page_source
    driver.quit()

    # Make the soup here...magic happens here!
    soup = BeautifulSoup(page, 'html.parser')
    # the part that is loaded by the script is accessible
    pg = soup.find("div", attrs={"class": "listado__izquierda"})
    p = pg.find_all("article", attrs={"class": "item_from_search margen_top_20"})

    # Just wanted to check how many records we got
    # print(len(p))

    for s in p:
        # p consists of all the different articles in the webpage and the following path leads to the "title"
        print(s.h2.text)
        # retrieving the more info link to access the email information from there
        s1 = s.find("div", attrs={"class": "item_more_info"})
        service = s.find("div", {"class":"item_category"}).text
        link = s1.a.get("href")
        # concat the base link and the retrieved one and ready to access that as well
        complete_link = base + link
        # print(complete_link)
        req = Request(complete_link)
        pge = urlopen(req)
        # sp now consists of the page with information for each article. e.g. email
        sp = BeautifulSoup(pge, "html.parser")
        email = sp.find("a", attrs={"class": "contenido__correo"}).get("href")
        company_url = sp.find("a", attrs={"class": "contenido__web"}).get("href")
        phone = sp.find("div", attrs={"class":"meta_info"}).find_all("div", attrs={"class":"item_meta_cell"})[1].text
        address = sp.find("div", attrs={"class":"mapa-google"}).p.text
        review = sp.find("div", attrs={"class":"item_stars"}).find_all("img", attrs={"class":"star-rosa"})

        # counts the stars in the review
        count = 0
        for star in review:
            if star['src'] == "/imagenes/ico-star-rosa.png":
                count += 1
            if star['src'] == "/imagenes/ico-star-halfrosa.png":
                count += 0.5

        # strip() to clean the useless spaces in the string
        address = address.strip()
        if email == "mailto:":
            email = ""
        print(email)
        print(company_url)
        print(phone)
        print(address)
        print(count)
        print(service)
        # add the info's to the data frame.
        df = df.append({'company_name': s.h2.text, 'email': email[7:], 'phone': phone, 'address': address,
                        'review': count, 'company_url': company_url, 'service': service}, ignore_index=True)
        # the most important thing is the object destructive function as we create a new object in each iteration
        # there's gonna be a heavy load on the system if we keep them all
        # So after each iteration we delete it
        del (sp)
        print("#####################")
    df.to_csv('./output.csv', index=False, header=False, mode='a')
    df = None
    print("##### Pushed to Csv #####")


