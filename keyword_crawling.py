import requests
import pandas as pd
from bs4 import BeautifulSoup
from search_keyword import search_keyword
from filter_words import filter_words



def torch_crawling():
    
    proxies = {'http': 'socks5h://localhost:9150',
           'https': 'socks5h://localhost:9150'}
    
    url1 = set()
    
    for keyword in search_keyword:
        url = "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query=" + keyword
        while True:
            try:
                response = requests.get(url, proxies=proxies, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                a_tags = soup.find_all('a')
                for a_tag in a_tags:
                    href = a_tag.get('href')
                    if '.onion' in href:
                        if '.onion' in href and ('http://' in href or 'https://' in href):
                            url1.add(href)
                break       

            except Exception as e: # HTTP 요청이 실패했을 때
                print("torch 접속시도 중")
    df1 = pd.DataFrame(url1, columns=['url'])
    return df1


def Sentor_crawling():

    proxies = {'http': 'socks5h://localhost:9150',
               'https': 'socks5h://localhost:9150'}
    
    url2 = set() # 중복을 제거할 set() 생성 / set은 중복 허용 x
    
    page = 1
    max_page = 10  # 테스트로 2으로 지정
    
    for keyword in search_keyword:
        page = 1  # 페이지 초기화
        while page <= max_page:
            url = f"http://e27slbec2ykiyo26gfuovaehuzsydffbit5nlxid53kigw3pvz6uosqd.onion/?q={keyword}&p={page}" 
            while True:
                try:
                    response = requests.get(url, proxies=proxies, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    a_tags = soup.find_all('a')
                    for a_tag in a_tags:
                        href = a_tag.get('href')
                        if '.onion' in href and ('http://' in href or 'https://' in href):
                            url2.add(href)
                    page += 1
                    break
                    
         
                except Exception as e:
                    print("Sentor 접속시도 중")
    df2 = pd.DataFrame(url2, columns=['url'])

    return df2

def make_csv1():
    df1 = torch_crawling()
    df2 = Sentor_crawling()
    result_df = pd.concat([df1,df2])
    result_df.to_csv('darkresults.csv',index=False)

    
def crawl_tor():
# Tor proxy 설정, tor 브라우저 필수 부분
    proxies = {'http': 'socks5h://localhost:9150',
               'https': 'socks5h://localhost:9150'}
    file_path = 'darkresults.csv'
    df = pd.read_csv(file_path, header=None, names=['url'])
    # Onion URLs를 DataFrame으로 로드하고 .onion이 포함된 URL만 선택하여 중복을 제거
  
    df = df[df['url'].str.contains('.onion')].drop_duplicates() # contains로 .onion 감지 및 drop_duplicates()중복제거
   
    result1 = []
    result2 = []
    result3 = []
 
    for url in df['url']:
        try:
            response = requests.get(url, proxies=proxies, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            print("접속성공")
        
            title_tag = soup.find('title')
            if title_tag:
                title_text = title_tag.text.strip() ## 공백제거
                print(f"Title: {title_text}")
            else:
                title_text = "search fail(title)"
                print(f"Title: {title_text}")
            
            
            html_tag = soup.find('html')
            if html_tag and html_tag.has_attr('lang'):
                lang = html_tag['lang']
                print(f"Language: {lang}")
            else:
                lang = "search fail(lang)"
                print(f"Language: {lang}")
                
    
            a_tags = soup.find_all('a')
            
            filtered_words_found = set() # 중복제거
        
      
            for a_tag in a_tags:
                anchor_text = a_tag.text.lower().strip()
                
                for word in filter_words:
                        if word in anchor_text and word not in filtered_words_found:
                            filtered_words_found.add(word) 

             

            print(f"Onion URL: {url}")
            if filtered_words_found:
 
                print("Filtered words: " + ', '.join(filtered_words_found)) 

                print()
                datas1 = {'Onion URL': url, 'Status': 'success', 'Title': title_text,
                      'Filtered words': ', '.join(filtered_words_found), 'Language': lang}
                result1.append(datas1) 
            
            else:
                print("word No!!")
                print()
                datas2 = {'Onion URL': url, 'Status': 'success', 'Title': title_text,
                      'Filtered words': 'search fail(filter_word)', 'Language': lang} 
                result2.append(datas2) 
            
        except Exception as e: # HTTP 요청이 실패했을 때
            print("접속불가")
            print(f"Onion URL: {url}")
            print()
            datas3 = {'Onion URL': url, 'Status': 'connect fail', 'Title': 'connect fail',
                      'Filtered words': 'connect fail', 'Language': 'connect fail'} 
            result3.append(datas3)
            
            
            
    furd3n = result1+result2+result3
    return furd3n


def make_csv2():
    dfresult = crawl_tor()
    result_df = pd.DataFrame(dfresult)
    result_df.to_csv('furd3n.csv', index=False)       
    
    

if __name__ == '__main__':
    torch_crawling()
    Sentor_crawling()
    make_csv1()
    crawl_tor()
    make_csv2()
    
    
   
