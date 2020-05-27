# 导入所需包
import pandas as pd
import re
import parsel
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 打开浏览器
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


# 定义函数登录淘宝
def login_taobao_acount():
    # 登录URL
    login_url = 'https://login.taobao.com/member/login.jhtml'

    # 打开网页
    browser.get(login_url)
    # 支付宝登录
    log = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-form > div.login-blocks.sns-login-links > a.alipay-login'))
    )
    log.click()

# 定义函数搜索商品
def search(key_word):
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(key_word)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return search(key_word)


# 定义函数获取单页的商品信息
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    # 解析数据
    html = parsel.Selector(browser.page_source)
    # 获取数据
    goods_name = html.xpath('//div[@class="grid g-clearfix"]//img/@alt').extract()
    shop_name = html.xpath('//div[@class="grid g-clearfix"]//div[@class="shop"]/a/span[2]/text()').extract()
    price = html.xpath('//div[@class="grid g-clearfix"]//div[contains(@class,"price")]/strong/text()').extract()
    purchase_num = [re.findall(r'<div class="deal-cnt">(.*?)</div>', i)
                    for i in html.xpath('//div[@class="grid g-clearfix"]//div[@class="row row-1 g-clearfix"]').extract()]
    location = html.xpath('//div[@class="grid g-clearfix"]//div[@class="location"]/text()').extract()

    # 存储数据
    df_one = pd.DataFrame({
        'goods_name': goods_name,
        'shop_name': shop_name,
        'price': price,
        'purchase_num': purchase_num,
        'location': location
    })
    return df_one


# 定义函数进行翻页
def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        # 运行函数
        df_product = get_products()
    except TimeoutException:
        next_page(page_number)

    return df_product

# 获取所有页信息
def main():
    try:
        total = search(key_word='520礼物')
        total = int(re.compile('(\d+)').search(total).group(1))
        # 存储数据
        df_all = pd.DataFrame()
        for i in range(1, total + 1):
            df_one = next_page(i)
            df_all = df_all.append(df_one, ignore_index=True)
            # 打印进度
            print('我正在获取第{}页的数据'.format(i))
            time.sleep(3)
    except Exception:
        print('出错啦')
    finally:
        browser.close()
    return df_all

# 从此处运行
if __name__ == '__main__':
    # 登录
    login_taobao_acount()
    time.sleep(10)
    df_all = main()

# 保存数据
df_all.to_excel('./data/520礼物天猫数据.xlsx', index=False)