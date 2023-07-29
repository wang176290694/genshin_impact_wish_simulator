from bs4 import BeautifulSoup
import requests
import os
import urllib.request as req
import json
import copy
import re
import pygame
import sys

download_dict = {
    "https://patchwiki.biligame.com/images/ys/5/50/resfhdf0vgvhqpo85alolzppqiabtsv.png": "./files/image/corner.png",
    "https://patchwiki.biligame.com/images/ys/9/9f/gous4mcm5zt6ru5yxviighe5tyem64q.png": "./files/image/corner2.png",
    "https://patchwiki.biligame.com/images/ys/2/2a/f5ogmdvyb04dsfcy3kk5ne8jud38l6j.png": "./files/image/top.png",
    "https://patchwiki.biligame.com/images/ys/b/b3/3vsmvlo8qo6192b89jmoqxvj5fpol6u.png": "./files/image/bottom.png",
    "https://patchwiki.biligame.com/images/ys/2/23/etuw92oibr0h0j4hyzly1epi69cz5zh.png": "./files/image/left.png",
    "https://patchwiki.biligame.com/images/ys/5/54/1am5v0yo8lect5lnhyym6nuce9ygt7x.png": "./files/image/one_background.png",
    "https://patchwiki.biligame.com/images/ys/thumb/2/2a/c6wlx8b019ocn9hcjaxoo3khxdlx6y8.png/220px-%E5%9B%BE%E6%A0%87%E8%83%8C%E6%99%AF-2.png": "./files/image/two_background.png",
    "https://patchwiki.biligame.com/images/ys/e/e3/7qifq6r1zm5yw0ki1ciknko23tgi7fq.png": "./files/image/three_background.png",
    "https://patchwiki.biligame.com/images/ys/thumb/e/eb/qtfzqnqw9fmpz3e73wbuq3ga3g8iht8.png/220px-%E5%9B%BE%E6%A0%87%E8%83%8C%E6%99%AF-4.png": "./files/image/four_background.png",
    "https://patchwiki.biligame.com/images/ys/thumb/4/4a/32s8veokd2purnqm4su6rmgx5lx0six.png/220px-%E5%9B%BE%E6%A0%87%E8%83%8C%E6%99%AF-5.png": "./files/image/five_background.png",
    "https://patchwiki.biligame.com/images/ys/1/13/7xzg7tgf8dsr2hjpmdbm5gn9wvzt2on.png": "./files/image/1s.png",
    "https://patchwiki.biligame.com/images/ys/b/bc/sd2ige6d7lvj7ugfumue3yjg8gyi0d1.png": "./files/image/2s.png",
    "https://patchwiki.biligame.com/images/ys/e/ec/l3mnhy56pyailhn3v7r873htf2nofau.png": "./files/image/3s.png",
    "https://patchwiki.biligame.com/images/ys/9/9c/sklp02ffk3aqszzvh8k1c3139s0awpd.png": "./files/image/4s.png",
    "https://patchwiki.biligame.com/images/ys/c/c7/qu6xcndgj6t14oxvv7yz2warcukqv1m.png": "./files/image/5s.png",
    "https://patchwiki.biligame.com/images/ys/b/b0/7uecwf4phmgjfnzevac1zye9m6qxkps.png": "./files/image/mouse.png",
    "https://patchwiki.biligame.com/images/ys/f/ff/0dlkmof43y8aam8fphgixaejy571iqc.png": "./files/image/five_stars.png",
    "https://patchwiki.biligame.com/images/ys/2/2a/ssqzx9cint7m3yudjwviabu4nkd8s9o.png": "./files/image/four_stars.png",
    "https://patchwiki.biligame.com/images/ys/2/27/pfo2hwmoxygf9nhkb2hxmqgpfrsgdpq.png": "./files/image/three_stars.png",
    "https://patchwiki.biligame.com/images/ys/7/76/pd9w1fbgtzy0gp8muauyusvpow2zvxg.png": "./files/image/two_stars.png",
    "https://patchwiki.biligame.com/images/ys/b/ba/6u05pqfxydhvkwf5nhqeb79tuk3lqxn.png": "./files/image/one_stars.png",
    "https://patchwiki.biligame.com/images/ys/thumb/b/b8/aszemkvmlkr8mlqbveucrlrktyf4qxq.png/270px-%E5%9B%BE%E9%89%B4-%E5%A4%A7%E5%9B%BE%E5%9B%BE%E6%A1%86.png": "./files/image/wish/weapon_rect.png",
    "https://patchwiki.biligame.com/images/ys/a/a1/iuekntkykk5chcknfp9q8d627lkqqqr.png": "./files/image/wish/user_want_corner.png",
    "https://patchwiki.biligame.com/images/ys/thumb/2/2e/1m47w1e73zyori1tb4em9e74lkltt6s.png/240px-%E7%81%AB.png": "./files/image/wish/element/火.png",
    "https://patchwiki.biligame.com/images/ys/thumb/a/a9/okiqd77ie0p6vyu1cz80rn8mh0m9b0w.png/240px-%E6%B0%B4.png": "./files/image/wish/element/水.png",
    "https://patchwiki.biligame.com/images/ys/thumb/e/eb/5g6eg7a5hdyk2izxrhqg6suphjh983u.png/240px-%E5%86%B0.png": "./files/image/wish/element/冰.png",
    "https://patchwiki.biligame.com/images/ys/thumb/a/af/bvgkk8noastajq7gbsapbszo1rkek6p.png/240px-%E9%9B%B7.png": "./files/image/wish/element/雷.png",
    "https://patchwiki.biligame.com/images/ys/thumb/a/af/lema9k39oklrmlw87pv0j2nl2ynzveg.png/240px-%E9%A3%8E.png": "./files/image/wish/element/风.png",
    "https://patchwiki.biligame.com/images/ys/thumb/c/cc/dyh0qx9nbgq4qcy7ytddke7hdt3gicm.png/240px-%E5%B2%A9.png": "./files/image/wish/element/岩.png",
    "https://patchwiki.biligame.com/images/ys/thumb/c/ca/dmgt70p4e9epw91ljaoyviwjjdla1g7.png/240px-%E8%8D%89.png": "./files/image/wish/element/草.png",
    "https://i0.hdslb.com/bfs/new_dyn/f606b45be92bc779e09c4ff9460a54fd401742377.jpg": "./files/image/starter/background/10.png",
    "https://i0.hdslb.com/bfs/new_dyn/354e957581e9b5e6338bb5f6ddb5419d401742377.jpg": "./files/image/starter/background/11.png",
    "https://i0.hdslb.com/bfs/new_dyn/7db468a94755525a6f67cdb418c9ece8401742377.jpg": "./files/image/starter/background/12.png",
    "https://i0.hdslb.com/bfs/new_dyn/df93c9ee05421279aa6159600084fcae401742377.jpg": "./files/image/starter/background/13.png",
    "https://i0.hdslb.com/bfs/new_dyn/6558470d1c894fc072a600286e966da2401742377.jpg": "./files/image/starter/background/14.png",
    "https://i0.hdslb.com/bfs/new_dyn/7afc70d9602ca17e1b337bfdae049191401742377.jpg": "./files/image/starter/background/15.png",
    "https://i0.hdslb.com/bfs/new_dyn/d0819e9f8e476fe8c8813baf40979776401742377.jpg": "./files/image/starter/background/16.png",
    "https://i0.hdslb.com/bfs/new_dyn/4b980cf86e1b5d19a49393f793272750401742377.jpg": "./files/image/starter/background/17.png",
    "https://i0.hdslb.com/bfs/new_dyn/84457793ae9c48b125a806f48d63a71b401742377.jpg": "./files/image/starter/background/18.png",
    "https://i0.hdslb.com/bfs/new_dyn/79242c344fa64b45f70cf93546c4cb71401742377.jpg": "./files/image/starter/background/19.png",
    "https://i0.hdslb.com/bfs/new_dyn/2ae0fddd5a111feb56b5730684ed226c401742377.jpg": "./files/image/starter/background/20.png",
    "https://i0.hdslb.com/bfs/new_dyn/cd15045894a5cb09ab0de1cb10628bbd401742377.jpg": "./files/image/starter/background/21.png",
    "https://i0.hdslb.com/bfs/album/4c0e8aa1286ac5d8227ab4d1908e462e50de1b95.jpg": "./files/image/starter/background/22.png",
    "https://i0.hdslb.com/bfs/album/19482bd40dd912f3cc319b49f3477d5b56d36f6e.jpg": "./files/image/starter/background/23.png",
    "https://i0.hdslb.com/bfs/album/bc693451d1d92356e5f21b2e1c773f42d0f7b60f.jpg": "./files/image/starter/background/24.png",
    "https://i0.hdslb.com/bfs/album/b8a1ec4b06921e183faaaa968a363d70dc201a59.png": "./files/image/starter/background/25.png",
    "https://i0.hdslb.com/bfs/album/6e48f13faeaee04b6f76348b0573796ebe0c0a57.png": "./files/image/starter/background/26.png",
    "https://i0.hdslb.com/bfs/album/02044dc19a31f9e85a5ad5a974eae4c10ef9c4b3.jpg": "./files/image/starter/background/27.png",
    "https://i0.hdslb.com/bfs/album/705721f505280005931bb03fdf172c0737a3afbe.jpg": "./files/image/starter/background/28.png",
    "https://i0.hdslb.com/bfs/album/5e0ba931ac93b1f5a60cb0269ba59738ff6bb561.jpg": "./files/image/starter/background/29.png",
    "https://i0.hdslb.com/bfs/album/daa9aa70ae29173ef8be58a313f3f56daf0a20aa.jpg": "./files/image/starter/background/30.png",
    "https://act-upload.mihoyo.com/ys-obc/2023/05/30/195563531/ed12ac9a3feb2369a3ab444b9d6e4e1e_7475245851251088988.png": "./files/image/wish/character_map.png",
    "https://act-upload.mihoyo.com/ys-obc/2023/05/30/195563531/e21d9dbe4b0a9f0181b7b701afe688f2_1340948458477159082.png": "./files/image/wish/character_map_now.png",
    "https://act-upload.mihoyo.com/ys-obc/2023/05/30/195563531/bf84a55173b5f1bc2764c558ea65965b_6275953452800414789.png": "./files/image/wish/weapon_map.png",
    "https://act-upload.mihoyo.com/ys-obc/2023/05/30/195563531/a79506c8e6570fd0aea5114dfa7e318b_3415504268600673789.png": "./files/image/wish/weapon_map_now.png"

}
download_dict2 = {
    "./files/image": ["closing_button.png", "get_sth.png", "input.png", "message_box.png", "mouse.png", "ok_box.png",
                      "scroll.png", "scroll_back.png"],
    "./files/image/wish": ["background.png", "background_wish.png", "background_wish2.png", "dust.png", "history.png",
                           "history_type.png", "jiu_chan_ball.png", "jiu_chan_ball2.png", "meet_ball.png",
                           "meet_ball2.png", "normal_wish.png", "pic_wish.png", "pic_wish2.png", "setting.png",
                           "star.png", "starter_wish.jpg", "stone.png", "store.png", "user_want_already.jpg",
                           "user_want_choose.png", "user_want_need_main.png", "user_want_text.jpg",
                           "user_want_uncertain.jpg", "user_want0.png", "user_want1.png", "user_want2.png",
                           "wish_back.png"],
    "./files/image/wish/element": ["水.png", "火.png", "冰.png", "雷.png", "风.png", "岩.png", "草.png", "长柄武器.png",
                                   "单手剑.png", "双手剑.png", "法器.png", "弓.png", "question.png"],
    "./files/ls": ["0.png", "1.png"]
}
pygame.init()


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def save_img():
    for i in download_dict2:
        for j in download_dict2[i]:
            if not os.path.isfile(f"{i}/{j}"):
                surface1 = image_load(f"{i}/{j}")
                pygame.image.save(surface1, f"{i}/{j}")
                print(f"{i}/{j} 保存成功")
    for i in dict_id:
        if not os.path.isfile(f"./files/ls/{dict_id[i]}.png"):
            try:
                surface1 = image_load(f"./files/ls/{dict_id[i]}.png")
                pygame.image.save(surface1, f"./files/ls/{dict_id[i]}.png")
                print(f"./files/ls/{dict_id[i]}.png 保存成功")
            except FileNotFoundError:
                print(f"./files/ls/{dict_id[i]}.png")


