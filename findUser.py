import requests
from bs4 import BeautifulSoup

def userInfo(character_name):
    url = "https://maple.gg/u/"+character_name # 크롤링할 웹 페이지 주소
    response = requests.get(url) # 웹 페이지 요청

    soup = BeautifulSoup(response.text, "html.parser") # HTML 파싱

    floor = soup.find("h1","user-summary-floor font-weight-bold").text + "층"
    level = soup.find("li","user-summary-item").text

    print(floor[:2])
    print(level)
    
    return [floor[:2]+"층",level]
