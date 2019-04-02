# -*- coding: utf-8 -*-
# __author__="maple"
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maplehouse.settings")
    import django
    django.setup()
    from renting import models

    import requests
    from bs4 import BeautifulSoup
    import re, random

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        'Referer':'https://sh.5i5j.com/jingjiren/n2/',
        'Cookie':'webim_token_6209882=YWMta0V83koZEemWt3XNiZkO70hiN_DRZBHmt4eJit69xiCnDhP6Rw8R6YO6lWDmHBapAwMAAAFplN9uSgBPGgDW7Y4Rz7vTcoXIg-YlpgR8qMqubnP7V9cx_ulLXdsgIA; __guid=268564659.2439746432518361000.1552627218477.9233; _ga=GA1.2.2000523734.1552627219; _gid=GA1.2.1017807643.1552627219; yfx_c_g_u_id_10000001=_ck19031513202316418801933916606; yfx_mr_f_n_10000001=baidu%3A%3Amarket_type_cpc%3A%3A%3A%3Abaidu_ppc%3A%3A%25e7%25a7%259f%25e6%2588%25bf%25e7%25bd%2591%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3Awww.baidu.com%3A%3A22975085394%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25B2%25BE%25E7%25A1%25AE%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3A41%3A%3Apmf_from_adv%3A%3Ash.5i5j.com%2F; yfx_s_u_id_10000001=6209882; yfx_s_u_name_10000001=13916895160; user_info=TBYRRFZKXlNdAUFbEANSDgIHXQoFAQMIQ08VXF1RDgtRXVUSChJWVl0BAQEAEhwSRUNVQnlUEgoSBgIACQgIAhJN; wiwj_token_ST-130619-57Rgl1HFeSZ7NetsGGO7-passport.5i5j.com=%7B%22uid%22%3A%226209882%22%7D; zufang_cookiekey=%5B%22%257B%2522url%2522%253A%2522%252Fzufang%252F_%2525E9%252587%252587%2525E5%252585%252589%253Fzn%253D%2525E9%252587%252587%2525E5%252585%252589%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E9%2587%2587%25E5%2585%2589%2522%252C%2522total%2522%253A%25220%2522%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fzufang%252F_%2525E9%252587%252591%2525E6%2525A1%2525A5%253Fzn%253D%2525E9%252587%252591%2525E6%2525A1%2525A5%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E9%2587%2591%25E6%25A1%25A5%2522%252C%2522total%2522%253A%25220%2522%257D%22%5D; baidu_OCPC_pc=53778ea42828c27c742c6e3055e0357331f7da2c50e31cc1406fbb0db765dd37a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22baidu_OCPC_pc%22%3Bi%3A1%3Bs%3A178%3A%22%22https%3A%5C%2F%5C%2Fsh.5i5j.com%5C%2F%3Fpmf_group%3Dbaidu%26pmf_medium%3Dppzq%26pmf_plan%3D%25E5%25B7%25A6%25E4%25BE%25A7%25E6%25A0%2587%25E9%25A2%2598%26pmf_unit%3D%25E6%25A0%2587%25E9%25A2%2598%26pmf_keyword%3D%25E6%25A0%2587%25E9%25A2%2598%26pmf_account%3D179%22%22%3B%7D; yfx_mr_n_10000001=baidu%3A%3Amarket_type_ppzq%3A%3A%3A%3Abaidu_ppc%3A%3A%25e6%2588%2591%25e7%2588%25b1%25e6%2588%2591%25e5%25ae%25b6%25e6%2588%25bf%25e4%25ba%25a7%25e5%25ae%2598%25e6%2596%25b9%25e7%25bd%2591%3A%3A%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3Awww.baidu.com%3A%3A%3A%3A%3A%3A%25E5%25B7%25A6%25E4%25BE%25A7%25E6%25A0%2587%25E9%25A2%2598%3A%3A%25E6%25A0%2587%25E9%25A2%2598%3A%3A179%3A%3Apmf_from_adv%3A%3Ash.5i5j.com%2F; yfx_key_10000001=%25e6%2588%2591%25e7%2588%25b1%25e6%2588%2591%25e5%25ae%25b6%25e6%2588%25bf%25e4%25ba%25a7%25e5%25ae%2598%25e6%2596%25b9%25e7%25bd%2591; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1552627242,1552956236; _Jo0OQK=43C98533A1191A2FCC2644E12FC7AE96C5A2D26492C475998D4B3C962972980E7C3795125852AC4FB8A7A86A291B4C06856E163C1A196831DBD8B37D0293DCC0D79A3A6B6373DCEA275A28E4E02FA79F6B8A28E4E02FA79F6B829A255F2F8BDEEBE20D2F0A621A51499GJ1Z1Xg==; zufang_BROWSES=42186852%2C42578462%2C42505857%2C42489473%2C36676927%2C35340841%2C31633647%2C42493992%2C37126395%2C36743008%2C36481025%2C35573359%2C24781313%2C41488215%2C35081298; wiwj_token_ticket=ST-103918-stUNcb7ABHknMVfMYVGR-passport.5i5j.com; wiwj_token_ST-103918-stUNcb7ABHknMVfMYVGR-passport.5i5j.com=%7B%22uid%22%3A%226209882%22%7D; domain=sh; yfx_f_l_v_t_10000001=f_t_1552821148088__r_t_1552956235924__v_t_1552980724471__r_c_5; PHPSESSID=ST-133652-AaGOOlV1mhtodNDiVZQm-passport5i5jcom; monitor_count=134; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1552980867'
    }

    def random_num():
        res = ''
        for i in range(4):
            num = str(random.randint(1, 9))
            res += num
        return res

    def random_num8():
        res = ''
        for i in range(8):
            num = str(random.randint(1, 9))
            res += num
        return res
    for i in range(4,15):
        url = "https://sh.5i5j.com/jingjiren/%s"%i
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        ul = soup.find(name="div", attrs={"class": "list-con-box"})
        print()
        div_list = ul.find_all(name="div",attrs={"class":"agent-con-box clear"})
        for div in div_list:
            agent=div.find(name="div",attrs={"class":"agent-tit"})
            name=agent.find(name="h3")

            p=div.find(name="p",attrs={"class":"iconsleft"})
            # print(p.text)
            p_list=p.text.split("·")
            try:
                quyu1=p_list[0]
            except Exception:
                quyu1=""
            try:
                quyu2=p_list[1]
            except Exception:
                quyu2=""
            try:
                dianpu=p_list[2]
            except Exception:
                dianpu=""
            contacty=div.find(name="div",attrs={"class":"contacty"})
            phone=contacty.find(name="span")

            img=div.find(name="div",attrs={"class":"agent-img lf"})
            img1=img.find(name="img").attrs.get("data-src")
            if not img1:
                img1 = img.find(name="img").attrs.get("src")
            print(img1)
            num8=random_num8()
            res=requests.get(url=img1)
            with open(r"D:\PycharmProjects\django\maplehouse\media\avatar\broker\%s.jpg"%num8,"wb")as f:
                f.write(res.content)

            num=random_num()
            num1=random.randint(1, 3)
            print(name.text,quyu1,quyu2,dianpu,phone.text)
            models.Broker.objects.create(username="broker%s"%num,password="broker%s"%num,
                                         nickname=name.text,serve_years=num1,serve_area=quyu1+quyu2,
                                         belong_store=dianpu,phone=int(phone.text),img=r"avatar\broker\%s.jpg"%num8)

