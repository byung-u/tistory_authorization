#!/usr/bin/env python3
import os
import re
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def tistory_login():
    tistory_id = os.environ.get('TISTORY_ID')
    tistory_pw = os.environ.get('TISTORY_PW')
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # chrome 띄워서 보려면 주석처리
    driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
    driver.implicitly_wait(3)
    driver.get('https://www.tistory.com/auth/login?redirectUrl=http%3A%2F%2Fwww.tistory.com%2F')
    driver.find_element_by_name('loginId').send_keys(tistory_id)
    driver.find_element_by_name('password').send_keys(tistory_pw)
    driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/button').click()
    return driver


def get_authentication_code(driver, client_id, redirect_url):
    req_url = 'https://www.tistory.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=langoo' % (client_id, redirect_url)
    driver.get(req_url)
    driver.find_element_by_xpath('//*[@id="contents"]/div[4]/button[1]').click()
    redirect_url = driver.current_url
    temp = re.split('code=', redirect_url)
    code = re.split('&state=', temp[1])[0]
    return code


# http://www.tistory.com/guide/api/index
def get_access_token(code, client_id, client_secret, redirect_url):
    url = 'https://www.tistory.com/oauth/access_token?'
    payload = {'client_id': client_id,
               'client_secret': client_secret,
               'redirect_uri': redirect_url,
               'code': code,
               'grant_type': 'authorization_code'}
    res = get(url, params=payload)
    token = res.text.split('=')[1]
    return token


def main():
    client_id = os.environ.get('TISTORY_CLIENT_ID')
    client_secret = os.environ.get('TISTORY_CLIENT_SECRET')
    redirect_url = os.environ.get('TISTORY_REDIRECT')
    driver = tistory_login()
    code = get_authentication_code(driver, client_id, redirect_url)
    token = get_access_token(code, client_id, client_secret, redirect_url)
    print(token)


if __name__ == '__main__':
    main()
