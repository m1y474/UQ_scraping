import time
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# WebDriverのインスタンスを生成
driver = webdriver.Chrome(executable_path='/Users/miyata/dev/UQ_scraping/chromedriver')

url = 'https://www.uqwimax.jp/mobile/products/sim/devices/'
driver.get(url)
time.sleep(1)  # jsの描画待ち
# element[s]であることに注意
search_strings = driver.find_elements_by_css_selector(
    'h3.uqv2-parts-text--lg.uqv2-parts-bold')


def has_torque_5g():
    for tag in search_strings:
        target_upper = tag.text.upper()
        if target_upper in 'TORQUE G05' or target_upper in 'TORQUE 5G' or target_upper in 'TORQUE 5G KYG01':
            return True
        return False


result = 'TORQUE 5GはまだUQモバイルの対象機種ではありません。'
if (has_torque_5g()):
    result = 'TORQUE 5GがUQモバイルの対象機種になりました。契約内容を変更しましょう。\n{}'.format(url)

# ブラウザを閉じる
driver.quit()

# SMTPログイン
smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
smtp_obj.ehlo()
smtp_obj.starttls()
smtp_obj.ehlo()

# smtp_obj.login(username, password)

msg = MIMEText(result)
msg['Subject'] = 'UQモバイルのTORQUE対応状況'
msg['From'] = 'from@example.jp'
msg['To'] = 'rm.eilsystem@gmail.com'
msg['Date'] = formatdate()

smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
smtp_obj.close()
