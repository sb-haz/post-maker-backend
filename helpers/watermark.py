"""
Imports
"""
from PIL import Image, ImageFont, ImageDraw
from helpers import constants


"""
Constants
"""
ABSOLUTE_FILEPATH = constants.ABSOLUTE_FILEPATH()
FONTS_FILEPATH = constants.fonts_filepath()
WATERMARKS_FILEPATH = constants.watermarks_filepath()
WATERMARK_FONT = constants.watermark_font()
WATERMARK_SIZE = constants.watermark_size()


"""
Make an image containing watermark
Returns exact filepath of created watermark
"""
def create_watermark(username, media_type="video"):

    # full watermark text
    watermark_text = constants.watermark_text(username)

    # watermark font and size
    font = ImageFont.truetype(
        f"{FONTS_FILEPATH}/{WATERMARK_FONT}.ttf", WATERMARK_SIZE)
    font_size_x, font_size_y = font.getsize(watermark_text)

    # different bg colour for images and videos
    bg_colour = (0, 0, 0)
    if media_type == "video":
        bg_colour = (235, 135, 140)
    elif media_type == "image":
        bg_colour = (250, 160, 160)

    # create coloured background for caption
    image = Image.new(
        'RGBA', (font_size_x+5*2, font_size_y+5*2), color=bg_colour)
    draw = ImageDraw.Draw(image)

    # draw watermark
    draw.text((5, 5), watermark_text, font=font, fill=(
        255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=1)

    # save watermark
    generated_watermark_filepath = f"{WATERMARKS_FILEPATH}{username}.png"
    image.save(generated_watermark_filepath, 'PNG')

    # return watermarks filepath
    return generated_watermark_filepath
