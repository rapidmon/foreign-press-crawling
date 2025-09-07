# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class NewsEmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = os.getenv('GMAIL_EMAIL')
        self.password = os.getenv('GMAIL_PASSWORD')  # Gmail 앱 비밀번호
        self.recipient = os.getenv('RECIPIENT_EMAIL')
    
    def format_news_html(self, foreign_news, yonhap_articles):
        """뉴스 데이터를 HTML 형식으로 포맷팅"""
        current_time = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; }}
                .foreign-news {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; }}
                .yonhap-news {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; }}
                .news-item {{ margin: 15px 0; padding: 10px; border-left: 4px solid #3498db; }}
                .news-title {{ font-weight: bold; font-size: 16px; margin-bottom: 5px; }}
                .news-link {{ color: #2980b9; text-decoration: none; }}
                .news-content {{ margin-top: 10px; color: #555; }}
                .timestamp {{ text-align: center; color: #7f8c8d; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📰 일간 뉴스 브리핑</h1>
                <p>{current_time} 발송</p>
            </div>
            
            <div class="section">
                <h2>🌍 외신 헤드라인</h2>
                <div class="foreign-news">
        """
        
        # 외신 뉴스 추가
        for site_name, news_data in foreign_news.items():
            if news_data:
                html_content += f"""
                    <div class="news-item">
                        <div class="news-title">{site_name}</div>
                        <a href="{news_data['link']}" class="news-link" target="_blank">
                            {news_data['title']}
                        </a>
                    </div>
                """
            else:
                html_content += f"""
                    <div class="news-item">
                        <div class="news-title">{site_name}</div>
                        <p style="color: #e74c3c;">크롤링 실패</p>
                    </div>
                """
        
        html_content += """
                </div>
            </div>
            
            <div class="section">
                <h2>🇰🇷 연합뉴스 국제</h2>
                <div class="yonhap-news">
        """
        
        # 연합뉴스 기사 추가
        if yonhap_articles:
            for i, article in enumerate(yonhap_articles, 1):
                published_time = article['published'].strftime('%m-%d %H:%M')
                html_content += f"""
                    <div class="news-item">
                        <div class="news-title">{i}. {article['title']}</div>
                        <p style="color: #7f8c8d; font-size: 12px;">발행시간: {published_time}</p>
                        <a href="{article['link']}" class="news-link" target="_blank">기사 보기</a>
                    </div>
                """
        else:
            html_content += """
                <div class="news-item">
                    <p style="color: #e74c3c;">연합뉴스 기사를 가져올 수 없습니다.</p>
                </div>
            """
        
        html_content += """
                </div>
            </div>
            
            <div class="timestamp">
                <p>자동 생성된 뉴스 브리핑입니다.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_email(self, foreign_news, yonhap_articles):
        """이메일 발송"""
        try:
            # 메시지 생성
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📰 일간 뉴스 브리핑 - {datetime.now().strftime('%Y.%m.%d')}"
            msg['From'] = self.email
            msg['To'] = self.recipient
            
            # HTML 콘텐츠 생성
            html_content = self.format_news_html(foreign_news, yonhap_articles)
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # SMTP 서버 연결 및 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print("✅ 이메일 발송 성공!")
            return True
            
        except Exception as e:
            print(f"❌ 이메일 발송 실패: {e}")
            return False