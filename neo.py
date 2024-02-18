import numpy as np
import pygame as pg
import time
from PIL import Image, ImageDraw, ImageFont

import weather
from weather import *

class Matrix:
    def __init__(self, app, font_size=10):
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.katakana = np.array([chr(int('0x30a0', 16) + i) for i in range(96)])
        self.font = pg.font.SysFont('ms mincho', self.FONT_SIZE, bold=True)

        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 750, size=self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()


        #ПОГОДА ТЕМПЕРАТУРА ВЛАЖНОСТЬ СКОРОСТЬ ВЕТРА ОБЛАЧНОСТЬ
        self.weather_data = weather.get_weather()

        self.start_path = 'img/template.jpg' #черный холст
        self.interm_path = 'img/intermediate.jpg'
        self.prefinal_path = 'img/intermediate.jpg'
        self.final_path = 'img/final.jpg'
        self.img = Image.open(self.start_path)
        if self.img.width < app.WIDTH or self.img.height < app.HEIGHT:
            self.img = self.img.resize(app.RES)
            self.img.save(self.start_path)
        self.font = ImageFont.truetype('arial.ttf', size=20+self.app.WIDTH//10) #шрифт времени
        self.widget_font = ImageFont.truetype('arial.ttf', size=10+self.app.WIDTH//15) #шрифт

    def add_rare_data_to_canvas(self): #добавляет дату и день недели РАЗ В СУТКИ
        self.img = Image.open(self.start_path)
        ImageDraw.Draw(self.img).text((app.WIDTH*0.65, app.HEIGHT*0.65), time.strftime('%a'), font=self.widget_font) #Day Of Week (dow)
        ImageDraw.Draw(self.img).text((app.WIDTH*0.6, app.HEIGHT*0.45), time.strftime('%d.%m'), font=self.widget_font) #day&month
        self.img.save(self.interm_path)

    def add_weather_data_to_canvas(self): #добавляет данные о погоде 4 РАЗА в СУТКИ

        self.img = Image.open(self.interm_path)
        ImageDraw.Draw(self.img).text((app.WIDTH*0.5-self.widget_font.size, app.HEIGHT*0.45), self.weather_data[0]+chr(176)+'C', font=self.widget_font) #temperature
        ImageDraw.Draw(self.img).text((app.WIDTH*0.3-self.widget_font.size, app.HEIGHT*0.65), self.weather_data[1]+'%', font=self.widget_font) #humidity
        ImageDraw.Draw(self.img).text((app.WIDTH*0.5-self.widget_font.size, app.HEIGHT*0.65), self.weather_data[2]+'км/ч', font=self.widget_font) #windspeed
        self.img.paste(Image.open(f'img/weather_icons/{self.weather_data[3]}.jpg'), (int(app.WIDTH*0.21), int(app.HEIGHT*0.43)))
        self.img.save(self.prefinal_path)

    def add_time_data_to_canvas(self): #добавляет текущее время КАЖДУЮ СЕКУНДУ
        self.img = Image.open(self.prefinal_path)
        ImageDraw.Draw(self.img).text((app.WIDTH//2-self.font.size*2, app.HEIGHT//2-self.font.size*1.5), time.strftime('%H:%M:%S'), font=self.font)  # >1
        self.img.save(self.final_path)

    def get_time(self, path):
        image = pg.image.load(path)
        image = pg.transform.scale(image, self.app.RES)
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array


    def run(self):
        frames = pg.time.get_ticks()
        self.add_time_data_to_canvas() #постоянно
        self.add_rare_data_to_canvas() #раз в сутки
        self.add_weather_data_to_canvas() #раз в 6 часов
        self.image = self.get_time(self.final_path)
        self.change_chars(frames)
        self.shift_columns(frames)
        self.draw()

    def get_prerendered_chars(self):
        char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    def shift_columns(self, frames):
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    __, red, green, blue = pg.Color(self.image[pos])
                    if red and green and blue:
                        color = (red+green+blue)//3
                        color = color+30 if color < 220 else color
                        color = 0 if color < 10 else color
                        char = self.prerendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color+60)
                        self.app.surface.blit(char, pos)


class MatrixVision:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1920, 1000
        pg.init()
        self.screen = pg.display.set_mode(self.RES)
        self.surface = pg.Surface(self.RES)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self)

    def draw(self):
        self.surface.fill(pg.Color('black'))
        self.matrix.run()
        self.screen.blit(self.surface, (0, 0))

    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            pg.display.set_caption(str(self.clock.get_fps()))
            self.clock.tick()


if __name__ == '__main__':
    app = MatrixVision()
    app.run()
