import requests
import re
import json



headers = {
    "authority": "s.taobao.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
cookies = {
    "cna": "uVxeHAqe2AYCAXBh8oGy/YRC",
    "thw": "cn",
    "tracknick": "gxg509",
    "sgcookie": "E100e3F6aIEAIeqtd%2BUAlU%2FYM7383rkj%2FyDNf0FRFGUHve8pVG00khHiDYhGhH6xqhH7EJi3E6F70XSC8SsEPZm%2BC6k5M%2FcSGM1a%2BSXkMROKFrQ%3D",
    "uc3": "id2=UondE66qIsLx4g%3D%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCsfULA3Ymcr5Fan8%3D&nk2=BI4y3u3A",
    "lgc": "gxg509",
    "uc4": "id4=0%40UOE3HTSjc1mDnC5aeijY27irF%2BAw&nk4=0%40BorIRCbkNb%2F9IFaCBfwLVyM%3D",
    "_cc_": "URm48syIZQ%3D%3D",
    "mt": "ci=-1_0",
    "_m_h5_tk": "e34fd729c332a06636b897160cd9aa1e_1682214279376",
    "_m_h5_tk_enc": "e8d4fb26bee182939dcbc0f1bc4d7794",
    "xlly_s": "1",
    "tfstk": "cjglB7cCR0rWSa8KhYaW7w5AT_-OZt_UI2ujuIIlm2EE-kuViFIVb9Bwi8v6UM1..",
    "l": "fBOcfY54TWqK368LBOfwourza77OkIRfguPzaNbMi9fP_BCH8MB5W1N1oNLMCnGVesNHR3Jfz-p8BfLRzyCqJxpsw3k_J_fm3dhyN3pR.",
    "isg": "BBwcqIIIlGYIHGckyMvQh8-O7TrOlcC_7l7rQPYdWIffQb3LHqFnT8Kzoam5SfgX",
    "JSESSIONID": "DA49D2959E966B0BDB77D76A99066286"
}

class taobaoApi():


    def __init__(self,q):
        self.q = q
        self.session = requests.Session()
        self.searchurl = "https://s.taobao.com/search"
        self.patternJsconfig = re.compile(r'g_page_config = (\{.+\});\s*', re.M)   # 匹配返回

    def createParams(self,q:str,page:int)->dict:
        '''
            构建查询参数
            传入关键词和页数
        '''
        params = {
            "q": q,
            "suggest": "history_1",
            "commend": "all",
            "ssid": "s5-e",
            'page':'1',
            "search_type": "item",
            "sourceId": "tb.index",
            "spm": "a21bo.jianhua.201856-taobao-item.2",
            "ie": "utf8",
            "initiative_id": "tbindexz_20170306",
            "_input_charset": "utf-8",
            "wq": "",
            "suggest_query": "",
            "source": "suggest",
            "p4ppushleft": "2,48",

        }
        if page>1:
            params["s"]=str(44 * page-1)
        #     params["bcoffset"] = "1"
        #     params["ntoffset"] = "1"
        return params

    def get_page_config(self,page:int)->dict:
        ''':
            获取当前关键词的第几页数据
            page: 传想获取的页数
        '''
        items = {}
        item_list = []
        response = self.session.get(self.searchurl, headers=headers, cookies=cookies, params=self.createParams(self.q,page))
        rest = self.patternJsconfig.search(response.text)
        if rest:
            data = json.loads(rest.group(1))
            bk_list = data['mods']['itemlist']['data']['auctions']
            for bk in bk_list:
                item = {}   # 存储数据对象
                # 标题
                item['title'] = bk["raw_title"]
                # 价格
                item['price'] = bk["view_price"]
                # 购买链接
                item['detail_url'] = bk["detail_url"]
                # 商家
                item['nick'] = bk["nick"]
                # 是否来源于淘宝
                item['isTabao'] = True if 'item.taobao.com' in  bk['detail_url'] else False
                item_list.append(item)
        items['data'] = item_list
        return items



if __name__ == '__main__':
    taobao = taobaoApi('灵芝孢子粉')
    print(taobao.get_page_config(2))