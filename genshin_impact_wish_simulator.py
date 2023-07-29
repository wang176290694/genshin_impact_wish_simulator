import ctypes
import inspect
import json
import os
import random
import sys
import threading
import time

import moviepy.video.io.preview as vp
import numpy as np
import pygame
import pygame.image
from moviepy.decorators import convert_masks_to_RGB, requires_duration
from moviepy.editor import VideoFileClip

pygame.init()


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


with open('./files/jsons/button_direction.json', 'r', encoding='utf-8') as f:
    dict_location = json.load(f)
with open('./files/jsons/object_id.json', 'r', encoding='utf-8') as file_prize:
    dict_id = json.load(file_prize)
element_dict = {'莫娜': '水', '芭芭拉': '水', '行秋': '水', '坎蒂丝': '水', '达达利亚': '水', '珊瑚宫心海': '水',
                '神里绫人': '水', '夜兰': '水', '妮露': '水', '迪卢克': '火', '迪希雅': '火', '安柏': '火',
                '班尼特': '火', '辛焱': '火', '烟绯': '火', '托马': '火', '香菱': '火', '可莉': '火', '胡桃': '火',
                '宵宫': '火', '林尼': '火', '七七': '冰', '凯亚': '冰', '重云': '冰', '迪奥娜': '冰', '罗莎莉亚': '冰',
                '莱依拉': '冰', '米卡': '冰', '甘雨': '冰', '优菈': '冰', '神里绫华': '冰', '申鹤': '冰', '刻晴': '雷',
                '丽莎': '雷', '雷泽': '雷', '北斗': '雷', '菲谢尔': '雷', '九条裟罗': '雷', '久岐忍': '雷',
                '多莉': '雷', '雷电将军': '雷', '八重神子': '雷', '赛诺': '雷', '琴': '风', '砂糖': '风', '早柚': '风',
                '珐露珊': '风', '鹿野院平藏': '风', '温迪': '风', '魈': '风', '枫原万叶': '风', '流浪者': '风',
                '琳妮特': '风', '凝光': '岩', '诺艾尔': '岩', '五郎': '岩', '云堇': '岩', '钟离': '岩', '阿贝多': '岩',
                '荒泷一斗': '岩', '提纳里': '草', '柯莱': '草', '卡维': '草', '瑶瑶': '草', '纳西妲': '草',
                '艾尔海森': '草', '白术': '草', '': '草', '天空之刃': '单手剑', '风鹰剑': '单手剑',
                '暗巷闪光': '单手剑', '西福斯的月光': '单手剑', '飞天御剑': '单手剑', '冷刃': '单手剑',
                '黎明神剑': '单手剑', '祭礼剑': '单手剑', '笛剑': '单手剑', '西风剑': '单手剑', '匣里龙吟': '单手剑',
                '斫峰之刃': '单手剑', '磐岩结绿': '单手剑', '苍古自由之誓': '单手剑', '雾切之回光': '单手剑',
                '波乱月白经津': '单手剑', '圣显之钥': '单手剑', '裁叶萃光': '单手剑', '天空之翼': '弓',
                '阿莫斯之弓': '弓', '曚云之月': '弓', '暗巷猎手': '弓', '幽夜华尔兹': '弓', '鸦羽弓': '弓',
                '神射手之誓': '弓', '弹弓': '弓', '弓藏': '弓', '祭礼弓': '弓', '绝弦': '弓', '西风猎弓': '弓',
                '终末嗟叹之诗': '弓', '飞雷之弦振': '弓', '冬极白星': '弓', '若水': '弓', '猎人之径': '弓',
                '天空之傲': '双手剑', '狼的末路': '双手剑', '千岩古剑': '双手剑', '恶王丸': '双手剑',
                '玛海菈的水色': '双手剑', '铁影阔剑': '双手剑', '以理服人': '双手剑', '沐浴龙血的剑': '双手剑',
                '雨裁': '双手剑', '祭礼大剑': '双手剑', '西风大剑': '双手剑', '钟剑': '双手剑', '无工之剑': '双手剑',
                '松籁响起之时': '双手剑', '赤角石溃杵': '双手剑', '苇海信标': '双手剑', '天空之卷': '法器',
                '四风原典': '法器', '暗巷的酒与诗': '法器', '翡玉法球': '法器', '讨龙英杰谭': '法器',
                '魔导绪论': '法器', '昭心': '法器', '祭礼残章': '法器', '流浪乐章': '法器', '西风秘典': '法器',
                '尘世之锁': '法器', '神乐之真意': '法器', '不灭月华': '法器', '千夜浮梦': '法器',
                '图莱杜拉的回忆': '法器', '碧落之珑': '法器', '天空之脊': '长柄武器', '和璞鸢': '长柄武器',
                '千岩长枪': '长柄武器', '断浪长鳍': '长柄武器', '黑缨枪': '长柄武器', '匣里灭辰': '长柄武器',
                '西风长枪': '长柄武器', '贯虹之槊': '长柄武器', '护摩之杖': '长柄武器', '薙草之稻光': '长柄武器',
                '息灾': '长柄武器', '赤沙之杖': '长柄武器'}


class BreakLoop(Exception):
    def __init__(self):
        self.value = 0

    def __str__(self):
        return repr(self.value)


def get_four_star_num():
    num = 0
    for key in dict_id:
        if key[0] == "c" and key[1] == "4":
            num += 1
    return num


def ok_box(screen, text: str, title: str, back_pic: pygame.surface.Surface):
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    surface8 = pygame.surface.Surface((1200, 675)).convert_alpha()
    surface8.fill((0, 0, 0, 120))
    message_box_img = pygame.image.load("./files/image/ok_box.png")
    a_font_title = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 26)
    a_font = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    result = False
    a_title = a_font_title.render(title, True, (80, 84, 95))
    text = text.split("\n")
    for it in range(len(text)):
        surface1 = pygame.surface.Surface((1200, 600)).convert_alpha()
        surface1.fill((0, 0, 0, 0))
        num = 0
        num1 = 0
        for j in text[it].split("*c"):
            num += 1
            if num >= 2:
                num = 0
            if num == 0:
                surface2 = a_font.render(j.split("*")[-1], True,
                                         (int(j.split("*")[0]), int(j.split("*")[1]), int(j.split("*")[2])))
                surface1.blit(surface2, (num1, 0))
            else:
                surface2 = a_font.render(j, True, (80, 84, 95))
                surface1.blit(surface2, (num1, 0))
            num1 += surface2.get_size()[0]
        surface6 = pygame.surface.Surface(
            (num1, a_font.render(text[it], True, (80, 84, 95)).get_size()[1])).convert_alpha()
        surface6.fill((0, 0, 0, 0))
        text[it] = surface6
        surface6.blit(surface1, (0, 0))
    run = True
    while run:
        screen.blit(back_pic, (0, 0))
        screen.blit(surface8, (0, 0))
        screen.blit(message_box_img,
                    ((1200 - message_box_img.get_size()[0]) / 2, (675 - message_box_img.get_size()[1]) / 2))
        for it in range(len(text)):
            screen.blit(text[it], ((1200 - text[it].get_size()[0]) / 2, 195 + (260 - 23 * len(text)) / 2 + 23 * it))
        screen.blit(a_title, (272 + (656 - a_title.get_size()[0]) / 2, 153))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 612 < mx < 877 and 471 < my < 516:
                    run = False
                    result = True
                    m1.play()
                if 322 < mx < 647 and 471 < my < 516:
                    run = False
                    m1.play()
                if 271 < mx < 929 and 128 < my < 548:
                    pass
                else:
                    run = False
                    m1.play()
        pygame.display.flip()
    return result


def message_box(screen, text: str, title: str, back_pic: pygame.surface.Surface, type1=1):
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    surface8 = pygame.surface.Surface((1200, 675)).convert_alpha()
    surface8.fill((0, 0, 0, 120))
    message_box_img = pygame.image.load("./files/image/message_box.png")
    a_font_title = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 26)
    a_font = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    a_title = a_font_title.render(title, True, (80, 84, 95))
    text = text.split("\n")
    for i in range(len(text)):
        surface1 = pygame.surface.Surface((1200, 600)).convert_alpha()
        surface1.fill((0, 0, 0, 0))
        num = 0
        num1 = 0
        for j in text[i].split("*c"):
            num += 1
            if num >= 2:
                num = 0
            if num == 0:
                surface2 = a_font.render(j.split("*")[-1], True,
                                         (int(j.split("*")[0]), int(j.split("*")[1]), int(j.split("*")[2])))
                surface1.blit(surface2, (num1, 0))
            else:
                surface2 = a_font.render(j, True, (80, 84, 95))
                surface1.blit(surface2, (num1, 0))
            num1 += surface2.get_size()[0]
        surface6 = pygame.surface.Surface(
            (num1, a_font.render(text[i], True, (80, 84, 95)).get_size()[1])).convert_alpha()
        surface6.fill((0, 0, 0, 0))
        text[i] = surface6
        surface6.blit(surface1, (0, 0))
    run = True
    while run:
        screen.blit(back_pic, (0, 0))
        screen.blit(surface8, (0, 0))
        if type1 == 1:
            screen.blit(message_box_img,
                        ((1200 - message_box_img.get_size()[0]) / 2, (675 - message_box_img.get_size()[1]) / 2))
            for i in range(len(text)):
                screen.blit(text[i],
                            ((1200 - text[i].get_size()[0]) / 2, 195 + (260 - 23 * len(text)) / 2 + 23 * i))
            screen.blit(a_title, (272 + (656 - a_title.get_size()[0]) / 2, 153))
        else:
            screen.blit(message_box_img,
                        ((960 - message_box_img.get_size()[0]) / 2, (540 - message_box_img.get_size()[1]) / 2))
            for i in range(len(text)):
                screen.blit(text[i], ((960 - text[i].get_size()[0]) / 2, 128 + (260 - 23 * len(text)) / 2 + 23 * i))
            screen.blit(a_title, (152 + (656 - a_title.get_size()[0]) / 2, 86))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if type1 == 1 and 322 < mx < 877 and 471 < my < 516:
                    run = False
                    m1.play()
                if type1 != 1 and 202 < mx < 757 and 414 < my < 449:
                    run = False
                    m1.play()
                if 271 < mx < 929 and 128 < my < 548:
                    pass
                else:
                    run = False
                    m1.play()
        pygame.display.flip()


