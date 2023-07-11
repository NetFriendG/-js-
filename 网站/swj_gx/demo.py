import requests
from lxml import etree
import re
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.append(['标题','网址','咨询时间','答复时间','受理单位','咨询内容','答复内容'])

def tostring(result_list:list)->str:
    return re.sub('\s','',''.join(result_list))

def href_scrapy(url):
    while True:
        try:
            response = requests.get(url,headers=headers,cookies=cookies)
            if response.status_code==200:
                break
        except:
            print(url,'没有获取到')
    response.encoding = 'utf-8'
    tree = etree.HTML(response.text)
    zxtime = tostring(tree.xpath('//*[@id="article-body"]//table/tbody/tr[1]/td[2]//text()'))
    dftime = tostring(tree.xpath('//*[@id="article-body"]//table/tbody/tr[1]/td[4]/p/span//text()'))
    unit = tostring(tree.xpath('//*[@id="article-body"]//table/tbody/tr[2]/td[2]/p/span//text()'))
    zxcontent = tostring(tree.xpath('//*[@id="article-body"]//table/tbody/tr[3]/td[2]/p/span//text()'))
    dfcontent = tostring(tree.xpath('//*[@id="article-body"]//table/tbody/tr[4]/td[2]/p/span//text()'))
    return {
        'zxtime':zxtime,
        'dftime':dftime,
        'unit':unit,
        'zxcontent':zxcontent,
        'dfcontent':dfcontent
    }

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
cookies = {
    "zh_choose": "n",
    "yfx_c_g_u_id_10003701": "_ck23021620043518416700573499871",
    "yfx_f_l_v_t_10003701": "f_t_1676549075842__r_t_1676549075842__v_t_1676549075842__r_c_0",
    "yfx_key_10003701": "",
    "yfx_mr_10003701": "%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search",
    "yfx_c_g_u_id_10003748": "_ck23042416542218741513176519961",
    "yfx_f_l_v_t_10003748": "f_t_1682326462875__r_t_1682326462875__v_t_1682326462875__r_c_0"
}
def main_scrapy(page):
    if page>0:
        if page == 1:
            url = "http://guangxi.chinatax.gov.cn/nsfw/nszx/rdwd/"
        else:
            url = f'http://guangxi.chinatax.gov.cn/nsfw/nszx/rdwd/index_{page}.html'
    else:
        return
    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
    response.encoding = 'utf8'

    tree = etree.HTML(response.text)
    info_span = tree.xpath('//div[@class="lmy_info"]/ul/li[not(@class="line1")]')

    item_list = []
    for info in info_span:
        item = {}
        title = tostring(info.xpath('./a/text()'))
        href = 'http://guangxi.chinatax.gov.cn/nsfw/nszx/rdwd'+tostring(info.xpath('./a/@href'))[1:]
        item['title'] = title
        item['href'] = href
        print(item)
        item_dict = href_scrapy(href)
        for k,v in item_dict.items():
            item[k] = v
        item_list.append(item)
    return item_list
def main():
    global ws,wb
    for page in range(1,21):
        if page >1:
            wb = openpyxl.load_workbook('test.xlsx')
            ws = wb.active
        item_list = main_scrapy(page)
        for item in item_list:
            ws.append([item['title'],item['href'],item['zxtime'],item['dftime'],item['unit'],item['zxcontent'],item['dfcontent']])
        wb.save('test.xlsx')


main()