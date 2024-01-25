"""
Imports
"""
from moviepy.editor import *
import youtube_dl
from TikTokApi import TikTokApi

from helpers import constants
from helpers import templates

"""
Constants
"""
ABSOLUTE_FILEPATH = constants.absolute_filepath()
VIDEO_DOWNLOADS_FILEPATH = constants.video_downloads_filepath()
VIDEO_OUTPUTS_FILEPATH = constants.video_outputs_filepath()
VIDEO_TEMPLATES_FILEPATH = constants.video_templates_filepath()

WATERMARK_ROTATE = 10
WATERMARK_OPACITY = 0.9


"""
Return filepaths of where to get/save videos
"""
def get_video_filepath(dir, tweet_id=None, dur=None, height=1080):
    if dir == "downloads":
        return f"{VIDEO_DOWNLOADS_FILEPATH}{tweet_id}.mp4"
    elif dir == "outputs":
        return f"{VIDEO_OUTPUTS_FILEPATH}{height}x1080/{tweet_id}.mp4"
    elif dir == "templates":
        return f"{VIDEO_TEMPLATES_FILEPATH}{height}x1080/{dur}.mp4"


"""
Download video from twitter with youtube-dl
"""
def download_twitter_video(tweet_url, tweet_id):

    # Download video from twitter and save
    ydl_opts = {'outtmpl': get_video_filepath("downloads", tweet_id=tweet_id)}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([tweet_url])


"""
Download video from tiktok with tiktokapi
"""
def download_tiktok_video(tiktok_url, tiktok_id):

    # Download video from tiktok and save
    verify_fp = "verify_xxx"
    api = TikTokApi(custom_verify_fp=verify_fp)
    video = api.video(url="https://vm.tiktok.com/ZMLra6w1C/")

    # Bytes of the TikTok video
    video_data = video.bytes()

    with open(get_video_filepath("downloads", tweet_id=tiktok_id), "wb") as out_file:
        out_file.write(video_data)


