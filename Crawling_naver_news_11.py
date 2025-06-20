import requests
import urllib.parse
import json
import pandas as pd
import time

# API 키 설정
client_id = "sWWRf8lI7cNIhd3hPKST"
client_secret = "RCgHFI5EcL"

# CSV 파일에서 기업명 리스트 불러오기
df = pd.read_csv("enterprise_df_11_utf8_data.csv", encoding="utf-8-sig")
companies = df["기업명"].tolist()

# 수집한 뉴스 데이터를 저장할 리스트
news_results = []

# 각 기업에 대해 뉴스 수집 반복
for idx, company in enumerate(companies, 1):
    encoded_query = urllib.parse.quote(company)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display=10&start=1&sort=sim"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            items = data.get("items", [])

            for item in items:
                news_results.append({
                    "기업명": company,
                    "제목": item.get("title"),
                    "오리지널 링크": item.get("originallink"),
                    "링크": item.get("link"),
                    "설명": item.get("description"),
                    "발행일": item.get("pubDate")
                })

            print(f"[{idx}/{len(companies)}] '{company}' 수집 완료 ({len(items)}건)")
        else:
            print(f"[{idx}] '{company}' 요청 실패: {response.status_code}")
    except Exception as e:
        print(f"[{idx}] '{company}' 예외 발생: {e}")

    time.sleep(0.3)  # 과도한 요청 방지

# 결과 저장
result_df = pd.DataFrame(news_results)
result_df.to_csv("naver_news_500_companies_11.csv", index=False, encoding="utf-8-sig")
print(" 모든 뉴스 수집이 완료되었습니다. 결과는 'naver_news_500_companies_11.csv'에 저장되었습니다.")






