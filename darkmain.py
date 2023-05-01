import requests
import pandas as pd
from bs4 import BeautifulSoup
from filter_words import filter_words

def crawl_tor(df, filter_words):
# Tor proxy 설정, tor 브라우저 필수 붑분
    proxies = {'http': 'socks5h://localhost:9150',
               'https': 'socks5h://localhost:9150'}

    # Onion URLs를 DataFrame으로 로드하고 .onion이 포함된 URL만 선택하여 중복을 제거
    # df = pd.read_csv('onion_urls.csv', header=None, names=['url'])
    df = df[df['url'].str.contains('.onion')].drop_duplicates() # contains로 .onion 감지 및 drop_duplicates()중복제거
    # https://wikidocs.net/154060
    result1 = []
    result2 = []
    result3 = []
    # title, lang, 키워드 사전 기반 앵커 태그 크롤링
    for url in df['url']:
        try:
            # 페이지 가져오기
            response = requests.get(url, proxies=proxies, timeout=30)
            # BeautifulSoup 객체 생성, html 파싱
            soup = BeautifulSoup(response.content, "html.parser")
            print("접속성공")
        
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.text.strip() ## 공백제거
                print(f"Title: {title_text}")
            else:
                print("Title NO!!")
            
            
            html_tag = soup.find('html')
            if html_tag and html_tag.has_attr('lang'):
                lang = html_tag['lang']
                print(f"Language: {lang}")
            else:
                print("no lang")
                
        # 모든 앵커 태그를 찾습니다.
            a_tags = soup.find_all('a')

            filtered_words_found = set() # Change this to set
        
        # 앵커 태그의 텍스트를 확인하고 필터링된 단어를 포함하고 있는지 확인합니다.
            for a_tag in a_tags:
                anchor_text = a_tag.text.lower()
                for word in filter_words:
                    if word in anchor_text:
                        filtered_words_found.add(a_tag.text.strip()) # Use strip() to remove whitespace

                # 출력되는 단어 중복 방지용.

            print(f"Onion URL: {url}")
            if filtered_words_found:
                print("Filtered words: " + ', '.join(filtered_words_found)) # filtered_words_found는 크롤링한 단어 중 set으로 저장 시켜 중복 제거
           # print(', '.join(filtered_words_found))  # join 메소드 사용 ,로 구분
                print()
                datas1 = {'Onion URL': url, 'Status': 'success', 'Title': title_text,
                      'Filtered words': ', '.join(filtered_words_found), 'Language': lang}
                result1.append(datas1) 
            
            else:
                print("word No!!")
                print()
                datas2 = {'Onion URL': url, 'Status': 'success', 'Title': title_text,
                      'Filtered words': 'world no', 'Language': lang} 
                result2.append(datas2) 
            
        except Exception as e: # HTTP 요청이 실패했을 때
            print("접속불가")
            print(f"Onion URL: {url}")
            print()
            datas3 = {'Onion URL': url, 'Status': 'fail', 'Title': 'no..',
                      'Filtered words': 'no..', 'Language': 'no..'} 
            result3.append(datas3) 
           
    # datas1 = {'Onion URL': url, 'Status': e, 'Title': title_text,
     #Filtered words': ', '.join(filtered_words_found), 'Language': lang}      
     
    """ 
    print(result1)
    print(result2)
    print(result3)
    """
    
    furd3n = result1+result2+result3
    print(furd3n)
    result_df = pd.DataFrame(furd3n)
    result_df.to_csv('furd3n.csv', index=False)
        # set 사용하면 단어 중복 제거 등이 가능하다고 함
if __name__ == '__main__':
    # 크롤링할 Onion URLs를 저장한 CSV 파일 경로
    file_path = 'onion_urls.csv'
    # 필터링할 단어
    #filter_words_dict = filter_words
    # CSV 파일을 DataFrame으로 로드
    df = pd.read_csv(file_path, header=None, names=['url'])
    # 크롤링 실행
    crawl_tor(df, filter_words)