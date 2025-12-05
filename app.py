import re
import streamlit as st
import pandas as pd

# ============================
# FULL RESPONSIVE PAGE CONFIG
# ============================
st.set_page_config(
    page_title="BEAST MODE LEAD HUNTER",
    layout="centered",
    initial_sidebar_state="auto"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
    }
    .big-title {
        font-size: 4.5rem !important;
        background: linear-gradient(90deg, #00ffea, #ff00ff, #00ffea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
        text-align: center;
        margin: 0;
    }
    @keyframes glow {
        from { text-shadow: 0 0 20px #00ffea; }
        to { text-shadow: 0 0 40px #ff00ff, 0 0 60px #ff00ff; }
    }
    .neon-text {color: #ff00ff; text-shadow: 0 0 20px #ff00ff;}
    
    /* MOBILE OPTIMIERUNGEN */
    @media (max-width: 768px) {
        .big-title {font-size: 2.5rem !important;}
        h2 {font-size: 1.5rem !important;}
        h3 {font-size: 1.2rem !important;}
        .stButton>button {padding: 12px 20px !important; font-size: 1rem !important;}
        [data-testid="stDataFrame"] {font-size: 0.8rem !important;}
        .card {padding: 15px !important;}
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00ffea);
        color: black;
        font-weight: bold;
        border-radius: 50px;
        border: none;
        padding: 15px 30px;
        font-size: 1.2rem;
        box-shadow: 0 0 20px #ff00ff;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 40px #ff00ff;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid #00ffea;
        box-shadow: 0 0 20px rgba(0, 255, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    /* Horizontales Scrollen auf Mobile */
    [data-testid="stHorizontalBlock"] {overflow-x: auto;}
</style>
""", unsafe_allow_html=True)


# ============================
# DATA (Stand 05. Dez 2025 – alle dicken Fische)
# ============================
data = {
    "Plattform": ["BeatStars","BeatStars","BeatStars","BeatStars","Reddit","Reddit","TikTok","TikTok","X","YouTube","BeatStars","Reddit","X","TikTok","Instagram","SoundCloud"],
    "Artist/User": ["Deadboy","Slime Krust","Blackketchupp","Yung Pluto","u/Blackketchupp","u/Ok-Professional-1898","@lilyoxo_","@kashkash2x","@RealYungSayian","@kashkash","Kash Kash","u/External_Pianist_86","@rarejpeg","@quaminamp","@yungplutoo","Yung Demon"],
    "Contact": ["deadboybeats@gmail.com","DM open","DM/Reddit","DM open","Reddit PM","Reddit PM","DM open","DM open","nickoliver2024@gmail.com","kashproductions2025@gmail.com","Open Collab","Reddit PM","DM open","bookquaminamp@gmail.com","DM open","DM open"],
    "Budget/Potenzial": ["bis $1.000","$800","$800–$1.200","$500","$800–$1.200","Paid good","Will pay good money","Will sign + pay","Paid for 2026 Album","$400 paid","$350–$400","$500+","Will pay whatever","Ghana Star – zahlt immer","800k Reel – high","3k Follower – serious"],
    "Vibe/Genre": ["Exclusive/Custom","Dark Plugg/Rage","Full Album","Yeat/Ken Carson Pack","First Album","Long-term Paid","Exact viral vibe","Rage – will sign","2026 Album Exclusives","Yeat x Opium","Rage/Plugg","Dark Trap/Plugg","Real shit now","Ghana/Afro","Rage ASAP","Plugg/Rage"],
    "Status": ["🔥 LIVE","🔥 LIVE","🔥 LIVE","🔥 LIVE","🔥 LIVE","🔥 LIVE","🔥 3.8M Views","🔥 1.4M Views","🔥 Aktiv","🔥 Hot","🔥 Open Collab","🔥 Aktiv","🔥 372+ Likes","🔥 Viral","🔥 800k Reel","🔥 Kommentare explodieren"]
}

df = pd.DataFrame(data)


# Helper: parse Budget/Potenzial to numeric score for sorting/filtering
def parse_budget(s):
    if pd.isna(s):
        return 0
    text = str(s)
    # Find numbers like 1.200 or 800 or 3k
    nums = re.findall(r"(\d+[\.,]?\d*)\s*(k|K)?", text)
    values = []
    for num, kflag in nums:
        n = num.replace('.', '').replace(',', '')
        try:
            iv = int(n)
        except ValueError:
            try:
                iv = int(float(n))
            except Exception:
                continue
        if kflag:
            iv *= 1000
        values.append(iv)
    # If words like 'Will pay' or 'Paid' appear, give moderate score
    if values:
        return max(values)
    if re.search(r"pay|paid|will pay|will sign|Ghana Star", text, re.IGNORECASE):
        return 1000
    # default small value
    return 0


df['Budget_score'] = df['Budget/Potenzial'].apply(parse_budget)
df = df.sort_values(by='Budget_score', ascending=False)


# ============================
# HEADER
# ============================
st.markdown('<h1 class="big-title">BEAST MODE<br>LEAD HUNTER</h1>', unsafe_allow_html=True)
st.markdown("<h2 class='neon-text' style='text-align:center;'>🔥 Stand: 05. Dezember 2025 – Voll mobil & PC ready 🔥</h2>", unsafe_allow_html=True)


# ============================
# SIDEBAR FILTERS
# ============================
with st.sidebar:
    st.markdown("### ⚙️ FILTERS")
    plattform = st.multiselect("Plattform", options=["Alle"] + sorted(df["Plattform"].unique()), default=["Alle"])
    min_budget = st.selectbox("Mindest-Potenzial", options=["Alle", "Will pay", "$350+", "$500+", "$800+", "$1000+"], index=0)
    genre = st.multiselect("Genre/Vibe", options=["Alle"] + sorted(df["Vibe/Genre"].unique()), default=["Alle"])
    
    if st.button("🦍 BEAST MODE AKTIVIEREN"):
        st.success("ALLE DICKEN FISCHE GELADEN!")


# Filter Logic
filtered = df.copy()
if not (len(plattform) == 1 and plattform[0] == "Alle"):
    filtered = filtered[filtered["Plattform"].isin(plattform)]
if min_budget != "Alle":
    if min_budget == "$1000+":
        filtered = filtered[filtered["Budget_score"] >= 1000]
    elif min_budget == "$800+":
        filtered = filtered[filtered["Budget_score"] >= 800]
    elif min_budget == "$500+":
        filtered = filtered[filtered["Budget_score"] >= 500]
    elif min_budget == "$350+":
        filtered = filtered[filtered["Budget_score"] >= 350]
    elif min_budget == "Will pay":
        filtered = filtered[filtered["Budget/Potenzial"].str.contains("pay|Paid|Will pay", case=False, na=False)]
if not (len(genre) == 1 and genre[0] == "Alle"):
    filtered = filtered[filtered["Vibe/Genre"].isin(genre)]


# ============================
# MAIN (Responsive Layout)
# ============================
mobile_flag = False
try:
    ua = st.get_option("client.userAgent", "")
    if isinstance(ua, str) and "mobile" in ua.lower():
        mobile_flag = True
except Exception:
    mobile_flag = st.session_state.get("mobile", False)

if mobile_flag:
    st.markdown(f"### 📊 Stats → **{len(filtered)} heiße Leads** aktiv")
    st.markdown("### 💰 Top 5 Geldbeutel")
    st.dataframe(filtered.head(5)[["Artist/User", "Budget/Potenzial"]], width='stretch')
    st.markdown("### 🔥 ALLE DICKEN FISCHE")
    st.dataframe(filtered.drop(columns=["Status", "Budget_score"]), width='stretch')
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### 📊 Stats\n**{len(filtered)} heiße Leads** aktiv")
        st.markdown("### 💰 Top 5 Geldbeutel")
        st.dataframe(filtered.head(5)[["Artist/User", "Budget/Potenzial"]], width='stretch')
    with col2:
        st.markdown("### 🔥 DIE DICKSTEN FISCHE")
        st.dataframe(filtered.drop(columns=["Status", "Budget_score"]), width='stretch', height=800)


# ============================
# FOOTER
# ============================
st.markdown("---")
st.markdown("<h3 style='text-align:center; color:#ff00ff; text-shadow: 0 0 20px #ff00ff;'>Deine Beast Mode App ist jetzt WELTWEIT ready – deploy sie auf Streamlit Cloud und schick mir den Link, ich will sehen wie sie bei dir ballert 🔥🚀</h3>", unsafe_allow_html=True)
