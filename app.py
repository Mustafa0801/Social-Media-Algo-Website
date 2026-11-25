import streamlit as st

st.set_page_config(layout="wide")

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
     "topics": ["Cooking"], "duration": "0:30", "views": "1.2M",
     "desc": "A fast weeknight noodle recipe using pantry staples."},
    {"title": "10-minute core workout, no equipment", "creator": "@moveandmore",
     "topics": ["Fitness"], "duration": "0:35", "views": "860K",
     "desc": "Five core exercises you can do on the living room floor."},
    {"title": "Three days in Lisbon on a small budget", "creator": "@wanderlist",
     "topics": ["Travel", "Cooking"], "duration": "0:40", "views": "2.4M",
     "desc": "Where to eat, walk and stay without overspending."},
    {"title": "The chip inside your phone, explained", "creator": "@siliconsketch",
     "topics": ["Tech"], "duration": "0:50", "views": "540K",
     "desc": "What a processor does, in plain language."},
]

if "index" not in st.session_state:
    st.session_state.index = 0


def go_next():
    st.session_state.index = (st.session_state.index + 1) % len(VIDEOS)

for key in ("liked", "commented", "followed"):
    st.session_state.setdefault(key, set())

def toggle(name):
    i = st.session_state.index
    st.session_state[name] ^= {i} 



i = st.session_state.index
v = VIDEOS[st.session_state.index]
c1, c2 = COLORS[v["topics"][0]]
chips = "".join(
    f'<span style="background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.5);'
    f'padding:3px 10px;border-radius:99px;font-size:13px;margin:0 6px 6px 0;'
    f'display:inline-block">#{t}</span>'
    for t in v["topics"]
)


card = f"""
<div style="width:320px;max-width:100%;aspect-ratio:9/16;margin:0;border-radius:20px;
            padding:20px;box-sizing:border-box;color:white;display:flex;flex-direction:column;
            justify-content:space-between;background:linear-gradient(160deg,{c1},{c2});">
  <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600">
    <span>{v['views']} views</span><span>{v['duration']}</span>
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

    with btn_col:
        st.button("❤️" if i in st.session_state.liked else "🤍", key="like",
                  on_click=toggle, args=("liked",), help="Like", use_container_width=True)
        st.button("💭" if i in st.session_state.commented else "💬", key="comment",
                  on_click=toggle, args=("commented",), help="Comment", use_container_width=True)
        st.button("✔️" if i in st.session_state.followed else "➕", key="follow",
                  on_click=toggle, args=("followed",), help="Follow", use_container_width=True)
        
        st.header(" ")
        st.header(" ")
        
        st.button("⬇", key="next", on_click=go_next, help="Next video", use_container_width=True)
