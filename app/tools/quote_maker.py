"""
Imports
"""
from PIL import Image, ImageFont, ImageDraw
import textwrap
import re
import emoji
import datetime

from helpers import constants
from helpers import emoji

"""
Constants
"""
ABSOLUTE_FILEPATH = constants.absolute_filepath()
CAPTION_FILEPATH = constants.caption_filepath()
EMOJI_FILEPATH = constants.emojis_filepath()
WATERMARK_FILEPATH = constants.watermarks_filepath()


"""
Change text/watermark
"""
FONTS_FILEPATH = constants.fonts_filepath()
TEXT_FONT = constants.tweet_font()
WATERMARK_FONT = constants.watermark_font()
FONT_SIZE = 55
WATERMARK_SIZE = 30

# Text pos
BASE_X_POS = 40
BASE_Y_POS = 0  # 25
LINE_WIDTH = 37
TEXT_PADDING_BOTTOM = 25

# Emoji replacement
EMOJI_PLACEHOLDER = constants.emoji_placeholder()


"""
Create tweet from quote
"""
def generate_quote(text, tweet_id, username):
    # create white background for image
    image = Image.open(constants.quote_template_filepath())

    # convert text to caption image
    caption_filepath, caption_height, timestamp = convert_text_to_image(text,
                                                                        tweet_id,
                                                                        username,
                                                                        draw_watermark=True)
    caption = Image.open(caption_filepath)

    # draw caption
    caption_y_pos = (1080 - caption_height) / 2
    image.paste(caption, (0, int(caption_y_pos)))

    # save
    quote_filepath = f"static/{timestamp}.png"
    image.save(f"{constants.absolute_filepath()}{quote_filepath}", "PNG")
    
    # return
    return quote_filepath


"""
Takes text string and produces a PNG of text
Renders emojis as ios emojis
Adds watermark if enabled
Returns: caption filepath, height of caption
"""
def convert_text_to_image(text, tweet_id, username, draw_watermark=False):

    # Remove emojis from texts
    text, emoji_list = emoji.remove_emoji(text)

    # Calculate num. of lines text will use
    num_of_lines = 0
    for line in textwrap.wrap(text, width=LINE_WIDTH):
        num_of_lines += 1

    # Load font and get font size
    font = ImageFont.truetype(f"{FONTS_FILEPATH}{TEXT_FONT}", FONT_SIZE)
    font_size_y = font.getsize(text)[1]

    # Create blank image based on num. of lines
    # padding above, text, less padding below
    caption_height = BASE_Y_POS + num_of_lines*font_size_y + TEXT_PADDING_BOTTOM

    # Create white background for caption
    image = Image.new('RGBA', (1080, caption_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw text onto image
    x_pos = BASE_X_POS
    y_pos = BASE_Y_POS

    # Replace emojis with emoji code
    # Load emoji
    # Replace background with white
    emoji_codes = {}
    for key, value in emoji_list.items():

        # Replace with emoji code
        emoji_code = '{:x}'.format(ord(value))
        emoji_codes[key] = emoji_code
        
    # Draw watermark
    # Open watermark, add opacity, resize
    def draw_watermark_after_text(first_line_width, line_y_pos, wm_username):
        watermark = Image.open(ABSOLUTE_FILEPATH + f"resources/images/watermarks/{wm_username}.png").convert("RGBA")
        watermark.load()
        watermark.putalpha(int(255*0.8))
        watermark = watermark.resize((int(watermark.width), int(watermark.height)))
        
        # Centre watermark in mid of first line
        watermark_x_pos = (first_line_width - watermark.size[0]) / 2 + x_pos
        watermark_y_pos = line_y_pos + font_size_y - 7
        # Draw watermark
        image.paste(watermark, (int(watermark_x_pos), int(watermark_y_pos)), watermark)
    
    # To calc watermark pos
    first_line_width = 0
    first_line_y_pos = 0

    # Write text on image
    line_num = 0
    # Current total num of chars checked for emojis
    previous_line_len = 0
    for line in textwrap.wrap(text, width=LINE_WIDTH):

        # Write text
        draw.text((x_pos, y_pos), line, font=font, fill=(20, 23, 26))

        # If contains emoji, draw emoji image
        # /4664850/how-to-find-all-occurrences-of-a-substring
        for match in [m.start() for m in re.finditer(EMOJI_PLACEHOLDER, line)]:

            match += line_num
            # Num of chars resets at every new line
            # So keep a tally of total num of chars in previous lines
            line_match = previous_line_len + match

            # Get length of text before match
            pre_match_text_len = font.getsize(line[:match - line_num])[0]

            # Emoji
            current_emoji_code = emoji_codes[line_match]

            # Load emoji image
            upper_code = current_emoji_code.upper()
            emoji_image = Image.open(
                ABSOLUTE_FILEPATH + f"{EMOJI_FILEPATH}{upper_code}.png").convert("RGBA")
            emoji_image.load()

            # Resize emoji
            emoji_image = emoji_image.resize(
                (int(emoji_image.width/2), int(emoji_image.width/2)))

            # Emoji background width/height
            # Slightly bigger width than emoji size
            emoji_bg_w = emoji_image.size[0]
            emoji_bg_h = emoji_image.size[1]

            # Put emoji on white background
            # /9166400/convert-rgba-png-to-rgb-with-pil
            emoji_with_bg = Image.new(
                "RGBA", (emoji_bg_w, emoji_bg_h), (255, 255, 255))
            emoji_with_bg.paste(emoji_image, mask=emoji_image.getchannel('A'))

            # Draw emoji
            image.paste(emoji_with_bg, (pre_match_text_len+40, y_pos+6))

        # Draw watermark
        if draw_watermark == True:
            # Draw watermark after first line
            if line_num == 0:

                # Draw watermark position
                first_line_width = font.getsize(line)[0]
                first_line_y_pos = y_pos

        # Increase line num
        line_num += 1

        # Update total num of chars iterated for emoji
        previous_line_len += len(line)

        # Change y pos to next line
        y_pos += font_size_y + 5

    # Draw watermark after text drawing done
    if draw_watermark == True:
        draw_watermark_after_text(first_line_width, first_line_y_pos, username)

    # Save image
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    caption_filepath = f"{CAPTION_FILEPATH}{timestamp}.png"
    
    # Add outline around caption for debugging
    # image = ImageOps.expand(image,border=2,fill='black')
    # Save image
    image.save(caption_filepath, 'PNG')

    # return filepath and height of caption
    return caption_filepath, caption_height, timestamp