from html import escape

def youtube_preview(video_id, title, poster, caption, *, portrait=False):
    shape = " field-video--portrait" if portrait else ""
    return f'''<figure id="field-video-{escape(video_id)}" class="field-video{shape}"><div class="field-video-player"><a class="youtube-preview" href="https://www.youtube.com/watch?v={escape(video_id)}" data-youtube-id="{escape(video_id)}" data-video-title="{escape(title)}" aria-label="Play video: {escape(title)}"><img src="{escape(poster)}" alt="Video preview: {escape(title)}" width="480" height="360" loading="lazy" decoding="async"><span class="field-video-play" aria-hidden="true">▶</span><span class="field-video-label">Play video</span></a></div><figcaption>{escape(caption)} <a href="https://www.youtube.com/watch?v={escape(video_id)}">Watch on YouTube</a></figcaption></figure>'''
