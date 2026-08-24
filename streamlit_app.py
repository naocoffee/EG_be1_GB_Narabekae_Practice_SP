import streamlit as st
import random

# ============================================================
# ページ設定
# ============================================================
st.set_page_config(
    page_title="Seijo Mondai Master",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 整序問題データ（Lesson 3〜5 全10問）
# 各問題は「日本語の意味」と「並べ替えるべき語句チャンク」から成る。
# チャンクを正しい順（correct_order）に並べると意味の通る英文になる。
# when節・because節は単語レベルまで分解している。
# ============================================================
QUESTIONS = [
    {
        "id": 1,
        "lesson": "Lesson 3 (will)",
        "japanese": "彼女はその競争に勝つだろう。",
        "correct_order": ["she", "will", "win", "the race"],
        "explanation": "「そうする・そうなる」と話し手がその場で思っていることは〈will＋動詞の原形〉で表します。willは、主語の意志や「そうなるだろう」という話し手の予測を表すときに使います。",
        "ref": "ClearGB Lesson 3-A「will / be going to」（教科書 pp.085-088）",
    },
    {
        "id": 2,
        "lesson": "Lesson 3 (be going to)",
        "japanese": "私はテニス部に入るつもりだ。",
        "correct_order": ["I'm", "going to", "join", "the tennis club"],
        "explanation": "「そうするつもりだ」とすでに決めていることは〈be going to＋動詞の原形〉で表します。willがその場で決めた意志を表すのに対し、be going toは前もって決めていた予定を表します。",
        "ref": "ClearGB Lesson 3-A「will / be going to」（教科書 pp.085-088）",
    },
    {
        "id": 3,
        "lesson": "Lesson 3 (when + 現在形)",
        "japanese": "彼が帰宅したらあなたに電話します。",
        "correct_order": ["I'll", "call", "you", "when", "he", "comes", "home"],
        "explanation": "「時」を表すwhenの節の中では、未来のことを表す場合でも動詞は現在形（comes）を使います。× when he will come home とはしません。",
        "ref": "ClearGB Lesson 3-C「when や if のあとの現在形」（教科書 pp.090-093）",
    },
    {
        "id": 4,
        "lesson": "Lesson 3 (if + 現在形)",
        "japanese": "明日雨が降れば、私は家にいます。",
        "correct_order": ["I'll", "stay", "home", "if it rains tomorrow"],
        "explanation": "「条件」を表すifの節の中では、未来のことを表す場合でも動詞は現在形（rains）を使います。× if it will rain tomorrow とはしません。",
        "ref": "ClearGB Lesson 3-C「when や if のあとの現在形」（教科書 pp.090-093）",
    },
    {
        "id": 5,
        "lesson": "Lesson 4 (現在完了形：経験)",
        "japanese": "私は以前、市長に会ったことがある。",
        "correct_order": ["I", "have", "met", "the mayor", "before"],
        "explanation": "現在完了形〈have/has＋過去分詞〉で「今までの経験」を表します。before（以前に）などの語句とともに使われることが多い表現です。",
        "ref": "ClearGB Lesson 4-A「現在完了形：経験」（教科書 pp.106-108）",
    },
    {
        "id": 6,
        "lesson": "Lesson 4 (現在完了形：完了・結果)",
        "japanese": "私たちはすでにチケットを買った。",
        "correct_order": ["we've", "already", "bought", "the", "tickets"],
        "explanation": "現在完了形で「完了していること」を表す場合、already（すでに）やjust（ちょうど）とともに使われることが多いです。",
        "ref": "ClearGB Lesson 4-B「現在完了形：完了・結果」（教科書 pp.103-106）",
    },
    {
        "id": 7,
        "lesson": "Lesson 4 (現在完了形：継続)",
        "japanese": "私たちは幼稚園以来の知り合いだ。",
        "correct_order": ["we", "have known", "each other", "since we were in kindergarten"],
        "explanation": "「ずっと続いている状態」は現在完了形で表します。since〜（〜以来）とともに用いて、状態がいつから続いているかを示すことができます。",
        "ref": "ClearGB Lesson 4-C「現在完了形・現在完了進行形：継続」（教科書 pp.108-110）",
    },
    {
        "id": 8,
        "lesson": "Lesson 5 (過去完了形：大過去)",
        "japanese": "私たちがホールに着いたとき、コンサートはすでに始まっていた。",
        "correct_order": ["the concert", "had already begun", "when", "we", "arrived", "at the hall"],
        "explanation": "過去のある時点（ホールに着いたとき）よりもさらに前に起きていたことを表すため、過去完了形〈had＋過去分詞〉を使います。",
        "ref": "ClearGB Lesson 5-A「過去完了形：完了・経験・大過去」（教科書 pp.112-114）",
    },
    {
        "id": 9,
        "lesson": "Lesson 5 (未来完了形)",
        "japanese": "そのショーは5時までには終わっているだろう。",
        "correct_order": ["the show", "will", "have ended", "by", "five o'clock"],
        "explanation": "未来のある時点で「完了しているであろうこと」を表すため、未来完了形〈will have＋過去分詞〉を使います。",
        "ref": "ClearGB Lesson 5-C「未来完了形〈will have＋過去分詞〉」（教科書 pp.117-119）",
    },
    {
        "id": 10,
        "lesson": "Lesson 5 (過去完了形 + because)",
        "japanese": "彼女はテレビを見たかったので、宿題を終えていた。",
        "correct_order": ["she", "had finished", "her homework", "because", "she", "wanted", "to watch TV"],
        "explanation": "過去のある時点（テレビを見たいと思った時点）よりも前に完了していたことを表すため、過去完了形〈had＋過去分詞〉を使います。becauseは理由を表す接続詞で、節の中は〈主語＋動詞〉の通常の語順になります。",
        "ref": "ClearGB Lesson 5-A（教科書 pp.112-117）",
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)

# ============================================================
# CSS（スマートフォン仕様：アスペクト比 9:15）
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body {
        background: #2b2a26;
    }

    .stApp {
        background: #2b2a26;
        color: #33312e;
    }

    #MainMenu, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 24px 0;
    }

    div.block-container {
        width: min(90vw, 380px);
        aspect-ratio: 9 / 15;
        max-height: 94vh;
        background: #f0eee9;
        border: 12px solid #171614;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5), inset 0 0 0 2px #3a3833;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 22px 18px !important;
        position: relative;
        scrollbar-width: thin;
    }

    section.main > div {
        padding-top: 0;
    }

    * {
        font-family: 'Space Grotesk', sans-serif;
    }

    h1, h2, h3 {
        color: #33312e;
        font-weight: 600;
    }

    .app-title {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        color: #33312e;
        letter-spacing: 0.5px;
        margin-bottom: 0;
    }
    .app-subtitle {
        text-align: center;
        font-size: 0.8rem;
        color: #8c887f;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }

    /* ---- 進捗バー ---- */
    .progress-label {
        text-align: center;
        color: #96917f;
        letter-spacing: 1px;
        margin-bottom: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .progress-bar-outer {
        width: 100%;
        height: 8px;
        background: #d8d4c8;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 6px;
    }
    .progress-bar-inner {
        height: 100%;
        background: #2f8fb8;
        border-radius: 4px;
        transition: width 0.4s ease-in-out;
    }
    .score-tag {
        text-align: center;
        font-size: 0.82rem;
        color: #6f6b62;
        margin-bottom: 14px;
    }

    /* ---- 問題エリア ---- */
    .question-card {
        background: #e7e4dc;
        border: 1px solid #d8d4c8;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    .lesson-tag {
        display: inline-block;
        background: #fdf0d0;
        color: #a97c0a;
        font-weight: 600;
        font-size: 0.68rem;
        padding: 2px 9px;
        border-radius: 20px;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    .japanese-text {
        font-size: 1.08rem;
        font-weight: 600;
        color: #33312e;
        line-height: 1.6;
    }

    /* ---- 組み立てエリア ---- */
    .assembled-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #96917f;
        letter-spacing: 0.5px;
        margin: 4px 0 6px 2px;
        text-transform: uppercase;
    }
    .assembled-box {
        background: #ffffff;
        border: 1px dashed #c9c4b8;
        border-radius: 8px;
        padding: 10px 12px;
        min-height: 46px;
        margin-bottom: 14px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        align-items: center;
    }
    .assembled-chip {
        background: #2f8fb814;
        border: 1px solid #2f8fb855;
        color: #1f6f92;
        padding: 4px 10px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .assembled-placeholder {
        color: #b3ae9f;
        font-size: 0.85rem;
    }

    .pool-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #96917f;
        letter-spacing: 0.5px;
        margin: 4px 0 6px 2px;
        text-transform: uppercase;
    }

    /* ---- 判定表示 ---- */
    .effect-text {
        text-align: center;
        font-size: 0.95rem;
        font-weight: 700;
        padding: 10px;
        margin: 10px 0 8px 0;
        border-radius: 8px;
    }
    .effect-win {
        color: #17a86b;
        background: #17a86b14;
        border: 1px solid #17a86b40;
    }
    .effect-lose {
        color: #d6394a;
        background: #d6394a14;
        border: 1px solid #d6394a40;
    }

    .explain-box {
        background: #e7e4dc;
        border-left: 3px solid #c48f10;
        border-radius: 6px;
        padding: 10px 14px;
        margin-top: 6px;
        font-size: 0.92rem;
        line-height: 1.6;
        color: #4a473f;
    }
    .explain-title {
        font-size: 0.68rem;
        font-weight: 700;
        color: #b5860a;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .ref-note {
        font-size: 0.76rem;
        color: #8c887f;
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px dashed #d8d4c8;
    }
    .correct-sentence {
        font-size: 0.95rem;
        color: #33312e;
        margin: 6px 0 8px 0;
        line-height: 1.5;
    }

    /* ---- ボタン ---- */
    div.stButton > button {
        font-weight: 600;
        font-size: 0.92rem;
        background: #e7e4dc;
        color: #33312e;
        border: 1px solid #d0ccc0;
        border-radius: 8px;
        padding: 7px 6px;
        width: 100%;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        background: #ddd8cb;
        border-color: #c48f10;
        color: #93690b;
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }

    .decide-btn button {
        background: #2f8fb8 !important;
        border-color: #2f8fb8 !important;
        color: #ffffff !important;
    }
    .decide-btn button:hover {
        background: #26759a !important;
        color: #ffffff !important;
    }

    .subtle-btn button {
        background: transparent !important;
        border: 1px solid #c9c4b8 !important;
        color: #8c887f !important;
        font-size: 0.8rem !important;
        padding: 4px !important;
    }

    /* ---- 結果画面 ---- */
    .result-title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 6px 0 4px 0;
        color: #33312e;
    }
    .result-score {
        text-align: center;
        font-size: 1.0rem;
        color: #6f6b62;
        margin-bottom: 16px;
    }

    .weakpoint-card {
        background: #e7e4dc;
        border: 1px solid #d8d4c8;
        border-left: 3px solid #d6394a;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .weakpoint-q {
        font-weight: 600;
        font-size: 0.98rem;
        color: #33312e;
        margin-bottom: 4px;
    }
    .weakpoint-ans {
        font-size: 0.88rem;
        color: #17a86b;
        margin-bottom: 4px;
    }

    .badge-correct {
        display:inline-block;
        background:#17a86b14;
        color:#17a86b;
        border:1px solid #17a86b40;
        border-radius:20px;
        padding:1px 10px;
        font-weight:600;
        font-size:0.78rem;
        margin-bottom:6px;
    }
    .badge-wrong {
        display:inline-block;
        background:#d6394a14;
        color:#d6394a;
        border:1px solid #d6394a40;
        border-radius:20px;
        padding:1px 10px;
        font-weight:600;
        font-size:0.78rem;
        margin-bottom:6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# セッション状態の初期化
# ============================================================
def start_question(idx):
    q = QUESTIONS[st.session_state.order[idx]]
    pool = list(q["correct_order"])
    random.shuffle(pool)
    # 万一シャッフル結果が正解と一致してしまったら、もう一度シャッフルする
    if len(pool) > 1:
        tries = 0
        while pool == q["correct_order"] and tries < 5:
            random.shuffle(pool)
            tries += 1
    st.session_state.available = pool
    st.session_state.selected = []


def init_state():
    order = list(range(TOTAL_QUESTIONS))
    random.shuffle(order)
    st.session_state.order = order
    st.session_state.current_index = 0
    st.session_state.answered = False
    st.session_state.test_over = False
    st.session_state.correct_count = 0
    st.session_state.weak_points = []
    st.session_state.last_correct = None
    start_question(0)


if "order" not in st.session_state:
    init_state()


# ============================================================
# ヘルパー関数
# ============================================================
def capitalize_sentence(sentence):
    """文頭を大文字にし、文末にピリオドを補って表示用の英文を整える。"""
    if not sentence:
        return sentence
    s = sentence[0].upper() + sentence[1:]
    if not s.endswith("."):
        s += "."
    return s


def render_progress_bar(current, total):
    pct = int(100 * current / total)
    return f'<div class="progress-bar-outer"><div class="progress-bar-inner" style="width:{pct}%;"></div></div>'


def render_assembled_box(selected):
    if not selected:
        return '<div class="assembled-box"><span class="assembled-placeholder">（ここにタップした語句が並びます）</span></div>'
    chips = "".join(f'<span class="assembled-chip">{c}</span>' for c in selected)
    return f'<div class="assembled-box">{chips}</div>'


def pick_chunk(pos):
    chunk = st.session_state.available.pop(pos)
    st.session_state.selected.append(chunk)


def undo_last():
    if st.session_state.selected:
        chunk = st.session_state.selected.pop()
        st.session_state.available.append(chunk)


def reset_current():
    start_question(st.session_state.current_index)


def submit_answer(q):
    st.session_state.answered = True
    is_correct = st.session_state.selected == q["correct_order"]
    st.session_state.last_correct = is_correct
    if is_correct:
        st.session_state.correct_count += 1
    else:
        st.session_state.weak_points.append(
            {
                "japanese": q["japanese"],
                "correct_order": q["correct_order"],
                "user_order": list(st.session_state.selected),
                "explanation": q["explanation"],
                "ref": q["ref"],
                "lesson": q["lesson"],
            }
        )


def go_next_question():
    st.session_state.current_index += 1
    st.session_state.answered = False
    if st.session_state.current_index >= TOTAL_QUESTIONS:
        st.session_state.test_over = True
    else:
        start_question(st.session_state.current_index)


# ============================================================
# ヘッダー
# ============================================================
st.markdown('<div class="app-title">SEIJO MONDAI MASTER</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">— Lesson 3〜5 整序問題 —</div>', unsafe_allow_html=True)

# ============================================================
# 結果画面
# ============================================================
if st.session_state.test_over:
    correct_count = st.session_state.correct_count
    wrong_count = len(st.session_state.weak_points)

    st.markdown('<div class="result-title">🏁 テスト終了！</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='result-score'>{TOTAL_QUESTIONS}問中 "
        f"<span style='color:#17a86b; font-weight:700;'>{correct_count}問正解</span>"
        f" / <span style='color:#d6394a; font-weight:700;'>{wrong_count}問不正解</span></div>",
        unsafe_allow_html=True,
    )

    if st.session_state.weak_points:
        st.markdown(
            "<div style='font-size:0.95rem; font-weight:600; color:#33312e; margin-bottom:2px;'>"
            "📖 今回の弱点（お守りブック）</div>"
            "<div style='color:#8c887f; font-size:0.82rem; margin-bottom:10px;'>"
            "間違えた問題をもう一度確認しよう</div>",
            unsafe_allow_html=True,
        )
        for i, wp in enumerate(st.session_state.weak_points, start=1):
            correct_sentence = capitalize_sentence(" ".join(wp["correct_order"]))
            user_sentence = capitalize_sentence(" ".join(wp["user_order"]))
            st.markdown(
                f"""
                <div class="weakpoint-card">
                    <span class="lesson-tag">{wp['lesson']}</span>
                    <div class="weakpoint-q">Q{i}. {wp['japanese']}</div>
                    <div style="color:#c0405a; font-size:0.85rem; margin-bottom:4px;">
                        あなたの解答: {user_sentence}
                    </div>
                    <div class="weakpoint-ans">✅ 正解: {correct_sentence}</div>
                    <div class="explain-box">
                        <div class="explain-title">📝 文法解説</div>
                        {wp['explanation']}
                        <div class="ref-note">📚 参照: {wp['ref']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div style='text-align:center; font-size:1.0rem; font-weight:600; "
            "color:#17a86b; margin:6px 0 14px 0;'>🎉 全問正解！お守りブックは空っぽです</div>",
            unsafe_allow_html=True,
        )

    if st.button("🔄 もう一度挑戦する", use_container_width=True):
        init_state()
        st.rerun()

# ============================================================
# 出題画面
# ============================================================
else:
    q_idx = st.session_state.order[st.session_state.current_index]
    q = QUESTIONS[q_idx]

    st.markdown(
        f'<div class="progress-label">Q{st.session_state.current_index + 1} / {TOTAL_QUESTIONS}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        render_progress_bar(st.session_state.current_index, TOTAL_QUESTIONS),
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='score-tag'>現在の正解数: "
        f"<b style='color:#17a86b;'>{st.session_state.correct_count}</b> / "
        f"{st.session_state.current_index}</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="question-card">
            <span class="lesson-tag">{q['lesson']}</span>
            <div class="japanese-text">{q['japanese']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.answered:
        st.markdown('<div class="assembled-label">組み立て中の英文</div>', unsafe_allow_html=True)
        st.markdown(render_assembled_box(st.session_state.selected), unsafe_allow_html=True)

        if st.session_state.available:
            st.markdown('<div class="pool-label">語句をタップして並べよう</div>', unsafe_allow_html=True)
            for i, chunk in enumerate(st.session_state.available):
                if st.button(chunk, key=f"chunk_{st.session_state.current_index}_{i}_{chunk}", use_container_width=True):
                    pick_chunk(i)
                    st.rerun()

        col_undo, col_reset = st.columns(2)
        with col_undo:
            st.markdown('<div class="subtle-btn">', unsafe_allow_html=True)
            if st.button("↩️ 一つ戻す", use_container_width=True, disabled=not st.session_state.selected):
                undo_last()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with col_reset:
            st.markdown('<div class="subtle-btn">', unsafe_allow_html=True)
            if st.button("🔄 やり直す", use_container_width=True, disabled=not st.session_state.selected):
                reset_current()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state.available:
            st.markdown('<div class="decide-btn">', unsafe_allow_html=True)
            if st.button("✅ 決定 (ANSWER)", use_container_width=True):
                submit_answer(q)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        is_correct = st.session_state.last_correct
        effect_class = "effect-win" if is_correct else "effect-lose"
        result_label = "◎ CORRECT!" if is_correct else "× INCORRECT..."
        st.markdown(f'<div class="effect-text {effect_class}">{result_label}</div>', unsafe_allow_html=True)

        badge_class = "badge-correct" if is_correct else "badge-wrong"
        badge_text = "正解" if is_correct else "不正解"
        st.markdown(f'<span class="{badge_class}">{badge_text}</span>', unsafe_allow_html=True)

        correct_sentence = capitalize_sentence(" ".join(q["correct_order"]))
        user_sentence = capitalize_sentence(" ".join(st.session_state.selected))

        st.markdown(
            f"""
            <div style="font-size:0.9rem; color:#4a473f; margin:6px 0 4px 0;">
                あなたの解答: <b>{user_sentence}</b>
            </div>
            <div class="correct-sentence">✅ 正解: <b style="color:#17a86b;">{correct_sentence}</b></div>
            <div class="explain-box">
                <div class="explain-title">日本語文法解説</div>
                {q['explanation']}
                <div class="ref-note">📚 参照: {q['ref']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        is_last = st.session_state.current_index + 1 >= TOTAL_QUESTIONS
        btn_label = "🏁 結果を見る (Finish)" if is_last else "▶ 次の問題へ (Next Question)"

        if st.button(btn_label, use_container_width=True):
            go_next_question()
            st.rerun()