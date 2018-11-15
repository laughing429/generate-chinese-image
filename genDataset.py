#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# Create on: 2018-11-15
# Author: Lyu
# Annotation: 利用pygame生成图片

import pygame
from glob import glob
import random
import os
from uuid import uuid1
import numpy as np
from multiprocessing import Pool
def yes_or_no():
    return np.random.randint(0, 2)

def random_text(num = 10):
    info_list = []
    for f in glob('*.txt'): # 包含文本的文件
        with open(f, 'r', encoding='utf-8') as file:
            info_list.append(''.join([part.strip().replace('\t', '') for part in file.readlines()]))
    info_str = ''.join(info_list)
    start = random.randint(0, len(info_str)-11)
    end = start + num
    random_word = info_str[start:end]

    return random_word

def random_fontsize():
    size = random.randint(13, 27)

    return size

def random_font(font_path):
    font_list = os.listdir(font_path)
    random_font = random.choice(font_list)

    return os.path.join(font_path, random_font)

def random_word_color():
    font_color_choice = [[54, 54, 54], [105, 105, 105]]
    font_color = random.choice(font_color_choice)
    noise = np.array([random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)])
    font_color = (np.array(font_color) + noise).tolist()

    return tuple(font_color)

def random_background_color():
    background_color_choice = [[186, 186, 186], [220, 220, 220]]
    background_color = random.choice(background_color_choice)
    noise = np.array([random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10)])
    background_color = (np.array(background_color) + noise).tolist()

    return tuple(background_color)

def random_rotate():
    angle = np.random.randint(-6, 7)

    return angle

def main(save_dir):
    index = uuid1().__str__()

    # 文本
    text = random_text()
    print(text)

    # 字体
    font = random_font('font')

    # 字号
    font_size = random_fontsize()

    # 字体颜色
    font_color = random_word_color()

    # 背景颜色
    background_color = random_background_color()

    # 倾斜角度
    angle = random_rotate()

    pygame.init()
    font = pygame.font.Font(font, font_size)

    if yes_or_no():
        font.set_bold(int(font_size*1.5)) # 加粗

    font.set_italic(yes_or_no())

    ftext = font.render(text, True, font_color, background_color)

    # 倾斜
    if yes_or_no():
        ftext = pygame.transform.rotate(ftext, angle)

    # 模糊度
    ftext.set_alpha(np.random.random_integers(50, 200))

    # display image
    # w = 640
    # h = 480
    # size = (w, h)
    # screen = pygame.display.set_mode(size)
    # screen.fill((255, 255, 255))
    # screen.blit(ftext, (20, 20))
    # pygame.display.flip()
    #
    # while True:
    #     # gets a single event from the event queue
    #     event = pygame.event.wait()
    #     if event.type == pygame.QUIT:
    #         # stops the application
    #         break

    # 保存文本信息和对应图片名称
    if not os.path.exists(os.path.join(save_dir, 'images')):
        os.mkdir(os.path.join(save_dir, 'images'))

    with open(os.path.join(save_dir, 'label.txt'), 'a+', encoding='utf-8') as file:
        file.write('images/' + '{}.jpg'.format(index) + ' ' + text + '\n')
    pygame.image.save(ftext, os.path.join(save_dir, 'images', '{}.jpg'.format(index)))

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, ['data_set']*50)
    pool.close()