def image_load(file_direction):
    return pygame.image.load(get_resource_path(file_direction))


def set_object_surface(name1: str, count1: int, type1: int, black: bool = False, stars: int = 5):
    font_14 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 16)
    pic1 = pygame.image.load(f"files/image/map/{name1}.png")
    if stars == 5:
        five_stars = pygame.image.load(f"./files/image/5s.png")
        background = pygame.transform.scale(pygame.image.load(f"./files/image/five_background.png"), (85, 85))
    elif stars == 4:
        five_stars = pygame.image.load(f"./files/image/4s.png")
        background = pygame.transform.scale(pygame.image.load(f"./files/image/four_background.png"), (85, 85))
    elif stars == 3:
        five_stars = pygame.image.load(f"./files/image/3s.png")
        background = pygame.transform.scale(pygame.image.load(f"./files/image/three_background.png"), (85, 85))
    elif stars == 2:
        five_stars = pygame.image.load(f"./files/image/2s.png")
        background = pygame.transform.scale(pygame.image.load(f"./files/image/two_background.png"), (85, 85))
    else:
        five_stars = pygame.image.load(f"./files/image/1s.png")
        background = pygame.transform.scale(pygame.image.load(f"./files/image/one_background.png"), (85, 85))
    five_stars = pygame.transform.scale(five_stars, (five_stars.get_size()[0] * (15 / five_stars.get_size()[1]), 15))
    corner = pygame.transform.scale(pygame.image.load(f"./files/image/wish/user_want_corner.png"), (85, 41))
    surface1 = pygame.surface.Surface((85, 105))
    surface1.blit(background, (0, 0))
    surface1.blit(pygame.transform.scale(pic1, (85, 85)), (0, 0))
    surface1.blit(corner, (0, 66))
    if type1 == 1:
        text1 = font_14.render(name1, True, (0, 0, 0))
    elif type1 == 2:
        text1 = font_14.render(f"{name1} : {count1}", True, (0, 0, 0))
    elif type1 == 5:
        text1 = pygame.surface.Surface((0, 0))
    else:
        text1 = font_14.render(str(count1), True, (0, 0, 0))
    if text1.get_size()[0] > 85:
        num_font = 16
        while True:
            num_font -= 1
            font_14 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), num_font)
            if type1 == 1:
                text1 = font_14.render(name1, True, (0, 0, 0))
            elif type1 == 2:
                text1 = font_14.render(f"{name1} : {count1}", True, (0, 0, 0))
            else:
                text1 = font_14.render(str(count1), True, (0, 0, 0))
            if text1.get_size()[0] <= 85:
                break
    surface1.blit(text1, ((85 - text1.get_size()[0]) / 2, 85))
    surface1.blit(five_stars, ((surface1.get_size()[0] - five_stars.get_size()[0]) / 2, 72))
    if black:
        black1 = pygame.surface.Surface((85, 105)).convert_alpha()
        black1.fill((0, 0, 0, 120))
        surface1.blit(black1, (0, 0))
    return surface1


