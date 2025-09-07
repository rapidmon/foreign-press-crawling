from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta, timezone
import time
import re
from urllib.parse import urljoin
import json
from email_sender import NewsEmailSender

KST = timezone(timedelta(hours=9))

class NewsCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def crawl_bbc_headline(self):       
        try:
            url = "https://www.bbc.com/news"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # BBC 메인 컨텐츠 영역
            main_content = soup.select_one("#main-content article section div div div")
            
            headline_link = main_content.select_one('a[href*="/news/"]')
            
            title = headline_link.get_text(strip=True)
            link = urljoin(url, headline_link.get('href', ''))
            
            print("BBC 메인 헤드라인:")
            print(f"제목: {title}")
            print(f"링크: {link}")
            return {
                'title': title,
                'link': link
            }
            
        except Exception as e:
            print(f"BBC 크롤링 실패: {e}")
            return None
    
    def crawl_cnn_headline(self):       
        try:
            url = "https://www.cnn.com/"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # CNN 메인 헤드라인 - 제공된 구조 기반
            headline_link = soup.select_one('.container__title--emphatic a')
            
            title_element = headline_link.select_one('h2') or headline_link
            title = title_element.get_text(strip=True)
            link = urljoin(url, headline_link.get('href', ''))
            
            print("CNN 메인 헤드라인:")
            print(f"제목: {title}")
            print(f"링크: {link}")
            return {
                'title': title,
                'link': link
            }

            return None
            
        except Exception as e:
            print(f"CNN 크롤링 실패: {e}")
            return None
    
    def crawl_fox_headline(self):       
        try:
            url = "https://www.foxnews.com/"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Fox News 메인 헤드라인 - big-top 영역의 첫 번째 기사
            headline_link = soup.select_one('.big-top .content article .info-header h3.title a')
            
            title = headline_link.get_text(strip=True)
            link = urljoin(url, headline_link.get('href', ''))
            
            print("Fox News 메인 헤드라인:")
            print(f"제목: {title}")
            print(f"링크: {link}")
            return {
                'title': title,
                'link': link
            }

            return None
            
        except Exception as e:
            print(f"Fox News 크롤링 실패: {e}")
            return None
    
    def crawl_nyt_headline(self):       
        try:
            url = "https://www.nytimes.com/"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # NYT 메인 헤드라인 - story-wrapper 영역의 링크
            headline_link = soup.select_one('.story-wrapper .indicate-hover')
            
            parent_link = headline_link.find_parent('a')
            title = headline_link.get_text(strip=True)
            link = urljoin(url, parent_link.get('href', ''))
            
            print("NYT 메인 헤드라인:")
            print(f"제목: {title}")
            print(f"링크: {link}")
            return {
                'title': title,
                'link': link
            }
            
            return None
            
        except Exception as e:
            print(f"NYT 크롤링 실패: {e}")
            return None

    def crawl_wp_headline_selenium(self):
        """Selenium으로 Washington Post 메인 헤드라인 크롤링"""
        driver = None
        try:
            # Chrome 옵션 설정
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 브라우저 창 숨기기
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # WebDriver 초기화
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            url = "https://www.washingtonpost.com/"
            driver.get(url)
            
            # 페이지 로딩 대기
            wait = WebDriverWait(driver, 10)
            
            # 요소가 나타날 때까지 대기
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.headline h2 a span')))
            
            if element:
                title = element.text.strip()
                
                # 부모 링크 찾기
                link_element = element.find_element(By.XPATH, './ancestor::a[1]')
                link = urljoin(url, link_element.get_attribute('href'))
                
                print("Washington Post 메인 헤드라인:")
                print(f"제목: {title}")
                print(f"링크: {link}")
                
                return {
                    'title': title,
                    'link': link
                }
            
        except Exception as e:
            print(f"❌ WP Selenium 크롤링 실패: {e}")
            return None
            
        finally:
            if driver:
                driver.quit()

    def crawl_yonhap_request(self):
        """연합뉴스 국제 기사 - requests로 웹페이지에서 크롤링 (수정된 버전)"""
        def parse_yonhap_time(time_text):
            """연합뉴스 시간 텍스트 파싱 (09-07 20:52 형식)"""
            try:
                # 현재 연도 가져오기
                current_year = datetime.now().year
                
                # 09-07 20:52 형식 파싱
                if len(time_text.split()) == 2:
                    date_part, time_part = time_text.split()
                    
                    # 월-일 시:분 형식
                    if '-' in date_part and ':' in time_part:
                        month, day = date_part.split('-')
                        hour, minute = time_part.split(':')
                        
                        parsed_time = datetime(
                            year=current_year,
                            month=int(month),
                            day=int(day),
                            hour=int(hour),
                            minute=int(minute),
                            tzinfo=KST
                        )
                        
                        return parsed_time
                
                return None
                
            except Exception as e:
                print(f"시간 파싱 실패: {time_text}, 오류: {e}")
                return None

        def get_yonhap_content_request(url):
            """연합뉴스 기사 본문 가져오기 (requests 방식)"""
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                content_div = soup.select_one('#articleWrap')
                
                if content_div:
                    for unwanted in content_div.find_all(['script', 'style', 'aside', 'footer', 'nav']):
                        unwanted.decompose()
                    
                    text = content_div.get_text(strip=True)
                    return text
                
            except Exception as e:
                print(f"본문 가져오기 실패: {e}")
                return None
                
        print("=== 연합뉴스 국제 기사 테스트 (requests) ===")
        try:
            # 시간 필터링 (전날 23:00 ~ 당일 08:30)
            now = datetime.now(KST)
            yesterday_23 = (now - timedelta(days=1)).replace(hour=23, minute=0, second=0, microsecond=0)
            today_0830 = now.replace(hour=8, minute=30, second=0, microsecond=0)
            
            print(f"필터링 시간: {yesterday_23} ~ {today_0830}")
            
            filtered_articles = []
            
            # 1페이지와 2페이지 크롤링
            for page in [1, 2, 3]:
                url = f"https://www.yna.co.kr/international/all/{page}"
                print(f"\n페이지 {page} 크롤링: {url}")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # div.section01 안의 뉴스 링크들
                news_links = soup.select('div.section01 a.tit-news')

                # div.section01 안의 시간 요소들  
                time_elements = soup.select('div.section01 span.txt-time')
                
                # 각 뉴스 링크 처리
                for i, link in enumerate(news_links):
                    try:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        # 절대 URL로 변환
                        full_link = urljoin('https://www.yna.co.kr', href)
                        
                        # 시간 정보 찾기
                        article_time = None
                        time_text = time_elements[i].get_text(strip=True)
                        article_time = parse_yonhap_time(time_text)
                        
                        # 시간 필터링
                        if yesterday_23 <= article_time <= today_0830:
                            filtered_articles.append({
                                'title': title,
                                'link': full_link,
                                'published': article_time
                            })
                            
                            print(f"\n📰 기사 {len(filtered_articles)}:")
                            print(f"제목: {title}")
                            print(f"발행시간: {article_time}")
                            print(f"링크: {full_link}")
                            content = get_yonhap_content_request(full_link)
                            print(f"본문 ({len(content)}자): {content}")

                    except Exception as e:
                        print(f"기사 {i+1} 처리 중 오류: {e}")
                        continue
            
            print(f"\n✅ 시간 범위 내 총 기사 수: {len(filtered_articles)}")
            return filtered_articles
            
        except Exception as e:
            print(f"❌ 연합뉴스 크롤링 실패: {e}")
            return []