"""
Add caption & watermark to video
"""
def generate_video(tweet_id, timestamp,
                   caption_height, caption_filepath,
                   watermark_filepath,
                   video_height=1080, video_width=1080):

    # Render output video size
    RENDER_VIDEO_HEIGHT = int(video_height)
    RENDER_VIDEO_WIDTH = int(video_width)

    # Set spacing between caption and video
    # Set video padding (left, right)
    if RENDER_VIDEO_HEIGHT == 1080:
        VIDEO_CAPTION_SPACING = 10
        VIDEO_PADDING = 10
    elif RENDER_VIDEO_HEIGHT == 1920:
        VIDEO_CAPTION_SPACING = 25
        VIDEO_PADDING = 0
        # Reels preview crops the video
        # So resize the video to be smaller
        REELS_VIDEO_WIDTH = 725
        REELS_VIDEO_HEIGHT = 1450
        REELS_VIDEO_CAPTION = 800
        REELS_VIDEO_TOP_PADDING = 275

    """
    Load tweet video
    """
    tweet_video = VideoFileClip(
        get_video_filepath("downloads", tweet_id=tweet_id))

    """
    Get template video, previously-created templates
    """
    rounded_video_duration = templates.round_down_duration(
        tweet_video.duration)
    template = VideoFileClip(get_video_filepath(
        "templates", dur=rounded_video_duration, height=RENDER_VIDEO_HEIGHT))

    """
    Create caption video from image
    """
    # Resize to fit video width if 1920x1080
    if RENDER_VIDEO_HEIGHT == 1080:
        caption = (ImageClip(caption_filepath)
                   .set_duration(rounded_video_duration))

    elif RENDER_VIDEO_HEIGHT == 1920:
        caption = (ImageClip(caption_filepath)
                   .set_duration(rounded_video_duration).resize(width=REELS_VIDEO_CAPTION))

    """
    Calculate resize ratio for video if 1080x1080 (square format)
    """
    resize_ratio = 0

    # Calculate resize ratio for 1080x1080 (square format)
    if RENDER_VIDEO_HEIGHT == 1080:

        # If height > width
        # Resize ratio for height
        if (tweet_video.size[1] + VIDEO_CAPTION_SPACING + caption_height + VIDEO_PADDING) > (tweet_video.size[0]):
            resize_ratio = (RENDER_VIDEO_HEIGHT - VIDEO_CAPTION_SPACING -
                            caption.size[1] - VIDEO_PADDING*2) / (tweet_video.size[1])

        # Or resize ratio for width
        else:
            resize_ratio = (RENDER_VIDEO_WIDTH -
                            VIDEO_PADDING*2) / (tweet_video.size[0])

        """
        Calculate resize ratio for video if 1920x1080 (reels format)
        """
    elif RENDER_VIDEO_HEIGHT == 1920:

        # If height > width
        # Resize ratio for height
        if (tweet_video.size[1] + VIDEO_CAPTION_SPACING + caption_height) > tweet_video.size[0]:

            # If video length is longer than the reels width limit
            if tweet_video.size[0] > REELS_VIDEO_WIDTH:
                resize_ratio = (REELS_VIDEO_HEIGHT - caption_height -
                                VIDEO_CAPTION_SPACING) / (tweet_video.size[1])

            else:
                resize_ratio = REELS_VIDEO_WIDTH / tweet_video.size[0]

        # Or resize for width
        else:

            # End video should be REELS_VIDEO_WIDTH x 1450
            resize_ratio = REELS_VIDEO_WIDTH / (tweet_video.size[0])

    # Resize video
    tweet_video = tweet_video.resize(resize_ratio)

    """
    Calculate video x, y pos
    """
    # Video x position
    video_new_x_pos = (RENDER_VIDEO_WIDTH - tweet_video.size[0]) / 2

    # Calculate video y pos
    video_new_y_pos = 0

    # If square format
    if RENDER_VIDEO_HEIGHT == 1080:
        video_new_y_pos = (RENDER_VIDEO_HEIGHT / 2) - \
            ((tweet_video.size[1] -
             VIDEO_CAPTION_SPACING - caption.size[1]) / 2)

    # If reels format
    # Move video to slightly below the vertical centre
    # Because instagram previews reels slightly off centre
    elif RENDER_VIDEO_HEIGHT == 1920:
        video_new_y_pos = REELS_VIDEO_TOP_PADDING + \
            (REELS_VIDEO_HEIGHT/2 -
             (tweet_video.size[1] - VIDEO_CAPTION_SPACING - caption.size[1])/2)

    """
    Calc caption pos
    """
    # Caption x, y pos
    caption_x_pos, caption_y_pos = (0, 0)

    # If video-size is 1080
    if RENDER_VIDEO_HEIGHT == 1080:
        caption_x_pos = 0
        caption_y_pos = video_new_y_pos - \
            VIDEO_CAPTION_SPACING - caption.size[1]

    # If video-size is 1920
    elif RENDER_VIDEO_HEIGHT == 1920:

        # Center if video width small
        if caption.size[0] > tweet_video.size[0]:
            caption_x_pos = (RENDER_VIDEO_WIDTH - caption.size[0]) / 2

        # Align with video
        else:
            caption_x_pos = video_new_x_pos

        # Caption y pos
        caption_y_pos = video_new_y_pos - \
            VIDEO_CAPTION_SPACING - caption.size[1]

    """
    Watermark
    """
    # Import watermark
    watermark = (ImageClip(watermark_filepath, transparent=True)
                 .set_duration(rounded_video_duration)
                 .rotate(WATERMARK_ROTATE)
                 .set_opacity(WATERMARK_OPACITY))

    # Update watermark x pos
    # Move it across the screen, right to left
    def calc_watermark_x_pos(t):
        wm_width = watermark.size[0]
        return (RENDER_VIDEO_WIDTH + wm_width) - ((t / rounded_video_duration) * (RENDER_VIDEO_WIDTH + wm_width*3))

    # Watermark y pos
    watermark_y_pos = video_new_y_pos + (tweet_video.size[1] * 0.75)

    """
    Composition
    """
    # Overlay caption and video ontop of blank template
    final_video = CompositeVideoClip([
        template,
        tweet_video.set_position((video_new_x_pos, video_new_y_pos)),
        caption.set_position((caption_x_pos, caption_y_pos)),
        watermark.set_position(lambda t: (
            calc_watermark_x_pos(t), watermark_y_pos))
    ]).set_duration(rounded_video_duration)

    """
    Export video
    """
    filepath = get_video_filepath( "outputs", tweet_id=timestamp, height=RENDER_VIDEO_HEIGHT)
    final_video.write_videofile(
        filepath,
        # Libx264 codec produces weird black frame at start of video
        # Mpeg4 doesn't seem to produce the same glitch
        # Aac audio codec required for audio on ios devices
        codec="libx264",
        audio_codec='aac',
        logger=None)

    return filepath, rounded_video_duration
