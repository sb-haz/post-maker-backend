"""
Filepaths
"""
def absolute_filepath():
    return "C:/Users/Hasan/Desktop/Post Maker/backend-flask/app/"

def resources_filepath():
    return f"{absolute_filepath()}resources/"

def static_filepath():
    return f"{absolute_filepath()}static/"


"""
Emoji Filepaths
"""
def emojis_filepath():
    return f"{resources_filepath()}emojis/"


"""
Emoji Filepaths
"""
def fonts_filepath():
    return f"{resources_filepath()}fonts/"


"""
Images Filepaths
"""
def caption_filepath():
    return f"{resources_filepath()}images/captions/"


def quote_output_filepath():
    return f"{resources_filepath()}images/outputs/quote_render.png"


def quote_template_filepath():
    return f"{resources_filepath()}images/templates/white_1080x1080.png"


def watermarks_filepath():
    return f"{resources_filepath()}images/watermarks/"


"""
Videos Filepaths
"""
def video_downloads_filepath():
    return f"{resources_filepath()}videos/downloads/"


def video_outputs_filepath():
    return f"{resources_filepath()}videos/outputs/"


def video_templates_filepath():
    return f"{resources_filepath()}videos/templates/"


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
