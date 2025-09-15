import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# メール設定
FROM_EMAIL = "nyan22chan22@gmail.com"
TO_EMAIL = "nyan22chan22@gmail.com"
APP_PASSWORD = "todu aetj twur rquo"

# 監視対象URLとキーワード
targets = [
    {
        "url": "https://ticket.pia.jp/sp/ticketInformation.do?eventCd=2525090&rlsCd=001",
        "keyword": "選択した公演"
    },
    {
        "url": "https://relief-ticket.jp/events/artist/16/105",
        "keyword": "購入"
    }
]

def check_site(url, keyword):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return keyword in res.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

def send_email(message):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "チケット通知"
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    for target in targets:
        if check_site(target["url"], target["keyword"]):
            send_email(f"販売開始を検知しました: {target['url']}")
