# kana_quiz_streamlit.py
import streamlit as st
import random
import uuid
import time

# -----------------------------
# Full kana mappings (hiragana, katakana, dakuten)
# -----------------------------
HIRAGANA = {
    "あ":"a","い":"i","う":"u","え":"e","お":"o",
    "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
    "さ":"sa","し":"shi","す":"su","せ":"せ","そ":"so",
    "た":"ta","ち":"chi","つ":"tsu","て":"te","と":"to",
    "な":"na","に":"ni","ぬ":"nu","ね":"ne","の":"no",
    "は":"ha","ひ":"hi","ふ":"fu","へ":"he","ほ":"ho",
    "ま":"ma","み":"mi","む":"mu","め":"me","も":"mo",
    "や":"ya","ゆ":"yu","よ":"yo",
    "ら":"ra","り":"ri","る":"ru","れ":"re","ろ":"ro",
    "わ":"wa","を":"wo","ん":"n",
    "きゃ":"kya","きゅ":"kyu","きょ":"kyo",
    "しゃ":"sha","しゅ":"shu","しょ":"sho",
    "ちゃ":"cha","ちゅ":"chu","ちょ":"cho",
    "にゃ":"nya","にゅ":"nyu","にょ":"nyo",
    "ひゃ":"hya","ひゅ":"hyu","ひょ":"hyo",
    "みゃ":"mya","みゅ":"myu","みょ":"mo",
    "りゃ":"rya","りゅ":"ryu","りょ":"ryo",
}

KATAKANA = {
    "ア":"a","イ":"i","ウ":"u","エ":"e","オ":"o",
    "カ":"ka","キ":"ki","ク":"ku","ケ":"ke","コ":"ko",
    "サ":"sa","シ":"shi","ス":"su","セ":"セ","ソ":"so",
    "タ":"ta","チ":"chi","ツ":"tsu","テ":"te","ト":"to",
    "ナ":"na","ニ":"ni","ヌ":"nu","ネ":"ne","ノ":"no",
    "ハ":"ha","ヒ":"hi","フ":"fu","ヘ":"he","ホ":"ho",
    "マ":"ma","ミ":"mi","ム":"mu","メ":"me","モ":"mo",
    "ヤ":"ya","ユ":"yu","ヨ":"yo",
    "ラ":"ra","リ":"ri","ル":"ru","レ":"re","ロ":"ro",
    "ワ":"wa","ヲ":"wo","ン":"n",
    "キャ":"kya","キュ":"kyu","キョ":"kyo",
    "シャ":"sha","シュ":"shu","ショ":"sho",
    "チャ":"cha","チュ":"chu","チョ":"cho",
    "ニャ":"nya","ニュ":"nyu","ニョ":"nyo",
    "ヒャ":"hya","ヒュ":"hyu","ヒョ":"hyo",
    "ミャ":"mya","ミュ":"myu","ミョ":"myo",
    "リャ":"rya","リュ":"ryu","リョ":"ryo",
}

DAKUTEN = {
    "が":"ga","ぎ":"gi","ぐ":"gu","げ":"ge","ご":"go",
    "ざ":"za","じ":"ji","ず":"zu","ぜ":"ze","ぞ":"zo",
    "だ":"da","ぢ":"ji","づ":"zu","で":"de","ど":"do",
    "ば":"ba","び":"bi","ぶ":"bu","べ":"be","ぼ":"bo",
    "ぱ":"pa","ぴ":"pi","ぷ":"pu","ぺ":"pe","ぽ":"po",
    "ガ":"ga","ギ":"gi","グ":"gu","ゲ":"ge","ゴ":"go",
    "ザ":"za","ジ":"ji","ズ":"zu","ゼ":"ze","ゾ":"zo",
    "ダ":"da","ヂ":"ji","ヅ":"zu","デ":"de","ド":"do",
    "バ":"ba","ビ":"bi","ブ":"bu","ベ":"be","ボ":"bo",
    "パ":"pa","ピ":"pi","プ":"pu","ペ":"pe","ポ":"po",
}

KANAS = {}
KANAS.update(HIRAGANA)
KANAS.update(KATAKANA)
KANAS.update(DAKUTEN)

ROMAJI_POOL = sorted(set(KANAS.values()))

# -----------------------------
# Helpers
# -----------------------------
def make_question():
    kana, romaji = random.choice(list(KANAS.items()))
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 500:
        cand = random.choice(ROMAJI_POOL)
        if cand != romaji and cand not in distractors:
            distractors.add(cand)
        attempts += 1
    options = list(distractors) + [romaji]
    random.shuffle(options)
    return {"id": str(uuid.uuid4()), "kana": kana, "options": options, "correct_index": options.index(romaji)}

def init_quiz(total):
    st.session_state.started = True
    st.session_state.total = int(total)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.questions = [make_question() for _ in range(st.session_state.total)]
    st.session_state.current_q = None
    st.session_state.answered = False
    st.session_state.last_result = None
    st.rerun()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Kana Quiz", layout="centered")

# --- CUSTOM CSS FOR BRIGHTER STYLING ---

# GITHUB RAW URL:
github_raw_url = "https://raw.githubusercontent.com/harshithvarma01/Images_Storage_for_projects/main/jpbg.jpg"
background_image_css = f"url('{github_raw_url}')"