def set_border(size: tuple):
    size = (size[0] * 3, size[1] * 3)
    left_up = pygame.image.load("./files/image/corner.png")
    right_up = pygame.transform.flip(left_up, True, False)
    left_down = pygame.image.load("./files/image/corner2.png")
    right_down = pygame.transform.flip(left_down, True, False)
    right = pygame.transform.scale(pygame.image.load("./files/image/left.png"), (57, size[1] - 270))
    left = pygame.transform.flip(right, True, False)
    top = pygame.transform.scale(pygame.image.load("./files/image/top.png"), (size[0] - 270, 36))
    bottom = pygame.transform.scale(pygame.image.load("./files/image/bottom.png"), (size[0] - 270, 54))
    screen_main = pygame.surface.Surface(size)
    screen_main.fill((248, 243, 239))
    screen_main.blit(left_up, (0, 0))
    screen_main.blit(right_up, (size[0] - left_up.get_size()[0], 0))
    screen_main.blit(left_down, (0, size[1] - left_down.get_size()[1]))
    screen_main.blit(right_down, (size[0] - right_down.get_size()[0], size[1] - right_down.get_size()[1]))
    screen_main.blit(left, (0, 135))
    screen_main.blit(right, (size[0] - right.get_size()[0], 135))
    screen_main.blit(top, (135, 0))
    screen_main.blit(bottom, (135, size[1] - bottom.get_size()[1]))
    screen_main = pygame.transform.scale(screen_main, (size[0] / 3, size[1] / 3))
    return screen_main


