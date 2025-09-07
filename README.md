# 📰 Daily News Crawler

매일 오전 8시 30분에 자동으로 외신 헤드라인과 연합뉴스 국제 기사를 수집하여 이메일로 발송하는 뉴스 크롤러입니다.

## 🌟 기능

### 외신 헤드라인 수집
- **BBC**: 메인 헤드라인
- **CNN**: 메인 헤드라인  
- **Fox News**: 메인 헤드라인
- **NYT**: 메인 헤드라인
- **Reuters**: 메인 헤드라인 (WSJ 대체)
- **Washington Post**: 메인 헤드라인 (Selenium 사용)

### 연합뉴스 국제 기사
- 전날 23:00 ~ 당일 08:30 시간 범위 내 모든 기사 수집
- 본문 500-550자 요약 및 "~했음" 어미 변경
- 제목, 링크, 발행시간, 본문 요약 포함

### 자동화
- GitHub Actions를 통한 매일 자동 실행
- 수집된 뉴스를 HTML 형식으로 정리하여 이메일 발송
- 실행 로그 및 에러 추적

## 🚀 설치 및 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/daily-news-crawler.git
cd daily-news-crawler
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
GitHub Repository Settings → Secrets and variables → Actions에서 다음 변수들을 설정:

- `GMAIL_EMAIL`: 발송용 Gmail 주소
- `GMAIL_PASSWORD`: Gmail 앱 비밀번호
- `RECIPIENT_EMAIL`: 수신할 이메일 주소

### 4. Gmail 앱 비밀번호 생성
1. [Google 계정 보안 설정](https://myaccount.google.com/security)
2. 2단계 인증 활성화
3. 앱 비밀번호 생성 → "메일" 선택
4. 생성된 16자리 비밀번호를 `GMAIL_PASSWORD`에 입력

## 📂 프로젝트 구조

```
daily-news-crawler/
├── .github/
│   └── workflows/
│       └── news_crawler.yml    # GitHub Actions 워크플로우
├── main.py                     # 메인 크롤링 스크립트
├── email_sender.py             # 이메일 발송 모듈
├── requirements.txt            # Python 의존성
└── README.md                   # 프로젝트 문서
```

## ⚙️ 실행 방법

### 자동 실행 (GitHub Actions)
- 매일 오전 8:30 (KST) 자동 실행
- 스케줄: `30 23 * * *` (UTC 기준)

### 수동 실행
1. **GitHub에서**: Actions 탭 → "Daily News Crawler" → "Run workflow"
2. **로컬에서**:
   ```bash
   python main.py
   ```

## 📧 이메일 형식

발송되는 이메일은 다음과 같은 구조로 구성됩니다:

### 외신 헤드라인
- 각 언론사별 메인 헤드라인 1개씩
- 제목과 원문 링크 포함

### 연합뉴스 국제
- 시간 범위 내 모든 기사 목록
- 제목, 발행시간, 기사 링크
- 본문 요약 (500-550자, "~했음" 어미)

## 🛠️ 기술 스택

- **Python 3.11**: 메인 언어
- **requests**: HTTP 요청 처리
- **BeautifulSoup4**: HTML 파싱
- **Selenium**: 동적 페이지 크롤링 (Washington Post)
- **GitHub Actions**: 자동화 및 스케줄링
- **Gmail SMTP**: 이메일 발송

## 🔧 커스터마이징

### 뉴스 사이트 추가/제거
`main.py`의 `crawl_all_foreign_news()` 함수에서 `foreign_sites` 리스트를 수정:

```python
foreign_sites = [
    ("BBC", self.crawler.crawl_bbc_headline),
    ("CNN", self.crawler.crawl_cnn_headline),
    # 새로운 사이트 추가
    ("새 사이트", self.crawler.crawl_new_site_headline),
]
```

### 실행 시간 변경
`.github/workflows/news_crawler.yml`의 cron 스케줄 수정:

```yaml
schedule:
  # 오전 9시로 변경 (UTC 기준 00:00)
  - cron: '0 0 * * *'
```

### 이메일 템플릿 수정
`email_sender.py`의 `format_news_html()` 함수에서 HTML 템플릿 커스터마이징

## 📋 요구사항

- Python 3.11+
- Chrome/Chromium (GitHub Actions에서 자동 설치)
- Gmail 계정 (앱 비밀번호 설정 필요)

## ⚠️ 주의사항

1. **이용약관 준수**: 각 뉴스 사이트의 robots.txt 및 이용약관을 확인하세요
2. **요청 제한**: 과도한 요청으로 인한 IP 차단을 방지하기 위해 요청 간격을 조절했습니다
3. **Gmail 보안**: 앱 비밀번호를 사용하며, 절대 일반 비밀번호를 사용하지 마세요
4. **개인정보**: 이메일 주소 등 개인정보는 GitHub Secrets에 안전하게 저장하세요

## 🐛 문제 해결

### 크롤링 실패
- 대상 사이트의 구조 변경 가능성
- 봇 차단 또는 접근 제한
- GitHub Actions 로그에서 상세 오류 확인

### 이메일 발송 실패
- Gmail 앱 비밀번호 확인
- 2단계 인증 활성화 여부 확인
- SMTP 설정 및 네트워크 연결 상태 확인

### 시간대 문제
- 모든 시간은 KST 기준으로 설정됨
- GitHub Actions는 UTC 기준으로 실행

## 📈 향후 개선사항

- [ ] 구글 드라이브 연동으로 데이터 백업
- [ ] 웹 대시보드 추가
- [ ] 더 많은 언론사 지원
- [ ] 키워드 필터링 기능
- [ ] 모바일 앱 푸시 알림 연동

## 📄 라이센스

이 프로젝트는 개인 사용 목적으로 제작되었습니다. 상업적 사용 시 각 뉴스 사이트의 이용약관을 반드시 확인하세요.

## 🤝 기여

버그 리포트나 개선 제안은 Issues를 통해 제출해 주세요.

---

**⏰ 마지막 업데이트**: 2025년 9월 7일