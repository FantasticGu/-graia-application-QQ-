# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re


def translate(s, flag=0, desLan='zh-CN'):
    url = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl='
    if flag == 0:
        if re.match(r'[\u4e00-\u9fa5]', s[0]):
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36', 'cookie': '__cfduid=d40b8cceb340be6a3e4e66acfe09241ef1610429186; first_visit_datetime_pc=2021-01-12+14%3A26%3A26; p_ab_id=2; p_ab_id_2=5; p_ab_d_id=1343175977; yuid_b=MFgwc3Q; _ga=GA1.2.1687434103.1610429284; PHPSESSID=20192742_qGdjZiY1mDUS81awYMFfBWnisOg6cYcR; device_token=8136801d229a5bd54062e45069592095; c_type=19; a_type=0; b_type=1; login_ever=yes; user_language=zh; privacy_policy_agreement=2; tag_view_ranking=og5cTSQtiT~Kh4mg2DS4s~aeYJNizZc6~0xsDLqCEW6~RTJMXD26Ak~JBqkgBEhOH~ZQngJx8lsH~wpJacsLYRf~HGDBRCKOc3~w-4q98p7vk~ZJ8a6ZRecA~aV7Ke9FORn~Bo1xMRD4DT~fTwYbGwbry~RcahSSzeRf~RNRT4YpoYL~FqVQndhufZ~skx_-I2o4Y~mzJgaDwBF5~q303ip6Ui5~0Sds1vVNKR~KsffjH82XV~9V46Zz_N_N~zyKU3Q5L4C~8hvl9OD4OK~7f-bbyR7A1~a3zvshTj4U~tgP8r-gOe_~p7TjX6YIQJ~jH0uD88V6F~OPmau8HTOc~QtSrCpB6CD~q3eUobDMJW~H0KKRBjKCB~GWWI6qdtXy~xIVzgCxLKX~69AJofSeas~r1osbc3bL3~oPq431c8P1~xaKPSzWiiE~IPNeYw2vRN~Bnnrgw1VpP; __cf_bm=59a2bf7cf5c1a9ccf2a2dc252086cbaefe76be26-1611920154-1800-AWLD5zoifHFjTf/+s/iu6ZWjkuLGZJ/xIcNedeBq6YqOiaOKlsjW5QPqWZtN3nZEKroUGuU9HGY0K1Q98oCGnDohZdC2ihN1P9QDqiNGHeGz0oJ3NMYkHHRZ4KUk6wLfj1EVhw+UJp1EHbgQPH9/iheThIA7fBqhGuM21Ju8izQm'
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
        print(preUrl, lastUrl)
        pageCount = content['illust'][s]['pageCount']
        for i in range(0, min(pageCount, pageCountMax)):
            desUrl = preUrl + str(i) + lastUrl
            print(desUrl)
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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36', 'cookie': '__cfduid=d40b8cceb340be6a3e4e66acfe09241ef1610429186; first_visit_datetime_pc=2021-01-12+14%3A26%3A26; p_ab_id=2; p_ab_id_2=5; p_ab_d_id=1343175977; yuid_b=MFgwc3Q; _ga=GA1.2.1687434103.1610429284; PHPSESSID=20192742_qGdjZiY1mDUS81awYMFfBWnisOg6cYcR; device_token=8136801d229a5bd54062e45069592095; c_type=19; a_type=0; b_type=1; login_ever=yes; user_language=zh; privacy_policy_agreement=2; tag_view_ranking=og5cTSQtiT~Kh4mg2DS4s~aeYJNizZc6~0xsDLqCEW6~RTJMXD26Ak~JBqkgBEhOH~ZQngJx8lsH~wpJacsLYRf~HGDBRCKOc3~w-4q98p7vk~ZJ8a6ZRecA~aV7Ke9FORn~Bo1xMRD4DT~fTwYbGwbry~RcahSSzeRf~RNRT4YpoYL~FqVQndhufZ~skx_-I2o4Y~mzJgaDwBF5~q303ip6Ui5~0Sds1vVNKR~KsffjH82XV~9V46Zz_N_N~zyKU3Q5L4C~8hvl9OD4OK~7f-bbyR7A1~a3zvshTj4U~tgP8r-gOe_~p7TjX6YIQJ~jH0uD88V6F~OPmau8HTOc~QtSrCpB6CD~q3eUobDMJW~H0KKRBjKCB~GWWI6qdtXy~xIVzgCxLKX~69AJofSeas~r1osbc3bL3~oPq431c8P1~xaKPSzWiiE~IPNeYw2vRN~Bnnrgw1VpP; __cf_bm=59a2bf7cf5c1a9ccf2a2dc252086cbaefe76be26-1611920154-1800-AWLD5zoifHFjTf/+s/iu6ZWjkuLGZJ/xIcNedeBq6YqOiaOKlsjW5QPqWZtN3nZEKroUGuU9HGY0K1Q98oCGnDohZdC2ihN1P9QDqiNGHeGz0oJ3NMYkHHRZ4KUk6wLfj1EVhw+UJp1EHbgQPH9/iheThIA7fBqhGuM21Ju8izQm'
    }
    url = 'https://www.pixiv.net/ajax/search/artworks/'+s+'%20100users入り?word=' + \
        s + '%20100users入り&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'
    pids = []
    urls = []
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        Datas = json.loads(r.text)['body']['illustManga']['data']
        for i in range(numsOfPic):
            urls.append(Datas[i]['url'])
            pids.append(Datas[i]['id'])
        headers['Referer'] = 'https://www.pixiv.net/'
        for i in range(numsOfPic):
            r = requests.get(urls[i], headers=headers)
            with open('tmp_'+str(i)+'.jpg', 'wb') as f:
                f.write(r.content)
                f.close()
        return pids
    except:
        print('error')
        return