def download_pictures():
    def save_object_surface(name1: str):
        if name1[1] == "0" or name1[1] == "5":
            stars = 5
        elif name1[1] == "3":
            stars = 3
        else:
            stars = 4
        name1 = dict_id[name1]
        pic1 = pygame.image.load(f"./files/image/map/{name1}.png")
        if stars == 5:
            five_stars = pygame.image.load(f"./files/image/5s.png")
            background = pygame.transform.scale(pygame.image.load(f"./files/image/five_background.png"), (85, 85))
        elif stars == 4:
            five_stars = pygame.image.load(f"./files/image/4s.png")
            background = pygame.transform.scale(pygame.image.load(f"./files/image/four_background.png"), (85, 85))
        elif stars == 3:
            five_stars = pygame.image.load(f"./files/image/3s.png")
            background = pygame.transform.scale(pygame.image.load(f"./files/image/three_background.png"), (85, 85))
        elif stars == 2:
            five_stars = pygame.image.load(f"./files/image/2s.png")
            background = pygame.transform.scale(pygame.image.load(f"./files/image/two_background.png"), (85, 85))
        else:
            five_stars = pygame.image.load(f"./files/image/1s.png")
            background = pygame.transform.scale(pygame.image.load(f"./files/image/one_background.png"), (85, 85))
        five_stars = pygame.transform.scale(five_stars,
                                            (five_stars.get_size()[0] * (15 / five_stars.get_size()[1]), 15))
        corner = pygame.transform.scale(pygame.image.load(f"./files/image/wish/user_want_corner.png"), (85, 41))
        surface1 = pygame.surface.Surface((85, 105))
        surface1.blit(background, (0, 0))
        surface1.blit(pygame.transform.scale(pic1, (85, 85)), (0, 0))
        surface1.blit(corner, (0, 66))
        surface1.blit(five_stars, ((surface1.get_size()[0] - five_stars.get_size()[0]) / 2, 72))
        return surface1

    def set_wish_use_pic(item):
        width_w = 600
        height_w = 150
        surface2 = set_border((width_w, height_w))
        font_145 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 40)
        for j in range(3):
            surface1 = set_object_surface(item['four'][j], 0, 1, stars=4)
            surface2.blit(surface1, (255 + 105 * j, (height_w - surface1.get_size()[1]) / 2))
        surface1 = set_object_surface(item['five'][0], 0, 1)
        surface2.blit(surface1, (150, (height_w - surface1.get_size()[1]) / 2))
        font_145 = font_145.render(str(item["id"]), True, (0, 0, 0))
        surface2.blit(font_145, (30, (height_w - font_145.get_size()[1]) / 2))
        surface2 = pygame.transform.scale(surface2, (480, 120))
        return surface2

    def set_wish_use_pic2(item):
        width_w = 600
        height_w = 150
        surface2 = set_border((width_w, height_w))
        font_145 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 40)
        for j in range(2):
            surface1 = set_object_surface(item['five'][j], 0, 1)
            surface2.blit(surface1, (150 + 105 * j, (height_w - surface1.get_size()[1]) / 2))
        surface1 = set_object_surface(item['four'][0], 0, 1, stars=4)
        surface2.blit(surface1, (360, (height_w - surface1.get_size()[1]) / 2))
        font_147 = font_145.render(str(item["id"]), True, (0, 0, 0))
        font_146 = font_145.render("...", True, (0, 0, 0))
        surface2.blit(font_147, (30, (height_w - font_147.get_size()[1]) / 2))
        surface2 = pygame.transform.scale(surface2, (480, 120))
        surface2.blit(font_146, (380, 60))
        return surface2

    def request_pic():
        bg_s = pygame.transform.scale(image_load("./files/image/wish/background.png"), (1200, 675))
        font_145 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 25)
        main_struct1 = {}
        rep = requests.get('https://wiki.biligame.com/ys/%E7%A5%88%E6%84%BF')
        text = rep.text
        rep.close()
        bs = BeautifulSoup(text, features="lxml")
        bta = bs.find_all("table")
        bta = bta[6].contents[1].contents
        for item in range(bta.count('\n')):
            bta.remove('\n')
        bta.pop(0)
        main_struct1['weapon'] = []
        main_struct1['character'] = []
        for tc in bta:
            for item in [1, 3]:
                for tb in tc.contents[item].find_all('table'):
                    if tb.string is None:
                        if tb.find(
                                'img').get("srcset") is not None:
                            sub_struct = {'img': tb.find(
                                'img').get("srcset").split(',')[-1].rstrip().rstrip('1.5x').rstrip('2x')}
                        else:
                            sub_struct = {'img': tb.find(
                                'img').get("src")}
                        trs = tb.find_all('tr')
                        sub_struct['five'] = [tr.string for tr in trs[2].find_all('a')]
                        sub_struct['four'] = [tr.string for tr in trs[3].find_all('a')]
                        main_struct1['weapon' if item - 1 else 'character'].insert(0, sub_struct)
        for item in [('weapon', '2'), ('character', '1')]:
            for ss in enumerate(main_struct1[item[0]]):
                main_struct1[item[0]][ss[0]]['id'] = int(item[1] + "%03d" % (ss[0],))
        character_surface_list = []
        weapon_surface_list = []
        cm = 1000
        wm = 2000
        for item in main_struct1['character']:
            print(item)
            for j in range(3):
                item['four'][j] = item['four'][j].split('·')[1].split('(')[0].split('」')[0]
                change = True
                for key in dict_id:
                    if dict_id[key] == item['four'][j]:
                        change = False
                        break
                if change:
                    print(item['four'][j])
                    number = 0
                    for key in dict_id:
                        if key[0] == "c" and key[1] == "4":
                            number = int(f"{key[2]}{key[3]}")
                    dict_id[f"c4{number + 1}"] = item['four'][j]
            item['five'][0] = item['five'][0].split('·')[1].split('(')[0].split('」')[0]
            if item["id"] > cm:
                cm = item["id"]
            change = True
            for key in dict_id:
                if dict_id[key] == item['five'][0]:
                    change = False
                    break
            if change:
                number = 0
                for key in dict_id:
                    if key[0] == "c" and key[1] == "5":
                        number = int(f"{key[2]}{key[3]}")
                dict_id[f"c5{number + 1}"] = item['five'][0]
            character_surface_list.append(set_wish_use_pic(item))
        for item in main_struct1['weapon']:
            print(item)
            for j in range(5):
                item['four'][j] = item['four'][j].split('·')[1].split('(')[0].split('」')[0]
                change = True
                for key in dict_id:
                    if dict_id[key] == item['four'][j]:
                        change = False
                        break
                if change:
                    print(item['four'][j])
                    number = 0
                    for key in dict_id:
                        if key[0] == "w" and key[1] == "4":
                            number = int(f"{key[2]}{key[3]}")
                    dict_id[f"w4{number + 1}"] = item['four'][j]
            for j in range(2):
                item['five'][j] = item['five'][j].split('·')[1].split('(')[0].split('」')[0]
                change = True
                for key in dict_id:
                    if dict_id[key] == item['five'][j]:
                        change = False
                        break
                if change:
                    number = 0
                    for key in dict_id:
                        if key[0] == "w" and key[1] == "5":
                            number = int(f"{key[2]}{key[3]}")
                    dict_id[f"w5{number + 1}"] = item['five'][j]
            if item["id"] > wm:
                wm = item["id"]
            weapon_surface_list.append(set_wish_use_pic2(item))
        with open(f'./files/jsons/object_id.json', 'w', encoding='utf-8') as file_data:
            file_data.write(json.dumps(dict_id, ensure_ascii=False))
        main_struct1["character_max"] = cm
        main_struct1["weapon_max"] = wm
        num_down = 0
        num_down2 = 0
        surface_down = pygame.surface.Surface((1200, 675))
        surface_down.blit(bg_s, (0, 0))
        num_x = 0
        num_y = 80
        for i in character_surface_list:
            surface_down.blit(i, (num_y, 10 + 125 * num_x))
            num_down += 1
            num_x += 1
            if num_down == 1:
                num_down2 += 1
            if num_down == 5:
                num_x = 0
                num_y = 640
            if num_down == 10:
                num_down = 0
                num_x = 0
                num_y = 80
                surface_down.blit(font_145.render("上一页      下一页", True, (255, 255, 255)), (500, 640))
                pygame.image.save(surface_down, f"./files/image/wish/prize/c{num_down2}.png")
                surface_down = pygame.surface.Surface((1200, 675))
                surface_down.blit(bg_s, (0, 0))
        main_struct1["character_page"] = num_down2
        if num_down != 0:
            surface_down.blit(font_145.render("上一页      下一页", True, (255, 255, 255)), (500, 640))
            pygame.image.save(surface_down, f"./files/image/wish/prize/c{num_down2}.png")
        num_down = 0
        num_down2 = 0
        surface_down = pygame.surface.Surface((1200, 675))
        surface_down.blit(bg_s, (0, 0))
        num_x = 0
        num_y = 80
        for i in weapon_surface_list:
            surface_down.blit(i, (num_y, 10 + 125 * num_x))
            num_down += 1
            num_x += 1
            if num_down == 1:
                num_down2 += 1
            if num_down == 5:
                num_x = 0
                num_y = 640
            if num_down == 10:
                num_down = 0
                num_x = 0
                num_y = 80
                surface_down.blit(font_145.render("上一页      下一页", True, (255, 255, 255)), (500, 640))
                pygame.image.save(surface_down, f"./files/image/wish/prize/w{num_down2}.png")
                surface_down = pygame.surface.Surface((1200, 675))
                surface_down.blit(bg_s, (0, 0))
        main_struct1["weapon_page"] = num_down2
        if num_down != 0:
            surface_down.blit(font_145.render("上一页      下一页", True, (255, 255, 255)), (500, 640))
            pygame.image.save(surface_down, f"./files/image/wish/prize/w{num_down2}.png")
        with open('./files/jsons/wish.json', 'w', encoding='utf-8') as f:
            json.dump(main_struct1, f, ensure_ascii=False)

    def download():
        with open('./files/jsons/wish.json', 'r', encoding='utf-8') as f:
            s = json.load(f)
        for item in [('weapon', '2'), ('character', '1')]:
            for ss in enumerate(s[item[0]]):
                ext_name = copy.deepcopy(ss[1]['img'])
                for j in range(1, len(ext_name) + 1):
                    if '.' == ext_name[-j]:
                        ext_name = ext_name[-j:]
                        break
                for j in range(0, len(ext_name)):
                    if '?' == ext_name[j]:
                        break
                if not os.path.isfile(f"./files/image/wish/{item[1]}{'%03d' % (ss[0],)}.png"):
                    req.urlretrieve(ss[1]['img'], f"./files/image/wish/{item[1]}{'%03d' % (ss[0],)}.png")
                    print(f"文件{ss[1]['img']}下载完成")
                else:
                    print("downloaded, pass")

    def download_pic():
        url1 = requests.get('https://wiki.biligame.com/ys/%E8%A7%92%E8%89%B2')
        soup = BeautifulSoup(url1.text, 'lxml')
        dict2 = soup.find_all("img")
        for ib in dict2:
            if "角色" in str(ib.get("alt")) and not os.path.isfile(
                    f"./files/image/map/{str(ib.get('alt')).split('-')[-1]}"):
                req.urlretrieve(ib.get("src"), f"./files/image/map/{str(ib.get('alt')).split('-')[-1]}")
                print(f"文件{ib.get('src')}下载完成")
            else:
                print("downloaded, pass")
        for key in dict_id:
            if not os.path.isfile(f"./files/image/map/{dict_id[key]}.png"):
                url1 = requests.get(f"https://wiki.biligame.com/ys/{dict_id[key]}")
                data1 = url1.text
                pattern1 = re.compile(f'<img alt="{dict_id[key]}" src="(.+?)"')
                req1 = re.findall(pattern1, data1)[0]
                req.urlretrieve(req1, f"./files/image/map/{dict_id[key]}.png")
                print(f"文件{req1}下载完成")
            else:
                print("downloaded, pass")
        main_struct = {}
        pmap = requests.get(
            'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/home/content/list?app_sn=ys_obc&channel_id=189').json()
        pmap = pmap['data']['list'][0]['children'][0]['list']
        for Sinfo in pmap:
            pic = get_pic(Sinfo['content_id'])
            main_struct[Sinfo['title']] = pic
            print(f"获取{pic}的数据成功")
        for keys in main_struct:
            if not os.path.isfile(f"./files/image/wish/one_wish/{keys}.png"):
                req.urlretrieve(main_struct[keys], f"./files/image/wish/one_wish/{keys}.png")
                print(f"文件{main_struct[keys]}下载完成")
            else:
                print("downloaded, pass")
        for i in download_dict:
            if not os.path.isfile(download_dict[i]):
                req.urlretrieve(i, download_dict[i])
                print(f"文件{i}下载完成")
            else:
                print("downloaded, pass")

    def get_pic(cid):
        text = requests.get(
            f'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id={cid}').json()
        head = text['data']["content"]["contents"][0]['text']
        bs = BeautifulSoup(head, 'lxml')
        stl = bs.find('div', attrs={"data-part": "newMain"}).find('div').find('div')['style'].split('url(\"')
        stl = stl[-1].split('\");')[0]
        return stl

    def save_map():
        for keys in dict_id:
            object_surface = save_object_surface(keys)
            if not os.path.isfile(get_resource_path(f"./files/image/wish/map/{dict_id[keys]}.png")):
                pygame.image.save(object_surface, f"./files/image/wish/map/{dict_id[keys]}.png")
                print(f"下载 ./files/image/wish/map/{dict_id[keys]}.png 成功")
            else:
                print("downloaded, pass")

    os.makedirs("./files/image/wish/prize", exist_ok=True)
    os.makedirs("./files/image/wish/one_wish", exist_ok=True)
    os.makedirs("./files/image/map", exist_ok=True)
    os.makedirs("./files/image/starter/background", exist_ok=True)
    os.makedirs("./files/image/wish/map", exist_ok=True)
    os.makedirs("./files/ls", exist_ok=True)
    os.makedirs("./files/image/wish/element", exist_ok=True)
    os.makedirs("./files/jsons", exist_ok=True)
    download_pic()
    save_map()
    request_pic()
    download()
    save_img()