def number_input(background: pygame.surface.Surface, screen: pygame.surface.Surface, max_num: int, title: str,
                 text_original: int):
    pygame.init()
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    a_font_math = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 30)
    a_font_title = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 26)
    a_title = a_font_title.render(title, True, (205, 183, 162))
    run = True
    if text_original == 0:
        text = ""
    else:
        text = str(text_original)
    surface_input = a_font_math.render(str(text), True, (0, 0, 0))
    surface_black = pygame.surface.Surface((1200, 675)).convert_alpha()
    surface_black.fill((0, 0, 0, 120))
    img_input = pygame.image.load("./files/image/input.png")
    mouse_bi = pygame.surface.Surface((3, 25))
    mouse_bi.fill((0, 0, 0))
    num_input = 0
    while run:
        num_input += 1
        if num_input >= 70:
            num_input = 0
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(surface_black, (0, 0))
        screen.blit(img_input, ((1200 - img_input.get_size()[0]) / 2, (675 - img_input.get_size()[1]) / 2))
        screen.blit(surface_input,
                    ((1200 - surface_input.get_size()[0]) / 2, 300))
        screen.blit(a_title, (272 + (656 - a_title.get_size()[0]) / 2, 153))
        if num_input >= 35:
            screen.blit(mouse_bi, (
                (1200 - surface_input.get_size()[0]) / 2 + 5 + surface_input.get_size()[0], 305))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if len(text) >= max_num:
                    pass
                else:
                    if event.key == pygame.K_1:
                        text = f'{text}1'
                    if event.key == pygame.K_2:
                        text = f'{text}2'
                    if event.key == pygame.K_3:
                        text = f'{text}3'
                    if event.key == pygame.K_4:
                        text = f'{text}4'
                    if event.key == pygame.K_5:
                        text = f'{text}5'
                    if event.key == pygame.K_6:
                        text = f'{text}6'
                    if event.key == pygame.K_7:
                        text = f'{text}7'
                    if event.key == pygame.K_8:
                        text = f'{text}8'
                    if event.key == pygame.K_9:
                        text = f'{text}9'
                    if event.key == pygame.K_0:
                        text = f'{text}0'
                if event.key == pygame.K_BACKSPACE:
                    text = text[0:len(text) - 1]
                surface_input = a_font_math.render(str(text), True, (0, 0, 0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx1, my1 = pygame.mouse.get_pos()
                if 612 < mx1 < 877 and 471 < my1 < 516:
                    run = False
                    m1.play()
                if 322 < mx1 < 647 and 471 < my1 < 516:
                    run = False
                    text = -1
                    m1.play()
                if 830 < mx1 < 928 and 128 < my1 < 228:
                    run = False
                    text = -1
                    m1.play()
                if 272 < mx1 < 928 and 128 < my1 < 546:
                    pass
                else:
                    run = False
                    text = -1
                    m1.play()
        pygame.display.flip()
    if text == "":
        text = 0
    else:
        text = int(text)
    return text


def scroll_box(screen, title: str, back_pic: pygame.surface.Surface, object_img: pygame.surface.Surface,
               object_name: str, max1: int, buy_img: pygame.surface.Surface, buy_num: int):
    color_surface = pygame.surface.Surface((1, 8))
    color_surface.fill((116, 115, 131))
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    m2 = pygame.mixer.Sound('files/music/scroll.mp3')
    m3 = pygame.mixer.Sound('files/music/get_sth.mp3')
    object_img = pygame.transform.scale(object_img,
                                        (object_img.get_size()[0] * (75 / object_img.get_size()[1]), 75))
    scroll_direction = 447
    scroll_png = pygame.transform.scale(pygame.image.load("./files/image/scroll.png"), (34, 34))
    scroll_back = pygame.transform.scale(pygame.image.load("./files/image/scroll_back.png"), (576, 367))
    black = pygame.surface.Surface((1200, 675)).convert_alpha()
    black.fill((0, 0, 0, 120))
    left = 447
    right = 727
    run = True
    move = False
    font1 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 35)
    font2 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 15)
    font3 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    title = font3.render(title, True, (55, 55, 55))
    now_num = font1.render("1", True, (55, 55, 55))
    now_num1 = 1
    max_num = font2.render(str(max1), True, (55, 55, 55))
    return1 = -1
    buy_surface = pygame.surface.Surface((95, 18)).convert_alpha()
    buy_surface.fill((0, 0, 0, 0))
    buy_surface.blit(pygame.transform.scale(buy_img, (17, 17)), (1, 1))
    buy_surface.blit(font2.render(str(buy_num), True, (255, 255, 255)), (23, 1))
    object_name2 = font3.render(object_name, True, (255, 255, 255))
    back1 = pygame.surface.Surface((576, 367)).convert_alpha()
    back1.blit(scroll_back, (0, 0))
    back1.blit(color_surface, (151, 235))
    back1.blit(object_img, (90, 80))
    back1.blit(now_num, ((576 - now_num.get_size()[0]) / 2, 192))
    back1.blit(max_num, (765, 385))
    back1.blit(buy_surface, (392, 81))
    back1.blit(object_name2, (180, 77))
    back1.blit(scroll_png, (scroll_direction - 312, 222))
    back1.blit(title, ((576 - title.get_size()[0]) / 2, 12 + (51 - title.get_size()[1]) / 2))
    for i in range(1, 11):
        screen.fill((0, 0, 0))
        black.fill((0, 0, 0, 12 * i))
        back1.set_alpha(25 * i)
        screen.fill((0, 0, 0))
        screen.blit(back_pic, (0, 0))
        screen.blit(black, (0, 0))
        screen.blit(back1, (312, 154))
        pygame.display.flip()
    while run:
        screen.blit(back_pic, (0, 0))
        screen.blit(black, (0, 0))
        screen.blit(scroll_back, ((1200 - scroll_back.get_size()[0]) / 2, (675 - scroll_back.get_size()[1]) / 2))
        screen.blit(color_surface,
                    ((1200 - scroll_back.get_size()[0]) / 2 + 151, (675 - scroll_back.get_size()[1]) / 2 + 235))
        screen.blit(object_img, ((1200 - scroll_back.get_size()[0]) / 2 + 90, 234))
        screen.blit(now_num, ((1200 - now_num.get_size()[0]) / 2, (675 - scroll_back.get_size()[1]) / 2 + 192))
        screen.blit(max_num, (765, 385))
        screen.blit(buy_surface,
                    ((1200 - scroll_back.get_size()[0]) / 2 + 392, (675 - scroll_back.get_size()[1]) / 2 + 81))
        screen.blit(object_name2,
                    ((1200 - scroll_back.get_size()[0]) / 2 + 180, (675 - scroll_back.get_size()[1]) / 2 + 77))
        screen.blit(scroll_png, (scroll_direction, 376))
        screen.blit(title, (
            (1200 - title.get_size()[0]) / 2,
            (675 - scroll_back.get_size()[1]) / 2 + 12 + (51 - title.get_size()[1]) / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 422 < mx < 772 and 354 < my < 424:
                    move = True
                if 375 < mx < 405 and 378 < my < 408 and now_num1 > 1:
                    now_num1 -= 1
                    now_num = font1.render(str(now_num1), True, (55, 55, 55))
                    scroll_direction = left + ((right - left) / (max1 - 1)) * (now_num1 - 1)
                    m1.play()
                if 802 < mx < 837 and 378 < my < 408 and now_num1 < max1:
                    now_num1 += 1
                    now_num = font1.render(str(now_num1), True, (55, 55, 55))
                    scroll_direction = left + ((right - left) / (max1 - 1)) * (now_num1 - 1)
                    m1.play()
                if 312 < mx < 600 and 444 < my < 521:
                    run = False
                    m1.play()
                if 600 < mx < 888 and 444 < my < 521:
                    return1 = now_num1
                    run = False
                    m1.play()
                if 312 < mx < 888 and 154 < my < 521:
                    pass
                else:
                    run = False
                    m1.play()
            if event.type == pygame.MOUSEBUTTONUP and move:
                move = False
        if move:
            scroll_direction = pygame.mouse.get_pos()[0] - 15
            if scroll_direction > right:
                scroll_direction = right
                now_num = font1.render(str(max1), True, (55, 55, 55))
                now_num1 = max1
            elif scroll_direction < left:
                scroll_direction = left
                now_num = font1.render(str(1), True, (55, 55, 55))
                now_num1 = 1
            for i in range(max1):
                if pygame.mouse.get_pos()[0] - 15 < left + (i + 1) * ((right - left) / max1):
                    now_num = font1.render(str(i + 1), True, (55, 55, 55))
                    if now_num1 != i + 1:
                        m2.play()
                    now_num1 = i + 1
                    break
        color_surface = pygame.transform.scale(color_surface, (scroll_direction - left + 1, 8))
        pygame.display.flip()
    get_img = pygame.image.load("./files/image/get_sth.png")
    back1.fill((0, 0, 0, 0))
    back1.blit(scroll_back, (0, 0))
    back1.blit(color_surface, (151, 235))
    back1.blit(object_img, (0, 212 + (122 - object_img.get_size()[1]) / 2))
    back1.blit(buy_img, (85, 75))
    back1.blit(now_num, ((576 - now_num.get_size()[0]) / 2, 192))
    back1.blit(max_num, (453, 231))
    back1.blit(scroll_png, (scroll_direction - 312, 222))
    back1 = pygame.surface.Surface((576, 367)).convert_alpha()
    back1.blit(scroll_back, (0, 0))
    back1.blit(object_img, (90, 80))
    back1.blit(now_num, ((576 - now_num.get_size()[0]) / 2, 192))
    back1.blit(max_num, (765, 385))
    back1.blit(buy_surface, (392, 81))
    back1.blit(object_name2, (180, 77))
    back1.blit(scroll_png, (scroll_direction - 312, 222))
    back1.blit(title, ((576 - title.get_size()[0]) / 2, 12 + (51 - title.get_size()[0]) / 2))
    for i in range(1, 11):
        screen.fill((0, 0, 0))
        black.fill((0, 0, 0, 120 - 12 * i))
        screen.fill((0, 0, 0))
        back1.set_alpha(25 * i)
        screen.blit(back_pic, (0, 0))
        screen.blit(black, (0, 0))
        back1.set_alpha(250 - 25 * i)
        screen.blit(back1, (312, 154))
        pygame.display.flip()
    if return1 != -1:
        m3.play()
        surface2 = pygame.surface.Surface((85, 85)).convert_alpha()
        surface2.fill((0, 0, 0, 0))
        surface3 = pygame.transform.scale(object_img, (65, 65))
        surface2.blit(surface3, ((85 - surface3.get_size()[0]) / 2, (85 - surface3.get_size()[1]) / 2))
        surface1 = set_object_surface2(surface2, object_name, return1, 0)
        get_img.blit(surface1, ((1200 - surface1.get_size()[0]) / 2, 270))
        for i in range(1, 6):
            screen.fill((0, 0, 0))
            get_img.set_alpha(44 * i)
            screen.blit(back_pic, (0, 0))
            screen.blit(get_img, (0, 0))
            pygame.display.flip()
        get_img.set_alpha(220)
        run = True
        while run:
            screen.fill((0, 0, 0))
            screen.blit(back_pic, (0, 0))
            screen.blit(get_img, (0, 0))
            screen.blit(surface1, ((1200 - surface1.get_size()[0]) / 2, 270))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m1.play()
                    run = False
            pygame.display.flip()
        for i in range(1, 6):
            screen.fill((0, 0, 0))
            get_img.set_alpha(220 - 44 * i)
            screen.blit(back_pic, (0, 0))
            screen.blit(get_img, (0, 0))
            pygame.display.flip()
    return return1


def breakplay():
    raise BreakLoop


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)


@requires_duration
@convert_masks_to_RGB
def preview(clip, eventa, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000,
            audio_nbytes=2, fullscreen=False):
    skip = False
    if fullscreen:
        flags = pygame.FULLSCREEN
    else:
        flags = 0
    screen = pygame.display.set_mode(clip.size, flags)
    audio = audio and (clip.audio is not None)
    if audio:
        video_flag = threading.Event()
        audio_flag = threading.Event()
        audiothread = threading.Thread(target=clip.audio.preview,
                                       args=(audio_fps, audio_buffersize, audio_nbytes, audio_flag, video_flag))
        audiothread.start()
    img = clip.get_frame(0)
    vp.imdisplay(img, screen)
    if audio:
        video_flag.set()
        audio_flag.wait()
    t0 = time.time()
    font_28 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    surface_blit = font_28.render("跳过", True, (255, 255, 255))
    for t in np.arange(1.0 / fps, clip.duration - .001, 1.0 / fps):
        img = clip.get_frame(t)
        try:
            for event in pygame.event.get():
                eventa(event)
        except BreakLoop:
            _async_raise(audiothread.ident, SystemExit)
            skip = True
            break
        t1 = time.time()
        time.sleep(max(0, t - (t1 - t0)))
        screen.blit(surface_blit, (1140, 15))
        vp.imdisplay(img, screen)
        screen.blit(surface_blit, (1140, 15))
        pygame.display.flip()
    pygame.mixer.quit()
    return skip


def aff(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = pygame.mouse.get_pos()
        if mx > 1120 and my < 60:
            breakplay()


def set_object_surface(name1: str, count1: int, type1: int, black: bool = False, stars: int = 5):
    font_14 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 16)
    pic1 = pygame.image.load(f"./files/image/wish/map/{name1}.png")
    surface1 = pygame.surface.Surface((85, 105))
    surface1.blit(pygame.transform.scale(pic1, (85, 105)), (0, 0))
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
    if black:
        black1 = pygame.surface.Surface((85, 105)).convert_alpha()
        black1.fill((0, 0, 0, 120))
        surface1.blit(black1, (0, 0))
    return surface1


def set_object_surface2(pic1: pygame.surface.Surface, name1: str, count1: int, type1: int, black: bool = False):
    font_14 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 16)
    five_stars = pygame.transform.scale(pygame.image.load(f"./files/image/five_stars.png"), (70, 10))
    background = pygame.transform.scale(pygame.image.load(f"./files/image/five_background.png"), (85, 85))
    corner = pygame.transform.scale(pygame.image.load(f"./files/image/wish/user_want_corner.png"), (85, 41))
    surface1 = pygame.surface.Surface((85, 105))
    surface1.blit(background, (0, 0))
    surface1.blit(pygame.transform.scale(pic1, (85, 85)), (0, 0))
    surface1.blit(corner, (0, 66))
    if type1 == 1:
        text1 = font_14.render(name1, True, (0, 0, 0))
    elif type1 == 2:
        text1 = font_14.render(f"{name1} : {count1}", True, (0, 0, 0))
    else:
        text1 = font_14.render(str(count1), True, (0, 0, 0))
    surface1.blit(text1, ((85 - text1.get_size()[0]) / 2, 85))
    surface1.blit(five_stars, (7, 75))
    if black:
        black1 = pygame.surface.Surface((85, 105)).convert_alpha()
        black1.fill((0, 0, 0, 120))
        surface1.blit(black1, (0, 0))
    return surface1


def rect_get(type1, mouse_x, mouse_y):
    tuple1 = dict_location[type1]
    return (mouse_x > tuple1[0]) and (mouse_x < tuple1[0] + tuple1[2]) and (mouse_y > tuple1[1]) and (
            mouse_y < tuple1[1] + tuple1[3])


def dict_init():
    dict_main = {
        "yuan_shi": 0,
        "jiu_chan_ball": 100,
        "meet_ball": 100,
        "user_want": 0,
        "user_want_num": 0,
        "user_like": [],
        "xing_chen": 0,
        "xing_hui": 0,
        "character_wish_total": 0,
        "weapon_wish_total": 0,
        "normal_wish_total": 0,
        "starter_wish_total": 0,
        "five_star_character_next": 0,
        "five_star_weapon_next": 0,
        "five_star_normal_next": 0,
        "five_star_starter_next": 0,
        "four_star_character_next": 0,
        "four_star_weapon_next": 0,
        "four_star_starter_next": 0,
        "four_star_normal_next": 0,
        "crooked_character": 0,
        "crooked_weapon": 0,
        "five_star_character_total": 0,
        "five_star_weapon_total": 0,
        "five_star_normal_total": 0,
        "five_star_starter_total": 0,
        "four_star_character_total": 0,
        "four_star_weapon_total": 0,
        "four_star_normal_total": 0,
        "four_star_starter_total": 0,
        "five_star_askew_character": 0,
        "five_star_askew_weapon": 0,
        "four_star_askew_character": 0,
        "four_star_askew_weapon": 0,
        "five_star_character_last": 0,
        "five_star_weapon_last": 0,
        "five_star_normal_last": 0,
        "five_star_starter_last": 0
    }
    return dict_main


def dict_init2():
    dict_main = {}
    for keys in dict_id:
        dict_main[keys] = 0
    return dict_main


def chen_hui(xing_chen, dict_data1, font_20):
    xing_hui_num = font_20.render(str(dict_data1["xing_hui"]), True, (255, 255, 255))
    xing_chen_num = font_20.render(str(dict_data1["xing_chen"]), True, (255, 255, 255))
    chen_hui_surface1 = pygame.surface.Surface(
        (30 + xing_hui_num.get_size()[0] + xing_chen_num.get_size()[0], 20)).convert_alpha()
    chen_hui_surface1.fill((0, 0, 0, 0))
    chen_hui_surface1.blit(xing_hui_num, (0, 0))
    chen_hui_surface1.blit(xing_chen, (xing_hui_num.get_size()[0] + 5, 0))
    chen_hui_surface1.blit(xing_chen_num, (xing_hui_num.get_size()[0] + 30, 0))
    return chen_hui_surface1


