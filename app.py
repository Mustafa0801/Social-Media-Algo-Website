import math
import random
import time

import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Social media algorithms", page_icon="📱", layout="wide")
ss = st.session_state

# ---------- look and feel: white page, light-blue panels, neon-red accents ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&display=swap');
:root{--red:#ff1f4b;--blue:#7dd3fc;--blue-soft:#f0f9ff;--blue-line:#bae6fd;--ink:#0f172a;--body:#334155;--muted:#64748b}
.stApp{background:#ffffff;color:var(--ink)}
.stApp,.stApp p,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp button,.stApp label{font-family:'Sora',system-ui,sans-serif}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}
.block-container{padding-top:2rem;padding-bottom:4rem;max-width:1280px}

/* hero */
.hero{padding:6px 0 20px}
.hero h1{font-size:3.1rem;font-weight:800;letter-spacing:-.035em;line-height:1.05;margin:0 0 10px;padding:0;color:var(--ink)}
.hero h1 span{color:var(--red)}
.hero p{font-size:1.08rem;color:var(--muted);max-width:660px;margin:0;line-height:1.55}

/* info cards, section titles */
.info{background:var(--blue-soft);border:1px solid var(--blue-line);border-radius:18px;padding:20px 24px;height:100%}
.info h4{margin:0 0 8px;font-size:1.05rem;font-weight:700;color:var(--ink);padding:0}
.info p{margin:0;color:var(--body);line-height:1.65;font-size:.95rem}
.sec{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 14px;margin:38px 0 16px}
.sec b{align-self:center;width:6px;height:28px;border-radius:4px;background:var(--red)}
.sec h2{font-size:1.55rem;font-weight:800;margin:0;padding:0;letter-spacing:-.02em;color:var(--ink)}
.sec span{color:var(--muted);font-size:.95rem}

/* panels (containers whose key starts with "panel") */
[class*="st-key-panel"]{background:#fff;border:1px solid var(--blue-line)!important;border-radius:18px!important;
  padding:8px 8px 2px}
.phead{margin:2px 0 2px}
.phead b{display:block;font-size:1.02rem;font-weight:700;color:var(--ink)}
.phead span{font-size:.82rem;color:var(--muted)}
.empty{border:1.5px dashed var(--blue-line);border-radius:14px;padding:46px 20px;text-align:center;color:var(--muted);background:var(--blue-soft)}

/* buttons */
.stButton>button{border-radius:12px;border:1.5px solid var(--blue-line);background:var(--blue-soft);color:var(--ink);
  font-weight:600;min-height:2.7rem;transition:all .15s ease}
.stButton>button:hover{border-color:var(--red);color:var(--red);background:#fff}
.stButton>button[kind="primary"],.stButton>button[data-testid="stBaseButton-primary"]{background:var(--red);border-color:var(--red);
  color:#fff}
.stButton>button[kind="primary"]:hover,.stButton>button[data-testid="stBaseButton-primary"]:hover{background:#e00b39;color:#fff;border-color:#e00b39}
.st-key-actions button{min-height:3.2rem;font-size:1.3rem;border-radius:16px}
[data-testid="stCaptionContainer"]{color:var(--muted)}

/* algorithm steps, filter bubble */
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
@media(max-width:1000px){.steps{grid-template-columns:1fr}}
.step{background:#fff;border:1px solid var(--blue-line);border-radius:16px;padding:18px 16px}
.step i{font-style:normal;display:inline-flex;width:32px;height:32px;border-radius:50%;background:var(--red);color:#fff;
  font-weight:800;align-items:center;justify-content:center;margin-bottom:12px}
.step p{margin:0;font-size:.92rem;color:var(--body);line-height:1.5}
.bubble{border-left:5px solid var(--red);background:var(--blue-soft);border-radius:0 18px 18px 0;padding:22px 28px}
.bubble p{margin:0 0 12px;color:var(--body);max-width:920px;line-height:1.7}
.bubble p:last-child{margin:0;color:var(--ink);font-weight:700}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "Cooking": ("#ff662e", "#822b05"),
    "Fitness": ("#22c27a", "#0b4a2d"),
    "Gaming": ("#7b6cff", "#241a6b"),
    "Travel": ("#5fc1eb", "#053a5b"),
    "Music": ("#ff5c8a", "#6b1230"),
    "Tech": ("#ffdb49", "#db9f07"),
    "Comedy": ("#a3e635", "#3f6212"),
    "Science": ("#2dd4bf", "#0f5f56"),
}

# slightly deeper colors for the pie chart
PIE_COLORS = {
    "Cooking": "#d33f00", "Travel": "#5fc1eb", "Fitness": "#00d54b", "Gaming": "#8e3dff",
    "Tech": "#ffd632", "Music": "#ff3f76", "Comedy": "#c3ff36", "Science": "#0de1e4",
}


VIDEOS = [
    # ---- Cooking ----
    {"title": "Crispy chili oil noodles in 5 minutes", "creator": "@noodlenights",
        "topics": ["Cooking"], "seconds": 30, "views": "1.2M",
        "desc": "A fast weeknight noodle recipe using pantry staples."},
    {"title": "The best cake ever", "creator": "@bakingbulletin",
        "topics": ["Cooking"], "seconds": 50, "views": "4M",
        "desc": "Recipe for a delicious chocolate cake."},
    {"title": "Best meals for $5 or less", "creator": "@foodhacks",
        "topics": ["Cooking"], "seconds": 30, "views": "1M",
        "desc": "Best food hacks to make cheap meals that taste great."},
    {"title": "Secret behind fast food fries", "creator": "@sara213",
        "topics": ["Cooking"], "seconds": 45, "views": "200K",
        "desc": "How fast food restaurants make their fries so crispy and golden."},

    # ---- Fitness ----
    {"title": "10-minute core workout, no equipment", "creator": "@moveandmore",
        "topics": ["Fitness"], "seconds": 35, "views": "860K",
        "desc": "Five core exercises you can do on the living room floor."},
    {"title": "Beginner workout routine", "creator": "@bruno_fitness",
        "topics": ["Fitness"], "seconds": 55, "views": "300K",
        "desc": "Weekly workout routine for beginners."},
    {"title": "Stretching routine for stiff mornings", "creator": "@flexwithfern",
        "topics": ["Fitness"], "seconds": 40, "views": "620K",
        "desc": "Six gentle stretches to loosen up your back and hips."},
    {"title": "Training for your first 5K", "creator": "@runwithrita",
        "topics": ["Fitness"], "seconds": 50, "views": "410K",
        "desc": "An eight-week plan that takes you from the couch to the finish line."},

    # ---- Travel ----
    {"title": "Experiencing the northern lights", "creator": "@scandinaviantravels",
        "topics": ["Travel"], "seconds": 20, "views": "10M",
        "desc": "A stunning time-lapse of the aurora borealis in Norway."},
    {"title": "Camping in rainy forest", "creator": "@outdooradventures",
        "topics": ["Travel"], "seconds": 60, "views": "70K",
        "desc": "A rainy weekend with a tent and a campfire."},
    {"title": "Hidden beaches of Sicily", "creator": "@islandhopper",
        "topics": ["Travel"], "seconds": 35, "views": "1.8M",
        "desc": "Five quiet coves that most tourists never find."},
    {"title": "Packing a carry-on for two weeks", "creator": "@lightpacker",
        "topics": ["Travel"], "seconds": 45, "views": "950K",
        "desc": "How to fit two weeks of clothes into one small bag."},

    # ---- Gaming ----
    {"title": "5 free games on pc!", "creator": "@mike40",
        "topics": ["Gaming"], "seconds": 30, "views": "200K",
        "desc": "Top games available on steam that you can play right now."},
    {"title": "Tips to get better at shooters", "creator": "@frankthetank",
        "topics": ["Gaming"], "seconds": 50, "views": "150K",
        "desc": "Tips for beginners to improve your gameplay."},
    {"title": "Games coming out next month", "creator": "@intergame_news",
        "topics": ["Gaming"], "seconds": 40, "views": "700K",
        "desc": "The most anticipated games coming out december 2026"},
    {"title": "Retro consoles worth collecting", "creator": "@pixelvault",
        "topics": ["Gaming"], "seconds": 35, "views": "480K",
        "desc": "Classic consoles that are still affordable and fun to play."},

    # ---- Tech ----
    {"title": "The chip inside your phone, explained", "creator": "@siliconsketch",
        "topics": ["Tech"], "seconds": 45, "views": "540K",
        "desc": "What a processor does, in plain language."},
    {"title": "The next gen robots", "creator": "@metalmech",
        "topics": ["Tech"], "seconds": 30, "views": "1.2M",
        "desc": "These new humanoid robots are more lifelike than ever before."},
    {"title": "Phone battery myths, debunked", "creator": "@chargecheck",
        "topics": ["Tech"], "seconds": 40, "views": "2.1M",
        "desc": "Does overnight charging really hurt your battery? Here is the truth."},
    {"title": "How to spot a phishing email", "creator": "@safebyte",
        "topics": ["Tech"], "seconds": 35, "views": "890K",
        "desc": "Four warning signs that an email is trying to trick you."},

    # ---- Music ----
    {"title": "Beginner guitar chords you can learn tonight", "creator": "@sixstringsam",
        "topics": ["Music"], "seconds": 40, "views": "1.5M",
        "desc": "Four open chords that cover hundreds of popular songs."},
    {"title": "How to mix your first song", "creator": "@studiosessions",
        "topics": ["Music"], "seconds": 60, "views": "380K",
        "desc": "Balance vocals, drums and bass with free software."},
    {"title": "How lo-fi beats are made", "creator": "@tapeloop",
        "topics": ["Music"], "seconds": 30, "views": "2.7M",
        "desc": "Dusty samples, soft drums and a little tape hiss."},
    {"title": "Is the vinyl comeback worth it?", "creator": "@spinthisrecord",
        "topics": ["Music"], "seconds": 45, "views": "260K",
        "desc": "Sound quality, cost and why people are buying records again."},

    # ---- Comedy ----
    {"title": "Stand-up: my smart fridge hates me", "creator": "@jokesbyjo",
        "topics": ["Comedy"], "seconds": 25, "views": "3.3M",
        "desc": "A comedian argues with an appliance that judges her midnight snacks."},
    {"title": "Cats vs the vacuum cleaner", "creator": "@pawsandlaughs",
        "topics": ["Comedy"], "seconds": 20, "views": "6M",
        "desc": "Five cats react to a robot vacuum, with dramatic commentary."},
    {"title": "Office small talk survival guide", "creator": "@deskdramas",
        "topics": ["Comedy"], "seconds": 40, "views": "1.1M",
        "desc": "A sketch about the weather chat that never ends."},
    {"title": "Parents try to use teen slang", "creator": "@familyfunnies",
        "topics": ["Comedy"], "seconds": 30, "views": "4.5M",
        "desc": "It goes about as well as you would expect."},

    # ---- Science ----
    {"title": "Why the sky is blue (and sunsets are red)", "creator": "@labcoatlive",
        "topics": ["Science"], "seconds": 35, "views": "2.2M",
        "desc": "How sunlight scatters in the atmosphere, in 35 seconds."},
    {"title": "Black holes in 60 seconds", "creator": "@cosmicbits",
        "topics": ["Science"], "seconds": 60, "views": "3.8M",
        "desc": "What happens when a star collapses, and what an event horizon is."},
    {"title": "How vaccines train your immune system", "creator": "@cellstories",
        "topics": ["Science"], "seconds": 45, "views": "720K",
        "desc": "A simple animation of how your body learns to fight a virus."},
    {"title": "The surprising physics of a spinning top", "creator": "@forcefield",
        "topics": ["Science"], "seconds": 30, "views": "510K",
        "desc": "Why a top stays upright while it spins and falls when it slows."},

    # ---- Multi-topic videos ----
    {"title": "How to make easy high-protein meals", "creator": "@nicklifts",
        "topics": ["Fitness", "Cooking"], "seconds": 60, "views": "750K",
        "desc": "Simple recipes for nutritious, protein-rich meals."},
    {"title": "Three days in Lisbon on a small budget", "creator": "@wanderlist",
        "topics": ["Travel", "Cooking"], "seconds": 60, "views": "2.4M",
        "desc": "Where to eat, walk and stay without overspending."},
    {"title": "Cycling across Europe", "creator": "@danielonwheels",
        "topics": ["Travel", "Fitness"], "seconds": 50, "views": "2M",
        "desc": "My journey from Portugal to Italy on a bike."},
    {"title": "Building a PC from scratch", "creator": "@techbuilds",
        "topics": ["Gaming", "Tech"], "seconds": 55, "views": "3M",
        "desc": "The best parts to build a gaming PC in 2026."},
    {"title": "Game development 101", "creator": "@rustprogramming",
        "topics": ["Gaming", "Tech"], "seconds": 70, "views": "200K",
        "desc": "The most important things to know about game development."},
    {"title": "Songs reimagined as sea shanties", "creator": "@shantysquad",
        "topics": ["Music", "Comedy"], "seconds": 30, "views": "5.1M",
        "desc": "Pop hits sung by a very serious crew of sailors."},
    {"title": "Why songs get stuck in your head", "creator": "@brainbeats",
        "topics": ["Music", "Science"], "seconds": 45, "views": "1.3M",
        "desc": "The psychology behind earworms and how to get rid of them."},
    {"title": "Science experiments gone hilariously wrong", "creator": "@oopslab",
        "topics": ["Comedy", "Science"], "seconds": 40, "views": "2.9M",
        "desc": "Exploding soda, collapsing towers and one very confused hamster."},
]


START_PAUSED = True  # start paused so the user can read the title and description before the clock starts
POINTS = {"watch": 1, "liked": 4, "commented": 5, "followed": 8}
SKIP_LIMIT = 1      # leaving after this many seconds or fewer counts as a skip
SKIP_PENALTY = 2
AWAY_LIMIT = 4      # if the page was frozen longer than this (tab hidden), pause the clock

# ----- recommendation settings -----
BASE_WEIGHT = 3        # every topic starts with this weight, so a 0-point topic can still appear
RECENT_BLOCK = 5       # a video can't repeat until this many other videos have been shown
FATIGUE_WINDOW = 5     # look at this many of the latest videos for topic repetition
FATIGUE = 0.3          # weight multiplier for each recent video sharing a topic
EXPLORE_CHANCE = 0.20  # chance of ignoring points entirely and picking any eligible video

ss.setdefault("index", random.randrange(len(VIDEOS)))   # start on a random video
ss.setdefault("history", [ss.index])    # videos shown so far, newest last
ss.setdefault("points", {t: 0 for t in COLORS})
ss.setdefault("started", time.time())   # when the current video began
ss.setdefault("awarded", 0)             # seconds already paid out for this video
ss.setdefault("last_tick", time.time()) # last time any timer code ran
for key in ("liked", "commented", "followed"):
    ss.setdefault(key, set())
ss.setdefault("paused", START_PAUSED)
ss.setdefault("paused_at", ss.started)


def add_points(n):
    for topic in VIDEOS[st.session_state.index]["topics"]:
        ss.points[topic] += n
        ss.points[topic] = max(ss.points[topic], 0)


def sync_clock():
    """If the browser tab was hidden/frozen, don't count that time as watching."""
    now = time.time()
    if ss.paused:                       # nothing is playing, so there is nothing to correct
        ss.last_tick = now
        return
    gap = now - ss.last_tick
    if gap > AWAY_LIMIT:
        ss.started += gap
    ss.last_tick = now


def watched_seconds():
    return min(int(elapsed()), VIDEOS[ss.index]["seconds"])


def pay_watchtime():
    sync_clock()
    secs = watched_seconds()
    if secs > ss.awarded:
        add_points((secs - ss.awarded) * POINTS["watch"])
        ss.awarded = secs


def elapsed():
    """Seconds watched. Frozen while paused."""
    return (ss.paused_at if ss.paused else time.time()) - ss.started


# ---------- the recommendation algorithm ----------
def topic_weight(topic):
    # sqrt softens the gap: 100 points is about 4x a 0-point topic, not 30x,
    # so one topic can't completely take over the feed.
    return BASE_WEIGHT + math.sqrt(ss.points[topic])


def video_weight(k):
    v = VIDEOS[k]
    # 1) more topic points -> bigger weight (average over the video's topics)
    w = sum(topic_weight(t) for t in v["topics"]) / len(v["topics"])
    # 2) topic fatigue: shrink the weight for each recent video sharing a topic
    shared = sum(1 for h in ss.history[-FATIGUE_WINDOW:]
                 if set(VIDEOS[h]["topics"]) & set(v["topics"]))
    return w * FATIGUE ** shared


def video_probs():
    """Chance of each eligible video being shown next ({video index: probability})."""
    n = min(RECENT_BLOCK, len(VIDEOS) - 1)
    blocked = set(ss.history[-n:])                       # 3) no recent repeats
    cands = [k for k in range(len(VIDEOS)) if k not in blocked]
    weights = [video_weight(k) for k in cands]
    total = sum(weights)
    # 4) exploration: blend in a small uniform chance for every eligible video
    return {k: (1 - EXPLORE_CHANCE) * w / total + EXPLORE_CHANCE / len(cands)
            for k, w in zip(cands, weights)}


def pick_next():
    probs = video_probs()
    return random.choices(list(probs), weights=list(probs.values()), k=1)[0]


def topic_odds():
    """Chance (%) that the next video carries each topic, for the chart."""
    odds = {t: 0.0 for t in COLORS}
    for k, p in video_probs().items():
        for t in VIDEOS[k]["topics"]:
            odds[t] += 100 * p / len(VIDEOS[k]["topics"])
    return odds


def change_video(step):
    if step < 0 and len(ss.history) < 2:
        return                                  # nothing earlier to go back to
    pay_watchtime()
    if int(elapsed()) <= SKIP_LIMIT:
        add_points(-SKIP_PENALTY)               # skipped too quickly
    if step > 0:
        ss.index = pick_next()                  # the algorithm chooses
        ss.history.append(ss.index)
    else:
        ss.history.pop()                        # go back to the previous video
        ss.index = ss.history[-1]
    ss.started, ss.awarded, ss.last_tick = time.time(), 0, time.time()
    ss.paused = False


def toggle(name):
    ss[name] ^= {ss.index}
    sign = 1 if ss.index in ss[name] else -1
    add_points(sign * POINTS[name])


def toggle_play():
    now = time.time()
    if ss.paused:                       # resume: push the start time forward by the paused stretch
        ss.started += now - ss.paused_at
        ss.last_tick = now
        ss.paused = False
    else:                               # pause: pay what was watched so far, then freeze
        pay_watchtime()
        ss.paused_at = time.time()
        ss.paused = True


def reset():
    ss.clear()


# ---------- small layout helpers ----------
def section(title, sub=""):
    st.markdown(f'<div class="sec"><b></b><h2>{title}</h2><span>{sub}</span></div>', unsafe_allow_html=True)


def panel_head(title, sub):
    st.markdown(f'<div class="phead"><b>{title}</b><span>{sub}</span></div>', unsafe_allow_html=True)


# ---------- progress bar (drawn in the browser, so the server doesn't refresh it) ----------
def progress_bar():
    total = VIDEOS[ss.index]["seconds"]
    components.html(f"""
    <style>@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600&display=swap');</style>
    <div id="t" style="font:600 13px Sora,system-ui,sans-serif;color:#475569;margin-bottom:7px"></div>
    <div style="height:9px;background:#e0f2fe;border-radius:9px;overflow:hidden">
      <div id="b" style="height:100%;width:0;border-radius:9px;background:linear-gradient(90deg,#ff1f4b,#ff5c7c)"></div>
    </div>
    <script>
      const total = {total};
      const base = {elapsed():.2f};          // seconds already watched when this was drawn
      const paused = {str(ss.paused).lower()};
      let t0 = performance.now(), hiddenAt = null;

      document.addEventListener("visibilitychange", () => {{
        if (document.hidden) hiddenAt = performance.now();
        else if (hiddenAt !== null) {{ t0 += performance.now() - hiddenAt; hiddenAt = null; }}
      }});

      function draw(e) {{
        const pos = e % total;                          // wraps to 0 = loop
        document.getElementById("b").style.width = (pos / total * 100) + "%";
        document.getElementById("t").textContent =
          Math.floor(pos) + "s / " + total + "s" +
          (e >= total ? "  ·  loop " + (Math.floor(e / total) + 1) : "") +
          (paused ? "  ·  paused" : "");
      }}
      function tick() {{
        draw(base + (performance.now() - t0) / 1000);
        requestAnimationFrame(tick);
      }}
      if (paused) draw(base); else tick();
    </script>
    """, height=52)


# ---------- charts ----------
def topic_chart(data, fmt="d", max_value=None):
    """Horizontal bars in each topic's own color, value labels, no clutter."""
    df = pd.DataFrame({"Topic": list(data), "Value": list(data.values())})
    top = max_value or max(df["Value"].max(), 10)     # at least 10 so tiny values don't fill the bar
    base = alt.Chart(df).encode(
        y=alt.Y("Topic:N", sort="-x", title=None,
                axis=alt.Axis(ticks=False, domain=False, labelFontSize=12, labelPadding=8, labelColor="#334155")),
        x=alt.X("Value:Q", title=None, axis=None, scale=alt.Scale(domain=[0, top * 1.18])),
    )
    bars = base.mark_bar(cornerRadiusEnd=6, size=15).encode(
        color=alt.Color("Topic:N", legend=None,
                        scale=alt.Scale(domain=list(COLORS), range=[c[0] for c in COLORS.values()])))
    labels = base.mark_text(align="left", dx=6, fontSize=12, fontWeight=600, color="#0f172a").encode(
        text=alt.Text("Value:Q", format=fmt))
    return ((bars + labels).properties(height=len(df) * 25)
            .configure(background="transparent").configure_view(strokeWidth=0))


@st.fragment(run_every=1)
def points_chart():
    pay_watchtime()
    pa, pb = st.columns(2)
    with pa:
        with st.container(border=True, key="panel_points"):
            panel_head("Your topic points", "Earned by watching, liking, commenting and following.")
            st.altair_chart(topic_chart(ss.points), height=200)
    with pb:
        with st.container(border=True, key="panel_odds"):
            panel_head("Next video probabilities (%)", "Depends on interests and how often/recently a topic has appeared")
            st.altair_chart(topic_chart(topic_odds(), fmt=".0f", max_value=100), height=200)


def mix_chart():
    if sum(ss.points.values()) == 0:
        st.markdown('<div class="empty">Watch or react to a video and your interest mix will appear here.</div>',
                    unsafe_allow_html=True)
        return
    df = pd.DataFrame({"Topic": list(ss.points), "Amount": list(ss.points.values())})
    df = df[df["Amount"] > 0]
    fig = px.pie(df, names="Topic", values="Amount", color="Topic", color_discrete_map=PIE_COLORS, hole=0.55)
    fig.update_traces(textinfo="label+percent", textposition="outside", textfont_size=13,
                      marker=dict(line=dict(color="#ffffff", width=2)))
    fig.update_layout(height=340, margin=dict(t=30, b=30, l=30, r=30), showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Sora, sans-serif", color="#0f172a"))
    st.plotly_chart(fig)


# ---------- the video card (size unchanged) ----------
v, i = VIDEOS[ss.index], ss.index
c1, c2 = COLORS[v["topics"][0]]
chips = "".join(
    f'<span style="background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.5);'
    f'padding:3px 10px;border-radius:99px;font-size:13px;margin:0 6px 6px 0;'
    f'display:inline-block">#{t}</span>' for t in v["topics"])
mins, secs = divmod(v["seconds"], 60)

card = f"""
<div style="width:320px;max-width:100%;aspect-ratio:9/12;margin:0;border-radius:20px;
            padding:20px;box-sizing:border-box;color:white;display:flex;flex-direction:column;
            justify-content:space-between;background:linear-gradient(160deg,{c1},{c2});
            text-shadow:0 1px 8px rgba(0,0,0,.25);">
  <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600">
    <span>{v['views']} views</span><span>{mins}:{secs:02d}</span>
  </div>
  <div>
    <div style="font-weight:600">{v['creator']}</div>
    <div style="font-size:28px;font-weight:800;line-height:1.1;margin:8px 0">{v['title']}</div>
    <div style="font-size:14px;opacity:.9;margin-bottom:12px">{v['desc']}</div>
    {chips}
  </div>
</div>
"""

# ======================= page =======================
st.markdown("""
<div class="hero">
  <h1>Social media <span>algorithms</span></h1>
  <p>See how a feed learns what you enjoy.</p>
</div>
""", unsafe_allow_html=True)

ia, ib = st.columns(2, gap="large")
with ia:
    st.markdown("""<div class="info"><h4>How does social media work?</h4>
    <p>Have you ever felt that Instagram, TikTok and YouTube can accurately guess what you wish to watch?
    Social media sites utilise algorithms to analyse your activity and infer which type of content they think you would enjoy.</p></div>""",
                unsafe_allow_html=True)
with ib:
    st.markdown("""<div class="info"><h4>What does it learn about you?</h4>
    <p>Simply by watching, liking, commenting upon, following and even skipping videos, data about your interests is collected.
    This is then applied so that your social media feed can be tailored to you, both in terms of content and 
    its sequence.</p></div>""",
                unsafe_allow_html=True)

st.write("") 

st.markdown("""<div class="info"><h4>What this website demonstrates:</h4>
    <p>The interactive mechanism below shows a simple version of how social media algorithms typically work. 
        It gives points to topics you engage with and deducts points from those you don't.
        It then adjusts what videos to show you according to your preferences, 
        while still keeping the content diverse and not repetitive.</p></div>""",
                unsafe_allow_html=True)

section("The demo", "Press start, then watch, react or skip and see the feed adapt.")

left, right = st.columns([2, 3], gap="large")

with left:
    card_col, btn_col = st.columns([5, 1])
    with card_col:
        with st.container(key="controls"):
            ra, rb = st.columns(2)
            with ra:
                st.button("↺ Reset", key="reset", on_click=reset, use_container_width=True)
            with rb:
                st.button("▶ Start" if ss.paused else "⏸ Pause", key="playpause", type="primary",
                          on_click=toggle_play, use_container_width=True)
        st.markdown(card, unsafe_allow_html=True)
        progress_bar()
        st.caption(f"Videos watched this session: {len(ss.history)}")
    with btn_col:
        st.markdown('<div style="height:3.6rem"></div>', unsafe_allow_html=True)   # lines buttons up with the card
        with st.container(key="actions"):
            st.button("❤️" if i in ss.liked else "🤍", key="like", on_click=toggle,
                      args=("liked",), help="Like", use_container_width=True)
            st.button("💭" if i in ss.commented else "💬", key="comment", on_click=toggle,
                      args=("commented",), help="Comment", use_container_width=True)
            st.button("✔️" if i in ss.followed else "➕", key="follow", on_click=toggle,
                      args=("followed",), help="Follow", use_container_width=True)
            st.markdown('<div style="height:1.6rem"></div>', unsafe_allow_html=True)
            st.button("⬆", key="prev", on_click=change_video, args=(-1,), help="Previous video", use_container_width=True)
            st.button("⬇", key="next", on_click=change_video, args=(1,), help="Next video", use_container_width=True)

with right:
    points_chart()
    with st.container(border=True, key="panel_mix"):
        panel_head("Your interest mix", "Share of your points by topic. Refreshes when you press a button.")
        mix_chart()

section("The algorithm loop", "A recommendation algorithm operates through a continuous cycle.")
st.markdown("""
<div class="steps">
  <div class="step"><i>1</i><p>The platform recommends content based on previous activity.</p></div>
  <div class="step"><i>2</i><p>The user then interacts with the new content.</p></div>
  <div class="step"><i>3</i><p>The platform collects new behavioural signals.</p></div>
  <div class="step"><i>4</i><p>The system updates its predictions.</p></div>
  <div class="step"><i>5</i><p>New recommendations are generated using the updated information.</p></div>
</div>
""", unsafe_allow_html=True)

section("Filter bubble")
st.markdown("""
<div class="bubble">
  <p>These are situations in which personalized content recommendations may repeatedly expose users to similar information,
  topics or viewpoints while reducing their exposure to other content.</p>
  <p>Personalization can make content discovery more convenient, but excessive reliance on past preferences may limit
  information diversity and reduce exposure to alternative perspectives.</p>
  <p>The challenge is to find a balance between relevant recommendations and diverse content discovery.</p>
</div>
""", unsafe_allow_html=True)