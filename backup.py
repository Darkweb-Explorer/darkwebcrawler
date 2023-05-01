import requests
from bs4 import BeautifulSoup
from filter_words import filter_words
import csv

# Tor proxy 설정
proxies = {'http': 'socks5h://localhost:9150',
           'https': 'socks5h://localhost:9150'}

onion_urls = []
with open('onion_urls.csv', mode='r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        onion_urls.extend(row)

# 각 onion 주소를 순회하면서 웹 페이지를 크롤링합니다.
for url in onion_urls:
    try:
        # 페이지 가져오기
        response = requests.get(url, proxies=proxies, timeout=30)

        # BeautifulSoup 객체 생성, html 파싱
        soup = BeautifulSoup(response.content, "html.parser")

        # 모든 앵커 태그를 찾습니다.
        a_tags = soup.find_all('a')

        filtered_words_found = set() # Change this to set
        
        # 앵커 태그의 텍스트를 확인하고 필터링된 단어를 포함하고 있는지 확인합니다.
        for a_tag in a_tags:
            anchor_text = a_tag.text.lower()
            for word in filter_words:
                if word in anchor_text:
                    filtered_words_found.add(a_tag.text.strip()) # Use strip() to remove whitespace

        print(f"Onion URL: {url}")
        if filtered_words_found:
            print("Filtered words:")
            print(', '.join(filtered_words_found)) # Use join() here to print words separated by commas
        else:
            print("No filtered words found.")
        print()
    except Exception as e:
        print(f"Error while processing URL {url}: {e}")
