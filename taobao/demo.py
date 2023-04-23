import requests
import re
import json

cookies = None
headers = None


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
            "s": str(44*page)
        }
        if page>1:
            params["bcoffset"] = "1"
            params["ntoffset"] = "1"
        return params

    def getpage(self,page:int)->dict:
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

taobao = taobaoApi('灵芝孢子粉')
taobao.getpage(1)