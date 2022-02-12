"""
Filepaths
"""
def absolute_filepath():
    return "/"


def fonts_filepath():
    return f"{absolute_filepath()}fonts"


def watermarks_filepath():
    return f"{absolute_filepath()}resources/images/watermarks/"


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
def watermark_font():
    return "luckiestguy-regular"


def watermark_text(username):
    return f"FOLLOW @{username}"


def watermark_size():
    return 30