screen = pygame.display.set_mode((900, 200))
font_40 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 40)
font_41 = font_40.render("请等待程序下载所需文件(预计需十分钟)", True, (255, 255, 255))
font_42 = font_40.render("在此期间程序可能无响应，属正常现象", True, (255, 255, 255))
font_43 = font_40.render("当此窗口关闭时即为下载成功", True, (255, 255, 255))
screen.blit(font_41, ((900 - font_41.get_size()[0]) / 2, 20))
screen.blit(font_42, ((900 - font_42.get_size()[0]) / 2, 80))
screen.blit(font_43, ((900 - font_43.get_size()[0]) / 2, 140))
pygame.display.flip()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
try:
    with open(get_resource_path('files/jsons/object_id.json'), 'r', encoding='utf-8') as file_prize:
        dict_id = json.load(file_prize)
    with open(get_resource_path('./files/jsons/button_direction.json'), 'r', encoding='utf-8') as f:
        dict_location = json.load(f)
    with open('./files/jsons/button_direction.json', 'w', encoding='utf-8') as f:
        json.dump(dict_location, f, ensure_ascii=False)
    download_pictures()
except requests.exceptions.ConnectionError:
    screen.fill((0, 0, 0))
    run = True
    font_42 = font_40.render("网络异常", True, (255, 255, 255))
    while run:
        screen.blit(font_42, ((900 - font_42.get_size()[0]) / 2, (200 - font_42.get_size()[1]) / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.flip()
except FileNotFoundError as e:
    print(e)
    run = True
    screen.fill((0, 0, 0))
    font_42 = font_40.render("源文件遭到篡改", True, (255, 255, 255))
    while run:
        screen.blit(font_42, ((900 - font_42.get_size()[0]) / 2, (200 - font_42.get_size()[1]) / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.flip()
