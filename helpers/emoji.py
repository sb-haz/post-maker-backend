"""
Imports
"""
import emoji
from helpers import constants


"""
Constants
"""
EMOJI_PLACEHOLDER = constants.emoji_placeholder()


"""
Returns strings without emojis
Returns dictionary of emojis with indexes
"""
def remove_emoji(string):

    string_without_emojis = ""
    emojis = {}

    # Iterate through string
    for index, element in enumerate(string):

        # If not emoji, add to string
        if element not in emoji.UNICODE_EMOJI['en']:
            string_without_emojis += element

        # If emoji, add emoji to emoji dictionary
        # & replace emoji with placeholder
        else:
            string_without_emojis += EMOJI_PLACEHOLDER
            emojis[index] = element

    # return string and emoji list
    return string_without_emojis, emojis
