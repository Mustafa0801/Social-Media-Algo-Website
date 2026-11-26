import math
import random
import time


import altair as alt
import pandas as pd
import plotly.express as px

import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(layout="wide")
ss = st.session_state


st.title("Social media algorithms")

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


def progress_bar():
    """Progress bar drawn in the browser, so the server doesn't have to refresh it."""
    total = VIDEOS[ss.index]["seconds"]
    components.html(f"""
    <div id="t" style="font:14px sans-serif;color:#888;margin-bottom:5px"></div>
    <div style="height:8px;background:rgba(128,128,128,.25);border-radius:9px;overflow:hidden">
      <div id="b" style="height:100%;width:0;background:#ff4b4b"></div>
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
    """, height=48)


def topic_chart(data, fmt="d", max_value=None):
    """Horizontal bars in each topic's own color, fixed order, value labels, no clutter."""
    df = pd.DataFrame({"Topic": list(data), "Value": list(data.values())})
    top = max_value or max(df["Value"].max(), 10)     # at least 10 so tiny values don't fill the bar
    base = alt.Chart(df).encode(
        y=alt.Y("Topic:N", sort="-x", title=None,
                axis=alt.Axis(ticks=False, domain=False, labelFontSize=13, labelPadding=8)),
        x=alt.X("Value:Q", title=None, axis=None, scale=alt.Scale(domain=[0, top * 1.15])),
    )
    bars = base.mark_bar(cornerRadiusEnd=6, size=20).encode(
        color=alt.Color("Topic:N", legend=None,
                        scale=alt.Scale(domain=list(COLORS), range=[c[0] for c in COLORS.values()])))
    labels = base.mark_text(align="left", dx=6, fontSize=13, color="white").encode(text=alt.Text("Value:Q", format=fmt))
    return (bars + labels).properties(height=len(df) * 38).configure_view(strokeWidth=0)

def reset():
    ss.clear()


@st.fragment(run_every=1)
def points_chart():
    pay_watchtime()
    st.altair_chart(topic_chart(ss.points), height=200)
    st.altair_chart(topic_chart(topic_odds(), fmt=".0f", max_value=100), height=200)


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
            justify-content:space-between;background:linear-gradient(160deg,{c1},{c2});">
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

df = pd.DataFrame({
    "Topic": ["Cooking", "Travel", "Fitness", "Gaming", "Tech", "Music", "Comedy", "Science"],
    "Amount": [ss.points["Cooking"], ss.points["Travel"], ss.points["Fitness"], 
               ss.points["Gaming"], ss.points["Tech"], ss.points["Music"], 
               ss.points["Comedy"], ss.points["Science"]]
})

color_map ={
    "Cooking": "#d33f00",
    "Travel": "#5fc1eb",
    "Fitness": "#00d54b",
    "Gaming": "#8e3dff",
    "Tech": "#ffd632",
    "Music": "#ff3f76",
    "Comedy": "#c3ff36",
    "Science": "#0de1e4"
}


algo_chart = px.pie(df, names="Topic", 
                    values="Amount", 
                    color="Topic", 
                    color_discrete_map=color_map)


st.subheader("How does social media work?")
st.markdown("Have you ever felt that Instagram, TikTok and YouTube can accurately guess what you wish to watch? " \
        "Social media sites utilise algorithms to analyse your activity and infer which type of content they think you would enjoy.", width = 900)

st.markdown("Simply by watching, liking, commenting upon, following and even skipping videos, data about your interests is collected. This is then applied so that your social media feed can be tailored to you, " \
            "both in terms of content, its sequence and how often certain subject matter is shown to you." , width = 900)

st.write(" ")

left, right = st.columns([1, 2])

with left:
    card_col, btn_col = st.columns([5, 1])
    with card_col:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Reset", key="reset", on_click=reset, use_container_width=True)
        with col2:
            st.button("▶ Start" if ss.paused else "⏸ Pause", key="playpause",
                       on_click=toggle_play, use_container_width=True)
        
        st.markdown(card, unsafe_allow_html=True)
        progress_bar()

        st.caption(f"Videos watched this session: {len(ss.history)}")

        st.subheader(" ")

        st.subheader("Algorithm Overview")
        st.markdown("A recommendation algorithm operates through a continuous cycle: \n"\
                    "1. The platform recommends content based on previous activity. \n"\
                    "2. The user then interacts with the new content. \n"\
                    "3. The platform collects new behavioural signals. \n"\
                    "4. The system updates its predictions. \n"\
                    "5. New recommendations are generated using the updated information.")
    with btn_col:
        st.subheader("")
        st.button("❤️" if i in ss.liked else "🤍", key="like", on_click=toggle,
                  args=("liked",), help="Like", use_container_width=True)
        st.button("💭" if i in ss.commented else "💬", key="comment", on_click=toggle,
                  args=("commented",), help="Comment", use_container_width=True)
        st.button("✔️" if i in ss.followed else "➕", key="follow", on_click=toggle,
                  args=("followed",), help="Follow", use_container_width=True)

        st.header(" ")

        st.button("⬆", key="prev", on_click=change_video, args=(-1,), help="Previous video", use_container_width=True)
        st.button("⬇", key="next", on_click=change_video, args=(1,), help="Next video", use_container_width=True)

with right:
    blank, col1, col2 = st.columns([1, 3, 4])
    with col1: 
        st.subheader("  Your topic points")

        st.header("")
        st.header("")

        st.subheader("Chance of each topic in the next video (%)")

    with col2:
        points_chart()

    st.header(" ")
    st.header(" ")
    st.plotly_chart(algo_chart)


st.subheader("Filter bubble")
st.markdown("These are situations in which personalized content recommendations may repeatedly expose users to similar information, topics or viewpoints while reducing their exposure to other content. \n"
            "Personalization can make content discovery more convenient, but excessive reliance on past preferences may limit information diversity and reduce exposure to alternative perspectives. \n"
            " \n"
            "The challenge is to find a balance between relevant recommendations and diverse content discovery.", width = 900)
