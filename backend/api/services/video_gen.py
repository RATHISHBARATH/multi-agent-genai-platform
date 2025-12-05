"""Simple text-to-video generator using gTTS for audio and MoviePy to create a slideshow-style MP4.
Produces a short video file path for given script/slides.

Note: Requires ffmpeg installed in system and moviepy & gTTS libraries.
"""
import os, uuid, logging, tempfile
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger('autoscillab.video_gen')

OUTPUT_DIR = os.getenv('VIDEO_OUTPUT_DIR', '/tmp/autoscillab_videos')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _make_slide_image(text: str, width=1280, height=720, bg_color=(18,18,18), fg_color=(255,255,255)):
    # create a simple image with PIL
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # basic font fallback
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 40)
    except Exception:
        font = ImageFont.load_default()
    # wrap text
    lines = []
    words = text.split()
    line = ''
    for w in words:
        if len(line + ' ' + w) > 60:
            lines.append(line.strip())
            line = w
        else:
            line += ' ' + w
    lines.append(line.strip())
    y = 120
    for l in lines[:8]:
        draw.text((80, y), l, font=font, fill=fg_color)
        y += 60
    tmpf = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tmpf.name)
    return tmpf.name

def generate_video_from_slides(slides, lang='en') -> str:
    """slides: list of strings (slide text)
    Returns: path to MP4 file
    """
    if not slides:
        raise ValueError('slides empty')

    assets = []
    audio_files = []
    try:
        for idx, s in enumerate(slides):
            img_path = _make_slide_image(s)
            # TTS audio
            tts = gTTS(text=s, lang=lang)
            audio_tmp = os.path.join(tempfile.gettempdir(), f'audio_{uuid.uuid4().hex}.mp3')
            tts.save(audio_tmp)
            audio_files.append(audio_tmp)
            clip = ImageClip(img_path).set_duration( max(3, len(s.split())/3) )
            clip = clip.set_fps(24)
            clip = clip.set_audio(AudioFileClip(audio_tmp))
            assets.append(clip)
        final = concatenate_videoclips(assets, method="compose")
        out_path = os.path.join(OUTPUT_DIR, f'video_{uuid.uuid4().hex}.mp4')
        final.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac', threads=2, verbose=False, logger=None)
        return out_path
    finally:
        # cleanup temp images/audio
        for f in audio_files:
            try: os.unlink(f)
            except: pass
