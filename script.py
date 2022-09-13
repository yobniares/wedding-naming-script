import os
import sys
from PIL import Image
from PIL import Image, ImageDraw, ImageFont

import csv
import enum

##
# Конфиги
##


# Имя файла таблицы
csv_filename = './example.csv'
# Имя файла шаблона
template_filename = "./template.png"
# Имя папки сохранения (/ в конце нужен)
save_folder = "./example/"

# шрифт имени
font_name = {
    "family": './fonts/AmadeusAP.otf',
    "size": 120,
    "color": "#000000",
    "bold": False
}
# отступ сверху для имени (в доле от высоты изображения)
name_margin_factor = 0.233

# шрифт верхней надписи
font_upper = {
    "family": './fonts/AmadeusAP.otf',
    "size": 80,
    "color": "#000000",
    "bold": True
}
# отступ сверху для верхней надписи (в доле от высоты изображения)
upper_margin_factor = 0.18


# статус приглашения
class InvitedStatus(enum.Enum):
    none = ''
    male = 'm'
    female = 'f'
    pair = 'p'


# словарь статусов (верхняя надпись)
dict_status = {
    InvitedStatus.male: "Дорогой",
    InvitedStatus.female: "Дорогая",
    InvitedStatus.pair: "Дорогие",
    InvitedStatus.none: ""
}

# рисует надписи по настройкам и сохраняет файл по указанному адресу


def save_image(text, savepath, inv_status):

    with Image.open(template_filename) as img:
        W, H = img.size
    with Image.open(template_filename) as im:
        draw_text = ImageDraw.Draw(im)
        text_upper = dict_status[inv_status]
        draw_text.text(
            (W/2, H*upper_margin_factor),
            text_upper,
            font=ImageFont.truetype(
                font_upper["family"], size=font_upper["size"]),
            fill=font_upper["color"],
            align='center',
            anchor="mm",
            stroke_width=(font_upper["bold"] and 1 or 0),
            stroke_fill=font_upper["color"]
        )
        draw_text.text(
            (W/2, H*name_margin_factor),
            text,
            font=ImageFont.truetype(
                font_name["family"], size=font_name["size"]),
            fill=font_name["color"],
            align='center',
            anchor="mm",
            stroke_width=(font_name["bold"] and 1 or 0),
            stroke_fill=font_name["color"]
        )

        im.save(savepath)


def main():
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        prev_name = ""
        prev_num = 0
        print("Добро пожаловать в интерфейс Пригласительных! начинаем работу")
        print("p - пара, m - муж, f - жен")
        for row in reader:
            number = row[0]
            name = row[1]
            surname = row[2]
            identifier = row[4]
            if number == "" or name == "":
                continue

            inv_status = InvitedStatus.none
            text = ""
            savename = ""
            if prev_name != "":
                # print multiple
                inv_status = InvitedStatus.pair
                text = "%s и %s" % (prev_name, name)
                savename = "%s.%s. %s.png" % (prev_num, number, text)
                prev_num = 0
                prev_name = ""
                save_image(text, save_folder+savename, inv_status)
                continue

            print("%s. %s %s вердикт?" % (number, name, surname))
            while True:
                if identifier != "":
                    if identifier in ("p", "m", "f"):
                        ans = InvitedStatus(identifier)
                    elif identifier == "-":
                        break
                    else:
                        ans = input()
                else:
                    ans = input()

                if ans == InvitedStatus.male or ans == InvitedStatus.female:
                    inv_status = ans
                    text = name
                    savename = "%s. %s.png" % (number, text)
                    break
                elif ans == InvitedStatus.pair:
                    prev_name = name
                    prev_num = number
                    break
                else:
                    print("Введите ещё раз")

            if inv_status == InvitedStatus.none:
                continue

            save_image(text, save_folder+savename, inv_status)


if(__name__ == '__main__'):
    main()
