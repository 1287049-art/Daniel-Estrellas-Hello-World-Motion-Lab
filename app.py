import html
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.write("A tiny app for experimenting with text, fonts, backgrounds, and motion.")

with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Enter your name or message", value="Hello World", max_chars=100)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Forest", "Lavender", "Ocean", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5,
                      help="1 is slow; 10 is fast.")

backgrounds = {
    "Light": ("#f7f8fc", "#202437"),
    "Dark": ("#10131c", "#f7f8ff"),
    "Sky": ("linear-gradient(135deg, #bde7ff, #f5fcff)", "#173c61"),
    "Sunset": ("linear-gradient(135deg, #ffb36b, #ff6f91, #7656a8)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #153d2b, #4f8b61)", "#f4fff4"),
    "Lavender": ("linear-gradient(135deg, #e9ddff, #c7d7ff)", "#342a5e"),
    "Ocean": ("linear-gradient(135deg, #006d83, #42c6c8)", "#ffffff"),
    "Midnight": ("radial-gradient(circle at top, #27356b, #090b18 75%)", "#ffffff"),
}
bg, text_color = backgrounds[background]

symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄️", "❅", "✻"],
    "Hail": ["🧊", "●"],
    "Wind Gust": ["〰", "💨", "﹏"],
    "Confetti": ["🎉", "✦", "●", "▲", "■", "✿"],
    "Tornado": ["🌪️", "〰", "·"],
}
effect_items = []
if effect != "None":
    rng = random.Random(23)
    count = 54 if effect in ("Rain", "Snow", "Hail", "Confetti") else 28
    for i in range(count):
        symbol = rng.choice(symbols[effect])
        left = rng.randint(0, 100)
        delay = rng.uniform(0, 5)
        duration = rng.uniform(1.5, 5.5) * (1.7 - speed / 12)
        size = rng.randint(12, 27) if effect != "Tornado" else rng.randint(15, 30)
        drift = rng.randint(-90, 90)
        if effect in ("Rain", "Hail"):
            animation = "fall"
        elif effect == "Snow":
            animation = "snowfall"
        elif effect == "Wind Gust":
            animation = "gust"
        elif effect == "Confetti":
            animation = "confetti"
        else:
            animation = "spin"
        effect_items.append(
            f'<span class="particle {animation}" style="left:{left}%;'
            f'animation-delay:-{delay:.2f}s;animation-duration:{duration:.2f}s;'
            f'font-size:{size}px;--drift:{drift}px;--spin:{rng.randint(180,720)}deg;">'
            f'{html.escape(symbol)}</span>'
        )

safe_name = html.escape(name.strip() or "Hello World")
if name_mode == "Ticker Tape":
    name_content = f'<div class="ticker"><span>{safe_name}&nbsp;&nbsp;&nbsp; ✨ &nbsp;&nbsp;&nbsp;{safe_name}&nbsp;&nbsp;&nbsp; ✨ &nbsp;&nbsp;&nbsp;</span></div>'
elif name_mode == "Repeated":
    name_content = '<div class="repeated">' + "<br>".join([safe_name] * 5) + "</div>"
else:
    name_content = f'<div class="center-name">{safe_name}</div>'

# Use only the font names offered in the dropdown; escape text before inserting it into HTML.
font_css = {
    "Arial": "Arial, sans-serif",
    "Courier New": "'Courier New', monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', serif",
    "Verdana": "Verdana, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, sans-serif",
}[font_family]

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; isolation: isolate; overflow: hidden;
  height: 620px; width: 100%; border-radius: 18px;
  background: {bg}; color: {text_color};
  font-family: {font_css}; box-shadow: inset 0 0 0 1px rgba(120,120,150,.18);
}}
.particle-layer {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; z-index:1; }}
.particle {{ position:absolute; top:-12%; opacity:.8; user-select:none; will-change:transform; }}
.center-name {{
  position:absolute; z-index:3; left:5%; right:5%; top:50%;
  transform:translateY(-50%); text-align:center; overflow-wrap:anywhere;
  font-size:{font_size}px; font-weight:700; line-height:1.18;
  text-shadow: 0 2px 16px rgba(0,0,0,.13);
}}
.repeated {{
  position:absolute; z-index:3; inset:7% 4%; text-align:center;
  font-size:{max(18, int(font_size * .72))}px; font-weight:700;
  line-height:1.65; overflow-wrap:anywhere;
}}
.ticker {{ position:absolute; z-index:3; top:43%; white-space:nowrap; font-size:{font_size}px; font-weight:700; }}
.ticker span {{ display:inline-block; padding-left:100%; animation: marquee {max(7, 24 - speed * 1.5)}s linear infinite; }}
@keyframes marquee {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-100%); }} }}
@keyframes fall {{ from {{ transform:translate3d(0,-10vh,0); }} to {{ transform:translate3d(var(--drift),115vh,0); }} }}
@keyframes snowfall {{ 0% {{ transform:translate3d(0,-10vh,0) rotate(0); }} 50% {{ transform:translate3d(calc(var(--drift) * -1),50vh,0) rotate(180deg); }} 100% {{ transform:translate3d(var(--drift),115vh,0) rotate(360deg); }} }}
@keyframes gust {{ 0% {{ transform:translate3d(-20vw,10vh,0) rotate(0); opacity:0; }} 15% {{ opacity:.85; }} 85% {{ opacity:.85; }} 100% {{ transform:translate3d(120vw,-8vh,0) rotate(20deg); opacity:0; }} }}
@keyframes confetti {{ 0% {{ transform:translate3d(0,-10vh,0) rotate(0); }} 100% {{ transform:translate3d(var(--drift),115vh,0) rotate(var(--spin)); }} }}
@keyframes spin {{ 0% {{ transform:translate3d(0,-12vh,0) rotate(0) scale(.8); }} 50% {{ transform:translate3d(var(--drift),50vh,0) rotate(360deg) scale(1.3); }} 100% {{ transform:translate3d(0,115vh,0) rotate(720deg) scale(.8); }} }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker span {{ animation-duration: 20s !important; }}
}}
</style>
</head>
<body>
<div class="stage">
  <div class="particle-layer">{''.join(effect_items)}</div>
  {name_content}
</div>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)
st.caption("Tip: change any control in the sidebar to update the preview. Animations loop continuously inside the preview.")
