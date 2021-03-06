import time
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
from selenium.webdriver.chrome.options import Options

url = 'https://www.uqwimax.jp/mobile/products/sim/devices/'
result = 'TORQUE 5GはまだUQモバイルの対象機種ではありません。'

def send_email(body):
    """メール送信処理

    Args:
        body (string): メール本文
    """
    # SMTPログイン
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.ehlo()

    EMAIL=''
    PASSWORD=''
    TO_EMAIL='rm.eilsystem@gmail.com'

    smtp_obj.login(EMAIL, PASSWORD)

    msg = MIMEText(body)
    msg['Subject'] = 'UQモバイルのTORQUE対応状況'
    msg['From'] = 'from@example.jp'
    msg['To'] = TO_EMAIL
    msg['Date'] = formatdate()

    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.close()

# ステータスコードの確認
if requests.get(url).status_code != 200:
    send_email('スクレイピング対象サイトのレスポンスが変更されました。対象サイトを確認してください。\n{}'.format(url))
    exit()

# バックグラウンドで実施するためのオプション
opt = Options()
opt.add_argument('--headless')
# WebDriverのインスタンスを生成
driver = webdriver.Chrome(executable_path='/Users/miyata/dev/UQ_scraping/chromedriver', options=opt)

time.sleep(1)  # ステータスコードの確認から1秒待機

driver.get(url)
time.sleep(1)  # jsの描画待ち

# element[s]であることに注意
search_strings = driver.find_elements_by_css_selector('h3.uqv2-parts-text--lg.uqv2-parts-bold span')

def has_torque_5g():
    if len(search_strings) == 0:
        return '要素が存在しないためスクレイピングに失敗しました。対象サイトのDOM構造を確認してください。\n{}'.format(url)
    else:
        for tag in search_strings:
            target_upper = tag.text.upper()
            if target_upper in 'TORQUE G05' or target_upper in 'TORQUE 5G' or target_upper in 'TORQUE 5G KYG01':
                return 'TORQUE 5GがUQモバイルの対象機種になりました。契約内容を変更しましょう。\n{}'.format(url)
        return 'TORQUE 5GはまだUQモバイルの対象機種ではありません。'

result = has_torque_5g()
# ブラウザを閉じる
driver.quit()

send_email(result)