def get_background(dict_data, pic_list):
    back_png = pic_list[0]
    wish_pic = pic_list[1]
    back_png2 = pic_list[2]
    wish_img = pic_list[3]
    pic_wish_now = pic_list[4]
    wish_stage = pic_list[5]
    user_want_pic = pic_list[6]
    user_want_font = pic_list[7]
    font_text_wish1 = pic_list[8]
    font_text_wish2 = pic_list[9]
    font_text_wish3 = pic_list[10]
    font_text_wish4 = pic_list[11]
    chen_hui_surface = pic_list[12]
    yuan_shi_surface = pic_list[13]
    jiu_chan_ball_surface = pic_list[14]
    meet_ball_surface = pic_list[15]
    last_img1 = pic_list[16]
    last_img2 = pic_list[17]
    surface_wish_list = pic_list[18]
    screen = pygame.surface.Surface((1200, 675))
    screen.fill((0, 0, 0))
    screen.blit(back_png, (0, 0))
    screen.blit(wish_pic, (120, (630 - wish_pic.get_size()[1]) / 2))
    screen.blit(back_png2, (0, 0))
    screen.blit(wish_img, (370, 21))
    screen.blit(wish_img, (490, 21))
    screen.blit(wish_img, (610, 21))
    screen.blit(wish_img, (730, 21))
    if wish_stage == 4:
        screen.blit(pic_wish_now, (370, 21))
    else:
        screen.blit(pic_wish_now, (370 + 120 * wish_stage, 21))
    if wish_stage == 2:
        screen.blit(user_want_pic, (40, 480))
        if dict_data["user_want"] == 0:
            user_want_text = "神铸定轨"
        elif dict_data["user_want"] != 0 and dict_data["user_want_num"] == 0:
            user_want_text = "0/2"
        elif dict_data["user_want"] != 0 and dict_data["user_want_num"] == 1:
            user_want_text = "1/2"
        else:
            print(dict_data["user_want"], dict_data["user_want_num"])
            user_want_text = "2/2"
        user_want_font1 = user_want_font.render(user_want_text, True, (0, 0, 0))
        screen.blit(user_want_font1, (
            40 + (125 - user_want_font1.get_size()[0]) / 2, 548 + (32 - user_want_font1.get_size()[1]) / 2))
    screen.blit(font_text_wish1, (370 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                  21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
    screen.blit(font_text_wish2, (490 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                  21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
    screen.blit(font_text_wish3, (610 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                  21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
    screen.blit(font_text_wish4, (730 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                  21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
    screen.blit(chen_hui_surface, (65, 596))
    screen.blit(yuan_shi_surface, (923, 22))
    screen.blit(last_img1, (1000, 75))
    screen.blit(last_img2, (1000, 125))
    if wish_stage == 1 or wish_stage == 2:
        screen.blit(jiu_chan_ball_surface, (1020, 20))
    else:
        screen.blit(meet_ball_surface, (1020, 20))
    screen.blit(surface_wish_list[0], (565, 630))
    screen.blit(surface_wish_list[1], (802, 630))
    screen.blit(surface_wish_list[2], (1031, 630))
    return screen


def load_dict(dict_data, uid):
    with open(f'./files/jsons/data{uid}.json', 'w', encoding='utf-8') as file_data:
        file_data.write(json.dumps(dict_data, ensure_ascii=False))


def set_ball_surface(font_15, dict_data, ball_pic, ball: str):
    ball_surface = pygame.surface.Surface((80, 22)).convert_alpha()
    ball_surface.fill((0, 0, 0, 0))
    ball_surface.blit(pygame.transform.scale(ball_pic, (20, 20)), (0, 0))
    ball_surface.blit(font_15.render(str(dict_data[ball]), True, (255, 255, 255)), (25, 2))
    return ball_surface


def set_last_surface(dict_data: dict, text: str, type1: int):
    height = 40
    width = 130
    last_surface = pygame.surface.Surface((width, height))
    last_surface2 = pygame.surface.Surface((width - 4, height - 4))
    last_surface2.fill((255, 198, 7))
    last_surface.blit(last_surface2, (2, 2))
    font20 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    if type1 == 1:
        font1 = font20.render(f"当前已垫：{dict_data[text]}", True, (0, 0, 0))
    else:
        font1 = font20.render(f"上次出金：{dict_data[text]}", True, (0, 0, 0))
    last_surface.blit(font1, ((width - font1.get_size()[0]) / 2, (height - font1.get_size()[1]) / 2))
    return last_surface


def set_pic(dict1: dict, name: str, element_dict1: dict, type_pic: int = 1):
    def set_u(dict2: dict, name1):
        wish_result_surface1 = pygame.transform.scale(
            pygame.image.load(f"./files/image/wish/one_wish/{dict2[name1]}.png"),
            (613, 714))
        wish_result_surface10 = set_border((651, 650))
        wish_result_surface10.blit(wish_result_surface1, (19, 12))
        return wish_result_surface10

    def set_w(dict2: dict, name1):
        surface_w1 = pygame.surface.Surface((540, 540)).convert_alpha()
        surface_w1.fill((0, 0, 0, 0))
        if name1[1] == "0" or name1[1] == "5":
            fs_surface = pygame.transform.scale(pygame.image.load("./files/image/five_background.png"), (420, 420))
        elif name1[1] == "3":
            fs_surface = pygame.transform.scale(pygame.image.load("./files/image/three_background.png"), (420, 420))
        else:
            fs_surface = pygame.transform.scale(pygame.image.load("./files/image/four_background.png"), (420, 420))
        weapon_img_w = pygame.transform.scale(pygame.image.load(f"./files/image/map/{dict2[name1]}.png"), (380, 380))
        surface_w1.blit(fs_surface, ((540 - fs_surface.get_size()[0]) / 2, (540 - fs_surface.get_size()[1]) / 2))
        surface_w1.blit(weapon_img_w, ((540 - weapon_img_w.get_size()[0]) / 2, (540 - weapon_img_w.get_size()[1]) / 2))
        pygame.draw.circle(surface_w1, (100, 61, 117), (270, 270), 270, 60)
        surface_w1.blit(pygame.transform.scale(pygame.image.load("./files/image/wish/weapon_rect.png"), (540, 540)),
                        (0, 0))
        pygame.draw.circle(surface_w1, (255, 255, 255), (270, 270), 220, 10)
        pygame.draw.lines(surface_w1, (255, 220, 174), True, [(0, 270), (270, 0), (540, 270), (270, 540)], 10)
        pygame.draw.circle(surface_w1, (248, 243, 239), (270, 270), 350, 80)
        surface_w1 = pygame.transform.scale(surface_w1, (400, 400))
        wish_result_surface10 = set_border((500, 500))
        wish_result_surface10.blit(surface_w1,
                                   ((500 - surface_w1.get_size()[0]) / 2, (500 - surface_w1.get_size()[1]) / 2))
        return wish_result_surface10

    wish_result_surface_main = pygame.surface.Surface((1200, 675))
    wish_result_surface_main.blit(
        pygame.transform.scale(pygame.image.load(f"./files/image/wish/wish_back.png"), (1200, 675)), (0, 0))
    if type_pic == 1:
        wish_result_surface_main.blit(set_u(dict1, name), (480, 8))
    else:
        wish_result_surface_main.blit(set_w(dict1, name), (500, 87))
    if name[1] == "0" or name[1] == "5":
        wish_result_surface2 = pygame.image.load(f"./files/image/five_stars.png")
    elif name[1] == "3":
        wish_result_surface2 = pygame.image.load(f"./files/image/three_stars.png")
    else:
        wish_result_surface2 = pygame.image.load(f"./files/image/four_stars.png")
    try:
        wish_result_surface3 = pygame.transform.scale(
            pygame.image.load(f"./files/image/wish/element/{element_dict1[dict1[name]]}.png"), (100, 100))
    except KeyError:
        wish_result_surface3 = pygame.image.load("./files/image/wish/element/question.png")
    wish_result_surface_main.blit(wish_result_surface2, (157, 424))
    wish_result_surface_main.blit(wish_result_surface3, (50, 356))
    font_27 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 50)
    wish_result_font1 = font_27.render(dict1[name], True, (255, 255, 255))
    wish_result_surface_main.blit(wish_result_font1, (157, 364))
    font_28 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    wish_result_surface_main.blit(font_28.render("跳过", True, (255, 255, 255)), (1140, 15))
    return wish_result_surface_main


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


def set_surface_wish_n(type1: int, user_like_dict: dict, have_data: dict, five_star_list: list, four_star_list: list):
    surface_wish_n_result = pygame.surface.Surface((1200, 675))
    surface_wish_n_result.blit(
        pygame.transform.scale(pygame.image.load(f"./files/image/wish/wish_back.png"), (1200, 675)),
        (0, 0))
    result_list = []
    if type1 == 1 or type1 == 3 or type1 == 4:
        for results in range(7):
            surface_wish_n_result.blit(set_object_surface(dict_id[f"c00{results + 1}"], 0, 5),
                                       (100 + 115 * results, 60))
            result_list.append([f"c00{results + 1}", have_data[f"c00{results + 1}"]])
    else:
        for results in range(9):
            surface_wish_n_result.blit(set_object_surface(dict_id[f"w00{results + 1}"], 0, 5),
                                       (100 + 115 * results, 60))
            result_list.append([f"w00{results + 1}", have_data[f"w00{results + 1}"]])
        for results in range(1):
            surface_wish_n_result.blit(set_object_surface(dict_id[f"w0{results + 10}"], 0, 5),
                                       (100 + 115 * results, 190))
            result_list.append([f"w0{results + 10}", have_data[f"w0{results + 10}"]])
    if type1 == 4:
        num = 0
        for results in user_like_dict["user_like"]:
            if num <= 1:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num + 7), 60))
            else:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num - 2), 190))
            result_list.append([results, have_data[results]])
            num += 1
    if type1 == 1:
        surface_wish_n_result.blit(set_object_surface(dict_id[five_star_list[0]], 0, 5), (905, 60))
        result_list.append([five_star_list[0], have_data[five_star_list[0]]])
        for results in range(3):
            if results == 0:
                surface_wish_n_result.blit(set_object_surface(dict_id[four_star_list[results]], 0, 5, stars=4),
                                           (100 + 115 * (results + 8), 60))
            else:
                surface_wish_n_result.blit(set_object_surface(dict_id[four_star_list[results]], 0, 5, stars=4),
                                           (-15 + 115 * results, 190))
            result_list.append([four_star_list[results], have_data[four_star_list[results]]])
        num = 0
        for results in user_like_dict["user_like"]:
            surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4), (330 + 115 * num, 190))
            num += 1
            result_list.append([results, have_data[results]])
    if type1 == 2:
        surface_wish_n_result.blit(set_object_surface(dict_id[five_star_list[0]], 0, 5), (215, 190))
        surface_wish_n_result.blit(set_object_surface(dict_id[five_star_list[1]], 0, 5), (330, 190))
        result_list.append([five_star_list[0], have_data[five_star_list[0]]])
        result_list.append([five_star_list[1], have_data[five_star_list[1]]])
        for results in range(5):
            surface_wish_n_result.blit(set_object_surface(dict_id[four_star_list[results]], 0, 5, stars=4),
                                       (445 + 115 * results, 190))
            result_list.append([four_star_list[results], have_data[four_star_list[results]]])
        num = 0
        for results in user_like_dict["user_like"]:
            if num == 0:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num + 8), 190))
            else:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num - 1), 320))
            num += 1
            result_list.append([results, have_data[results]])
    if type1 == 3:
        for results in range(2):
            surface_wish_n_result.blit(set_object_surface(dict_id[f"w00{results + 1}"], 0, 5),
                                       (100 + 115 * (results + 7), 60))
            result_list.append([f"w00{results + 1}", have_data[f"w00{results + 1}"]])
        for results in range(8):
            if results < 7:
                surface_wish_n_result.blit(set_object_surface(dict_id[f"w00{results + 3}"], 0, 5),
                                           (100 + 115 * results, 190))
                result_list.append([f"w00{results + 3}", have_data[f"w00{results + 3}"]])
            else:
                surface_wish_n_result.blit(set_object_surface(dict_id[f"w0{results + 3}"], 0, 5),
                                           (100 + 115 * results, 190))
                result_list.append([f"w0{results + 3}", have_data[f"w0{results + 3}"]])
        num = 0
        for results in user_like_dict["user_like"]:
            if num == 0:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num + 8), 190))
            else:
                surface_wish_n_result.blit(set_object_surface(dict_id[results], 0, 5, stars=4),
                                           (100 + 115 * (num - 1), 320))
            result_list.append([results, have_data[results]])
            num += 1
    return surface_wish_n_result, result_list


def set_surface_wish(type1):
    font_15 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 15)
    font_wish_n = font_15.render("x n", True, (154, 149, 141))
    surface_wish1 = pygame.surface.Surface((80, 22)).convert_alpha()
    surface_wish1.fill((0, 0, 0, 0))
    surface1 = pygame.image.load('./files/image/wish/meet_ball2.png')
    surface2 = pygame.image.load('./files/image/wish/jiu_chan_ball2.png')
    if type1 == 1:
        surface_wish1.blit(surface1, (0, 3))
    else:
        surface_wish1.blit(surface2, (0, 3))
    surface_wish1.blit(font_wish_n, (21, 2))
    font_wish_n = font_15.render("x 1", True, (154, 149, 141))
    surface_wish2 = pygame.surface.Surface((80, 22)).convert_alpha()
    surface_wish2.fill((0, 0, 0, 0))
    if type1 == 1:
        surface_wish2.blit(surface1, (0, 3))
    else:
        surface_wish2.blit(surface2, (0, 3))
    surface_wish2.blit(font_wish_n, (21, 2))
    font_wish_n = font_15.render("x 10", True, (154, 149, 141))
    surface_wish3 = pygame.surface.Surface((80, 22)).convert_alpha()
    surface_wish3.fill((0, 0, 0, 0))
    if type1 == 1:
        surface_wish3.blit(surface1, (0, 3))
    else:
        surface_wish3.blit(surface2, (0, 3))
    surface_wish3.blit(font_wish_n, (21, 2))
    surface_wish_list = [surface_wish1, surface_wish2, surface_wish3]
    return surface_wish_list