def main():
    """메인 실행 함수"""
    print("=== 일일 뉴스 크롤링 시작 ===")
    
    # 기존 크롤러 인스턴스 생성
    crawler = NewsCrawler()
    email_sender = NewsEmailSender()
    
    # 외신 크롤링
    foreign_news = {}
    foreign_sites = [
        ("BBC", crawler.crawl_bbc_headline),
        ("CNN", crawler.crawl_cnn_headline),
        ("Fox News", crawler.crawl_fox_headline),
        ("NYT", crawler.crawl_nyt_headline),
        ("Washington Post", crawler.crawl_wp_headline_selenium)
    ]
    
    for site_name, crawl_func in foreign_sites:
        try:
            print(f"\n{site_name} 크롤링 중...")
            result = crawl_func()
            foreign_news[site_name] = result
            time.sleep(2)
        except Exception as e:
            print(f"{site_name} 크롤링 실패: {e}")
            foreign_news[site_name] = None
    
    # 연합뉴스 크롤링
    try:
        print(f"\n연합뉴스 크롤링 중...")
        yonhap_articles = crawler.crawl_yonhap_request()
    except Exception as e:
        print(f"연합뉴스 크롤링 실패: {e}")
        yonhap_articles = []
    
    # 결과 요약
    print(f"\n=== 크롤링 결과 요약 ===")
    print(f"외신 성공: {sum(1 for v in foreign_news.values() if v)}/{len(foreign_news)}")
    print(f"연합뉴스 기사: {len(yonhap_articles)}개")
    
    # 이메일 발송
    print(f"\n이메일 발송 중...")
    success = email_sender.send_email(foreign_news, yonhap_articles)
    
    if success:
        print("🎉 일일 뉴스 브리핑 완료!")
    else:
        print("❌ 이메일 발송 실패")

if __name__ == "__main__":
    main()