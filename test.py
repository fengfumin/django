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

    # 浦东


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        'Referer': 'https://sh.5i5j.com/zufang/minxingqu/',
        'Cookie': 'morCon=null; webim_token_6209882=YWMtshE0TkcPEemPqKPbs2zSrUhiN_DRZBHmt4eJit69xiCnDhP6Rw8R6YO6lWDmHBapAwMAAAFpgPaK2gBPGgB_VxXJKn1bnZMkL5Blr37nlZNaP0SOp3JOtr_wp7yYdA; __guid=268564659.2439746432518361000.1552627218477.9233; _ga=GA1.2.2000523734.1552627219; _gid=GA1.2.1017807643.1552627219; yfx_c_g_u_id_10000001=_ck19031513202316418801933916606; yfx_mr_n_10000001=baidu%3A%3Amarket_type_cpc%3A%3A%3A%3Abaidu_ppc%3A%3A%25e7%25a7%259f%25e6%2588%25bf%25e7%25bd%2591%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3Awww.baidu.com%3A%3A22975085394%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25B2%25BE%25E7%25A1%25AE%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3A41%3A%3Apmf_from_adv%3A%3Ash.5i5j.com%2F; yfx_mr_f_n_10000001=baidu%3A%3Amarket_type_cpc%3A%3A%3A%3Abaidu_ppc%3A%3A%25e7%25a7%259f%25e6%2588%25bf%25e7%25bd%2591%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3Awww.baidu.com%3A%3A22975085394%3A%3A%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25B2%25BE%25E7%25A1%25AE%3A%3A%25E7%25A7%259F%25E6%2588%25BF%25E7%25BD%2591%3A%3A41%3A%3Apmf_from_adv%3A%3Ash.5i5j.com%2F; yfx_key_10000001=%25e7%25a7%259f%25e6%2588%25bf%25e7%25bd%2591; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1552627242; yfx_s_u_id_10000001=6209882; yfx_s_u_name_10000001=13916895160; user_info=TBYRRFZKXlNdAUFbEANSDgIHXQoFAQMIQ08VXF1RDgtRXVUSChJWVl0BAQEAEhwSRUNVQnlUEgoSBgIACQgIAhJN; wiwj_token_ticket=ST-130619-57Rgl1HFeSZ7NetsGGO7-passport.5i5j.com; wiwj_token_ST-130619-57Rgl1HFeSZ7NetsGGO7-passport.5i5j.com=%7B%22uid%22%3A%226209882%22%7D; PHPSESSID=ST-131531-E1M3lwyRp320zKnyiuOQ-passport5i5jcom; _Jo0OQK=70398533A1191A2FCC2644E12FC7AE96C5A2D26492C475998D4B3C962972980E7C3795125852AC4FB8A7A86A291B4C068561DC3B9EFD554F36E8F4969CF1DEEDE10A3A6B6373DCEA275A28E4E02FA79F6B8A28E4E02FA79F6B8B5D6E3B97032599B31B6D6E25FE18ACFGJ1Z1Tg==; zufang_BROWSES=42186852%2C42578462%2C42505857%2C42489473%2C36676927%2C35340841%2C31633647%2C42493992%2C37126395%2C36743008%2C36481025%2C35573359; zufang_cookiekey=%5B%22%257B%2522url%2522%253A%2522%252Fzufang%252F_%2525E9%252587%252587%2525E5%252585%252589%253Fzn%253D%2525E9%252587%252587%2525E5%252585%252589%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E9%2587%2587%25E5%2585%2589%2522%252C%2522total%2522%253A%25220%2522%257D%22%2C%22%257B%2522url%2522%253A%2522%252Fzufang%252F_%2525E9%252587%252591%2525E6%2525A1%2525A5%253Fzn%253D%2525E9%252587%252591%2525E6%2525A1%2525A5%2522%252C%2522x%2522%253A%25220%2522%252C%2522y%2522%253A%25220%2522%252C%2522name%2522%253A%2522%25E9%2587%2591%25E6%25A1%25A5%2522%252C%2522total%2522%253A%25220%2522%257D%22%5D; domain=sh; yfx_f_l_v_t_10000001=f_t_1552743438459__r_t_1552748838728__v_t_1552748838728__r_c_2; monitor_count=73; _gat=1; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1552749575'
    }


    def random_num():
        res = ''
        for i in range(8):
            num = str(random.randint(1, 9))
            res += num
        return res


    for i in range(2,3):
        url = "https://sh.5i5j.com/zufang/qingpuqu/n%s/"%i
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        ul = soup.find(name="ul", attrs={"class": "pList"})
        li_list = ul.find_all(name="li")

        for li in li_list:
            title = li.find(name="h3", attrs={"class": "listTit"})
            house_msg = li.find(name="div", attrs={"class": "listX"})
            month_price = house_msg.find(name="strong")
            # print(month_price.text, "<<价格")
            p_list = house_msg.find_all(name="p")
            # bedroom_num=p_list[0].text[0]
            # drawing_room_num=p_list[0].text[4]
            # area=p_list[0].text[10:12]
            num_list = p_list[0].text.split("·")
            res = re.findall("\d+", num_list[0])
            bed_num = res
            # print(bed_num, "<<室和厅")
            # 匹配整数或者浮点数
            res = re.findall("([0-9]+\.[0-9]*[1-9][0-9]*|[0-9]*[1-9][0-9]*)", num_list[1])
            area = res
            # print(area, "<<面积")
            # print(num_list[2], "<<朝向")
            res = re.findall("\d+", num_list[3])
            floor_num = res
            # print(floor_num, "<<楼层数")
            res = num_list[3].split("/")
            floor_type = res[0].strip(" ")
            # print(floor_type, "<<楼层位置")
            try:
                print(num_list[4], "<<装修情况")
            except Exception as e:
                print(e)

            house_name = p_list[1].text.split("·")[0].split(" ")[1]
            trading_area = p_list[1].text.split("·")[0].split(" ")[0]
            # print(house_name, "<<小区名称")
            # print(trading_area, "<<商圈")

            # print(bedroom_num,drawing_room_num,area)
            ran_num = random_num()

            img = li.find(name="img", attrs={"class": "lazy"}).attrs.get("src")
            if not img:
                img = li.find(name="img", attrs={"class": "lazy"}).attrs.get("data-src")
            # 图片链接
            url_img = img
            # print(url_img)
            res = requests.get(url=url_img)
            img = res.content
            with open(r"D:\PycharmProjects\django\maplehouse\media\avatar\house\%s.jpg" % ran_num, "wb")as f:
                f.write(img)
            title_img = "avatar\house\%s.jpg" % ran_num
            dic = {"低楼层": 0, "中楼层": 1, "高楼层": 2, "顶层": 3,"底层":4}
            print(title.text)
            print(ran_num)
            print(float(area[0]))
            print(int(bed_num[0]))
            print(int(bed_num[1]))
            print(dic[floor_type])
            print(int(floor_num[0]))
            print(int(month_price.text))
            print(trading_area)
            print(title_img)
            house_id=models.House.objects.create(title=title.text, huose_num=ran_num, house_name=house_name, area=float(area[0]),
                                        bedroom_num=int(bed_num[0]), drawing_room_num=int(bed_num[1]),
                                        orientation=1, floor_type=dic[floor_type], floor_num=int(floor_num[0]),
                                        month_price=int(month_price.text), area_location=12, rent_way=0,
                                        decoration=0, trading_area=trading_area, title_img=title_img)


            a_div = li.find(name="div", attrs={"class": "listImg"})
            a_href = a_div.find(name="a").attrs.get("href")
            a_href = "https://sh.5i5j.com%s" % a_href
            # 向详情页发送请求
            print(a_href)
            resp = requests.get(url=a_href, headers=headers)
            soup_d = BeautifulSoup(resp.text, "lxml")

            ul_d = soup_d.find(name="ul", attrs={"class": "fytese"})
            li_list_d = ul_d.find_all(name="li")
            label_list = []
            for li_d in li_list_d:
                label = li_d.find(name="label")
                label_list.append(label.text)
            print(label_list)
            try:
                l0=label_list[0]
            except Exception as e:
                l0=""
            try:
                l1=label_list[1]
            except Exception as e:
                l1=""
            try:
                l2=label_list[2]
            except Exception as e:
                l2=""
            try:
                l3=label_list[3]
            except Exception as e:
                l3=""
            try:
                l4=label_list[4]
            except Exception as e:
                l4=""


            models.HousingCharacteristics.objects.create(house=house_id,lightspot=l0,
                                                         introduce=l1,traffic=l2,rim=l3,housing_message=l4,)

            ul_i = soup_d.find(name="ul", attrs={"class": "listimg"})
            li_list_i = ul_i.find_all(name="li")
            for li_i in li_list_i:
                a_img = li_i.find(name="a").attrs.get("href")
                print(a_img)
                file = a_img.split("/")[-1]
                res = requests.get(a_img)
                with open(r"D:\PycharmProjects\django\maplehouse\media\avatar\house\%s" % file, "wb")as f:
                    f.write(res.content)
                house_p = "avatar\house\%s" % file
                models.HousingPictures.objects.create(house=house_id,picture=house_p)
