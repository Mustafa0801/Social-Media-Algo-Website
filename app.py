import streamlit as st
import time 


st.set_page_config(layout="wide")
ss = st.session_state


st.title("Social media algorithms")
st.subheader("A simple demo")

COLORS = {
    "Cooking": ("#ff8a4c", "#7a2e0e"),
    "Fitness": ("#22c27a", "#0b4a2d"),
    "Gaming": ("#7b6cff", "#241a6b"),
    "Travel": ("#5fc1eb", "#053a5b"),
    "Music": ("#ff5c8a", "#6b1230"),
    "Tech": ("#ffdb49", "#db9f07"),

}


VIDEOS = [
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
  
    {"title": "10-minute core workout, no equipment", "creator": "@moveandmore",
        "topics": ["Fitness"], "seconds": 35, "views": "860K",
        "desc": "Five core exercises you can do on the living room floor."},
    {"title": "How to make easy high-protein meals", "creator": "@nicklifts",
        "topics": ["Fitness", "Cooking"], "seconds": 60, "views": "750K",
        "desc": "Simple recipes for nutritious, protein-rich meals."},
    {"title": "Beginner workout routine", "creator": "@bruno_fitness",
        "topics": ["Fitness"], "seconds": 55, "views": "300K",
        "desc": "Weekly workout routine for beginnerss."},

    {"title": "Three days in Lisbon on a small budget", "creator": "@wanderlist",
        "topics": ["Travel", "Cooking"], "seconds": 60, "views": "2.4M",
        "desc": "Where to eat, walk and stay without overspending."},
    {"title": "Experiencing the northern lights", "creator": "@scandanaviantravels",
        "topics": ["Travel"], "seconds": 20, "views": "10M",
        "desc": "A stunning time-lapse of the aurora borealis in Norway."},
    {"title": "Cycling across Europe", "creator": "@danielonwheels",
        "topics": ["Travel", "Fitness"], "seconds": 50, "views": "2M",
        "desc": "My journey from Portugal to Italy on a bike."},
    {"title": "Camping in rainy forest", "creator": "@outdooradventures",
        "topics": ["Travel"], "seconds": 60, "views": "70K",
        "desc": "A rainy weekend with a tent and a campfire."},
        
    {"title": "The chip inside your phone, explained", "creator": "@siliconsketch",
        "topics": ["Tech"], "seconds": 45, "views": "540K",
        "desc": "What a processor does, in plain language."},
    {"title": "The next gen robots", "creator": "@metalmech",
        "topics": ["Tech"], "seconds": 30, "views": "1.2M",
        "desc": "These new humanoid robots are more lifelike than ever before."},
    {"title": "Building a PC from scratch", "creator": "@techbuilds",
        "topics": ["Gaming", "Tech"], "seconds": 55, "views": "3M",
        "desc": "The best parts to build a gaming PC in 2026."},

    {"title": "5 free games on pc!", "creator": "@mike40",
        "topics": ["Gaming"], "seconds": 30, "views": "200K",
        "desc": "Top games available on steam that you can play right now."},
    {"title": "Tips to get better at shooters", "creator": "@frankthetank",
        "topics": ["Gaming"], "seconds": 50, "views": "150K",
        "desc": "Tips for beginners to improve your gameplay."},
    {"title": "Games coming out next month", "creator": "@intergame_news",
        "topics": ["Gaming"], "seconds": 40, "views": "700K",
        "desc": "The most anticipated games coming out december 2026"},
    {"title": "Game development 101", "creator": "@rustprogramming",
        "topics": ["Gaming", "Tech"], "seconds": 70, "views": "200K",
        "desc": "The most important things to know about game development."},
]

POINTS = {"watch":1, "liked": 4, "commented": 5, "followed": 8}
SKIP_LIMIT = 2      # leaving after this many seconds or fewer counts as a skip
SKIP_PENALTY = 3

ss.setdefault("index", 0)
ss.setdefault("points", {t: 0 for t in COLORS})
ss.setdefault("started", time.time())   # when the current video began
ss.setdefault("awarded", 0)             # seconds already paid out for this video
for key in ("liked", "commented", "followed"):
    ss.setdefault(key, set())


def add_points(n):
    for topic in VIDEOS[st.session_state.index]["topics"]:
        ss.points[topic] += n
        ss.points[topic] = max(ss.points[topic], 0)   


def watched_seconds():
    return min(int(time.time() - ss.started), VIDEOS[ss.index]["seconds"])

def pay_watchtime():
    secs = watched_seconds()
    if secs > ss.awarded:
        add_points((secs - ss.awarded) * POINTS["watch"])
        ss.awarded = secs

def elapsed():
    return time.time() - ss.started


def change_video(step):
    pay_watchtime()
    if int(elapsed()) <= SKIP_LIMIT:
        add_points(-SKIP_PENALTY)               # skipped too quickly
    ss.index = (ss.index + step) % len(VIDEOS)
    ss.started, ss.awarded = time.time(), 0

def toggle(name):
    ss[name] ^= {ss.index}
    sign = 1 if ss.index in ss[name] else -1
    add_points(sign * POINTS[name])



@st.fragment(run_every=0.5)
def progress_bar():
    pay_watchtime()
    total = VIDEOS[ss.index]["seconds"]
    pos = elapsed() % total                 # wraps back to 0 at the end = loop
    loops = int(elapsed() // total)
    st.progress(pos / total, text=f"{int(pos)}s / {total}s" + (f"  ·  loop {loops + 1}" if loops else ""))


@st.fragment(run_every=0.5)
def points_chart():
    pay_watchtime()
    st.subheader("Your topic points")
    st.bar_chart(ss.points, horizontal=True, sort=True)



v, i = VIDEOS[ss.index], ss.index
c1, c2 = COLORS[v["topics"][0]]
chips = "".join(
    f'<span style="background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.5);'
    f'padding:3px 10px;border-radius:99px;font-size:13px;margin:0 6px 6px 0;'
    f'display:inline-block">#{t}</span>' for t in v["topics"])
mins, secs = divmod(v["seconds"], 60)


card = f"""
<div style="width:320px;max-width:100%;aspect-ratio:9/16;margin:0;border-radius:20px;
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


left, right = st.columns([1, 2])

with left:
    card_col, btn_col = st.columns([5, 1])
    with card_col:
        st.markdown(card, unsafe_allow_html=True)
        progress_bar()
        st.caption(f"Video {i + 1} of {len(VIDEOS)}")
    with btn_col:
        st.button("❤️" if i in ss.liked else "🤍", key="like", on_click=toggle,
                  args=("liked",), help="Like", use_container_width=True)
        st.button("💭" if i in ss.commented else "💬", key="comment", on_click=toggle,
                  args=("commented",), help="Comment", use_container_width=True)
        st.button("✔️" if i in ss.followed else "➕", key="follow", on_click=toggle,
                  args=("followed",), help="Follow", use_container_width=True)
        st.button("⬆", key="prev", on_click=change_video, args=(-1,), help="Previous video", use_container_width=True)
        st.button("⬇", key="next", on_click=change_video, args=(1,), help="Next video", use_container_width=True)

with right:
    points_chart()