import os
import sys
import io

from PIL import Image, ImageDraw, ImageFont

from models.shemas import CardData
from src.config import PATH_TO_CARD_SOURCE, PATH_TO_PHOTOS, PATH_TO_CARDS

# 1051 x 685

font_file = os.path.join(PATH_TO_CARD_SOURCE, 'bahnschrift.ttf')
font = ImageFont.truetype(font_file, size=35)
font.set_variation_by_name('SemiBold')
font_2 = ImageFont.truetype(font_file, size=22)
font_2.set_variation_by_name('SemiBold')


def merge(face_: Image) -> Image:
    card_name = 'card_background.png'
    card_ = Image.open(os.path.join(PATH_TO_CARD_SOURCE, card_name))
    w = card_.size[0]
    h = card_.size[1]
    im = Image.new("RGBA", (w, h))
    im.paste(face_, (int(w * 0.60), int(h * 0.11)))
    im.paste(card_, mask=card_)
    return im


def face_preprocess(content: bytes) -> Image or None:
    image = Image.open(io.BytesIO(content))
    # TO DO
    # check size w x h (247 x 328)
    # find face
    # cut  247 x 328
    # delete metadata
    return image


def gen_fake_card(card_data_: CardData, photo_name) -> os.path:
    face = Image.open(os.path.join(PATH_TO_PHOTOS, photo_name))  # TODO
    new_card = merge(face)

    pencil = ImageDraw.Draw(new_card)
    pencil.text((46, 112), text=card_data_.last_name, font=font, fill='white', size=36)
    pencil.text((46, 151), text=card_data_.name, font=font, fill='white', size=36)
    pencil.text((46, 190), text=card_data_.surname, font=font, fill='white', size=36)
    pencil.text((46, 401), text=f'Корпус {card_data_.first_corp_number}. {card_data_.second_corp_number}',
                font=font_2,
                fill='white', size=36)
    card_path = os.path.join(PATH_TO_CARDS, card_data_.session_key + '.png')
    new_card.save(card_path)

    return card_path


def metadata_delete_by_path(photo_path: str) -> None:
    image = Image.open(photo_path)  # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(photo_path)


def metadata_delete_by_obj(image: Image) -> Image:
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    return image_without_exif