def choose_four_star(screen, dict_data):
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    m5 = pygame.mixer.Sound('files/music/close_win.mp3')
    font_145 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 25)
    font_35 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 35)
    text_s = font_35.render("提示：设置完成后退出时会自动保存", True, (0, 0, 0))
    four_star_list = []
    four_star_surface_list = []
    four_star_list2 = []
    four_star_list3 = []
    direction_list = []
    bg_s = pygame.transform.scale(pygame.image.load("./files/image/wish/background.png"),
                                  (1200, 675))
    for i in dict_data["user_like"]:
        four_star_list3.append(i)
    num = 0
    for key in dict_id:
        screen.blit(bg_s, (0, 0))
        screen.blit(text_s,
                    ((1200 - text_s.get_size()[0]) / 2, (675 - text_s.get_size()[1]) / 2))
        for event_s in pygame.event.get():
            if event_s.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.flip()
        if key[1] == "2" or key[1] == "4":
            four_star_list.append(set_object_surface(dict_id[key], 0, 1, stars=4))
            four_star_list2.append(key)
            if key in four_star_list3:
                direction_list.append(num)
            num += 1
    choose = pygame.image.load("./files/image/wish/user_want_choose.png")
    weapon_surface1 = pygame.surface.Surface((1030, 675)).convert_alpha()
    weapon_surface1.fill((0, 0, 0, 0))
    num_s1 = 0
    num_s2 = 0
    num_s3 = 0
    for i in four_star_list:
        weapon_surface1.blit(i, (0 + num_s1 * 105, 0 + num_s2 * 125))
        num_s1 += 1
        num_s3 += 1
        if num_s1 >= 10:
            num_s1 = 0
            num_s2 += 1
        if num_s3 >= 50:
            num_s1 = 0
            num_s2 = 0
            num_s3 = 0
            four_star_surface_list.append(weapon_surface1)
            weapon_surface1 = pygame.surface.Surface((1030, 675)).convert_alpha()
            weapon_surface1.fill((0, 0, 0, 0))
    if num_s3 != 0:
        four_star_surface_list.append(weapon_surface1)
    run = True
    stage = 1
    closing_button = pygame.image.load("./files/image/closing_button.png")
    surface_now = four_star_surface_list[0]
    surface_main = pygame.surface.Surface((1200, 675))
    while run:
        surface_main.fill((0, 0, 0))
        surface_main.blit(bg_s, (0, 0))
        surface_main.blit(closing_button, (1145, 15))
        surface_main.blit(surface_now, ((1200 - surface_now.get_size()[0]) / 2, 10))
        for i in direction_list:
            if (stage - 1) * 50 <= i < stage * 50:
                i = i % 50
                surface_main.blit(choose, ((1200 - surface_now.get_size()[0]) / 2 + i % 10 * 105, 10 + i // 10 * 125))
        surface_main.blit(font_145.render("上一页      下一页", True, (255, 255, 255)), (500, 640))
        screen.blit(surface_main, (0, 0))
        for event_s in pygame.event.get():
            if event_s.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event_s.type == pygame.MOUSEBUTTONDOWN:
                mxs, mys = pygame.mouse.get_pos()
                if rect_get("close", mxs, mys):
                    run = False
                    m5.play()
                elif mys > 640 and 600 < mxs < 900 and stage < len(four_star_surface_list):
                    stage += 1
                    surface_now = four_star_surface_list[stage - 1]
                    m1.play()
                elif mys > 640 and 300 < mxs < 600 and stage > 1:
                    stage -= 1
                    surface_now = four_star_surface_list[stage - 1]
                    m1.play()
                else:
                    for i in range(10):
                        for j in range(5):
                            if i * 105 + (1200 - surface_now.get_size()[0]) / 2 < mxs < i * 105 + 90 + (1200 - surface_now.get_size()[0]) / 2 and j * 125 + 10 < mys < j * 125 + 120 and len(four_star_list2) > (stage - 1) * 50 + j * 10 + i:
                                m1.play()
                                if four_star_list2[(stage - 1) * 50 + j * 10 + i] not in four_star_list3:
                                    if len(four_star_list3) >= 5:
                                        message_box(screen, "至多选择五个四星", "至多选择五个四星", surface_main)
                                    else:
                                        four_star_list3.append(four_star_list2[(stage - 1) * 50 + j * 10 + i])
                                        direction_list.append((stage - 1) * 50 + j * 10 + i)
                                else:
                                    four_star_list3.remove(four_star_list2[(stage - 1) * 50 + j * 10 + i])
                                    direction_list.remove((stage - 1) * 50 + j * 10 + i)
        pygame.display.flip()
    dict_data["user_like"] = four_star_list3
    return dict_data


def wish(uid):
    pygame.init()
    pygame.mixer.init()
    font_35 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 35)
    screen = pygame.display.set_mode((1200, 675))
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    m2 = pygame.mixer.Sound('files/music/wish_button.mp3')
    m3 = pygame.mixer.Sound('files/music/change_wish.mp3')
    m4 = pygame.mixer.Sound('files/music/get_wish.mp3')
    m5 = pygame.mixer.Sound('files/music/close_win.mp3')
    m6 = pygame.mixer.Sound('files/music/open.mp3')
    get_four_star_num1 = get_four_star_num()
    surf = pygame.Surface((35, 35), pygame.SRCALPHA, 32).convert_alpha()
    im = pygame.image.load('files/image/mouse.png')
    surf.blit(im, (8, 8))
    color = pygame.cursors.Cursor((0, 0), surf)
    pygame.mouse.set_cursor(color)
    bg_s = pygame.transform.scale(pygame.image.load("./files/image/wish/background.png"),
                                  (1200, 675))
    text_s = font_35.render("请稍候……", True, (0, 0, 0))
    screen.blit(bg_s, (0, 0))
    screen.blit(text_s,
                ((1200 - text_s.get_size()[0]) / 2, (675 - text_s.get_size()[1]) / 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
    clip1 = VideoFileClip('files/video/10j.mp4')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
    clip2 = VideoFileClip('files/video/1j.mp4')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
    clip3 = VideoFileClip('files/video/10z.mp4')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
    clip4 = VideoFileClip('files/video/1z.mp4')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.flip()
    clip5 = VideoFileClip('files/video/1l.mp4')
    with open('./files/jsons/wish.json', 'r', encoding='utf-8') as file_wish:
        dict_prize = json.load(file_wish)
    if os.path.isfile(f'./files/jsons/data{uid}.json'):
        with open(f'./files/jsons/data{uid}.json', 'r', encoding='utf-8') as file_data:
            dict_data = json.load(file_data)
    else:
        dict_data = dict_init()
    if os.path.isfile(f'./files/jsons/history_data{uid}.json'):
        with open(f'./files/jsons/history_data{uid}.json', 'r', encoding='utf-8') as file_data:
            history_data = json.load(file_data)
    else:
        history_data = {"character": [], "weapon": [], "normal": [], "starter": []}
    if os.path.isfile(f'./files/jsons/have_data{uid}.json'):
        with open(f'./files/jsons/have_data{uid}.json', 'r', encoding='utf-8') as file_data:
            have_data = json.load(file_data)
    else:
        have_data = dict_init2()
    prize_list = []
    character_list = []
    weapon_list = []
    for keys in dict_prize['character']:
        prize_list.append(f"{keys['id']}:{keys['five'][0]}, {keys['four'][0]}, {keys['four'][1]}, {keys['four'][2]}")
        character_list.append(
            f"{keys['id']}:{keys['five'][0]}, {keys['four'][0]}, {keys['four'][1]}, {keys['four'][2]}")
    for keys in dict_prize['weapon']:
        prize_list.append(
            f"{keys['id']}:{keys['five'][0]}, {keys['five'][1]}, {keys['four'][0]}, {keys['four'][1]}, {keys['four'][2]}, {keys['four'][3]}, {keys['four'][4]}")
        weapon_list.append(
            f"{keys['id']}:{keys['five'][0]}, {keys['five'][1]}, {keys['four'][0]}, {keys['four'][1]}, {keys['four'][2]}, {keys['four'][3]}, {keys['four'][4]}")
    xing_chen = pygame.transform.scale(pygame.image.load("./files/image/wish/dust.png"), (20, 20))
    pic_jiu_chan_ball = pygame.image.load("./files/image/wish/jiu_chan_ball.png")
    pic_meet_ball = pygame.image.load("./files/image/wish/meet_ball.png")
    font_40 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 40)
    font_20 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    font_15 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 15)
    chen_hui_surface = chen_hui(xing_chen, dict_data, font_20)
    yuan_shi_surface = font_15.render(str(dict_data["yuan_shi"]), True, (255, 255, 255))
    jiu_chan_ball_surface = set_ball_surface(font_15, dict_data, pic_jiu_chan_ball, "jiu_chan_ball")
    meet_ball_surface = set_ball_surface(font_15, dict_data, pic_meet_ball, "meet_ball")
    wish_stage = 4
    wish_times = 0
    back_png = pygame.image.load('files/image/wish/background_wish.png')
    back_png = pygame.transform.scale(back_png, (1200, 675))
    back_png2 = pygame.image.load('files/image/wish/background_wish2.png')
    back_png2 = pygame.transform.scale(back_png2, (1200, 675))
    wish_img = pygame.image.load('./files/image/wish/pic_wish.png')
    pic_wish_now = pygame.image.load('./files/image/wish/pic_wish2.png')
    wish_back = pygame.transform.scale(pygame.image.load(f"./files/image/wish/wish_back.png"), (1200, 675))
    setting_pic = pygame.transform.scale(pygame.image.load("./files/image/wish/setting.png"), (1200, 675))
    font_14 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 14)
    user_want_font = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 18)
    font_text_wish1 = font_14.render("新手祈愿", True, (0, 0, 0))
    font_text_wish2 = font_14.render("角色祈愿", True, (0, 0, 0))
    font_text_wish3 = font_14.render("武器祈愿", True, (0, 0, 0))
    font_text_wish4 = font_14.render("常驻祈愿", True, (0, 0, 0))
    user_want_pic0 = pygame.image.load("./files/image/wish/user_want0.png")
    user_want_pic0 = pygame.transform.scale(user_want_pic0, (125, 100))
    user_want_pic1 = pygame.image.load("./files/image/wish/user_want1.png")
    user_want_pic1 = pygame.transform.scale(user_want_pic1, (125, 100))
    user_want_pic2 = pygame.image.load("./files/image/wish/user_want2.png")
    user_want_pic2 = pygame.transform.scale(user_want_pic2, (125, 100))
    user_want_list = [user_want_pic0, user_want_pic1, user_want_pic2]
    ok = font_40.render("请等待祈愿结果...", True, (255, 255, 255))
    ok_button = font_40.render("祈愿结束，点击任意位置关闭", True, (255, 255, 255))
    five_star_list = []
    four_star_list = []
    n_wish_list = []
    n_wish_surface = pygame.surface.Surface((0, 0))
    if dict_data["user_want"] != 0:
        user_want_pic = user_want_list[dict_data["user_want_num"]]
    else:
        user_want_pic = user_want_list[0]
    wish_pic = pygame.image.load("./files/image/wish/starter_wish.jpg")
    last_img1 = set_last_surface(dict_data, "five_star_starter_next", 1)
    last_img2 = set_last_surface(dict_data, "five_star_starter_last", 2)
    surface_wish_list = set_surface_wish(1)
    first_cycle = True
    main_cycle = True
    while first_cycle:
        back_local = False
        while main_cycle:
            screen.fill((0, 0, 0))
            screen.blit(back_png, (0, 0))
            screen.blit(wish_pic, (120, (630 - wish_pic.get_size()[1]) / 2))
            screen.blit(back_png2, (0, 0))
            screen.blit(wish_img, (370, 21))
            screen.blit(wish_img, (490, 21))
            screen.blit(wish_img, (610, 21))
            screen.blit(wish_img, (730, 21))
            if wish_stage == 4:
                screen.blit(pic_wish_now, (370, 21))
            else:
                screen.blit(pic_wish_now, (370 + 120 * wish_stage, 21))
            if wish_stage == 2:
                screen.blit(user_want_pic, (40, 480))
                if dict_data["user_want"] == 0:
                    user_want_text = "神铸定轨"
                elif dict_data["user_want"] != 0 and dict_data["user_want_num"] == 0:
                    user_want_text = "0/2"
                elif dict_data["user_want"] != 0 and dict_data["user_want_num"] == 1:
                    user_want_text = "1/2"
                else:
                    print(dict_data["user_want"], dict_data["user_want_num"])
                    user_want_text = "2/2"
                user_want_font1 = user_want_font.render(user_want_text, True, (0, 0, 0))
                screen.blit(user_want_font1, (
                    40 + (125 - user_want_font1.get_size()[0]) / 2, 548 + (32 - user_want_font1.get_size()[1]) / 2))
            screen.blit(font_text_wish1, (370 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                          21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
            screen.blit(font_text_wish2, (490 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                          21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
            screen.blit(font_text_wish3, (610 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                          21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
            screen.blit(font_text_wish4, (730 + (wish_img.get_size()[0] - font_text_wish1.get_size()[0]) / 2,
                                          21 + (wish_img.get_size()[1] - font_text_wish1.get_size()[1]) / 2))
            screen.blit(chen_hui_surface, (65, 596))
            screen.blit(yuan_shi_surface, (923, 22))
            screen.blit(last_img1, (1000, 75))
            screen.blit(last_img2, (1000, 125))
            if wish_stage == 1 or wish_stage == 2:
                screen.blit(jiu_chan_ball_surface, (1020, 20))
            else:
                screen.blit(meet_ball_surface, (1020, 20))
            screen.blit(surface_wish_list[0], (565, 630))
            screen.blit(surface_wish_list[1], (802, 630))
            screen.blit(surface_wish_list[2], (1031, 630))
            pic_list = [back_png, wish_pic, back_png2, wish_img, pic_wish_now, wish_stage, user_want_pic,
                        user_want_font, font_text_wish1, font_text_wish2, font_text_wish3, font_text_wish4,
                        chen_hui_surface, yuan_shi_surface, jiu_chan_ball_surface, meet_ball_surface, last_img1,
                        last_img2, surface_wish_list]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if wish_stage == 1 or wish_stage == 2:
                        text_ball = "纠缠之缘"
                        text_ball2 = "jiu_chan_ball"
                    else:
                        text_ball = "相遇之缘"
                        text_ball2 = "meet_ball"
                    if rect_get("wish_10", mouse_x, mouse_y):
                        m2.play()
                        wish_bool = True
                        if dict_data[text_ball2] >= 10:
                            dict_data[text_ball2] -= 10
                        else:
                            if ok_box(screen,
                                      f"{text_ball}不足，是否使用*c228*157*33*{160 * (10 - dict_data[text_ball2])}*c原石购买？",
                                      f"{text_ball}不足",
                                      get_background(dict_data, pic_list)):
                                if dict_data["yuan_shi"] >= 160 * (10 - dict_data[text_ball2]):
                                    dict_data["yuan_shi"] -= 160 * (10 - dict_data[text_ball2])
                                    dict_data[text_ball2] = 0
                                else:
                                    message_box(screen,
                                                f"原石不足，您可以使用*c228*157*33*无主的星尘*c或*c228*157*33*无主的星辉*c\n在尘辉商店中购买{text_ball}\n或点击*c228*157*33*右上角加号*c获取",
                                                "原石不足", get_background(dict_data, pic_list))
                                    wish_bool = False
                            else:
                                wish_bool = False
                        if wish_bool:
                            wish_times = 10
                            main_cycle = False
                    elif rect_get("wish_1", mouse_x, mouse_y):
                        m2.play()
                        wish_bool = True
                        if dict_data[text_ball2] >= 1:
                            dict_data[text_ball2] -= 1
                        else:
                            if ok_box(screen, f"{text_ball}不足，是否使用*c228*157*33*160*c原石购买？",
                                      f"{text_ball}不足",
                                      get_background(dict_data, pic_list)):
                                if dict_data["yuan_shi"] >= 160:
                                    dict_data["yuan_shi"] -= 160
                                else:
                                    message_box(screen,
                                                f"原石不足，您可以使用*c228*157*33*无主的星尘*c或*c228*157*33*无主的星辉*c\n在尘辉商店中购买{text_ball}\n或点击*c228*157*33*右上角加号*c获取",
                                                "原石不足", get_background(dict_data, pic_list))
                                    wish_bool = False
                            else:
                                wish_bool = False
                        if wish_bool:
                            wish_times = 1
                            main_cycle = False
                    elif rect_get("wish_n", mouse_x, mouse_y):
                        m2.play()
                        wish_times = number_input(get_background(dict_data, pic_list), screen, 4,
                                                  "输入祈愿次数（小于10000次）", 10)
                        if int(wish_times) != -1:
                            main_cycle = False
                    elif rect_get("user_want", mouse_x, mouse_y) and wish_stage == 2:
                        m1.play()
                        vel_b = 0
                        vel_y = 0
                        vel_d = 0
                        user_want_weapon_pic1 = pygame.image.load(f"./files/image/map/{dict_id[five_star_list[0]]}.png")
                        user_want_weapon_pic2 = pygame.image.load(f"./files/image/map/{dict_id[five_star_list[1]]}.png")
                        user_want_need_main = pygame.image.load(f"./files/image/wish/user_want_need_main.png")
                        five_star_background = pygame.image.load(f"./files/image/five_background.png")
                        five_star_background = pygame.transform.scale(five_star_background, (85, 85))
                        user_want_already = pygame.image.load(f"./files/image/wish/user_want_already.jpg")
                        user_want_black = pygame.surface.Surface((1200, 675)).convert_alpha()
                        user_want_black.fill((0, 0, 0, 120))
                        user_want_uncertain = pygame.image.load(f"./files/image/wish/user_want_uncertain.jpg")
                        user_want_choose = pygame.image.load(f"./files/image/wish/user_want_choose.png")
                        user_want_text1 = pygame.image.load(f"./files/image/wish/user_want_text.jpg")
                        user_want_corner = pygame.image.load(f"./files/image/wish/user_want_corner.png")
                        user_want_corner = pygame.transform.scale(user_want_corner, (85, 41))
                        five_stars = pygame.image.load(f"./files/image/five_stars.png")
                        five_stars = pygame.transform.scale(five_stars, (70, 10))
                        user_want_cycle = True
                        font_17 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 17)
                        text_want1 = font_17.render(f"为{dict_id[five_star_list[0]]}定轨", True, (224, 135, 35))
                        text_want2 = font_17.render(f"为{dict_id[five_star_list[1]]}定轨", True, (224, 135, 35))
                        text_list = [text_want1, text_want2]
                        text_move = False
                        text_location = 0
                        user_want_text2 = pygame.surface.Surface((292, 329))
                        user_want_text2.blit(user_want_text1, (0, text_location))
                        user_want_num = 1
                        user_want_surface1 = pygame.surface.Surface((85, 100))
                        user_want_surface2 = pygame.surface.Surface((85, 100))
                        user_want_surface1.blit(five_star_background, (0, 0))
                        user_want_surface2.blit(five_star_background, (0, 0))
                        user_want_surface1.blit(pygame.transform.scale(user_want_weapon_pic1, (85, 85)), (0, 0))
                        user_want_surface2.blit(pygame.transform.scale(user_want_weapon_pic2, (85, 85)), (0, 0))
                        user_want_surface1.blit(user_want_corner, (0, 66))
                        user_want_surface2.blit(user_want_corner, (0, 66))
                        text1 = font_14.render(dict_id[five_star_list[0]], True, (0, 0, 0))
                        text2 = font_14.render(dict_id[five_star_list[1]], True, (0, 0, 0))
                        user_want_surface1.blit(text1, ((85 - text1.get_size()[0]) / 2, 85))
                        user_want_surface2.blit(text2, ((85 - text2.get_size()[0]) / 2, 85))
                        user_want_surface1.blit(five_stars, (7, 75))
                        user_want_surface2.blit(five_stars, (7, 75))
                        user_want_background = get_background(dict_data, pic_list)
                        while user_want_cycle:
                            screen.blit(user_want_background, (0, 0))
                            screen.blit(user_want_black, (0, 0))
                            screen.blit(user_want_text2, (43 + (1200 - user_want_need_main.get_size()[0]) / 2,
                                                          83 + (675 - user_want_need_main.get_size()[1]) / 2))
                            screen.blit(user_want_need_main, ((1200 - user_want_need_main.get_size()[0]) / 2,
                                                              (675 - user_want_need_main.get_size()[1]) / 2))
                            if dict_data["user_want"] == 0:
                                screen.blit(user_want_uncertain, (398 + (1200 - user_want_need_main.get_size()[0]) / 2,
                                                                  32 + (675 - user_want_need_main.get_size()[1]) / 2))
                                screen.blit(user_want_surface1, (695, 245))
                                screen.blit(user_want_surface2, (800, 245))
                                screen.blit(text_list[user_want_num - 1],
                                            ((331 - text_list[user_want_num - 1].get_size()[0]) / 2 + 624, 400))
                                screen.blit(user_want_choose, (695 + 105 * (user_want_num - 1), 245))
                            else:
                                screen.blit(user_want_already, (398 + (1200 - user_want_need_main.get_size()[0]) / 2,
                                                                32 + (675 - user_want_need_main.get_size()[1]) / 2))
                                if dict_data["user_want"] == 1:
                                    screen.blit(pygame.transform.scale(user_want_surface1, (80, 94)), (748, 253))
                                else:
                                    screen.blit(pygame.transform.scale(user_want_surface2, (80, 94)), (748, 253))
                            for event_want in pygame.event.get():
                                if event_want.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                if event_want.type == pygame.MOUSEBUTTONDOWN:
                                    xm, ym = pygame.mouse.get_pos()
                                    if 906 < xm < 1006 and 113 < ym < 163:
                                        user_want_cycle = False
                                        m5.play()
                                    elif 680 < xm < 960 and 481 < ym < 525:
                                        if dict_data["user_want"] == 0:
                                            dict_data["user_want"] = user_want_num
                                        else:
                                            dict_data["user_want"] = 0
                                        m1.play()
                                    elif 695 < xm < 770 and 245 < ym < 350 and dict_data["user_want"] == 0:
                                        user_want_num = 1
                                        m1.play()
                                    elif 800 < xm < 885 and 245 < ym < 350 and dict_data["user_want"] == 0:
                                        user_want_num = 2
                                        m1.play()
                                    elif 269 < xm < 549 and 196 < ym < 523:
                                        text_move = True
                                        vel_y = text_location
                                        vel_b = pygame.mouse.get_pos()[1]
                                        m1.play()
                                vel_d = pygame.mouse.get_pos()[1]
                                if event_want.type == pygame.MOUSEBUTTONUP and text_move is True:
                                    text_move = False
                                    text_location = -(vel_b - vel_y) + vel_d
                                    vel_y = 0
                                    vel_b = 0
                            if text_move:
                                text_location = -(vel_b - vel_y) + vel_d
                                if text_location > 0:
                                    text_location = 0
                                if text_location < -94:
                                    text_location = -94
                                user_want_text2 = pygame.surface.Surface((292, 329))
                                user_want_text2.blit(user_want_text1, (0, text_location))
                            if text_location > 0:
                                text_location = 0
                            if text_location < -94:
                                text_location = -94
                            pygame.display.flip()
                        load_dict(dict_data, uid)
                    elif rect_get("type1", mouse_x, mouse_y):
                        m3.play()
                        wish_pic = pygame.image.load('./files/image/wish/starter_wish.jpg')
                        wish_stage = 4
                        last_img1 = set_last_surface(dict_data, "five_star_starter_next", 1)
                        last_img2 = set_last_surface(dict_data, "five_star_starter_last", 2)
                        surface_wish_list = set_surface_wish(1)
                    elif rect_get("type2", mouse_x, mouse_y):
                        m3.play()
                        run_c = True
                        page_now = 1
                        prize_surface_now = pygame.image.load("./files/image/wish/prize/c1.png")
                        prize = 0
                        while run_c:
                            screen.fill((0, 0, 0))
                            screen.blit(prize_surface_now, (0, 0))
                            for event_c in pygame.event.get():
                                if event_c.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                elif event_c.type == pygame.MOUSEBUTTONDOWN:
                                    mcx, mcy = pygame.mouse.get_pos()
                                    if 1100 < mcx < 1200 and mcy < 100:
                                        run_c = False
                                        m5.play()
                                    elif mcy > 640 and 600 < mcx < 900 and page_now < dict_prize["character_page"]:
                                        page_now += 1
                                        prize_surface_now = pygame.image.load(
                                            f"./files/image/wish/prize/c{page_now}.png")
                                        m1.play()
                                    elif mcy > 640 and 300 < mcx < 600 and page_now > 1:
                                        page_now -= 1
                                        prize_surface_now = pygame.image.load(
                                            f"./files/image/wish/prize/c{page_now}.png")
                                        m1.play()
                                    else:
                                        for index in range(2):
                                            for index2 in range(5):
                                                if 80 + 580 * index < mcx < 560 + 580 * index and 10 + 125 * index2 < mcy < 130 + index2 * 125 and int(str((page_now - 1) * 10 + index * 5 + index2).zfill(3)) <= int(f'{str(dict_prize["character_max"])[1:4]}'):
                                                    run_c = False
                                                    prize = f"1{str((page_now - 1) * 10 + index * 5 + index2).zfill(3)}"
                                                    m1.play()
                            pygame.display.flip()
                        for key in dict_prize['character']:
                            if int(prize) == int(key['id']):
                                for key_prize in dict_id:
                                    if dict_id[key_prize] == key['five'][0]:
                                        five_star_list = [key_prize]
                                        break
                                wish_pic = pygame.image.load(f"files/image/wish/{prize}.png")
                                wish_pic = pygame.transform.scale(wish_pic, (
                                    920, int((920 / wish_pic.get_size()[0]) * wish_pic.get_size()[1])))
                                four_star_list = [key['four'][0], key['four'][1], key['four'][2]]
                                for key_prize in dict_id:
                                    if dict_id[key_prize] == key['four'][0]:
                                        four_star_list[0] = key_prize
                                    elif dict_id[key_prize] == key['four'][1]:
                                        four_star_list[1] = key_prize
                                    elif dict_id[key_prize] == key['four'][2]:
                                        four_star_list[2] = key_prize
                                wish_stage = 1
                                break
                        last_img1 = set_last_surface(dict_data, "five_star_character_next", 1)
                        last_img2 = set_last_surface(dict_data, "five_star_character_last", 2)
                        surface_wish_list = set_surface_wish(2)
                    elif rect_get("type3", mouse_x, mouse_y):
                        m3.play()
                        page_now = 1
                        prize_surface_now = pygame.image.load("./files/image/wish/prize/w1.png")
                        run_c = True
                        prize = 0
                        while run_c:
                            screen.fill((0, 0, 0))
                            screen.blit(prize_surface_now, (0, 0))
                            for event_c in pygame.event.get():
                                if event_c.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                elif event_c.type == pygame.MOUSEBUTTONDOWN:
                                    mcx, mcy = pygame.mouse.get_pos()
                                    if 1100 < mcx < 1200 and mcy < 100:
                                        run_c = False
                                        m5.play()
                                    elif mcy > 600 and 600 < mcx < 900 and page_now < dict_prize["weapon_page"]:
                                        page_now += 1
                                        prize_surface_now = pygame.image.load(
                                            f"./files/image/wish/prize/w{page_now}.png")
                                        m1.play()
                                    elif mcy > 601 and 300 < mcx < 600 and page_now > 1:
                                        page_now -= 1
                                        prize_surface_now = pygame.image.load(
                                            f"./files/image/wish/prize/w{page_now}.png")
                                        m1.play()
                                    else:
                                        for index in range(2):
                                            for index2 in range(5):
                                                if 80 + 580 * index < mcx < 560 + 580 * index and 10 + 125 * index2 < mcy < 130 + index2 * 125 and int(str((page_now - 1) * 10 + index * 5 + index2).zfill(3)) <= int(f'{str(dict_prize["weapon_max"])[1:4]}'):
                                                    run_c = False
                                                    prize = f"2{str((page_now - 1) * 10 + index * 5 + index2).zfill(3)}"
                                                    m1.play()
                            pygame.display.flip()
                        with open('./files/jsons/wish.json', 'r', encoding='utf-8') as file1:
                            dict_prize = json.load(file1)
                        for key in dict_prize['weapon']:
                            if int(prize) == int(key['id']):
                                five_star_list = [key['five'][0], key['five'][1]]
                                for key_prize in dict_id:
                                    if dict_id[key_prize] == key['five'][0]:
                                        five_star_list[0] = key_prize
                                    elif dict_id[key_prize] == key['five'][1]:
                                        five_star_list[1] = key_prize
                                wish_pic = pygame.image.load(f"files/image/wish/{prize}.png")
                                wish_pic = pygame.transform.scale(wish_pic, (
                                    920, int((920 / wish_pic.get_size()[0]) * wish_pic.get_size()[1])))
                                four_star_list = [key['four'][0], key['four'][1], key['four'][2], key['four'][3],
                                                  key['four'][4]]
                                for key_prize in dict_id:
                                    if dict_id[key_prize] == key['four'][0]:
                                        four_star_list[0] = key_prize
                                    elif dict_id[key_prize] == key['four'][1]:
                                        four_star_list[1] = key_prize
                                    elif dict_id[key_prize] == key['four'][2]:
                                        four_star_list[2] = key_prize
                                    elif dict_id[key_prize] == key['four'][3]:
                                        four_star_list[3] = key_prize
                                    elif dict_id[key_prize] == key['four'][4]:
                                        four_star_list[4] = key_prize
                                wish_stage = 2
                                break
                        last_img1 = set_last_surface(dict_data, "five_star_weapon_next", 1)
                        last_img2 = set_last_surface(dict_data, "five_star_weapon_last", 2)
                        surface_wish_list = set_surface_wish(2)
                    elif rect_get("type4", mouse_x, mouse_y):
                        m3.play()
                        wish_pic = pygame.transform.scale(pygame.image.load('./files/image/wish/normal_wish.png'),
                                                          (879, 500))
                        wish_stage = 3
                        last_img1 = set_last_surface(dict_data, "five_star_normal_next", 1)
                        last_img2 = set_last_surface(dict_data, "five_star_normal_last", 2)
                        surface_wish_list = set_surface_wish(1)
                    elif rect_get("left_button1", mouse_x, mouse_y):
                        m6.play()
                        store_img = pygame.transform.scale(pygame.image.load("./files/image/wish/store.png"),
                                                           (1200, 675))
                        surface_store1 = font_15.render(str(dict_data["xing_hui"]), True, (255, 255, 255))
                        surface_store2 = font_15.render(str(dict_data["xing_chen"]), True, (255, 255, 255))
                        surface_store3 = font_15.render(str(dict_data["meet_ball"]), True, (255, 255, 255))
                        surface_store4 = font_15.render(str(dict_data["jiu_chan_ball"]), True, (255, 255, 255))
                        store_run = True
                        while store_run:
                            screen.blit(store_img, (0, 0))
                            screen.blit(surface_store1, (490, 20))
                            screen.blit(surface_store2, (632, 20))
                            screen.blit(yuan_shi_surface, (770, 20))
                            screen.blit(surface_store3, (904, 20))
                            screen.blit(surface_store4, (1030, 20))
                            for et in pygame.event.get():
                                if et.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                if et.type == pygame.MOUSEBUTTONDOWN:
                                    mtx, mty = pygame.mouse.get_pos()
                                    store_back = pygame.surface.Surface((1200, 675))
                                    store_back.blit(store_img, (0, 0))
                                    store_back.blit(surface_store1, (490, 20))
                                    store_back.blit(surface_store2, (632, 21))
                                    store_back.blit(yuan_shi_surface, (770, 21))
                                    store_back.blit(surface_store3, (904, 21))
                                    store_back.blit(surface_store4, (1030, 21))
                                    reset_store = True
                                    if rect_get("close", mtx, mty):
                                        store_run = False
                                        m5.play()
                                    elif rect_get("store_buy", mtx, mty):
                                        m1.play()
                                        yuan_shi = number_input(store_back, screen, 5,
                                                                "请输入原石数量", dict_data["yuan_shi"])
                                        if yuan_shi != -1:
                                            dict_data["yuan_shi"] = yuan_shi
                                            load_dict(dict_data, uid)
                                        yuan_shi_surface = font_15.render(str(dict_data["yuan_shi"]), True,
                                                                          (255, 255, 255))
                                    elif rect_get("store1", mtx, mty):
                                        m1.play()
                                        if dict_data["yuan_shi"] >= 160:
                                            max_store = dict_data["yuan_shi"] // 160
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_jiu_chan_ball, "纠缠之缘", max_store,
                                                                   pygame.image.load("./files/image/wish/stone.png"),
                                                                   dict_data["yuan_shi"])
                                            if store_get != -1:
                                                dict_data["yuan_shi"] -= store_get * 160
                                                dict_data["jiu_chan_ball"] += store_get
                                        else:
                                            message_box(screen, "原石不足", "原石不足", store_back)
                                    elif rect_get("store2", mtx, mty):
                                        m1.play()
                                        if dict_data["yuan_shi"] >= 160:
                                            max_store = dict_data["yuan_shi"] // 160
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_meet_ball, "相遇之缘", max_store,
                                                                   pygame.image.load("./files/image/wish/stone.png"),
                                                                   dict_data["yuan_shi"])
                                            if store_get != -1:
                                                dict_data["yuan_shi"] -= store_get * 160
                                                dict_data["meet_ball"] += store_get
                                        else:
                                            message_box(screen, "原石不足", "原石不足", store_back)
                                    elif rect_get("store3", mtx, mty):
                                        m1.play()
                                        if dict_data["xing_chen"] >= 75:
                                            max_store = dict_data["xing_chen"] // 75
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_jiu_chan_ball, "纠缠之缘", max_store,
                                                                   xing_chen, dict_data["xing_chen"])
                                            if store_get != -1:
                                                dict_data["xing_chen"] -= store_get * 75
                                                dict_data["jiu_chan_ball"] += store_get
                                        else:
                                            message_box(screen, "无主的星尘不足", "无主的星尘不足", store_back)
                                    elif rect_get("store4", mtx, mty):
                                        m1.play()
                                        if dict_data["xing_chen"] >= 75:
                                            max_store = dict_data["xing_hui"] // 75
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_meet_ball, "相遇之缘", max_store,
                                                                   xing_chen, dict_data["xing_chen"])
                                            if store_get != -1:
                                                dict_data["xing_chen"] -= store_get * 75
                                                dict_data["meet_ball"] += store_get
                                        else:
                                            message_box(screen, "无主的星尘不足", "无主的星尘不足", store_back)
                                    elif rect_get("store5", mtx, mty):
                                        m1.play()
                                        if dict_data["xing_hui"] >= 5:
                                            max_store = dict_data["xing_hui"] // 5
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_jiu_chan_ball, "纠缠之缘", max_store,
                                                                   pygame.image.load("./files/image/wish/star.png"),
                                                                   dict_data["xing_hui"])
                                            if store_get != -1:
                                                dict_data["xing_hui"] -= store_get * 5
                                                dict_data["jiu_chan_ball"] += store_get
                                        else:
                                            message_box(screen, "无主的星辉不足", "无主的星辉不足", store_back)
                                    elif rect_get("store6", mtx, mty):
                                        m1.play()
                                        if dict_data["xing_hui"] >= 5:
                                            max_store = dict_data["xing_hui"] // 5
                                            if max_store > 99:
                                                max_store = 99
                                            store_get = scroll_box(screen, "购买物品", store_back,
                                                                   pic_meet_ball, "相遇之缘", max_store,
                                                                   pygame.image.load("./files/image/wish/star.png"),
                                                                   dict_data["xing_hui"])
                                            if store_get != -1:
                                                dict_data["xing_hui"] -= store_get * 5
                                                dict_data["meet_ball"] += store_get
                                        else:
                                            message_box(screen, "无主的星辉不足", "无主的星辉不足", store_back)
                                    else:
                                        reset_store = False
                                    if reset_store:
                                        surface_store1 = font_15.render(str(dict_data["xing_hui"]), True,
                                                                        (255, 255, 255))
                                        surface_store2 = font_15.render(str(dict_data["xing_chen"]), True,
                                                                        (255, 255, 255))
                                        surface_store3 = font_15.render(str(dict_data["meet_ball"]), True,
                                                                        (255, 255, 255))
                                        surface_store4 = font_15.render(str(dict_data["jiu_chan_ball"]), True,
                                                                        (255, 255, 255))
                                        yuan_shi_surface = font_15.render(str(dict_data["yuan_shi"]), True,
                                                                          (255, 255, 255))
                                        load_dict(dict_data, uid)
                            pygame.display.flip()
                    elif rect_get("left_button2", mouse_x, mouse_y):
                        m6.play()
                        text_s = font_35.render("请稍候……", True, (0, 0, 0))
                        weapon1 = pygame.transform.scale(pygame.image.load("./files/image/wish/weapon_map.png"),
                                                         (186, 48))
                        weapon2 = pygame.transform.scale(pygame.image.load("./files/image/wish/weapon_map_now.png"),
                                                         (186, 48))
                        character1 = pygame.transform.scale(pygame.image.load("./files/image/wish/character_map.png"),
                                                            (186, 48))
                        character2 = pygame.transform.scale(
                            pygame.image.load("./files/image/wish/character_map_now.png"), (186, 48))
                        character_type_have_list = []
                        character_type_not_list = []
                        weapon_type_have_list = []
                        weapon_type_not_list = []
                        for keys in have_data:
                            screen.blit(bg_s, (0, 0))
                            screen.blit(text_s,
                                        ((1200 - text_s.get_size()[0]) / 2, (675 - text_s.get_size()[1]) / 2))
                            for event_s in pygame.event.get():
                                if event_s.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                            if keys[0] == "c":
                                if have_data[keys] == 0:
                                    if keys[1] == "0" or keys[1] == "5":
                                        character_type = set_object_surface(dict_id[keys], have_data[keys], 1,
                                                                            black=True)
                                    else:
                                        character_type = set_object_surface(dict_id[keys], have_data[keys], 1,
                                                                            black=True, stars=4)
                                    character_type_not_list.append(character_type)
                                else:
                                    if keys[1] == "0" or keys[1] == "5":
                                        character_type = set_object_surface(dict_id[keys], have_data[keys], 2)
                                    else:
                                        character_type = set_object_surface(dict_id[keys], have_data[keys], 2, stars=4)
                                    character_type_have_list.append(character_type)
                            if keys[0] == "w":
                                if have_data[keys] == 0:
                                    if keys[1] == "0" or keys[1] == "5":
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 1, black=True)
                                    elif keys[1] == "3":
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 1, black=True,
                                                                         stars=3)
                                    else:
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 1, black=True,
                                                                         stars=4)
                                    weapon_type_not_list.append(weapon_type)
                                else:
                                    if keys[1] == "0" or keys[1] == "5":
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 2)
                                    elif keys[1] == "3":
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 2, stars=3)
                                    else:
                                        weapon_type = set_object_surface(dict_id[keys], have_data[keys], 2, stars=4)
                                    weapon_type_have_list.append(weapon_type)
                            pygame.display.flip()
                        character_surface1 = pygame.surface.Surface((1030, 4000)).convert_alpha()
                        weapon_surface1 = pygame.surface.Surface((1030, 4000)).convert_alpha()
                        character_surface1.fill((0, 0, 0, 0))
                        weapon_surface1.fill((0, 0, 0, 0))
                        num_s1 = 0
                        num_s2 = 0
                        for i in character_type_have_list:
                            character_surface1.blit(i, (0 + num_s1 * 105, 0 + num_s2 * 125))
                            num_s1 += 1
                            if num_s1 >= 10:
                                num_s1 = 0
                                num_s2 += 1
                        for i in character_type_not_list:
                            character_surface1.blit(i, (0 + num_s1 * 105, 0 + num_s2 * 125))
                            num_s1 += 1
                            if num_s1 >= 10:
                                num_s1 = 0
                                num_s2 += 1
                        num_s1 = 0
                        num_s3 = 0
                        for i in weapon_type_have_list:
                            weapon_surface1.blit(i, (0 + num_s1 * 105, 0 + num_s3 * 125))
                            num_s1 += 1
                            if num_s1 >= 10:
                                num_s1 = 0
                                num_s3 += 1
                        for i in weapon_type_not_list:
                            weapon_surface1.blit(i, (0 + num_s1 * 105, 0 + num_s3 * 125))
                            num_s1 += 1
                            if num_s1 >= 10:
                                num_s1 = 0
                                num_s3 += 1
                        character_surface = pygame.surface.Surface((1030, num_s2 * 125 + 155)).convert_alpha()
                        weapon_surface = pygame.surface.Surface((1030, num_s3 * 125 + 155)).convert_alpha()
                        character_surface.fill((0, 0, 0, 0))
                        weapon_surface.fill((0, 0, 0, 0))
                        character_surface.blit(character_surface1, (0, 0))
                        weapon_surface.blit(weapon_surface1, (0, 0))
                        run_s = True
                        stage_s = 1
                        direction_s = 50
                        move_s = False
                        vel_b = 0
                        vel_y = 0
                        vel_d = 0
                        weapon_now = weapon1
                        character_now = character2
                        closing_button = pygame.image.load("./files/image/closing_button.png")
                        while run_s:
                            surface_bg_s = pygame.surface.Surface((1200, 100))
                            surface_bg_s.blit(bg_s, (0, 0))
                            surface_bg_s.blit(character_now, (400, 26))
                            surface_bg_s.blit(weapon_now, (700, 26))
                            surface_bg_s.blit(closing_button, (1145, 15))
                            screen.fill((0, 0, 0))
                            screen.blit(bg_s, (0, 0))
                            if direction_s > 100:
                                direction_s = 100
                            if stage_s == 1:
                                if character_surface.get_size()[1] < 625:
                                    direction_s = 50
                                elif direction_s < 675 - character_surface.get_size()[1]:
                                    direction_s = 675 - character_surface.get_size()[1]
                                screen.blit(character_surface,
                                            ((1200 - character_surface.get_size()[0]) / 2, direction_s))
                            else:
                                if weapon_surface.get_size()[1] < 625:
                                    direction_s = 50
                                elif direction_s < 675 - weapon_surface.get_size()[1]:
                                    direction_s = 675 - weapon_surface.get_size()[1]
                                screen.blit(weapon_surface, ((1200 - weapon_surface.get_size()[0]) / 2, direction_s))
                            screen.blit(surface_bg_s, (0, 0))
                            pygame.display.flip()
                            for event_s in pygame.event.get():
                                if event_s.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                if event_s.type == pygame.MOUSEBUTTONDOWN:
                                    mxs, mys = pygame.mouse.get_pos()
                                    if rect_get("close", mxs, mys):
                                        run_s = False
                                        m5.play()
                                    elif 400 < mxs < 600 and 20 < mys < 80 and stage_s == 2:
                                        weapon_now = weapon1
                                        character_now = character2
                                        stage_s = 1
                                        direction_s = 200
                                        m1.play()
                                    elif 700 < mxs < 900 and 20 < mys < 80 and stage_s == 1:
                                        weapon_now = weapon2
                                        character_now = character1
                                        stage_s = 2
                                        direction_s = 200
                                        m1.play()
                                    else:
                                        move_s = True
                                        vel_y = direction_s
                                        vel_b = pygame.mouse.get_pos()[1]
                                vel_d = pygame.mouse.get_pos()[1]
                                if event_s.type == pygame.MOUSEBUTTONUP:
                                    move_s = False
                                    vel_y = 0
                                    vel_b = 0
                            if move_s:
                                direction_s = -(vel_b - vel_y) + vel_d
                                if direction_s > 100:
                                    direction_s = 100
                                if stage_s == 1:
                                    if character_surface.get_size()[1] < 625:
                                        direction_s = 50
                                    elif direction_s < 675 - character_surface.get_size()[1]:
                                        direction_s = 675 - character_surface.get_size()[1]
                                    screen.blit(character_surface,
                                                ((1200 - character_surface.get_size()[0]) / 2, direction_s))
                                else:
                                    if weapon_surface.get_size()[1] < 625:
                                        direction_s = 50
                                    elif direction_s < 675 - weapon_surface.get_size()[1]:
                                        direction_s = 675 - weapon_surface.get_size()[1]
                                    screen.blit(weapon_surface,
                                                ((1200 - weapon_surface.get_size()[0]) / 2, direction_s))
                                screen.blit(surface_bg_s, (0, 0))
                            pygame.display.flip()
                    elif rect_get("left_button3", mouse_x, mouse_y):
                        m6.play()
                        history_img = pygame.image.load("./files/image/wish/history.png")
                        history_type = pygame.transform.scale(pygame.image.load("./files/image/wish/history_type.png"),
                                                              (527, 154))
                        history_json_list = [history_data["normal"], history_data["starter"], history_data["character"],
                                             history_data["weapon"]]
                        if wish_stage == 3 or wish_stage == 4:
                            history_stage = wish_stage - 2
                        else:
                            history_stage = wish_stage + 2
                        history_surface_list = []
                        for i in history_json_list:
                            history_surface_list2 = []
                            history_num = len(i)
                            if len(i) == 0:
                                pass
                            else:
                                for history_times in range(len(i) // 5 + 1):
                                    history_surface = pygame.surface.Surface((333, 240)).convert_alpha()
                                    history_surface.fill((0, 0, 0, 0))
                                    for history_times2 in range(5):
                                        history_font = font_20.render(str(history_num), True, (55, 55, 55))
                                        history_font2 = font_20.render(i[history_num - 1][0], True, (55, 55, 55))
                                        if i[history_num - 1][2] == 5:
                                            history_font3 = font_20.render(f"{i[history_num - 1][1]}(五星)", True,
                                                                           (228, 157, 53))
                                        elif i[history_num - 1][2] == 4:
                                            history_font3 = font_20.render(f"{i[history_num - 1][1]}(四星)", True,
                                                                           (155, 96, 222))
                                        else:
                                            history_font3 = font_20.render(i[history_num - 1][1], True, (55, 55, 55))
                                        history_surface.blit(history_font, (
                                            (65 - history_font.get_size()[0]) / 2, 40 * history_times2 + 50))
                                        history_surface.blit(history_font2,
                                                             (65 + (68 - history_font2.get_size()[0]) / 2,
                                                              40 * history_times2 + 50))
                                        history_surface.blit(history_font3,
                                                             (133 + (200 - history_font3.get_size()[0]) / 2,
                                                              40 * history_times2 + 50))
                                        history_num -= 1
                                        if history_num <= 0:
                                            break
                                    history_surface_list2.append(history_surface)
                                    if history_num <= 0:
                                        break
                            history_surface_list.append(history_surface_list2)
                        page_history = 0
                        if history_stage == 1:
                            history_text3 = "normal"
                            history_text4 = "常驻祈愿"
                        elif history_stage == 2:
                            history_text3 = "starter"
                            history_text4 = "新手祈愿"
                        elif history_stage == 3:
                            history_text3 = "character"
                            history_text4 = "角色活动祈愿与角色活动祈愿-2"
                        else:
                            history_text3 = "weapon"
                            history_text4 = "武器活动祈愿"
                        history_text5 = font_20.render(history_text4, True, (0, 0, 0))
                        if history_stage == 3 or history_stage == 4:
                            history_text = font_15.render(
                                f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，非限定UP五星{dict_data[f"crooked_{history_text3}"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                True, (0, 0, 0))
                        else:
                            history_text = font_15.render(
                                f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                True, (0, 0, 0))
                        history_page = font_15.render(
                            f"{page_history + 1} / {(len(history_json_list[history_stage - 1]) - 1) // 10 + 1}", True,
                            (0, 0, 0))
                        history_run = True
                        while history_run:
                            screen.blit(history_img, (0, 0))
                            if len(history_surface_list[history_stage - 1]) > page_history * 2:
                                screen.blit(history_surface_list[history_stage - 1][page_history * 2], (215, 278))
                            if len(history_surface_list[history_stage - 1]) > page_history * 2 + 1:
                                screen.blit(history_surface_list[history_stage - 1][page_history * 2 + 1], (654, 278))
                            screen.blit(history_text, (217, 242))
                            screen.blit(history_text5, (465, 182))
                            if history_stage == 3 or history_stage == 4:
                                history_text = font_15.render(
                                    f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，非限定UP五星{dict_data[f"crooked_{history_text3}"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                    True, (0, 0, 0))
                            else:
                                history_text = font_15.render(
                                    f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                    True, (0, 0, 0))
                            screen.blit(history_page, (518 + (164 - history_page.get_size()[0]) / 2, 539))
                            for event_h in pygame.event.get():
                                if event_h.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                elif event_h.type == pygame.MOUSEBUTTONDOWN:
                                    mhx, mhy = pygame.mouse.get_pos()
                                    if rect_get("history_left", mhx, mhy) and page_history > 0:
                                        m1.play()
                                        page_history -= 1
                                        history_page = font_15.render(
                                            f"{page_history + 1} / {(len(history_json_list[history_stage - 1]) - 1) // 10 + 1}",
                                            True,
                                            (0, 0, 0))
                                    elif rect_get("history_right", mhx, mhy) and page_history + 1 < (
                                            len(history_json_list[history_stage - 1]) - 1) // 10 + 1:
                                        m1.play()
                                        page_history += 1
                                        history_page = font_15.render(
                                            f"{page_history + 1} / {(len(history_json_list[history_stage - 1]) - 1) // 10 + 1}",
                                            True,
                                            (0, 0, 0))
                                    elif rect_get("history_change", mhx, mhy):
                                        m1.play()
                                        history_stage1 = 10
                                        history_type_run = True
                                        while history_type_run:
                                            screen.blit(history_img, (0, 0))
                                            if len(history_surface_list[history_stage - 1]) > page_history * 2:
                                                screen.blit(history_surface_list[history_stage - 1][page_history * 2],
                                                            (215, 278))
                                            if len(history_surface_list[history_stage - 1]) > page_history * 2 + 1:
                                                screen.blit(
                                                    history_surface_list[history_stage - 1][page_history * 2 + 1],
                                                    (654, 278))
                                            screen.blit(history_text, (217, 242))
                                            screen.blit(history_text5, (465, 182))
                                            screen.blit(history_page,
                                                        (518 + (164 - history_page.get_size()[0]) / 2, 539))
                                            screen.blit(history_type, (442, 214))
                                            for event_ht in pygame.event.get():
                                                if event_ht.type == pygame.QUIT:
                                                    pygame.quit()
                                                    sys.exit(0)
                                                elif event_ht.type == pygame.MOUSEBUTTONDOWN:
                                                    m1.play()
                                                    mhx1, mhy1 = pygame.mouse.get_pos()
                                                    history_type_run = False
                                                    history_stage1 = history_stage
                                                    if rect_get("history_type1", mhx1, mhy1):
                                                        history_stage = 1
                                                    elif rect_get("history_type2", mhx1, mhy1):
                                                        history_stage = 2
                                                    elif rect_get("history_type3", mhx1, mhy1):
                                                        history_stage = 3
                                                    elif rect_get("history_type4", mhx1, mhy1):
                                                        history_stage = 4
                                            pygame.display.flip()
                                        if history_stage != history_stage1:
                                            page_history = 0
                                            if history_stage == 1:
                                                history_text3 = "normal"
                                                history_text4 = "常驻祈愿"
                                            elif history_stage == 2:
                                                history_text3 = "starter"
                                                history_text4 = "新手祈愿"
                                            elif history_stage == 3:
                                                history_text3 = "character"
                                                history_text4 = "角色活动祈愿与角色活动祈愿-2"
                                            else:
                                                history_text3 = "weapon"
                                                history_text4 = "武器活动祈愿"
                                            history_text5 = font_20.render(history_text4, True, (0, 0, 0))
                                            if history_stage == 3 or history_stage == 4:
                                                history_text = font_15.render(
                                                    f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，非限定UP五星{dict_data[f"crooked_{history_text3}"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                                    True, (0, 0, 0))
                                            else:
                                                history_text = font_15.render(
                                                    f'累计共抽该卡池{dict_data[f"{history_text3}_wish_total"]}发，抽中五星{dict_data[f"five_star_{history_text3}_total"]}发，四星{dict_data[f"four_star_{history_text3}_total"]}发',
                                                    True, (0, 0, 0))
                                            history_page = font_15.render(
                                                f"{page_history + 1} / {(len(history_json_list[history_stage - 1]) - 1) // 10 + 1}",
                                                True,
                                                (0, 0, 0))
                                    elif rect_get("history_close", mhx, mhy):
                                        m5.play()
                                        history_run = False
                            pygame.display.flip()
                    elif rect_get("close", mouse_x, mouse_y):
                        m1.play()
                        if ok_box(screen, "确定退出模拟器？", "退出", get_background(dict_data, pic_list)):
                            first_cycle = False
                            main_cycle = False
                            back_local = True
                    elif rect_get("reset", mouse_x, mouse_y):
                        m1.play()
                        if ok_box(screen, "确定要重置当前用户数据吗", "重置", get_background(dict_data, pic_list)):
                            dict_data = dict_init()
                            history_data = {"character": [], "weapon": [], "normal": [], "starter": []}
                            have_data = dict_init2()
                            load_dict(dict_data, uid)
                            with open(f'./files/jsons/history_data{uid}.json', 'w', encoding='utf-8') as file_data:
                                file_data.write(json.dumps(history_data, ensure_ascii=False))
                            with open(f'./files/jsons/have_data{uid}.json', 'w', encoding='utf-8') as file_data:
                                file_data.write(json.dumps(have_data, ensure_ascii=False))
                            if wish_stage == 1:
                                text_ = "character"
                            elif wish_stage == 2:
                                text_ = "weapon"
                            elif wish_stage == 3:
                                text_ = "normal"
                            else:
                                text_ = "starter"
                            last_img1 = set_last_surface(dict_data, f"five_star_{text_}_next", 1)
                            last_img2 = set_last_surface(dict_data, f"five_star_{text_}_last", 2)
                            if dict_data["user_want"] != 0:
                                user_want_pic = user_want_list[dict_data["user_want_num"]]
                            else:
                                user_want_pic = user_want_list[0]
                            message_box(screen, "重置成功", "重置成功", get_background(dict_data, pic_list))
                    elif rect_get("settings", mouse_x, mouse_y):
                        m6.play()
                        run1 = True
                        while run1:
                            screen.blit(setting_pic, (0, 0))
                            for event1 in pygame.event.get():
                                if event1.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit(0)
                                elif event1.type == pygame.MOUSEBUTTONDOWN:
                                    mx, my = pygame.mouse.get_pos()
                                    if rect_get("close", mx, my):
                                        run1 = False
                                        m5.play()
                                    elif rect_get("setting1", mx, my):
                                        m1.play()
                                        dict_data = choose_four_star(screen, dict_data)
                                        load_dict(dict_data, uid)
                            pygame.display.flip()
                    elif rect_get("buy", mouse_x, mouse_y):
                        m1.play()
                        yuan_shi = number_input(get_background(dict_data, pic_list), screen, 5,
                                                "请输入原石数量", dict_data["yuan_shi"])
                        if yuan_shi != -1:
                            dict_data["yuan_shi"] = yuan_shi
                            load_dict(dict_data, uid)
                    elif rect_get("buy2", mouse_x, mouse_y):
                        m1.play()
                        if wish_stage == 1 or wish_stage == 2:
                            yuan_shi = number_input(get_background(dict_data, pic_list), screen, 5,
                                                    "请输入纠缠之缘数量", dict_data["jiu_chan_ball"])
                            if yuan_shi != -1:
                                dict_data["jiu_chan_ball"] = yuan_shi
                                load_dict(dict_data, uid)
                        else:
                            yuan_shi = number_input(get_background(dict_data, pic_list), screen,
                                                    5, "请输入相遇之缘数量", dict_data["meet_ball"])
                            if yuan_shi != -1:
                                dict_data["meet_ball"] = yuan_shi
                                load_dict(dict_data, uid)
                        load_dict(dict_data, uid)
                    chen_hui_surface = chen_hui(xing_chen, dict_data, font_20)
                    yuan_shi_surface = font_15.render(str(dict_data["yuan_shi"]), True, (255, 255, 255))
                    jiu_chan_ball_surface = set_ball_surface(font_15, dict_data, pic_jiu_chan_ball, "jiu_chan_ball")
                    meet_ball_surface = set_ball_surface(font_15, dict_data, pic_meet_ball, "meet_ball")
            pygame.display.flip()
        if back_local:
            continue
        if wish_times == 1 or wish_times == 10:
            white_img = pygame.surface.Surface((1200, 675))
            white_img.fill((255, 255, 255))
            for i in range(10):
                white_img.set_alpha(500 - 50 * i)
                screen.blit(white_img, (0, 0))
                pygame.display.flip()
        get_five_star = False
        get_four_star = False
        listing = []
        xing_chen_temporary = 0
        xing_hui_temporary = 0
        five_star_temporary = 0
        four_star_temporary = 0
        if wish_stage == 1:
            stage_text = "character"
        elif wish_stage == 2:
            stage_text = "weapon"
        elif wish_stage == 3:
            stage_text = "normal"
        else:
            stage_text = "starter"
        if wish_times != 10 and wish_times != 1:
            n_wish_surface, n_wish_list = set_surface_wish_n(wish_stage, dict_data, have_data, five_star_list,
                                                             four_star_list)
        for wish_items in range(int(wish_times)):
            main_cycle = True
            if wish_stage == 1:
                dict_data["character_wish_total"] += 1
                if dict_data["five_star_character_next"] <= 72:
                    five_star_chance = 6
                elif dict_data["five_star_character_next"] <= 88:
                    five_star_chance = 6 + (dict_data["five_star_character_next"] - 72) * 60
                else:
                    five_star_chance = 1000
                five_star_random1 = random.randint(1, 1000)
                if five_star_random1 <= five_star_chance:
                    dict_data["five_star_character_last"] = dict_data["five_star_character_next"] + 1
                    get_five_star = True
                    dict_data["five_star_character_total"] += 1
                    if dict_data["five_star_askew_character"] >= 1:
                        listing.append(five_star_list[0])
                        dict_data["five_star_askew_character"] = 0
                    else:
                        five_star_askew_bool = random.randint(2, 3)
                        if five_star_askew_bool <= 2:
                            dict_data["five_star_askew_character"] += 1
                            dict_data["crooked_character"] += 1
                            five_star_id = random.randint(1, 7)
                            five_star_id = str(five_star_id).zfill(2)
                            listing.append(f"c0{five_star_id}")
                        else:
                            listing.append(five_star_list[0])
                            dict_data["five_star_askew_character"] = 0
                    dict_data["five_star_character_next"] = 0
                else:
                    dict_data["five_star_character_next"] += 1
                    if dict_data["four_star_character_next"] <= 7:
                        four_star_random1 = 51
                    elif dict_data["four_star_character_next"] == 8:
                        four_star_random1 = 561
                    else:
                        four_star_random1 = 1000
                    v = random.randint(1, 1000)
                    if v <= four_star_random1:
                        dict_data["xing_hui"] += 2
                        get_four_star = True
                        dict_data["four_star_character_total"] += 1
                        if dict_data["four_star_askew_character"] >= 1:
                            dict_data["four_star_askew_character"] = 0
                            four_star_get = random.randint(0, 2)
                            listing.append(four_star_list[four_star_get])
                        else:
                            kk = random.randint(1, 2)
                            if kk == 1:
                                dict_data["four_star_askew_character"] = 0
                                four_star_get = random.randint(0, 2)
                                listing.append(four_star_list[four_star_get])
                            else:
                                dict_data["four_star_askew_character"] += 1
                                four_star_type = random.randint(1, 2)
                                if four_star_type == 1:
                                    four_star_id = random.randint(1, get_four_star_num1)
                                    four_star_id = str(four_star_id).zfill(2)
                                    listing.append(f"c4{four_star_id}")
                                else:
                                    four_star_id = random.randint(1, 17)
                                    four_star_id = str(four_star_id).zfill(2)
                                    listing.append(f"w4{four_star_id}")
                        dict_data["four_star_character_next"] = 0
                    else:
                        dict_data["four_star_character_next"] += 1
                        three_star_id = random.randint(1, 13)
                        three_star_id = str(three_star_id).zfill(2)
                        listing.append(f"w3{three_star_id}")
            elif wish_stage == 2:
                dict_data["weapon_wish_total"] += 1
                if dict_data["five_star_weapon_next"] <= 50:
                    five_star_chance = 3
                elif dict_data["five_star_weapon_next"] <= 63:
                    five_star_chance = 10
                elif dict_data["five_star_weapon_next"] <= 73:
                    five_star_chance = 35 * (dict_data["five_star_weapon_next"] - 62)
                elif dict_data["five_star_weapon_next"] < 79:
                    five_star_chance = 388 + 17.5 * (dict_data["five_star_weapon_next"] - 73)
                else:
                    five_star_chance = 500
                e = random.randint(1, 500)
                if e <= five_star_chance:
                    dict_data["five_star_weapon_last"] = dict_data["five_star_weapon_next"] + 1
                    get_five_star = True
                    dict_data["five_star_weapon_total"] += 1
                    if dict_data["user_want"] != 0 and dict_data["user_want_num"] >= 2:
                        listing.append([dict_data["user_want"] - 1])
                        dict_data["user_want"] = 0
                        dict_data["user_want_num"] = 0
                        dict_data["five_star_askew_weapon"] = 0
                    elif dict_data["five_star_askew_weapon"] >= 1:
                        five_star_id = random.randint(1, 2)
                        if five_star_id == 1:
                            listing.append(five_star_list[0])
                            if dict_data["user_want"] == 1:
                                dict_data["user_want"] = 0
                                dict_data["user_want_num"] = 0
                            elif dict_data["user_want"] == 2:
                                dict_data["user_want_num"] += 1
                        else:
                            listing.append(five_star_list[1])
                            if dict_data["user_want"] == 2:
                                dict_data["user_want"] = 0
                                dict_data["user_want_num"] = 0
                            elif dict_data["user_want"] == 1:
                                dict_data["user_want_num"] += 1
                        dict_data["five_star_askew_weapon"] = 0
                    else:
                        five_star_askew_bool = random.randint(0, 3)
                        if five_star_askew_bool == 0:
                            dict_data["five_star_askew_weapon"] += 1
                            if dict_data["user_want"] != 0:
                                dict_data["user_want_num"] += 1
                            dict_data["crooked_weapon"] += 1
                            five_star_id = random.randint(1, 10)
                            five_star_id = str(five_star_id).zfill(2)
                            listing.append(f"w0{five_star_id}")
                        else:
                            five_star_id = random.randint(1, 2)
                            if five_star_id == 1:
                                listing.append(five_star_list[0])
                                if dict_data["user_want"] == 1:
                                    dict_data["user_want"] = 0
                                    dict_data["user_want_num"] = 0
                                elif dict_data["user_want"] == 2:
                                    dict_data["user_want_num"] += 1
                            else:
                                listing.append(five_star_list[1])
                                if dict_data["user_want"] == 2:
                                    dict_data["user_want"] = 0
                                    dict_data["user_want_num"] = 0
                                elif dict_data["user_want"] == 1:
                                    dict_data["user_want_num"] += 1
                            dict_data["five_star_askew_weapon"] = 0
                    dict_data["five_star_weapon_next"] = 0
                else:
                    dict_data["five_star_weapon_next"] += 1
                    if dict_data["four_star_weapon_next"] < 7:
                        four_star_randint = 6
                    elif dict_data["four_star_weapon_next"] == 7:
                        four_star_randint = 66
                    elif dict_data["four_star_weapon_next"] == 8:
                        four_star_randint = 96
                    else:
                        four_star_randint = 100
                    v = random.randint(1, 100)
                    if v <= four_star_randint:
                        get_four_star = True
                        dict_data["four_star_weapon_total"] += 1
                        if dict_data["four_star_askew_weapon"] >= 1:
                            dict_data["four_star_askew_weapon"] = 0
                            four_star_get = random.randint(0, 4)
                            listing.append(four_star_list[four_star_get])
                        else:
                            kk = random.randint(1, 2)
                            if kk == 1:
                                dict_data["four_star_askew_weapon"] = 0
                                four_star_get = random.randint(0, 4)
                                listing.append(four_star_list[four_star_get])
                            else:
                                dict_data["four_star_askew_weapon"] += 1
                                four_star_type = random.randint(1, 2)
                                if four_star_type == 1:
                                    four_star_id = random.randint(1, get_four_star_num1)
                                    four_star_id = str(four_star_id).zfill(2)
                                    listing.append(f"c4{four_star_id}")
                                else:
                                    four_star_id = random.randint(1, 17)
                                    four_star_id = str(four_star_id).zfill(2)
                                    listing.append(f"w4{four_star_id}")
                        dict_data["four_star_weapon_next"] = 0
                    else:
                        dict_data["xing_chen"] += 15
                        xing_chen_temporary += 15
                        dict_data["four_star_weapon_next"] += 1
                        three_star_id = random.randint(1, 13)
                        three_star_id = str(three_star_id).zfill(2)
                        listing.append(f"w3{three_star_id}")
            elif wish_stage == 3:
                dict_data["normal_wish_total"] += 1
                if dict_data["five_star_normal_next"] <= 72:
                    five_star_chance = 6
                elif dict_data["five_star_normal_next"] <= 88:
                    five_star_chance = 6 + (dict_data["five_star_normal_next"] - 72) * 60
                else:
                    five_star_chance = 1000
                five_star_random1 = random.randint(1, 1000)
                if five_star_random1 <= five_star_chance:
                    get_five_star = True
                    dict_data["five_star_normal_last"] = 1 + dict_data["five_star_normal_next"]
                    dict_data["five_star_normal_total"] += 1
                    dict_data["five_star_normal_next"] = 0
                    five_star_type = random.randint(1, 2)
                    if five_star_type == 1:
                        five_star_id = random.randint(1, 7)
                        five_star_id = str(five_star_id).zfill(2)
                        listing.append(f"c0{five_star_id}")
                    else:
                        five_star_id = random.randint(1, 10)
                        five_star_id = str(five_star_id).zfill(2)
                        listing.append(f"w0{five_star_id}")
                else:
                    dict_data["five_star_normal_next"] += 1
                    four_star_random = random.randint(1, 1000)
                    if dict_data["four_star_normal_next"] <= 7:
                        four_star_randint = 51
                    elif dict_data["four_star_normal_next"] == 8:
                        four_star_randint = 561
                    else:
                        four_star_randint = 1000
                    if four_star_random <= four_star_randint:
                        get_four_star = True
                        dict_data["four_star_normal_total"] += 1
                        four_star_type = random.randint(1, 2)
                        if four_star_type == 1:
                            four_star_id = random.randint(1, get_four_star_num1 + 3)
                            if four_star_id > get_four_star_num1:
                                listing.append(f"c20{four_star_id - get_four_star_num1}")
                            else:
                                four_star_id = str(four_star_id).zfill(2)
                                listing.append(f"c4{four_star_id}")
                        else:
                            four_star_id = random.randint(1, 17)
                            four_star_id = str(four_star_id).zfill(2)
                            listing.append(f"w4{four_star_id}")
                        dict_data["four_star_normal_next"] = 0
                    else:
                        dict_data["four_star_normal_next"] += 1
                        three_star_id = random.randint(1, 13)
                        three_star_id = str(three_star_id).zfill(2)
                        listing.append(f'w3{three_star_id}')
            else:
                dict_data["starter_wish_total"] += 1
                five_star_random = random.randint(0, 1000)
                if five_star_random <= 6:
                    dict_data["five_star_starter_last"] = 1 + dict_data["five_star_starter_next"]
                    get_five_star = True
                    dict_data["five_star_starter_total"] += 1
                    five_star_id = random.randint(1, 7)
                    five_star_id = str(five_star_id).zfill(2)
                    listing.append(f"c0{five_star_id}")
                    dict_data["five_star_starter_next"] = 0
                else:
                    dict_data["five_star_starter_next"] += 1
                    four_star_random = random.randint(1, 1000)
                    if dict_data["four_star_starter_next"] <= 7:
                        four_star_randint = 51
                    elif dict_data["four_star_starter_next"] == 8:
                        four_star_randint = 561
                    else:
                        four_star_randint = 1000
                    if four_star_random <= four_star_randint:
                        get_four_star = True
                        dict_data["four_star_starter_total"] += 1
                        four_star_type = random.randint(1, 2)
                        if four_star_type == 1:
                            four_star_id = random.randint(1, get_four_star_num1 + 3)
                            if four_star_id > get_four_star_num1:
                                listing.append(f"c20{four_star_id - get_four_star_num1}")
                            else:
                                four_star_id = str(four_star_id).zfill(2)
                                listing.append(f"c4{four_star_id}")
                        else:
                            four_star_id = random.randint(1, 17)
                            four_star_id = str(four_star_id).zfill(2)
                            listing.append(f"w4{four_star_id}")
                        dict_data["four_star_starter_next"] = 0
                    else:
                        dict_data["four_star_starter_next"] += 1
                        three_star_id = random.randint(1, 13)
                        three_star_id = str(three_star_id).zfill(2)
                        listing.append(f"w3{three_star_id}")
            try:
                have_data[listing[-1]] += 1
            except KeyError:
                have_data[listing[-1]] = 1
            if listing[-1][1] == "0" or listing[-1][1] == "5":
                five_star_temporary += 1
            elif listing[-1][1] == "2" or listing[-1][1] == "4":
                four_star_temporary += 1
            if listing[-1][0] == "w":
                text_type = "武器"
                if listing[-1][1] == "0" or listing[-1][1] == "5":
                    text_type2 = 5
                    dict_data["xing_hui"] += 10
                    xing_hui_temporary += 10
                elif listing[-1][1] == "3":
                    text_type2 = 3
                    dict_data["xing_chen"] += 15
                    xing_chen_temporary += 15
                else:
                    text_type2 = 4
                    dict_data["xing_hui"] += 2
                    xing_hui_temporary += 2
            else:
                text_type = "角色"
                if listing[-1][1] == "0" or listing[-1][1] == "5":
                    text_type2 = 5
                    if have_data[listing[-1]] == 1:
                        pass
                    elif have_data[listing[-1]] >= 7:
                        dict_data["xing_hui"] += 25
                        xing_hui_temporary += 25
                    else:
                        dict_data["xing_hui"] += 10
                        xing_hui_temporary += 10
                else:
                    text_type2 = 4
                    if have_data[listing[-1]] == 1:
                        pass
                    elif have_data[listing[-1]] >= 7:
                        dict_data["xing_hui"] += 5
                        xing_hui_temporary += 5
                    else:
                        dict_data["xing_hui"] += 2
                        xing_hui_temporary += 2
            history_data[stage_text].append([text_type, dict_id[listing[-1]], text_type2])
            if len(history_data[stage_text]) > 1000:
                history_data[stage_text].pop(0)
            if wish_times != 10 and wish_times != 1:
                screen.fill((0, 0, 0))
                screen.blit(n_wish_surface, (0, 0))
                screen.blit(font_40.render(f"五星总计：{five_star_temporary}    无主的星尘：{xing_chen_temporary}", True,
                                           (255, 255, 255)), (100, 450))
                screen.blit(font_40.render(f"四星总计：{four_star_temporary}   无主的星辉：{xing_hui_temporary}", True,
                                           (255, 255, 255)), (100, 500))
                screen.blit(ok, ((1200 - ok.get_size()[0]) / 2, 580))
                num1 = 0
                num2 = 0
                for i in n_wish_list:
                    if num1 >= 9:
                        num1 = 0
                        num2 += 1
                    font_n_wish = font_15.render(str(have_data[i[0]] - i[1]), True, (0, 0, 0))
                    screen.blit(font_n_wish,
                                ((85 - font_n_wish.get_size()[0]) / 2 + 100 + 115 * num1, 145 + 130 * num2))
                    if have_data[i[0]] - i[1] == 0:
                        black1 = pygame.surface.Surface((85, 105)).convert_alpha()
                        black1.fill((0, 0, 0, 120))
                        screen.blit(black1, (100 + 115 * num1, 60 + 130 * num2))
                    num1 += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
                pygame.display.flip()
        with open(f'./files/jsons/history_data{uid}.json', 'w', encoding='utf-8') as file_data:
            file_data.write(json.dumps(history_data, ensure_ascii=False))
        with open(f'./files/jsons/have_data{uid}.json', 'w', encoding='utf-8') as file_data:
            file_data.write(json.dumps(have_data, ensure_ascii=False))
        skip = False
        if wish_times == 1 or wish_times == 10:
            if get_five_star:
                if wish_times == 10:
                    skip = preview(clip1, eventa=aff)
                if wish_times == 1:
                    skip = preview(clip2, eventa=aff)
            else:
                if get_four_star != 0:
                    if wish_times == 10:
                        skip = preview(clip3, eventa=aff)
                    if wish_times == 1:
                        skip = preview(clip4, eventa=aff)
                else:
                    skip = preview(clip5, eventa=aff)
            pygame.mixer.init()  # -------------------------------------------------------------------------------
        surface_wish = pygame.surface.Surface((1200, 675))
        surface_wish.blit(wish_back, (0, 0))
        if wish_times == 10:
            for i in listing:
                if not skip:
                    if i[0] == "c":
                        surface_wish1 = set_pic(dict_id, i, element_dict)
                    else:
                        surface_wish1 = set_pic(dict_id, i, element_dict, type_pic=2)
                    wish_run = True
                    m4.play()
                    while wish_run:
                        screen.blit(surface_wish1, (0, 0))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                m1.play()
                                wish_run = False
                                mx, my = pygame.mouse.get_pos()
                                if mx > 1130 and my < 45:
                                    skip = True
                        pygame.display.flip()
            screen.fill((0, 0, 0))
            image_list6 = []
            five_star_list1 = []
            for index in listing:
                try:
                    pic = pygame.image.load(f'./files/ls/{dict_id[index]}.png')
                except FileNotFoundError:
                    text1_list = []
                    surface_unknown_num = 0
                    for items in dict_id[index]:
                        text1_list.append(font_40.render(items, True, (255, 255, 255)))
                        surface_unknown_num += font_40.render(items, True, (255, 255, 255)).get_size()[1]
                    surface_unknown = pygame.surface.Surface((40, surface_unknown_num)).convert_alpha()
                    surface_unknown.fill((0, 0, 0, 0))
                    surface_unknown_num = 0
                    for items in text1_list:
                        surface_unknown.blit(items, (0, surface_unknown_num))
                        surface_unknown_num += items.get_size()[1]
                    if index[1] == "0" or index[1] == "5":
                        pic = pygame.image.load('./files/ls/1.png')
                    else:
                        pic = pygame.image.load('./files/ls/0.png')
                    pic = pygame.transform.scale(pic, (99, 675))
                    pic.blit(surface_unknown, (29, (675 - surface_unknown.get_size()[1]) / 2))
                ax = pygame.surface.Surface((99, 675)).convert_alpha()
                ax.fill((0, 0, 0, 0))
                ax.blit(pygame.transform.scale(pic, (99, 675)), (0, 0))
                if index[1] == "0" or index[1] == "5":
                    five_star_list1.append(ax)
                elif index[1] == "3":
                    image_list6.append(ax)
                else:
                    image_list6.insert(0, ax)
                screen.fill((0, 0, 0))
            for j in five_star_list1:
                image_list6.insert(0, j)
            num1 = 0
            image_list = [image_list6[0]]
            number1 = 41
            for k in range(9):
                for m in range(10, 1, -1):
                    screen.fill((0, 0, 0))
                    screen.blit(wish_back, (0, 0))
                    for n in range(len(image_list)):
                        screen.blit(image_list[n], (105 + 99 * n + number1 ** 2 / 10, 0))
                    time.sleep(0.001)
                    screen.blit(image_list6[k + 1], (204 + 5 * m + num1 + number1 ** 2 / 10 - 10, 0))
                    pygame.display.flip()
                    number1 -= 0.5
                image_list.append(image_list6[k + 1])
                num1 += 99
            for i in range(10):
                surface_wish.blit(image_list6[i], (105 + 99 * i, 0))
        elif wish_times == 1:
            m4.play()
            if listing[0][0] == "c":
                surface_wish = set_pic(dict_id, listing[0], element_dict)
            else:
                surface_wish = set_pic(dict_id, listing[0], element_dict, type_pic=2)
        flags = True
        while flags:
            screen.fill((0, 0, 0))
            screen.blit(wish_back, (0, 0))
            if wish_times == 1 or wish_times == 10:
                screen.blit(surface_wish, (0, 0))
            else:
                screen.blit(n_wish_surface, (0, 0))
                screen.blit(font_40.render(f"五星总计：{five_star_temporary}    无主的星尘：{xing_chen_temporary}", True,
                                           (255, 255, 255)), (100, 450))
                screen.blit(font_40.render(f"四星总计：{four_star_temporary}   无主的星辉：{xing_hui_temporary}", True,
                                           (255, 255, 255)), (100, 500))
                num1 = 0
                num2 = 0
                for i in n_wish_list:
                    if num1 >= 9:
                        num1 = 0
                        num2 += 1
                    font_n_wish = font_15.render(str(have_data[i[0]] - i[1]), True, (0, 0, 0))
                    screen.blit(font_n_wish,
                                ((85 - font_n_wish.get_size()[0]) / 2 + 100 + 115 * num1, 145 + 130 * num2))
                    if have_data[i[0]] - i[1] == 0:
                        black1 = pygame.surface.Surface((85, 105)).convert_alpha()
                        black1.fill((0, 0, 0, 120))
                        screen.blit(black1, (100 + 115 * num1, 60 + 130 * num2))
                    num1 += 1
                screen.blit(ok_button, ((1200 - ok_button.get_size()[0]) / 2, 580))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m1.play()
                    flags = False
            pygame.display.flip()
        for i in listing:
            print(dict_id[i])
        if wish_stage == 2:
            if dict_data["user_want"] != 0:
                user_want_pic = user_want_list[dict_data["user_want_num"]]
            else:
                user_want_pic = user_want_list[0]
        chen_hui_surface = chen_hui(xing_chen, dict_data, font_20)
        yuan_shi_surface = font_15.render(str(dict_data["yuan_shi"]), True, (255, 255, 255))
        jiu_chan_ball_surface = set_ball_surface(font_15, dict_data, pic_jiu_chan_ball, "jiu_chan_ball")
        meet_ball_surface = set_ball_surface(font_15, dict_data, pic_meet_ball, "meet_ball")
        if wish_stage == 1:
            text_ = "character"
        elif wish_stage == 2:
            text_ = "weapon"
        elif wish_stage == 3:
            text_ = "normal"
        else:
            text_ = "starter"
        load_dict(dict_data, uid)
        last_img1 = set_last_surface(dict_data, f"five_star_{text_}_next", 1)
        last_img2 = set_last_surface(dict_data, f"five_star_{text_}_last", 2)
        print('\n')


def starter():
    def set_surface(text12: str, color: tuple = (255, 198, 7)):
        surface_user4 = pygame.surface.Surface((650, 50))
        surface_user11 = pygame.surface.Surface((646, 46))
        surface_user11.fill(color)
        surface_user4.blit(surface_user11, (2, 2))
        surface_user21 = pygame.surface.Surface((2, 50))
        surface_user4.blit(surface_user21, (500, 0))
        text1 = font_30.render("删除", True, (0, 0, 0))
        surface_user4.blit(text1, ((150 - text1.get_size()[0]) / 2 + 500, (50 - text1.get_size()[1]) / 2))
        text1 = font_30.render(f"{text12}", True, (0, 0, 0))
        surface_user4.blit(text1, (20, (50 - text1.get_size()[1]) / 2))
        return surface_user4

    def set_change(bg2: pygame.surface.Surface):
        cb = pygame.image.load("./files/image/closing_button.png")
        change_user_surface1 = pygame.surface.Surface((960, 540)).convert_alpha()
        change_user_surface1.fill((0, 0, 0, 0))
        change_user_surface1.blit(bg2, (0, 0))
        change_user_surface1.blit(font_30.render("用户列表", True, (255, 198, 7)), (100, 80))
        for j in range(len(user_data["user_total"])):
            if user_data["user_total"][j] == user_data["user_now"]:
                surface1 = set_surface(f"{user_data['user_total'][j]}(当前用户)", (0, 162, 232))
            else:
                surface1 = set_surface(f"{user_data['user_total'][j]}")
            change_user_surface1.blit(surface1, (100, 120 + j * 65))
        surface_button = pygame.surface.Surface((200, 50))
        surface_button1 = pygame.surface.Surface((196, 46))
        surface_button1.fill((255, 198, 7))
        surface_button.blit(surface_button1, (2, 2))
        text1 = font_30.render("添加用户", True, (0, 0, 0))
        surface_button.blit(text1, ((200 - text1.get_size()[0]) / 2, (50 - text1.get_size()[1]) / 2))
        change_user_surface1.blit(surface_button, (380, 450))
        change_user_surface1.blit(cb, (900, 20))
        return change_user_surface1

    screen1 = pygame.display.set_mode((960, 540))
    m1 = pygame.mixer.Sound('files/music/click.mp3')
    if os.path.isfile(f'./files/jsons/user_data.json'):
        with open(f'./files/jsons/user_data.json', 'r', encoding='utf-8') as file_data:
            user_data = json.load(file_data)
    else:
        user_data = {
            "user_now": 100000000,
            "user_total": [100000000]
        }
    bg_num1 = 30
    bg_num = random.randint(10, bg_num1)
    bg1 = pygame.transform.scale(pygame.image.load(f"./files/image/starter/background/{bg_num}.png"), (960, 540))
    button = pygame.surface.Surface((290, 47))
    button.fill((255, 197, 7))
    surface_button2 = pygame.surface.Surface((2, 47))
    surface_button2.fill((239, 191, 0))
    button.blit(surface_button2, (150, 0))
    font_30 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 20)
    text = font_30.render("开启模拟器", True, (0, 0, 0))
    button.blit(text, ((150 - text.get_size()[0]) / 2, (46 - text.get_size()[1]) / 2))
    text = font_30.render("用户设置", True, (0, 0, 0))
    button.blit(text, (150 + (140 - text.get_size()[0]) / 2, (46 - text.get_size()[1]) / 2))
    run3 = True
    fps_num = 0
    while run3:
        fps_num += 1
        if fps_num > 400:
            fps_num = 0
            if bg_num >= bg_num1:
                bg_num = 10
            else:
                bg_num += 1
            bg1 = pygame.transform.scale(pygame.image.load(f"./files/image/starter/background/{bg_num}.png"),
                                         (960, 540))
        if fps_num <= 50:
            bg1.set_alpha(int(5.1 * fps_num))
        screen1.blit(bg1, (0, 0))
        screen1.blit(button, (584, 423))
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 584 < mx < 734 and 423 < my < 469:
                    run3 = False
                    m1.play()
                elif 734 < mx < 874 and 423 < my < 469:
                    m1.play()
                    run4 = True
                    change_user_surface = set_change(bg1)
                    while run4:
                        screen1.blit(bg1, (0, 0))
                        screen1.blit(change_user_surface, (0, 0))
                        for event1 in pygame.event.get():
                            if event1.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event1.type == pygame.MOUSEBUTTONDOWN:
                                mx1, my1 = pygame.mouse.get_pos()
                                if 380 < mx1 < 580 and 450 < my1 < 520:
                                    m1.play()
                                    if len(user_data["user_total"]) >= 5:
                                        message_box(screen1, "最多新建五个用户", "提示", change_user_surface,
                                                    type1=2)
                                    else:
                                        while True:
                                            new_id = random.randint(100000000, 999999999)
                                            id_bool = True
                                            for ids in user_data["user_total"]:
                                                if new_id == int(ids):
                                                    id_bool = False
                                            if id_bool:
                                                break
                                        user_data["user_total"].append(new_id)
                                        change_user_surface.blit(set_surface(str(user_data["user_total"][-1])),
                                                                 (100, 55 + len(user_data["user_total"] * 65)))
                                        with open(f'./files/jsons/user_data.json', 'w',
                                                  encoding='utf-8') as file_data:
                                            file_data.write(json.dumps(user_data, ensure_ascii=False))
                                if 900 < mx1 < 960 and 0 < my1 < 60:
                                    m1.play()
                                    run4 = False
                                for im in range(len(user_data["user_total"])):
                                    if 600 < mx1 < 750 and 120 + im * 65 < my1 < 170 + im * 65:
                                        m1.play()
                                        if len(user_data["user_total"]) <= 1:
                                            message_box(screen1, "至少需要有一个用户", "提示", change_user_surface,
                                                        type1=2)
                                        elif str(user_data["user_total"][im]) == str(user_data["user_now"]):
                                            user_data["user_total"].pop(im)
                                            user_data["user_now"] = user_data["user_total"][0]
                                            change_user_surface = set_change(bg1)
                                            with open(f'./files/jsons/user_data.json', 'w',
                                                      encoding='utf-8') as file_data:
                                                file_data.write(json.dumps(user_data, ensure_ascii=False))
                                        else:
                                            user_data["user_total"].pop(im)
                                            change_user_surface = set_change(bg1)
                                            with open(f'./files/jsons/user_data.json', 'w',
                                                      encoding='utf-8') as file_data:
                                                file_data.write(json.dumps(user_data, ensure_ascii=False))
                                    elif 100 < mx1 < 600 and 120 + im * 65 < my1 < 170 + im * 65:
                                        m1.play()
                                        user_data["user_now"] = user_data["user_total"][im]
                                        change_user_surface = set_change(bg1)
                        pygame.display.flip()
        pygame.display.flip()
    pygame.quit()
    return user_data["user_now"]


run56 = True
try:
    a = pygame.image.load("./files/image/wish/prize/w5.png")
except FileNotFoundError:
    run56 = False
    screen67 = pygame.display.set_mode((900, 140))
    font_404 = pygame.font.Font(get_resource_path('./files/hk4e_zh-cn.ttf'), 40)
    font_41 = font_404.render("请先运行downloader.exe", True, (255, 255, 255))
    run16 = True
    while run16:
        screen67.blit(font_41, ((900 - font_41.get_size()[0]) / 2, 20))
        pygame.display.flip()
        for event67 in pygame.event.get():
            if event67.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
if run56:
    while True:
        pygame.init()
        pygame.mixer.init()
        UID = starter()
        wish(UID)
        pygame.quit()
