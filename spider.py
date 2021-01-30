# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re


def translate(s, flag=0, desLan='zh-CN'):
    url = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl='
    if flag == 0:
        if re.match(r'[\u4e00-\u9fa5]', s[0]):  # 匹配中文
            desLan = 'en'
    try:
        r = requests.get(url+desLan+'&q='+s)
        r.raise_for_status()
        res = json.loads(r.text)
        info = res['sentences'][0]['trans']
        return info
    except:
        print("error")
        return


def getImgByPid(s: str, dst='tmp', pageCountMax=5):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'cookie': ''  # 使用你的账户登陆pixiv后获得的cookie
    }
    url = 'https://www.pixiv.net/artworks/' + s
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        jsonContent = soup('meta', id='meta-preload-data')[0].attrs['content']
        content = json.loads(jsonContent)
        desUrl = content['illust'][s]['urls']['original']
        headers['Referer'] = 'https://www.pixiv.net/'
        preUrl = desUrl[:desUrl.rfind('.') - 1]
        lastUrl = desUrl[desUrl.rfind('.'):]
        pageCount = content['illust'][s]['pageCount']
        for i in range(0, min(pageCount, pageCountMax)):
            desUrl = preUrl + str(i) + lastUrl
            r = requests.get(desUrl, headers=headers)
            with open(dst+'_'+str(i)+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
        return min(pageCount, pageCountMax)
    except:
        print("error")
        return 0


def getImgBySearch(s: str, numsOfPic=3):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'cookie': ''        # 使用你的账户登陆pixiv后获得的cookie
    }
    url = 'https://www.pixiv.net/ajax/search/artworks/'+s+'%20100users入り?word=' + \
        s + '%20100users入り&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'
    pids = []
    urls = []
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        Datas = json.loads(r.text)['body']['illustManga']['data']
        headers['Referer'] = 'https://www.pixiv.net/'
        for i in range(numsOfPic):
            urls.append(Datas[i]['url'])
            pids.append(Datas[i]['id'])
            r = requests.get(urls[i], headers=headers)
            with open('tmp_'+str(i)+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
        return pids
    except:
        print('error')
        return
