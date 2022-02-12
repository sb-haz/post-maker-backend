"""
Filepaths
"""
def absolute_filepath():
    return ""


def caption_filepath():
    return f"{absolute_filepath()}resources/images/captions/"


def emojis_filepath():
    return f"{absolute_filepath()}resources/emojis/"


def fonts_filepath():
    return f"{absolute_filepath()}resources/fonts/"


def quote_output_filepath():
    return f"{absolute_filepath()}resources/images/outputs/quote_render.png"


def quote_template_filepath():
    return f"{absolute_filepath()}resources/images/templates/white_1080x1080.png"


def watermarks_filepath():
    return f"{absolute_filepath()}resources/images/watermarks/"


"""
Fonts
"""
def tweet_font():
    return "chirp-standard-light.ttf"


def watermark_font():
    return "luckiest-guy-regular.ttf"

"""
Captions
"""
def default_caption(tweet_author):
    return f"😂😂😂 (Twitter @ {tweet_author})"


"""
Emojis
"""
def emoji_placeholder():
    return "█"


"""
Watermarks
"""
def watermark_text(username):
    return f"FOLLOW @{username}"


def watermark_size():
    return 30