# Colors
COLOR_RED = "#a83232"
COLOR_GOLD = "#ffcc00"
COLOR_LIGHT_BLUE = "#3e90b7"
COLOR_ACCENT = "#ff7f50" # Coral for buttons

st.markdown(f"""
<style>
/* 1. APP BACKGROUND STYLING (No dark overlay on main content area!) */
.stApp {{
    background: {background_image_css}, linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* 2. MAIN CONTENT CARD (Remove the dark background to show image through!) */
/* We target the outermost container block and remove the background color */
.main .block-container {{
    /* Removed: background-color: rgba(0, 0, 0, 0.6); */
    padding: 40px;
    border-radius: 15px;
    box-shadow: none; /* Reduced shadow for cleaner look */
}}

/* 3. HEADERS AND TEXT (Use text shadow to ensure readability over the busy background) */
h1, h2, h3, h4, h5, h6 {{
    color: #ffffff;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.9); /* Stronger shadow for contrast */
    font-weight: 800;
}}
.stMarkdown, .stMarkdown > div {{
    color: #f0f0f0;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
}}

/* 4. KANA CHARACTER DISPLAY (Large and prominent with a light, transparent card) */
div[data-testid="stMarkdownContainer"] div[style*="font-size:84px"] {{
    background-color: rgba(255, 255, 255, 0.25) !important; /* Lighter, clearer card */
    color: {COLOR_GOLD}; 
    border-radius: 12px;
    padding: 30px;
    margin: 20px 0;
    text-shadow: 3px 3px 5px rgba(0,0,0,0.7);
    font-size: 100px !important;
    border: 1px solid rgba(255, 255, 255, 0.4);
}}

/* 5. OPTION BUTTONS (Vibrant and responsive) */
div.stButton > button:first-child {{
    background-color: {COLOR_ACCENT}; /* Coral/Orange base color */
    color: white;
    font-weight: bold;
    border: none;
    padding: 12px 24px;
    text-align: center;
    font-size: 18px;
    margin: 8px 0;
    cursor: pointer;
    border-radius: 25px; 
    transition: all 0.2s ease-in-out;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}}

/* Button Hover Effect */
div.stButton > button:hover {{
    background-color: {COLOR_LIGHT_BLUE}; 
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}}

/* 6. FEEDBACK STYLING */
h3:has(> .st-emotion-cache-16p0o8c:contains("Correct!")) {{
    color: #4CAF50; /* Green */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}}
h3:has(> .st-emotion-cache-16p0o8c:contains("Correct is")) {{
    color: {COLOR_RED}; /* Deep Red */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}}

</style>
""", unsafe_allow_html=True)
# --- END CUSTOM CSS ---

st.title(" Japanese Quiz")

# init session keys
if "started" not in st.session_state:
    st.session_state.started = False

# START screen (no timer setting)
if not st.session_state.started:
    st.header(" Quiz Settings")
    total_q = st.number_input("Number of Questions", min_value=1, max_value=500, value=50)
    if st.button("Start Quiz", key="start_button"):
        init_quiz(total_q)
    st.stop()

# Load next question if current is None
if st.session_state.current_q is None:
    # If quiz finished
    if st.session_state.index >= st.session_state.total:
        st.header("Quiz Completed! 🎊")
        st.subheader(f"Final Score: {st.session_state.score} / {st.session_state.total}")
        if st.button("Restart", key="restart_button_final"):
            st.session_state.started = False
            st.session_state.current_q = None
            st.session_state.last_result = None
            st.rerun()
        st.stop()

    # prepare a new question and reset feedback
    st.session_state.current_q = st.session_state.questions[st.session_state.index]
    st.session_state.answered = False
    st.session_state.last_result = None

q = st.session_state.current_q
correct_i = q["correct_index"]

# Header
st.subheader(f"Question {st.session_state.index+1}/{st.session_state.total} — Score: {st.session_state.score}")
st.markdown(f"<div style='font-size:84px;text-align:center;background-color:rgba(255,255,255,0.1);border-radius:10px;padding:20px;margin:20px 0;text-shadow:2px 2px 4px rgba(0,0,0,0.5);'>{q['kana']}</div>", unsafe_allow_html=True)

# Show 2x2 option buttons while unanswered
if not st.session_state.answered:
    cols = st.columns(2)
    for i, opt in enumerate(q["options"]):
        if cols[i % 2].button(opt, key=f"{q['id']}_{i}"):
            user_ans = opt
            correct_ans = q["options"][correct_i]
            
            # update score
            if i == correct_i:
                st.session_state.score += 1
            else:
                st.session_state.score -= 1
            
            # store last_result and set answered
            st.session_state.last_result = (user_ans, correct_ans)
            st.session_state.answered = True

# ONE-LINE feedback (only) after answering
if st.session_state.answered and st.session_state.last_result is not None:
    chosen, correct = st.session_state.last_result
    if chosen == correct:
        st.markdown(f"### ✔ You selected **{chosen}** — Correct!")
    else:
        st.markdown(f"### ✖ You selected **{chosen}** — Correct is **{correct}**")

    # Auto-advance to next question after 2 seconds
    time.sleep(2)
    st.session_state.index += 1
    st.session_state.current_q = None
    st.session_state.answered = False
    st.session_state.last_result = None
    st.rerun()