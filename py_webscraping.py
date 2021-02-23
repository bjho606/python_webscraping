from selenium import webdriver
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

def create_soup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return BeautifulSoup(res.text, "lxml")

def scrape_weather():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8"
    soup = create_soup(url)

    print("[오늘의 날씨]")

    weather_datas = soup.find("div", attrs={"class":"api_subject_bx"})
    cast = weather_datas.find("p", attrs={"class":"cast_txt"}).get_text().strip()
    today_temp = weather_datas.find("span", attrs={"class":"todaytemp"}).get_text().strip()
    min_temp = weather_datas.find("span", attrs={"class":"min"}).find("span").get_text().strip()
    max_temp = weather_datas.find("span", attrs={"class":"max"}).find("span").get_text().strip()
    morning_rain = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip()
    afternoon_rain = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip()

    print(cast)
    print(f"현재 {today_temp}˚C (최저 {min_temp}˚ / 최고 {max_temp}˚)")
    print(morning_rain + " / " + afternoon_rain)
    print()

    dust_datas = soup.find("dl", attrs={"class":"indicator"}).find_all("dd")
    dust = dust_datas[0].get_text().strip()
    small_dust = dust_datas[1].get_text().strip()

    print("미세먼지 " + dust)
    print("초미세먼지 " + small_dust)
    print()

def scrape_headline_news():
    url = "https://news.naver.com/"
    soup = create_soup(url)

    print("[헤드라인 뉴스]")

    news_datas = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3) # limit : 몇 개 찾을지 개수 정할 수 있음
    for index, news in enumerate(news_datas):
        article = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print(f"{index+1}. {article}")
        print(f"(링크 : {link})")
    print()

def scrape_it_news():
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)

    print("[IT 뉴스]")

    news_datas = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_datas):
        article = news.find_all("dt")[1].find("a").get_text().strip()
        link = url + news.find_all("dt")[1].find("a")["href"]
        print(f"{index+1}. {article}")
        print(f"(링크 : {link})")
    print()

def scrape_english():
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    
    print("[오늘의 영어 회화]")

    conversations = soup.find_all("div", attrs={"class":"conv_txtBox"})

    print("(영어 지문)")
    english_conv = conversations[1].find("div", attrs={"class":"conv_txt"}).find_all("div")
    for conv in english_conv:
        print(conv.get_text().strip())
    print()
    print("(한글 지문)")
    korean_conv = conversations[0].find("div", attrs={"class":"conv_txt"}).find_all("div")
    for conv in korean_conv:
        print(conv.get_text().strip())
    print()

if __name__ == "__main__":
    scrape_weather()
    scrape_headline_news()
    scrape_it_news()
    scrape_english()