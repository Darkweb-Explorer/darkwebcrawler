import requests
import pandas as pd
from bs4 import BeautifulSoup
from filter_words import filter_words
import argparse

def read_csv_file(csv_file):
    df = pd.read_csv(csv_file, header=None, names=['url'])
    return df


def crawl_tor(df):
    proxies = {'http': 'socks5h://localhost:9150',
               'https': 'socks5h://localhost:9150'}
    

    df = df[df['url'].str.contains('.onion')].drop_duplicates() # contains로 .onion 감지 및 drop_duplicates()중복제거

    result1 = []
    result2 = []
    result3 = []

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
    print(furd3n)
    result_df = pd.DataFrame(furd3n)
    result_df.to_csv('furd3ncyber.csv', index=False)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read csv")
    parser.add_argument("csv_file", help="The path to the CSV file.")
    args = parser.parse_args()
    df = read_csv_file(args.csv_file)
    crawl_tor(df)