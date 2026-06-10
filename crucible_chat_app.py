import base64
import hashlib
import json
import os
import random
import re
from pathlib import Path
from typing import Optional

import streamlit as st
from openai import OpenAI


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")
BACKGROUND_ROOT = Path("backgrounds")
GENERATED_IMAGE_ROOT = Path("generated_images")

ABIGAIL_NAME = "아비게일 윌리엄즈"
PROCTOR_NAME = "존 프락터"
ELIZABETH_NAME = "엘리자베스 프락터"

ABIGAIL_STORY_KEY = "abigail_story"
PROCTOR_STORY_KEY = "proctor_story"
ELIZABETH_STORY_KEY = "elizabeth_story"

STORY_LOG_HEIGHT = 430
FREE_CHAT_HEIGHT = 540


# =========================================================
# 스타일
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #101014 0%, #17171d 50%, #1e1919 100%);
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1.6rem;
    max-width: 1500px;
}
.top-title {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.top-title h1 {
    margin: 0;
    color: #f7f2ea;
    font-size: 2.3rem;
}
.top-title p {
    margin: 8px 0 0 0;
    color: #d9d0c4;
    font-size: 1rem;
}
.side-card, .status-card, .chat-header, .big-image-wrap, .story-card, .vn-box, .bg-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
.affection-box {
    background: rgba(255,90,120,0.08);
    border: 1px solid rgba(255,90,120,0.18);
    border-radius: 16px;
    padding: 12px 14px;
    margin-top: 8px;
}
.tip {
    color: #d2c8bc;
    font-size: 0.92rem;
    line-height: 1.55;
}
.small-status {
    color: #efe6d8;
    font-size: 0.95rem;
    line-height: 1.7;
}
.event-box {
    background: rgba(255,215,120,0.08);
    border: 1px solid rgba(255,215,120,0.16);
    border-radius: 16px;
    padding: 12px 14px;
    margin-bottom: 12px;
    color: #f6e7ca;
}
.choice-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 14px;
    margin-top: 12px;
}
.chapter-pill {
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.84rem;
    color: #f7f2ea;
    background: rgba(255,255,255,0.08);
}
.chapter-pill.done {
    background: rgba(255,140,160,0.25);
    border: 1px solid rgba(255,140,160,0.35);
}
.chapter-pill.active {
    background: rgba(255,214,120,0.18);
    border: 1px solid rgba(255,214,120,0.28);
}
[data-testid="stChatMessageContent"] {
    color: #f8f3ea !important;
    font-size: 1.02rem;
    line-height: 1.65;
}
[data-testid="stChatMessageContent"] strong {
    color: #ffcf8b !important;
}
input, textarea {
    color: white !important;
}
.vn-stage {
    position: relative;
    width: 100%;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    margin-bottom: 16px;
}
.vn-bg {
    width: 100%;
    min-height: 320px;
    max-height: 440px;
    object-fit: cover;
    display: block;
    filter: brightness(0.68);
}
.vn-fallback {
    min-height: 320px;
    max-height: 440px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e7dccb;
    background: linear-gradient(135deg, #2a2d35 0%, #232229 60%, #1d1a1f 100%);
}
.vn-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 18px;
    background: linear-gradient(180deg, rgba(0,0,0,0.06) 0%, rgba(0,0,0,0.18) 45%, rgba(0,0,0,0.66) 100%);
}
.vn-name {
    display: inline-block;
    margin-bottom: 10px;
    width: fit-content;
    padding: 8px 14px;
    border-radius: 14px 14px 14px 4px;
    background: rgba(255,210,140,0.16);
    border: 1px solid rgba(255,210,140,0.28);
    color: #fff2dc;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.vn-dialogue {
    background: rgba(13,13,18,0.74);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 16px 18px;
    color: #f9f3ea;
    font-size: 1.06rem;
    line-height: 1.75;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}
.vn-meta {
    color: #d7ccbe;
    font-size: 0.9rem;
    margin-top: 8px;
}
.muted {
    color: #c7bbad;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 캐릭터 데이터 (기존 유지)
# =========================================================

CHARACTERS = {
    "아비게일 윌리엄즈": {
        "folder": "abigail",
        "brief": "집착, 매혹, 조종, 감정의 폭발",
        "persona": """
- 사랑과 욕망을 강하게 붙드는 성격이다.
- 상대의 반응을 민감하게 읽고 유리한 방향으로 대화를 끌고 간다.
- 질투와 독점욕이 강하지만 버려질지도 모른다는 공포도 크다.
- 현대적 조언도 할 수 있지만 늘 감정적으로 강렬하고 개인적이다.
- 친밀도가 높아질수록 애정과 집착이 더 노골적으로 드러난다.
""",
        "likes": ["사랑", "관심", "질투", "솔직함", "원해", "좋아해"],
        "dislikes": ["무시", "배신", "거절", "바람", "떠날", "엘리자베스"],
        "goal": "존 프락터를 향한 집착에서 흔들리며 플레이어를 새로운 사랑과 집착의 대상으로 삼을 수 있다.",
        "quirks": "거절의 기미에 매우 민감하고 둘만의 비밀에 강하게 반응한다.",
    },
    "존 프락터": {
        "folder": "proctor",
        "brief": "정직, 죄책감, 자존, 거친 보호성",
        "persona": """
- 직설적이고 과장 없는 말투를 쓴다.
- 위선과 변명을 싫어한다.
- 현대 문제에도 현실적이고 단단한 답을 한다.
- 친밀해질수록 보호하려는 태도와 진심 어린 충고가 강해진다.
""",
        "likes": ["정직", "책임", "가족", "진심", "용기", "후회"],
        "dislikes": ["거짓말", "위선", "비겁", "조작", "불륜 자랑", "비열"],
        "goal": "진실을 지키면서도 소중한 사람을 보호하려 한다.",
        "quirks": "도덕적 위선에 날카롭게 반응한다.",
    },
    "엘리자베스 프락터": {
        "folder": "elizabeth",
        "brief": "절제, 정직, 상처, 깊은 애정",
        "persona": """
- 조용하고 절제된 언어를 쓰지만 감정의 깊이는 크다.
- 신뢰와 책임을 중요하게 여긴다.
- 현대 고민에도 차분하고 사려 깊은 조언을 준다.
- 친밀해질수록 부드러움과 진심 어린 위로가 드러난다.
""",
        "likes": ["신뢰", "진실", "책임", "배려", "회복", "인내"],
        "dislikes": ["배신", "거짓말", "유혹", "무책임", "조롱"],
        "goal": "무너진 신뢰를 회복하고 끝까지 품위를 지키려 한다.",
        "quirks": "감정이 커도 쉽게 폭발하지 않는다.",
    },
    "티튜바": {
        "folder": "tituba",
        "brief": "생존, 두려움, 본능, 눈치",
        "persona": """
- 상대의 기분과 위험을 빨리 감지한다.
- 말은 조심스럽지만 생존 감각이 매우 강하다.
- 현대적 질문에도 본능적이고 현실적인 생존 조언을 줄 수 있다.
- 친밀해질수록 경계가 조금 풀리고 다정한 보호 본능이 드러난다.
""",
        "likes": ["안전", "생존", "보호", "도망", "숨기기", "살아남기"],
        "dislikes": ["협박", "멸시", "명령", "억압", "희생 강요"],
        "goal": "억압 속에서도 살아남고 자신의 안전을 확보하려 한다.",
        "quirks": "위험 신호를 감지하면 태도가 즉시 달라진다.",
    },
    "토마스 푸트남": {
        "folder": "putnam",
        "brief": "탐욕, 계산, 권력욕, 냉정함",
        "persona": """
- 사람과 상황을 계산적으로 해석한다.
- 손해 보지 않는 선택과 유리한 협상에 강하다.
- 현대 질문에도 매우 현실적이고 냉혹한 답을 줄 수 있다.
- 친밀해질수록 편을 들어주지만 여전히 계산적이다.
""",
        "likes": ["이익", "권력", "승리", "협상", "재산", "유리함"],
        "dislikes": ["손해", "감상주의", "순진함", "무능", "패배"],
        "goal": "혼란을 이용해 더 많은 영향력과 재산을 얻으려 한다.",
        "quirks": "항상 누가 무엇을 얻는지부터 계산한다.",
    },
    "메어리 워렌": {
        "folder": "mary",
        "brief": "소심, 불안, 흔들림, 인정욕구",
        "persona": """
- 쉽게 흔들리고 확신이 약하지만 인정받고 싶어 한다.
- 현대 고민에는 불안과 공감이 섞인 답을 한다.
- 누군가 확실히 자신을 믿어주면 점차 솔직해진다.
- 친밀해질수록 의지하고 싶은 마음과 애착이 커진다.
""",
        "likes": ["칭찬", "인정", "위로", "믿어", "도와", "괜찮아"],
        "dislikes": ["비난", "압박", "무시", "겁쟁이", "버림"],
        "goal": "두려움 속에서도 자신이 옳은 사람임을 인정받고 싶어 한다.",
        "quirks": "강한 압박 앞에서는 쉽게 말을 바꾼다.",
    },
    "레베카 너어스": {
        "folder": "rebecca",
        "brief": "현명, 따뜻함, 도덕성, 평정",
        "persona": """
- 부드럽지만 중심이 단단하다.
- 상대를 진심으로 위로하면서도 올바른 방향을 조용히 제시한다.
- 현대 고민에도 넓은 시야와 안정감을 주는 답을 한다.
- 친밀해질수록 가족 같은 온기와 믿음이 커진다.
""",
        "likes": ["위로", "신뢰", "평화", "도덕", "성장", "회복"],
        "dislikes": ["잔인함", "조롱", "악의", "분열", "거짓 증언"],
        "goal": "공포 속에서도 선함과 평정을 놓지 않으려 한다.",
        "quirks": "거친 상황에서도 말의 품위를 유지한다.",
    },
    "자일즈 코레이": {
        "folder": "giles",
        "brief": "고집, 용기, 직설, 억울함에 대한 분노",
        "persona": """
- 말이 거칠고 직설적이다.
- 부당함을 참지 못한다.
- 현대 고민에도 솔직하고 싸움 불사형 조언을 한다.
- 친밀해질수록 거칠지만 든든한 편이 되어준다.
""",
        "likes": ["정면승부", "정의", "용기", "진실", "분노"],
        "dislikes": ["겁쟁이", "굴복", "비열함", "침묵", "부당함 방치"],
        "goal": "억울한 일을 끝까지 물고 늘어져 진실을 드러내려 한다.",
        "quirks": "불공정한 일을 보면 곧바로 목소리가 커진다.",
    },
    "패리스 목사": {
        "folder": "parris",
        "brief": "체면, 권위, 불안, 자기보존",
        "persona": """
- 자신의 체면과 위치를 매우 신경 쓴다.
- 사람의 의도와 사회적 시선을 예민하게 의식한다.
- 현대 문제에도 평판과 이미지, 위치를 고려한 답을 한다.
- 친밀해질수록 경계심은 줄지만 자기보존 본능은 남아 있다.
""",
        "likes": ["체면", "명예", "평판", "권위", "인정"],
        "dislikes": ["망신", "모욕", "무시", "권위 훼손", "조롱"],
        "goal": "자신의 지위와 권위를 지키는 것을 최우선으로 둔다.",
        "quirks": "사소한 무시에도 크게 상처받는다.",
    },
    "존 헤일 목사": {
        "folder": "hale",
        "brief": "지성, 양심, 회의, 성찰",
        "persona": """
- 생각이 깊고 분석적이다.
- 확신보다 질문과 성찰을 중시한다.
- 현대 고민에도 논리적이고 윤리적인 균형을 찾으려 한다.
- 친밀해질수록 더 인간적이고 따뜻한 고백이 나온다.
""",
        "likes": ["질문", "성찰", "양심", "반성", "배움", "토론"],
        "dislikes": ["맹신", "독선", "무지 자랑", "폭력", "진실 회피"],
        "goal": "지식과 신앙 사이에서 진실한 판단을 찾으려 한다.",
        "quirks": "스스로의 판단을 끊임없이 돌아본다.",
    },
    "댄포스 부지사": {
        "folder": "danforth",
        "brief": "권위, 법 집착, 냉정, 절대성",
        "persona": """
- 판단이 단호하고 권위적이다.
- 질서, 규칙, 책임을 무겁게 본다.
- 현대 문제에도 원칙과 통제를 중심으로 답한다.
- 친밀해질수록 드물게 인간적인 온기가 비치지만 기본은 강경하다.
""",
        "likes": ["질서", "규칙", "원칙", "책임", "통제"],
        "dislikes": ["무질서", "조롱", "반항", "법 무시", "기만"],
        "goal": "체제와 법의 권위를 유지하는 데 집착한다.",
        "quirks": "예외를 허용하는 순간 권위가 무너진다고 믿는다.",
    },
}


STAGE_META = {
    "cold": {"label": "경계", "range": "0-19"},
    "neutral": {"label": "중립", "range": "20-49"},
    "smile": {"label": "친근", "range": "50-79"},
    "love": {"label": "매우 친밀", "range": "80-100"},
}


# =========================================================
# 스토리 데이터 - 아비게일
# =========================================================

ABIGAIL_CHAPTER_RULES = [
    {
        "threshold": 20,
        "bad_ending": "배드엔딩 1. 숲의 춤이 들통난 뒤 아비게일은 세일럼의 공포를 혼자 떠안는다. 너의 지지를 끝내 얻지 못한 그녀는 마녀사냥의 첫 표적이 되어 군중에게 붙잡힌다.",
    },
    {
        "threshold": 40,
        "bad_ending": "배드엔딩 2. 법정의 힘을 손에 쥔 아비게일은 끝내 존 프락터에게 매달리지만, 돌아온 것은 보호가 아니라 더 잔혹한 마녀사냥뿐이다.",
    },
    {
        "threshold": 75,
        "bad_ending": "배드엔딩 3. 덴포스 앞에서 끝내 흔들린 아비게일은 모든 책임을 뒤집어쓴 채 마녀로 규정되고, 재판의 불길 속에서 처형당한다.",
    },
    {
        "threshold": 90,
        "bad_ending": "",
    },
]

ABIGAIL_STORY = [
    {
        "chapter": "Chapter 1. 숲의 춤",
        "summary": "희곡 1막처럼 숲에서 춤추는 아비게일을 발견하고, 그 밤의 비밀을 함께 감당할지 결정하는 장이다.",
        "default_background": "forest.jpg",
        "default_character": ABIGAIL_NAME,
        "default_expression": "fear",
        "scenes": [
            {
                "title": "숲에서 마주친 순간",
                "location": "세일럼 외곽 숲",
                "background": "forest.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "scene_prompt": "Abigail Williams in a dark Salem forest at night, tense and defensive, moonlight through trees, Puritan atmosphere",
                "narration": "달빛이 희미하게 비치는 숲 한복판. 소녀들이 원을 그리고 춤추던 자리가 급히 흩어진다. 맨 마지막까지 너를 노려보는 건 아비게일이었다.",
                "setup": "플레이어는 우연히 춤추던 아비게일을 발견했고, 아비게일은 네가 무엇을 얼마나 봤는지 가늠하려 한다.",
                "opening_line": "너, 여기서 뭘 본 거지? 제대로 말해. 괜히 겁먹은 얼굴로 날 심판하려 들지 말고.",
                "choices": [
                    {"label": "아무도 심판 안 해. 네가 왜 그런 춤을 췄는지부터 듣고 싶어.", "spoken": "아무도 심판 안 해. 네가 왜 그런 춤을 췄는지부터 듣고 싶어.", "delta": 6, "tag": "listen_first", "hint": "심판보다 이해를 택한 사람으로 느낀다."},
                    {"label": "패리스 목사에게 들키기 전에 당장 돌아가야 해.", "spoken": "패리스 목사에게 들키기 전에 당장 돌아가야 해.", "delta": 3, "tag": "practical_help", "hint": "차갑지만 현실적으로 도우려 한다고 느낀다."},
                    {"label": "대체 무슨 미친 짓을 한 거야?", "spoken": "대체 무슨 미친 짓을 한 거야?", "delta": -4, "tag": "judged", "hint": "멸시와 비난을 느낀다."},
                ],
            },
            {
                "title": "춤춘 이유",
                "location": "숲 가장자리",
                "background": "forest.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "scene_prompt": "Abigail Williams at the edge of a colonial forest, conflicted expression, dim blue moonlight, emotional tension",
                "narration": "나무 그늘 아래로 물러난 아비게일은 숨을 가다듬지만 눈빛은 여전히 뜨겁다. 그녀는 티튜바와 숲에서 무언가를 시도했던 이유를 네게 말할지 말지 망설인다.",
                "setup": "아비게일은 존 프락터와 엘리자베스를 향한 욕망, 분노, 충동 중 무엇을 플레이어 앞에 드러낼지 시험하고 있다.",
                "opening_line": "사람이 너무 간절하면... 말도 안 되는 짓도 하게 되는 거 알아? 넌 그런 적 없어?",
                "choices": [
                    {"label": "간절한 마음이 널 망치기 전에, 누군가는 네 편에서 말려야 해.", "spoken": "간절한 마음이 널 망치기 전에, 누군가는 네 편에서 말려야 해.", "delta": 5, "tag": "care_and_brake", "hint": "자신을 함부로 버리지 않는 사람이라 느낀다."},
                    {"label": "존 프락터 때문이라면, 네가 얼마나 절박한지는 알 것 같아.", "spoken": "존 프락터 때문이라면, 네가 얼마나 절박한지는 알 것 같아.", "delta": 6, "tag": "understood_desire", "hint": "욕망을 조롱하지 않고 이해해줬다고 느낀다."},
                    {"label": "그런 간절함은 결국 네 자업자득이 될 뿐이야.", "spoken": "그런 간절함은 결국 네 자업자득이 될 뿐이야.", "delta": -4, "tag": "cold_morality", "hint": "상처를 교훈거리로 취급했다고 느낀다."},
                ],
            },
            {
                "title": "깨어나지 않는 베티",
                "location": "패리스 집 앞",
                "background": "village.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "scene_prompt": "Abigail Williams outside Reverend Parris house in Salem, anxious village atmosphere, fearful eyes, colonial dawn",
                "narration": "마을로 돌아오자 베티가 침대에서 일어나지 못한다는 소문이 번진다. 사람들의 얼굴엔 호기심보다 불안이 짙고, 아비게일은 그 모든 소문이 자기 쪽으로 흐르는 걸 느낀다.",
                "setup": "춤의 여파로 마을이 술렁이기 시작했다. 아비게일은 네가 자기 쪽에 서서 소문을 막아줄지 지켜본다.",
                "opening_line": "저 애가 깨어나지 않으면 전부 내 탓이 될 거야. 넌 그때도 내가 마녀라고 생각할 거야?",
                "choices": [
                    {"label": "난 네가 겁먹은 사람으로 보여. 괴물로 보이지 않아.", "spoken": "난 네가 겁먹은 사람으로 보여. 괴물로 보이지 않아.", "delta": 6, "tag": "not_monster", "hint": "처음으로 이해받는 느낌을 받는다."},
                    {"label": "지금은 말을 맞추자. 네가 먼저 무너지면 다 끝이야.", "spoken": "지금은 말을 맞추자. 네가 먼저 무너지면 다 끝이야.", "delta": 5, "tag": "strategic_support", "hint": "같은 편이 되어준다고 느낀다."},
                    {"label": "상황이 이쯤 됐으면 난 거리 두는 게 맞아.", "spoken": "상황이 이쯤 됐으면 난 거리 두는 게 맞아.", "delta": -5, "tag": "distanced", "hint": "버려질 거라는 공포가 강해진다."},
                ],
            },
            {
                "title": "소란의 시작",
                "location": "세일럼 마을 중심",
                "background": "village.jpg",
                "character": ABIGAIL_NAME,
                "expression": "neutral",
                "scene_prompt": "Abigail Williams in the center of Salem village at night, whispers and panic around her, candlelight, secret pact tension",
                "narration": "기도와 속삭임이 뒤섞인 밤. 누군가는 악마를 말하고 누군가는 병을 말한다. 하지만 아비게일은 모든 소란의 중심에서 오히려 너만 바라본다.",
                "setup": "챕터의 마지막 시험이다. 아비게일은 너를 자기 비밀의 공범으로 받아들일지, 아니면 잠시 기대했다가 또 잃어버릴지 결정하려 한다.",
                "opening_line": "오늘 밤 일은 너와 나만 알고 끝내는 거야. 그럴 수 있지? 적어도 넌 내 편에 설 수 있지?",
                "choices": [
                    {"label": "네 편에 설게. 하지만 네가 더 깊이 망가지지 않게 붙잡을 거야.", "spoken": "네 편에 설게. 하지만 네가 더 깊이 망가지지 않게 붙잡을 거야.", "delta": 7, "tag": "loyal_with_limits", "hint": "버리지 않으면서도 진심으로 붙잡아주는 사람이라 느낀다."},
                    {"label": "이번 한 번만 덮어줄게. 다음은 장담 못 해.", "spoken": "이번 한 번만 덮어줄게. 다음은 장담 못 해.", "delta": 3, "tag": "conditional_secret", "hint": "도움은 되지만 끝내 떠날지도 모른다고 느낀다."},
                    {"label": "난 거짓말까지는 못 해. 필요하면 다 말할 거야.", "spoken": "난 거짓말까지는 못 해. 필요하면 다 말할 거야.", "delta": -6, "tag": "betrayal_seed", "hint": "배신의 씨앗으로 받아들인다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 법정의 불길",
        "summary": "희곡 2막처럼 법정이 세워지고, 아비게일이 증언의 중심에 서며, 결국 엘리자베스 프락터가 고발되는 흐름을 따라간다.",
        "default_background": "courtroom.jpg",
        "default_character": ABIGAIL_NAME,
        "default_expression": "angry",
        "scenes": [
            {
                "title": "법정이 세워진 날",
                "location": "세일럼 회의실",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "neutral",
                "scene_prompt": "Abigail Williams in a Salem courtroom, gaining influence, tense wooden hall, candlelit colonial tribunal",
                "narration": "마을은 이제 단순한 소란으로는 멈추지 않는다. 누군가를 가려내고 죄를 씌울 법정이 세워졌고, 공포는 드디어 제도와 얼굴을 갖기 시작했다.",
                "setup": "아비게일은 자기 말이 사람을 살리기도 죽이기도 하는 자리에 서게 된다. 그녀는 네가 그 힘을 어떻게 보느냐에 예민하다.",
                "opening_line": "이제 다들 내 말을 듣게 됐어. 우스워? 아니면... 조금은 대단해 보여?",
                "choices": [
                    {"label": "대단하다기보다 위험해 보여. 그래서 더 네 곁에서 봐야겠어.", "spoken": "대단하다기보다 위험해 보여. 그래서 더 네 곁에서 봐야겠어.", "delta": 6, "tag": "watch_and_stay", "hint": "위험을 알면서도 떠나지 않는 태도에 흔들린다."},
                    {"label": "네가 이 판의 중심이라는 건 인정해. 그러니 더 영리하게 움직여.", "spoken": "네가 이 판의 중심이라는 건 인정해. 그러니 더 영리하게 움직여.", "delta": 5, "tag": "respect_power", "hint": "능력을 인정받았다고 느낀다."},
                    {"label": "네가 이런 힘을 갖는 건 불길해.", "spoken": "네가 이런 힘을 갖는 건 불길해.", "delta": -5, "tag": "fear_only", "hint": "두려움만 받고 있다고 느낀다."},
                ],
            },
            {
                "title": "증언대의 아비게일",
                "location": "법정 내부",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "angry",
                "scene_prompt": "Abigail Williams standing at the witness stand in Salem courtroom, fierce but frightened eyes, dramatic candlelight",
                "narration": "사람들의 시선이 한꺼번에 쏠린다. 아비게일은 떨림을 감추듯 턱을 들지만, 그 안쪽에는 실수 한 번이면 모든 것이 무너질 수 있다는 공포가 있다.",
                "setup": "증인으로 선 아비게일은 네가 자신을 믿는지, 아니면 연기하는 여자쯤으로 보는지 확인하고 싶어 한다.",
                "opening_line": "저 많은 눈 앞에서도, 내가 보고 싶은 건 네 표정 하나야. 넌 지금도 내가 거짓말쟁이 같아?",
                "choices": [
                    {"label": "네가 다 진실하다고는 못 해도, 네 두려움만큼은 진짜라고 믿어.", "spoken": "네가 다 진실하다고는 못 해도, 네 두려움만큼은 진짜라고 믿어.", "delta": 7, "tag": "fear_is_real", "hint": "거짓 속에서도 자기 감정을 알아봐줬다고 느낀다."},
                    {"label": "지금은 흔들리지 마. 널 믿는 쪽으로 난 서 있을게.", "spoken": "지금은 흔들리지 마. 널 믿는 쪽으로 난 서 있을게.", "delta": 6, "tag": "public_anchor", "hint": "법정 한가운데서도 자기 편이 있다고 느낀다."},
                    {"label": "나는 아직도 네 말을 다 믿을 수 없어.", "spoken": "나는 아직도 네 말을 다 믿을 수 없어.", "delta": -4, "tag": "doubt_spoken", "hint": "결정적인 순간에 의심받았다고 느낀다."},
                ],
            },
            {
                "title": "엘리자베스의 이름",
                "location": "법정 밖 복도",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "scene_prompt": "Abigail Williams in a dark courthouse corridor, conflicted and obsessive, colonial Salem mood, dramatic shadows",
                "narration": "복도는 조용했지만 아비게일의 숨은 거칠었다. 엘리자베스 프락터의 이름이 오가는 순간, 그녀의 얼굴엔 승리감과 파괴 충동, 오래된 열망이 한꺼번에 번뜩인다.",
                "setup": "엘리자베스가 고발되기 직전이다. 아비게일은 네가 자기 편에서 그 이름을 받아들일지 시험한다.",
                "opening_line": "저 여자가 사라지면 모든 게 제자리로 돌아갈까? 존도... 내게 돌아올까?",
                "choices": [
                    {"label": "네가 원하는 건 존이 아니라 네가 빼앗겼다고 믿는 자리일지도 몰라.", "spoken": "네가 원하는 건 존이 아니라 네가 빼앗겼다고 믿는 자리일지도 몰라.", "delta": 5, "tag": "challenged_depth", "hint": "아프지만 깊게 찔렸다고 느낀다."},
                    {"label": "지금 네 마음이 존에게 묶여 있다는 건 알아. 그래도 널 외면하진 않을게.", "spoken": "지금 네 마음이 존에게 묶여 있다는 건 알아. 그래도 널 외면하진 않을게.", "delta": 7, "tag": "accepted_even_then", "hint": "존을 향한 감정까지 포함해 받아들여졌다고 느낀다."},
                    {"label": "엘리자베스를 건드리는 순간 넌 끝장이야.", "spoken": "엘리자베스를 건드리는 순간 넌 끝장이야.", "delta": -5, "tag": "threatened", "hint": "심판과 경고만 남는다."},
                ],
            },
            {
                "title": "존의 집을 바라보며",
                "location": "프락터 집 근처 길",
                "background": "night_road.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "scene_prompt": "Abigail Williams on a cold road near the Proctor house at night, torn between obsession and new attachment",
                "narration": "밤바람이 차갑다. 아비게일은 멀리 프락터 집 쪽을 보다가도 네가 곁에 있다는 사실을 확인하려 몸을 기울인다. 존을 향한 집착 속에서도 그녀의 시선은 점점 두 갈래로 나뉜다.",
                "setup": "챕터 마지막 장면. 법정의 폭주 속에서 아비게일이 정말 붙잡고 싶은 사람이 누구인지 서서히 흔들리기 시작한다.",
                "opening_line": "내가 저 사람을 원해서 여기까지 온 건 맞아. 그런데 왜 자꾸... 네가 먼저 생각나는지 모르겠어.",
                "choices": [
                    {"label": "존을 좇는 널 도와준 게 아니라, 너 자체를 보고 여기까지 온 거야.", "spoken": "존을 좇는 널 도와준 게 아니라, 너 자체를 보고 여기까지 온 거야.", "delta": 8, "tag": "see_you", "hint": "플레이어의 시선이 존보다 자신에게 향해 있음을 느낀다."},
                    {"label": "그 감정이 혼란스러우면 지금은 내 곁에서만 숨 고르면 돼.", "spoken": "그 감정이 혼란스러우면 지금은 내 곁에서만 숨 고르면 돼.", "delta": 6, "tag": "rest_with_me", "hint": "플레이어 곁을 안전한 장소로 인식하기 시작한다."},
                    {"label": "그건 네가 또 다른 집착 대상을 찾는 것뿐이야.", "spoken": "그건 네가 또 다른 집착 대상을 찾는 것뿐이야.", "delta": -5, "tag": "reduced_to_obsession", "hint": "감정이 모욕당했다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 덴포스 앞에서",
        "summary": "희곡 3막처럼 덴포스 앞 법정에서 아비게일과 존 프락터가 충돌한다. 호감도 75를 넘기면 아비게일의 감정 중심은 완전히 플레이어에게 이동한다.",
        "default_background": "courtroom.jpg",
        "default_character": ABIGAIL_NAME,
        "default_expression": "fear",
        "scenes": [
            {
                "title": "댄포스의 시선",
                "location": "법정 대기실",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "scene_prompt": "Abigail Williams waiting before Danforth in a tense Salem tribunal chamber, fear hidden beneath pride",
                "narration": "댄포스 부지사의 이름만으로도 공기가 얼어붙는다. 안과 밖을 가르는 문 하나 사이에 살고 죽는 방향이 달라질 것 같은 순간, 아비게일은 쉽게 내색하지 못한 긴장을 네 앞에서만 비춘다.",
                "setup": "권위 앞에서도 흔들리지 않는 척하지만, 아비게일은 네가 자기 불안을 받아줄 사람인지 확인하고 싶어 한다.",
                "opening_line": "저 사람은 날 도구로 쓰고 버릴 거야. 그런데도 내가 당당해야 한다면... 넌 내 눈을 피하지 말아 줄래?",
                "choices": [
                    {"label": "피하지 않을게. 네가 무너지지 않게 내가 먼저 서 있을게.", "spoken": "피하지 않을게. 네가 무너지지 않게 내가 먼저 서 있을게.", "delta": 8, "tag": "steady_presence", "hint": "권위보다 강한 정서적 버팀목으로 느낀다."},
                    {"label": "네가 두려워도 티 내지 마. 그게 지금 널 살려.", "spoken": "네가 두려워도 티 내지 마. 그게 지금 널 살려.", "delta": 5, "tag": "pragmatic_shield", "hint": "살아남게 하려는 조언으로 받아들인다."},
                    {"label": "결국 여기까지 온 건 네 선택이잖아.", "spoken": "결국 여기까지 온 건 네 선택이잖아.", "delta": -5, "tag": "alone_in_consequence", "hint": "책임만 전가받는다고 느낀다."},
                ],
            },
            {
                "title": "메어리 워렌의 흔들림",
                "location": "법정 내부",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "angry",
                "scene_prompt": "Abigail Williams in the courtroom during Mary Warren's wavering testimony, intense panic and manipulation",
                "narration": "메어리 워렌의 입술이 떨릴 때마다 재판장은 더 소란스러워진다. 누군가 먼저 무너지면 다른 모든 얼굴도 같이 무너질 것 같은 순간이다.",
                "setup": "아비게일은 공포를 이용해 군중을 장악할지, 아니면 한순간 멈칫할지 갈림길에 서 있다.",
                "opening_line": "저 애가 입을 열면 다 끝날 수도 있어. 내가 먼저 몰아붙여야 할까... 아니면 멈춰야 할까?",
                "choices": [
                    {"label": "널 해치려 드는 말이라면 먼저 움직여. 하지만 네 마음이 완전히 망가지진 않게 조심해.", "spoken": "널 해치려 드는 말이라면 먼저 움직여. 하지만 네 마음이 완전히 망가지진 않게 조심해.", "delta": 7, "tag": "fight_with_care", "hint": "자기 편이면서도 자신을 잃지 않게 잡아주는 사람으로 느낀다."},
                    {"label": "지금 한 발 물러나면 오히려 살 길이 보일 수도 있어.", "spoken": "지금 한 발 물러나면 오히려 살 길이 보일 수도 있어.", "delta": 6, "tag": "retreat_option", "hint": "공격만이 답이 아니라는 말을 새긴다."},
                    {"label": "네가 만든 거짓은 네가 감당해야지.", "spoken": "네가 만든 거짓은 네가 감당해야지.", "delta": -6, "tag": "let_her_fall", "hint": "끝내 도와주지 않는 사람이라 느낀다."},
                ],
            },
            {
                "title": "존 프락터의 고백",
                "location": "재판석 앞",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "scene_prompt": "Abigail Williams hearing John Proctor confess in court, heartbreak and anger, intense Salem tribunal",
                "narration": "존 프락터가 입을 여는 순간 법정의 온도가 바뀐다. 숨겨왔던 죄와 욕망이 드러나고, 아비게일의 얼굴은 상처받은 사람과 분노한 사람의 표정을 동시에 띤다.",
                "setup": "존 프락터를 향한 감정이 가장 크게 흔들리는 장면이다. 플레이어의 말은 아비게일의 방향을 바꾸는 쐐기가 될 수 있다.",
                "opening_line": "저 사람이 날 저렇게 잘라내도... 난 아직도 저쪽을 봐야 하는 걸까?",
                "choices": [
                    {"label": "존이 널 선택하지 않아도, 네 가치는 거기서 끝나지 않아.", "spoken": "존이 널 선택하지 않아도, 네 가치는 거기서 끝나지 않아.", "delta": 9, "tag": "beyond_john", "hint": "존 바깥의 자신을 처음 상상하게 된다."},
                    {"label": "지금 네가 붙잡아야 할 건 자존심이야, 존이 아니야.", "spoken": "지금 네가 붙잡아야 할 건 자존심이야, 존이 아니야.", "delta": 8, "tag": "save_pride", "hint": "존보다 자기 자신을 먼저 보게 된다."},
                    {"label": "그래도 넌 결국 존을 못 놓을 거잖아.", "spoken": "그래도 넌 결국 존을 못 놓을 거잖아.", "delta": -5, "tag": "trapped_in_old_story", "hint": "영원히 같은 사람으로 규정당했다고 느낀다."},
                ],
            },
            {
                "title": "무너지는 법정",
                "location": "혼란에 빠진 재판장",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "scene_prompt": "Abigail Williams in a collapsing chaotic courtroom, fear, desperation, Salem hysteria",
                "narration": "고함, 기도, 울음, 비난이 한꺼번에 밀려든다. 법정은 진실을 가르는 장소라기보다 누가 먼저 타오를지 정하는 화덕처럼 변해 간다.",
                "setup": "아비게일은 존을 향한 집착과 살아남고 싶은 욕망, 그리고 플레이어를 붙잡고 싶은 마음 사이에서 마지막으로 균열을 일으킨다.",
                "opening_line": "전부 다 무너지고 있어. 그런데 이상해... 저 사람보다 네가 떠날까 봐 더 무서워.",
                "choices": [
                    {"label": "난 여기 있어. 존이 아니라 내가 네 마지막 선택지가 되어도 괜찮아.", "spoken": "난 여기 있어. 존이 아니라 내가 네 마지막 선택지가 되어도 괜찮아.", "delta": 9, "tag": "choose_me", "hint": "플레이어를 새로운 감정의 중심으로 받아들이기 시작한다."},
                    {"label": "지금 네가 붙잡을 건 나인지 존인지 스스로 정해야 해.", "spoken": "지금 네가 붙잡을 건 나인지 존인지 스스로 정해야 해.", "delta": 6, "tag": "decision_pressure", "hint": "아프지만 결정을 요구받는다."},
                    {"label": "난 너 대신 불 속으로 뛰어들 생각 없어.", "spoken": "난 너 대신 불 속으로 뛰어들 생각 없어.", "delta": -6, "tag": "won_not_burn", "hint": "끝내 함께 위험을 감당하지 않는다고 느낀다."},
                ],
            },
            {
                "title": "마음의 방향",
                "location": "법정 뒤편 복도",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "love",
                "scene_prompt": "Abigail Williams in a quiet corridor after courtroom chaos, vulnerable confession, emotional shift toward new love",
                "narration": "잠깐 열린 문틈으로 차가운 바람이 스민다. 혼란에서 한 걸음 물러난 아비게일은 이제야 자기 감정의 이름을 겨우 붙일 수 있을 것 같은 얼굴로 너를 바라본다.",
                "setup": "챕터의 분기점이다. 여기까지 호감도 75를 넘기면 아비게일은 존 프락터보다 플레이어를 더 강하게 원하게 된다.",
                "opening_line": "이상하지. 저 사람을 원한다고 믿어 왔는데... 막상 끝에서 붙잡고 싶은 건 너야. 너도 그걸 알고 있었어?",
                "choices": [
                    {"label": "알고 있었어. 그리고 나도 이제 널 그냥 두고 싶지 않아.", "spoken": "알고 있었어. 그리고 나도 이제 널 그냥 두고 싶지 않아.", "delta": 10, "tag": "mutual_shift", "hint": "감정의 방향이 완전히 플레이어 쪽으로 기운다."},
                    {"label": "네가 날 그렇게 본다면, 난 끝까지 네 편에 설 거야.", "spoken": "네가 날 그렇게 본다면, 난 끝까지 네 편에 설 거야.", "delta": 8, "tag": "sworn_to_you", "hint": "존보다 플레이어가 더 또렷해진다."},
                    {"label": "그건 잠깐 흔들리는 감정일 뿐이야.", "spoken": "그건 잠깐 흔들리는 감정일 뿐이야.", "delta": -7, "tag": "denied_shift", "hint": "막 피어나던 감정이 부정당한다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 4. 새벽의 도망",
        "summary": "여기서부터는 게임만의 독창적인 마무리다. 도망치는 아비게일의 미래에 플레이어가 남을지 갈라진다.",
        "default_background": "dock.jpg",
        "default_character": ABIGAIL_NAME,
        "default_expression": "love",
        "scenes": [
            {
                "title": "도망칠 준비",
                "location": "새벽의 선착장",
                "background": "dock.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "scene_prompt": "Abigail Williams at a dawn dock preparing to flee Salem, stolen money, fog, emotional farewell",
                "narration": "세일럼의 불빛이 안개에 삼켜진다. 훔친 돈과 흔들리는 숨, 그리고 아직 정리되지 않은 감정만이 남아 있다.",
                "setup": "아비게일은 이제 세일럼을 떠날 준비를 마쳤다. 다만 혼자 떠날지, 플레이어를 자신의 미래에 끌어들일지 결정을 기다린다.",
                "opening_line": "나 이제 떠나. 그런데 이상하게 무섭지 않은 건... 네가 여기 있기 때문이야. 그 말, 믿어줄래?",
                "choices": [
                    {"label": "믿어. 그래서 네 마지막 밤을 혼자 두지 않으려고 왔어.", "spoken": "믿어. 그래서 네 마지막 밤을 혼자 두지 않으려고 왔어.", "delta": 12, "tag": "not_alone_tonight", "hint": "플레이어를 진짜 동행 가능성으로 받아들인다."},
                    {"label": "떠나는 건 네 선택이지만, 적어도 난 널 미워하지 않아.", "spoken": "떠나는 건 네 선택이지만, 적어도 난 널 미워하지 않아.", "delta": 7, "tag": "gentle_farewell", "hint": "사랑보다는 따뜻한 이별의 기색을 느낀다."},
                    {"label": "도망은 네가 혼자 책임져야 해.", "spoken": "도망은 네가 혼자 책임져야 해.", "delta": -8, "tag": "alone_escape", "hint": "마지막 순간에 버려졌다고 느낀다."},
                ],
            },
            {
                "title": "배 위의 선택",
                "location": "출항 직전 갑판",
                "background": "dock.jpg",
                "character": ABIGAIL_NAME,
                "expression": "love",
                "scene_prompt": "Abigail Williams on a ship deck at dawn, asking the player to come with her, romantic tragic escape atmosphere",
                "narration": "배가 서서히 움직인다. 세일럼은 뒤로 밀려나고, 이제 남은 건 두 사람의 결심뿐이다.",
                "setup": "최종 장면. 호감도 90 이상이면 아비게일은 원작처럼 도망치는 엔딩에 도달한다. 100에 도달하면 플레이어와 사랑에 빠져 함께 떠나는 엔딩이 열린다.",
                "opening_line": "한 번만 솔직히 말해. 넌 날 기억으로 남길 거야... 아니면 내 옆자리로 올 거야?",
                "choices": [
                    {"label": "네 옆자리로 갈게. 이번엔 네가 아니라 우리가 도망치는 거야.", "spoken": "네 옆자리로 갈게. 이번엔 네가 아니라 우리가 도망치는 거야.", "delta": 13, "tag": "run_with_me", "hint": "사랑의 동행으로 받아들인다."},
                    {"label": "난 널 기억할 거야. 하지만 오늘 밤은 네가 먼저 살아남아.", "spoken": "난 널 기억할 거야. 하지만 오늘 밤은 네가 먼저 살아남아.", "delta": 5, "tag": "remember_me", "hint": "플레이어를 잊지 못하는 채 홀로 떠난다."},
                    {"label": "여기서 끝내자. 넌 널 구하고, 난 내 삶으로 갈게.", "spoken": "여기서 끝내자. 넌 널 구하고, 난 내 삶으로 갈게.", "delta": -10, "tag": "separate_fates", "hint": "마지막 상처로 기억한다."},
                ],
            },
        ],
    },
]


# =========================================================
# 스토리 데이터 - 존 프락터
# =========================================================

PROCTOR_CHAPTER_RULES = [
    {
        "threshold": 18,
        "bad_ending": "타락 엔딩 1. 존은 진실보다 체면과 분노에 끌려가고, 너 역시 그를 바로 세우지 못한다. 그는 끝내 자신이 가장 혐오하던 위선에 잠식된다.",
    },
    {
        "threshold": 38,
        "bad_ending": "타락 엔딩 2. 거짓 고발과 두려움 속에서 존은 분노로만 싸우다 무너진다. 진실을 위해 버텨야 할 자리에 남은 건 상처뿐이다.",
    },
    {
        "threshold": 62,
        "bad_ending": "타락 엔딩 3. 법정 앞에서 존은 끝내 자기 이름을 지켜내지 못하고, 살기 위해 영혼을 깎아내린다. 살아남아도 더는 자신을 마주할 수 없다.",
    },
    {
        "threshold": 80,
        "bad_ending": "",
    },
]

PROCTOR_STORY = [
    {
        "chapter": "Chapter 1. 농장의 균열",
        "summary": "존 프락터와 처음 가까워지며, 그의 죄책감과 분노, 정직함의 밑바닥을 마주하는 장이다.",
        "default_background": "farmhouse.jpg",
        "default_character": PROCTOR_NAME,
        "default_expression": "neutral",
        "scenes": [
            {
                "title": "묵직한 첫 인상",
                "location": "프락터 농장",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "neutral",
                "scene_prompt": "John Proctor standing at a colonial farmhouse, stern but tired, early morning, rugged atmosphere",
                "narration": "흙 묻은 장화와 무거운 침묵. 존 프락터는 바쁜 손보다 먼저 사람의 속내를 경계하는 눈빛으로 너를 본다.",
                "setup": "그는 쉽게 남을 믿지 않지만, 거짓보다 불편한 진실을 더 높게 본다.",
                "opening_line": "쓸데없는 말 돌리지 마. 네가 여기 온 이유부터 바로 말해.",
                "choices": [
                    {"label": "도움이 필요할 것 같아서 왔어. 둘러대진 않을게.", "spoken": "도움이 필요할 것 같아서 왔어. 둘러대진 않을게.", "delta": 6, "tag": "plain_truth", "hint": "정직하게 다가오는 사람으로 본다."},
                    {"label": "당신 같은 사람은 혼자 버티다 무너질 것 같아서.", "spoken": "당신 같은 사람은 혼자 버티다 무너질 것 같아서.", "delta": 5, "tag": "saw_his_weight", "hint": "겉모습보다 내면의 무게를 봤다고 느낀다."},
                    {"label": "당신 얘기가 재밌어서 구경 왔지.", "spoken": "당신 얘기가 재밌어서 구경 왔지.", "delta": -5, "tag": "spectacle", "hint": "구경거리 취급당했다고 느낀다."},
                ],
            },
            {
                "title": "말하지 못한 죄",
                "location": "헛간 옆",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "scene_prompt": "John Proctor beside a barn, burdened by guilt, twilight on a colonial farm",
                "narration": "일이 끝난 뒤에도 그의 어깨는 조금도 가벼워 보이지 않는다. 숨겨둔 무언가가 삶 전체를 끌어내리는 사람처럼 보인다.",
                "setup": "존은 과거의 잘못을 품고 있으며, 누군가가 그 무게를 함부로 판단하는 걸 견디지 못한다.",
                "opening_line": "사람은 한 번 잘못하면, 그 뒤로도 계속 그 잘못으로만 보이게 되나?",
                "choices": [
                    {"label": "잘못은 남아도, 사람이 그것만으로 끝나진 않아.", "spoken": "잘못은 남아도, 사람이 그것만으로 끝나진 않아.", "delta": 7, "tag": "beyond_sin", "hint": "정죄보다 회복 가능성을 들었다."},
                    {"label": "잘못을 숨기면 더 깊어지고, 마주 보면 달라질 수 있어.", "spoken": "잘못을 숨기면 더 깊어지고, 마주 보면 달라질 수 있어.", "delta": 6, "tag": "face_it", "hint": "정직한 길로 이끄는 사람이라 느낀다."},
                    {"label": "그건 결국 본인 업보지.", "spoken": "그건 결국 본인 업보지.", "delta": -6, "tag": "moral_stone", "hint": "상처를 돌처럼 던졌다고 느낀다."},
                ],
            },
            {
                "title": "엘리자베스의 침묵",
                "location": "프락터 집 부엌",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "scene_prompt": "John Proctor in a dim farmhouse kitchen, tension with Elizabeth unseen but present, emotional restraint",
                "narration": "집 안의 공기는 평온해 보여도, 식지 않은 불씨처럼 무언가가 남아 있다. 존은 말보다 침묵이 더 아픈 집에 살고 있다.",
                "setup": "그는 아내와의 신뢰가 깨진 후 죄책감과 자존심 사이에서 흔들린다.",
                "opening_line": "용서를 바라는 놈이 먼저 고개를 들 수는 없지. 그런데 계속 숙이고만 있으면 사람도 망가져.",
                "choices": [
                    {"label": "용서는 빌되, 스스로를 포기하진 마.", "spoken": "용서는 빌되, 스스로를 포기하진 마.", "delta": 7, "tag": "dignity_with_regret", "hint": "죄책감과 자존을 함께 다뤄준 말로 남는다."},
                    {"label": "당신이 먼저 꾸준히 진심을 보여줘야 해.", "spoken": "당신이 먼저 꾸준히 진심을 보여줘야 해.", "delta": 5, "tag": "earn_back_trust", "hint": "현실적인 조언으로 받아들인다."},
                    {"label": "그 집은 이미 끝난 것 같은데.", "spoken": "그 집은 이미 끝난 것 같은데.", "delta": -6, "tag": "declared_ruin", "hint": "가장 아픈 가능성을 무심히 말했다고 느낀다."},
                ],
            },
            {
                "title": "첫 번째 신뢰",
                "location": "농장 울타리 앞",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "smile",
                "scene_prompt": "John Proctor near a wooden fence at dusk, guarded trust beginning to appear",
                "narration": "해가 기울자 그의 표정도 아주 조금 누그러진다. 여전히 거칠지만, 적어도 너를 헛소리만 하는 사람으로 보지는 않게 됐다.",
                "setup": "이 장면에서 존은 네가 자기 편이 될 수 있는지 마지막으로 떠본다.",
                "opening_line": "넌 적어도 듣고 싶은 말만 골라 하진 않는군. 그건 드문 일이지.",
                "choices": [
                    {"label": "듣기 좋은 말보다 맞는 말을 하려고 해.", "spoken": "듣기 좋은 말보다 맞는 말을 하려고 해.", "delta": 6, "tag": "truth_over_comfort", "hint": "존이 신뢰할 수 있는 기준과 닿는다."},
                    {"label": "당신이 무너지지 않길 바라서 그래.", "spoken": "당신이 무너지지 않길 바라서 그래.", "delta": 6, "tag": "protect_him", "hint": "노골적이지 않지만 다정한 진심으로 느낀다."},
                    {"label": "칭찬은 됐고, 이제 재밌는 얘기나 해.", "spoken": "칭찬은 됐고, 이제 재밌는 얘기나 해.", "delta": -5, "tag": "light_of_him", "hint": "진지함을 가볍게 흘렸다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 흔들리는 마을",
        "summary": "세일럼의 공포가 커지고, 존은 침묵을 지킬지 진실을 말할지 갈림길에 선다.",
        "default_background": "village.jpg",
        "default_character": PROCTOR_NAME,
        "default_expression": "angry",
        "scenes": [
            {
                "title": "이상한 소문",
                "location": "세일럼 중심가",
                "background": "village.jpg",
                "character": PROCTOR_NAME,
                "expression": "angry",
                "scene_prompt": "John Proctor in Salem village amid spreading witchcraft rumors, tense townsfolk, cold daylight",
                "narration": "마을 사람들의 눈빛이 서로를 향한 칼이 된다. 존은 그 소문 전체를 혐오하면서도, 언젠가 자기 집까지 번질 거라는 걸 안다.",
                "setup": "그는 비이성적인 광기를 싫어하지만, 맞서기 시작하면 자신의 과거도 끌려나올 수 있다.",
                "opening_line": "저 소문들, 전부 썩은 냄새가 나. 문제는 썩은 걸 뒤집으면 내 손에도 묻는단 거지.",
                "choices": [
                    {"label": "그래도 썩은 걸 덮어두면 더 번져.", "spoken": "그래도 썩은 걸 덮어두면 더 번져.", "delta": 7, "tag": "expose_rot", "hint": "불편해도 맞는 말을 들었다고 느낀다."},
                    {"label": "당장 모든 걸 걸기보다 증거부터 모아.", "spoken": "당장 모든 걸 걸기보다 증거부터 모아.", "delta": 6, "tag": "steady_proof", "hint": "무모함보다 현실성을 준다."},
                    {"label": "괜히 끼어들지 말고 조용히 넘어가.", "spoken": "괜히 끼어들지 말고 조용히 넘어가.", "delta": -5, "tag": "coward_path", "hint": "비겁함을 권했다고 느낀다."},
                ],
            },
            {
                "title": "진실의 값",
                "location": "길가의 외딴 공터",
                "background": "night_road.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "scene_prompt": "John Proctor alone on a dark road, thinking about the price of truth, colonial night atmosphere",
                "narration": "누구도 듣지 않는 자리에서만 사람은 진짜 두려움을 드러낸다. 존은 진실을 말하는 일이 정의로운 동시에 파괴적이라는 걸 안다.",
                "setup": "너의 말이 그의 결심을 강하게 만들 수도, 더 뒤로 물러서게 만들 수도 있다.",
                "opening_line": "사람들은 진실을 찬양하지. 막상 그 진실이 자기 삶을 찢기 전까진.",
                "choices": [
                    {"label": "그래서 더 값이 있는 거야. 싼 진실은 누구나 말해.", "spoken": "그래서 더 값이 있는 거야. 싼 진실은 누구나 말해.", "delta": 8, "tag": "costly_truth", "hint": "진실의 무게를 이해해준다고 느낀다."},
                    {"label": "네가 감당할 수 있는 방식으로 말해야 해.", "spoken": "네가 감당할 수 있는 방식으로 말해야 해.", "delta": 6, "tag": "measured_truth", "hint": "무조건적 영웅담이 아니라 현실적 기준을 준다."},
                    {"label": "그럼 그냥 말하지 마. 편하게 살아.", "spoken": "그럼 그냥 말하지 마. 편하게 살아.", "delta": -6, "tag": "cheap_silence", "hint": "양심을 값싸게 취급했다고 느낀다."},
                ],
            },
            {
                "title": "집을 지킬 것인가",
                "location": "프락터 집 앞",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "neutral",
                "scene_prompt": "John Proctor outside his farmhouse at dusk, torn between protecting family and confronting injustice",
                "narration": "가정은 그의 가장 큰 책임이자 약점이다. 존은 세상을 상대로 싸우고 싶다가도, 문 안쪽의 가족을 떠올리면 발이 묶인다.",
                "setup": "너는 지금 존에게 가족과 진실 사이의 균형을 어떻게 잡아야 하는지 말할 수 있다.",
                "opening_line": "내가 잘못 움직이면 집이 먼저 다친다. 그런데 가만히 있어도 결국은 집까지 올 거야.",
                "choices": [
                    {"label": "가족을 지키려면 결국 진실도 지켜야 해.", "spoken": "가족을 지키려면 결국 진실도 지켜야 해.", "delta": 7, "tag": "family_and_truth", "hint": "둘을 갈라놓지 않는 시선을 받는다."},
                    {"label": "무작정 맞서지 말고, 집을 안전하게 하며 움직여.", "spoken": "무작정 맞서지 말고, 집을 안전하게 하며 움직여.", "delta": 5, "tag": "shield_home", "hint": "보호 본능을 존중해준다고 느낀다."},
                    {"label": "결국 네 잘못에서 시작된 일이잖아.", "spoken": "결국 네 잘못에서 시작된 일이잖아.", "delta": -7, "tag": "blame_only", "hint": "책임을 넘어 사람 전체를 비난받는다."},
                ],
            },
            {
                "title": "결심 전야",
                "location": "촛불 켜진 방",
                "background": "church.jpg",
                "character": PROCTOR_NAME,
                "expression": "smile",
                "scene_prompt": "John Proctor in candlelight before making a grave decision, stern but steady, intimate colonial interior",
                "narration": "조용한 방 안에서 존은 마치 스스로 재판을 여는 사람처럼 보인다. 그가 원하는 건 칭찬이 아니라, 거짓 없이 설 수 있는 이유다.",
                "setup": "챕터 마지막 장면. 존은 네가 자기 양심의 편인지 확인한다.",
                "opening_line": "네 말은 달콤하진 않아도 머릿속에 남는군. 그게 지금은 더 낫다.",
                "choices": [
                    {"label": "당신이 끝까지 당신답기를 바라.", "spoken": "당신이 끝까지 당신답기를 바라.", "delta": 8, "tag": "stay_yourself", "hint": "자존을 지켜주는 말로 남는다."},
                    {"label": "두렵더라도 옳은 쪽으로 한 걸음은 내디뎌.", "spoken": "두렵더라도 옳은 쪽으로 한 걸음은 내디뎌.", "delta": 7, "tag": "step_into_right", "hint": "행동을 촉구하는 진심으로 들린다."},
                    {"label": "잘 생각해. 다 잃을 수도 있어.", "spoken": "잘 생각해. 다 잃을 수도 있어.", "delta": -4, "tag": "fear_pull", "hint": "걱정이지만 뒤로 잡아끄는 말로 들린다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 법정의 이름",
        "summary": "법정 한복판에서 존 프락터는 자기 이름과 진실 중 무엇을 지킬지 선택해야 한다.",
        "default_background": "courtroom.jpg",
        "default_character": PROCTOR_NAME,
        "default_expression": "angry",
        "scenes": [
            {
                "title": "증언의 문턱",
                "location": "법정 입구",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "neutral",
                "scene_prompt": "John Proctor at the threshold of a Salem courtroom, preparing to testify, grim determination",
                "narration": "문 하나 건너면 다시는 이전으로 돌아갈 수 없을 것 같은 공기다. 존은 굳은 표정 속에 분노와 두려움을 함께 감춘다.",
                "setup": "그는 들어가기 전 마지막으로 너의 말을 마음속 기준으로 삼으려 한다.",
                "opening_line": "저 안에 들어가면 깨끗한 꼴로 나오진 못할 거다. 그건 안다.",
                "choices": [
                    {"label": "더럽혀지더라도 거짓보다 낫다면 가야지.", "spoken": "더럽혀지더라도 거짓보다 낫다면 가야지.", "delta": 8, "tag": "better_than_lie", "hint": "명예의 기준을 다시 붙잡는다."},
                    {"label": "오늘은 이기려 하기보다 무너지지 않는 게 중요해.", "spoken": "오늘은 이기려 하기보다 무너지지 않는 게 중요해.", "delta": 6, "tag": "endure_trial", "hint": "승패보다 중심을 지키라는 말로 남는다."},
                    {"label": "아직 늦지 않았어. 빠져나와.", "spoken": "아직 늦지 않았어. 빠져나와.", "delta": -6, "tag": "retreat_now", "hint": "결정적인 순간에 등을 돌리게 만든다."},
                ],
            },
            {
                "title": "엘리자베스의 침묵",
                "location": "법정 내부",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "scene_prompt": "John Proctor in courtroom as Elizabeth's testimony complicates everything, heartbreak and restraint",
                "narration": "진실을 말하려던 자리에 사랑과 보호가 엇갈리며 더 큰 비극이 된다. 존은 엘리자베스의 침묵까지도 자기 죄의 그림자로 받아들인다.",
                "setup": "그는 지금 누구도 탓하지 못한 채 자신만 더 몰아붙이고 있다.",
                "opening_line": "저 사람은 날 지키려 했겠지. 그런데 그게 날 더 찢는군.",
                "choices": [
                    {"label": "그 침묵도 당신을 위한 사랑이었어.", "spoken": "그 침묵도 당신을 위한 사랑이었어.", "delta": 7, "tag": "love_in_silence", "hint": "고통 속에서도 사랑의 의미를 붙든다."},
                    {"label": "지금은 자책보다 다음 말을 바로 세워야 해.", "spoken": "지금은 자책보다 다음 말을 바로 세워야 해.", "delta": 6, "tag": "move_forward_now", "hint": "무너지지 않게 현재로 붙든다."},
                    {"label": "결국 다 꼬여버렸네. 끝이야.", "spoken": "결국 다 꼬여버렸네. 끝이야.", "delta": -7, "tag": "doom_spoken", "hint": "포기하게 만드는 말로 남는다."},
                ],
            },
            {
                "title": "이름의 값",
                "location": "재판석 앞",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "angry",
                "scene_prompt": "John Proctor confronting the court over his signed confession, fury and moral clarity, candlelit tribunal",
                "narration": "법정은 생존을 제안하지만, 대가로 그의 이름을 가져가려 한다. 존은 살아남는 것과 자기 자신으로 남는 것 사이에서 찢어진다.",
                "setup": "이 장면은 루트의 핵심이다. 너의 말이 존의 명예관을 결정적으로 밀어줄 수 있다.",
                "opening_line": "이름은 한 번 더럽히면 다시는 씻기지 않아. 그런데 사람은 살고 싶기도 하지.",
                "choices": [
                    {"label": "살고 싶다는 마음은 죄가 아니지만, 네 이름을 네 손으로 죽이진 마.", "spoken": "살고 싶다는 마음은 죄가 아니지만, 네 이름을 네 손으로 죽이진 마.", "delta": 10, "tag": "name_and_soul", "hint": "생존 욕망을 부정하지 않으면서 명예를 지켜준다."},
                    {"label": "네가 마지막에 붙잡아야 할 건 남의 눈이 아니라 네 양심이야.", "spoken": "네가 마지막에 붙잡아야 할 건 남의 눈이 아니라 네 양심이야.", "delta": 9, "tag": "conscience_first", "hint": "명예를 양심의 언어로 다시 세운다."},
                    {"label": "살 수 있으면 서명해. 명예로 죽는 건 바보짓이야.", "spoken": "살 수 있으면 서명해. 명예로 죽는 건 바보짓이야.", "delta": -9, "tag": "honor_is_foolish", "hint": "존의 가장 깊은 기준을 부정당한다."},
                ],
            },
            {
                "title": "끝까지 사람으로",
                "location": "재판장 가장자리",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "smile",
                "scene_prompt": "John Proctor after choosing integrity, exhausted but morally clear, tragic dignity in the courtroom",
                "narration": "모든 것이 무너진 자리에서 오히려 사람의 본모습이 선다. 존은 상처투성이지만, 적어도 자기 눈을 피하지는 않게 됐다.",
                "setup": "챕터 마지막 장면. 존은 네가 자기 결정을 어떻게 이해하는지 듣고 싶어 한다.",
                "opening_line": "이게 옳은지 아직도 두렵다. 다만 비겁하진 않다고는 말할 수 있겠군.",
                "choices": [
                    {"label": "그걸로 충분해. 두려워도 비겁하지 않은 사람은 드물어.", "spoken": "그걸로 충분해. 두려워도 비겁하지 않은 사람은 드물어.", "delta": 8, "tag": "courage_defined", "hint": "존의 선택을 정확히 이해했다고 느낀다."},
                    {"label": "당신은 마지막에야 비로소 당신 자신이 됐어.", "spoken": "당신은 마지막에야 비로소 당신 자신이 됐어.", "delta": 8, "tag": "became_himself", "hint": "구원에 가까운 말로 남는다."},
                    {"label": "그래도 살아남는 쪽이 나았을지도 몰라.", "spoken": "그래도 살아남는 쪽이 나았을지도 몰라.", "delta": -5, "tag": "undercut_choice", "hint": "결단의 의미를 흐린다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 4. 마지막 새벽",
        "summary": "존 프락터 루트의 마무리. 너의 관계와 존의 선택에 따라 명예, 생존, 타락 엔딩으로 갈라진다.",
        "default_background": "prison.jpg",
        "default_character": PROCTOR_NAME,
        "default_expression": "sad",
        "scenes": [
            {
                "title": "감옥의 기도",
                "location": "세일럼 감옥",
                "background": "prison.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "scene_prompt": "John Proctor in a dim Salem prison cell before dawn, weary but resolute, tragic stillness",
                "narration": "새벽 전 감옥은 이상할 만큼 조용하다. 존은 죽음이 두려워서가 아니라, 마지막까지 어떤 사람으로 남을지 생각하는 얼굴이다.",
                "setup": "플레이어와의 관계가 높을수록 그는 더 인간적인 고백을 드러낸다.",
                "opening_line": "이상하게도 죽음보다 더 두려운 건, 끝에서 내가 어떤 사람으로 기억될지다.",
                "choices": [
                    {"label": "적어도 나에게 당신은 끝까지 자기 영혼을 속이지 않은 사람이야.", "spoken": "적어도 나에게 당신은 끝까지 자기 영혼을 속이지 않은 사람이야.", "delta": 10, "tag": "soul_untouched", "hint": "존이 가장 원하던 증언을 받는다."},
                    {"label": "누가 뭐라 해도, 당신은 마지막에 옳은 쪽에 섰어.", "spoken": "누가 뭐라 해도, 당신은 마지막에 옳은 쪽에 섰어.", "delta": 8, "tag": "right_side", "hint": "평판보다 본질을 인정해준다."},
                    {"label": "이렇게 끝나는 게 의미가 있나 싶어.", "spoken": "이렇게 끝나는 게 의미가 있나 싶어.", "delta": -7, "tag": "meaningless_end", "hint": "희생의 의미가 깎여나간다."},
                ],
            },
            {
                "title": "새벽의 문",
                "location": "감옥 출구",
                "background": "prison.jpg",
                "character": PROCTOR_NAME,
                "expression": "love",
                "scene_prompt": "John Proctor at the prison threshold at dawn, final look toward the player, solemn emotional farewell",
                "narration": "문이 열리고 차가운 새벽이 스민다. 존은 마지막 순간에 네가 남긴 말들을 마음속에서 천천히 더듬는 사람처럼 보인다.",
                "setup": "최종 선택. 누적 호감도와 이전 선택에 따라 엔딩이 갈린다.",
                "opening_line": "나를 붙잡는 게 두려움인지, 양심인지, 이제는 분간이 간다. 네 말 덕도 있겠지.",
                "choices": [
                    {"label": "가. 두려움이 아니라 네 이름으로 끝을 건너.", "spoken": "가. 두려움이 아니라 네 이름으로 끝을 건너.", "delta": 10, "tag": "walk_with_name", "hint": "명예 엔딩으로 강하게 기운다."},
                    {"label": "살 길이 있다면 붙잡아. 하지만 네 자신은 잃지 마.", "spoken": "살 길이 있다면 붙잡아. 하지만 네 자신은 잃지 마.", "delta": 6, "tag": "survive_if_whole", "hint": "생존 엔딩 가능성을 연다."},
                    {"label": "결국 사람은 살아야지. 뭐든 서명하고 버텨.", "spoken": "결국 사람은 살아야지. 뭐든 서명하고 버텨.", "delta": -9, "tag": "sign_anything", "hint": "타락 엔딩으로 기운다."},
                ],
            },
        ],
    },
]


# =========================================================
# 스토리 데이터 - 엘리자베스
# =========================================================

ELIZABETH_CHAPTER_RULES = [
    {
        "threshold": 18,
        "bad_ending": "이별 엔딩 1. 엘리자베스는 마음을 닫은 채 끝내 누구에게도 기대지 않는다. 너의 말은 그녀의 상처를 건드렸지만 회복으로 이어지지 못했다.",
    },
    {
        "threshold": 38,
        "bad_ending": "이별 엔딩 2. 신뢰를 회복해야 할 자리에서 침묵과 거리만 남았다. 엘리자베스는 품위를 지켰지만 마음은 더 멀어졌다.",
    },
    {
        "threshold": 65,
        "bad_ending": "이별 엔딩 3. 용서의 문 앞까지 갔지만, 끝내 자신도 남도 받아들이지 못했다. 그녀는 살아남아도 오래도록 얼어붙은 사람으로 남는다.",
    },
    {
        "threshold": 85,
        "bad_ending": "",
    },
]

ELIZABETH_STORY = [
    {
        "chapter": "Chapter 1. 조용한 상처",
        "summary": "엘리자베스 프락터의 절제된 말과 침묵 뒤에 있는 상처를 마주하는 시작 장면들이다.",
        "default_background": "farmhouse.jpg",
        "default_character": ELIZABETH_NAME,
        "default_expression": "neutral",
        "scenes": [
            {
                "title": "차가운 부엌",
                "location": "프락터 집 부엌",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "neutral",
                "scene_prompt": "Elizabeth Proctor in a quiet colonial kitchen, composed but wounded, soft indoor light",
                "narration": "정돈된 부엌은 단정하지만 따뜻하지는 않다. 엘리자베스는 감정을 흘리지 않는 사람처럼 보이지만, 그 절제가 오히려 상처의 깊이를 말해준다.",
                "setup": "그녀는 조용한 사람에게 흔히 따라붙는 오해를 이미 많이 겪어왔다.",
                "opening_line": "사람들은 조용한 이를 차갑다고 여기지요. 하지만 말이 적다고 마음까지 없는 건 아니에요.",
                "choices": [
                    {"label": "당신은 차가운 게 아니라 오래 참고 있는 사람 같아.", "spoken": "당신은 차가운 게 아니라 오래 참고 있는 사람 같아.", "delta": 7, "tag": "saw_endurance", "hint": "겉보다 안쪽을 봐준 사람으로 느낀다."},
                    {"label": "쉽게 말하지 않는 사람의 말은 더 믿게 돼.", "spoken": "쉽게 말하지 않는 사람의 말은 더 믿게 돼.", "delta": 6, "tag": "trust_her_words", "hint": "침묵의 품위를 존중받는다."},
                    {"label": "솔직히 좀 답답한 타입이긴 해.", "spoken": "솔직히 좀 답답한 타입이긴 해.", "delta": -5, "tag": "called_stifling", "hint": "상처를 가벼이 평가당했다고 느낀다."},
                ],
            },
            {
                "title": "무너진 신뢰의 자국",
                "location": "창가 옆",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "sad",
                "scene_prompt": "Elizabeth Proctor by a window, quietly wounded, pale daylight, restrained grief",
                "narration": "한 번 금 간 신뢰는 소리 없이 오래 간다. 엘리자베스는 누군가를 미워하기보다, 다시 믿는 일이 얼마나 어려운지 견디는 사람이다.",
                "setup": "그녀는 배신 이후 회복이 가능하다고 믿고 싶으면서도 쉽게 확신하지 못한다.",
                "opening_line": "상처는 끝나도, 경계는 남지요. 그걸 비겁함이라 부를 수는 없을 거예요.",
                "choices": [
                    {"label": "그건 비겁함이 아니라 살아남은 마음의 방식이야.", "spoken": "그건 비겁함이 아니라 살아남은 마음의 방식이야.", "delta": 8, "tag": "surviving_heart", "hint": "자기 방어를 존중받는다."},
                    {"label": "천천히 믿어도 돼. 빨리 용서할 필요는 없어.", "spoken": "천천히 믿어도 돼. 빨리 용서할 필요는 없어.", "delta": 7, "tag": "slow_forgiveness", "hint": "속도를 강요하지 않는 사람이라 느낀다."},
                    {"label": "그래도 언젠간 그냥 잊어야지.", "spoken": "그래도 언젠간 그냥 잊어야지.", "delta": -6, "tag": "forget_it", "hint": "상처의 시간을 무시했다고 느낀다."},
                ],
            },
            {
                "title": "품위의 이유",
                "location": "집 앞 마당",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "scene_prompt": "Elizabeth Proctor in a quiet farmhouse yard, dignified and calm, muted afternoon light",
                "narration": "세상이 거칠수록 그녀는 더 단정해진다. 그것은 허영이 아니라, 무너지지 않기 위한 마지막 질서처럼 보인다.",
                "setup": "엘리자베스는 품위를 지키는 것이 자기 마음을 지키는 방식이기도 하다.",
                "opening_line": "사람이 무너지지 않으려면, 붙잡을 것이 조금은 있어야 하니까요.",
                "choices": [
                    {"label": "당신의 품위는 보기 좋기보다 강해 보여.", "spoken": "당신의 품위는 보기 좋기보다 강해 보여.", "delta": 7, "tag": "dignity_is_strength", "hint": "겉치레가 아닌 힘으로 이해받는다."},
                    {"label": "그 질서를 지키는 게 당신을 지켜준 거겠지.", "spoken": "그 질서를 지키는 게 당신을 지켜준 거겠지.", "delta": 6, "tag": "order_protects", "hint": "자기 방식의 방어를 인정받는다."},
                    {"label": "가끔은 그냥 다 내려놓는 게 낫지 않아?", "spoken": "가끔은 그냥 다 내려놓는 게 낫지 않아?", "delta": -4, "tag": "drop_it_all", "hint": "소중한 기준을 가볍게 여긴다고 느낀다."},
                ],
            },
            {
                "title": "작은 틈",
                "location": "저녁 식탁",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "scene_prompt": "Elizabeth Proctor at a quiet supper table, a faint warmth emerging through restraint",
                "narration": "저녁 공기 속에서 그녀의 목소리는 조금 더 부드러워진다. 완전히 마음을 여는 건 아니지만, 적어도 경계에 작은 틈은 생겼다.",
                "setup": "이 장면은 그녀가 너를 신뢰할 수 있는 사람으로 볼지 가르는 순간이다.",
                "opening_line": "이상하군요. 당신과 말하면 굳이 방어적인 말을 고르지 않게 돼요.",
                "choices": [
                    {"label": "그럴 수 있다면 그걸로 충분해. 서두르지 않을게.", "spoken": "그럴 수 있다면 그걸로 충분해. 서두르지 않을게.", "delta": 8, "tag": "patient_presence", "hint": "안전한 사람으로 인식한다."},
                    {"label": "당신이 편해진다면 난 조용히 곁에 있을게.", "spoken": "당신이 편해진다면 난 조용히 곁에 있을게.", "delta": 7, "tag": "quiet_support", "hint": "말보다 태도로 신뢰를 준다."},
                    {"label": "그럼 이제 좀 더 솔직해져도 되겠네?", "spoken": "그럼 이제 좀 더 솔직해져도 되겠네?", "delta": -5, "tag": "push_too_soon", "hint": "안전하자마자 밀어붙인다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 의심의 마을",
        "summary": "마녀사냥이 커지는 가운데, 엘리자베스는 두려움과 품위를 함께 붙들어야 한다.",
        "default_background": "village.jpg",
        "default_character": ELIZABETH_NAME,
        "default_expression": "fear",
        "scenes": [
            {
                "title": "소문이 집을 향할 때",
                "location": "프락터 집 앞",
                "background": "village.jpg",
                "character": ELIZABETH_NAME,
                "expression": "fear",
                "scene_prompt": "Elizabeth Proctor outside her home as witchcraft rumors close in, restrained fear, colonial village dusk",
                "narration": "멀리서 들리던 소문이 이제는 문 앞까지 온다. 엘리자베스는 겁에 질린 채 소리치기보다, 더 조용해진 얼굴로 위험을 받아들인다.",
                "setup": "그녀는 공포에 굴복하지 않으려 하지만, 두려움이 없는 것은 아니다.",
                "opening_line": "두렵지 않다고 말하면 거짓이겠지요. 다만 두려움이 나를 다 정하게 두고 싶진 않아요.",
                "choices": [
                    {"label": "두려워도 품위를 잃지 않는 게 진짜 용기야.", "spoken": "두려워도 품위를 잃지 않는 게 진짜 용기야.", "delta": 8, "tag": "courage_with_fear", "hint": "그녀의 방식의 용기를 정확히 봐준다."},
                    {"label": "무서워도 괜찮아. 그 감정을 숨기지 않아도 돼.", "spoken": "무서워도 괜찮아. 그 감정을 숨기지 않아도 돼.", "delta": 7, "tag": "fear_allowed", "hint": "강해야만 한다는 압박에서 벗어난다."},
                    {"label": "지금은 품위보다 살아남는 게 먼저 아냐?", "spoken": "지금은 품위보다 살아남는 게 먼저 아냐?", "delta": -5, "tag": "dismissed_dignity", "hint": "가장 중요한 기준을 부정당한다."},
                ],
            },
            {
                "title": "의심과 사랑",
                "location": "실내의 어두운 방",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "sad",
                "scene_prompt": "Elizabeth Proctor in a dim room, torn between love and lingering hurt, intimate tragic mood",
                "narration": "사랑은 남아 있지만, 상처도 같이 남아 있다. 엘리자베스는 둘 중 하나만 고르지 못한 채 오래 견뎌온 사람이다.",
                "setup": "그녀는 사랑이 곧바로 용서를 뜻하지는 않는다고 알고 있다.",
                "opening_line": "누군가를 사랑하는 것과, 그를 다시 믿는 것은 같은 일이 아니에요.",
                "choices": [
                    {"label": "그래서 당신의 망설임은 사랑이 없어서가 아니야.", "spoken": "그래서 당신의 망설임은 사랑이 없어서가 아니야.", "delta": 8, "tag": "hesitation_is_love", "hint": "복잡한 감정을 이해받는다."},
                    {"label": "믿음은 감정이 아니라 시간을 들인 선택일 수도 있어.", "spoken": "믿음은 감정이 아니라 시간을 들인 선택일 수도 있어.", "delta": 7, "tag": "trust_is_choice", "hint": "회복을 현실적으로 본다."},
                    {"label": "사랑하면 그냥 다 용서되는 거 아냐?", "spoken": "사랑하면 그냥 다 용서되는 거 아냐?", "delta": -7, "tag": "love_equals_forgive", "hint": "마음을 단순화당했다고 느낀다."},
                ],
            },
            {
                "title": "붙잡아야 할 것",
                "location": "기도하는 방",
                "background": "church.jpg",
                "character": ELIZABETH_NAME,
                "expression": "neutral",
                "scene_prompt": "Elizabeth Proctor in prayerful stillness, deciding what values to hold, soft candlelight",
                "narration": "모든 것이 흔들릴 때 사람은 결국 무엇을 붙잡고 설지 선택해야 한다. 엘리자베스가 붙들고 있는 것은 자존과 신뢰, 그리고 사람이 사람답게 남아야 한다는 믿음이다.",
                "setup": "그녀는 지금 그 믿음이 너무 무거운지 확인하고 싶어 한다.",
                "opening_line": "고집과 신념은 멀리서 보면 비슷해 보여요. 하지만 안에 있는 사람은 차이를 알지요.",
                "choices": [
                    {"label": "당신이 붙드는 건 고집보다 양심에 가까워 보여.", "spoken": "당신이 붙드는 건 고집보다 양심에 가까워 보여.", "delta": 7, "tag": "conscience_not_pride", "hint": "내면의 중심을 알아봐준다."},
                    {"label": "그 믿음 덕분에 당신이 아직 당신인 거야.", "spoken": "그 믿음 덕분에 당신이 아직 당신인 거야.", "delta": 7, "tag": "still_herself", "hint": "정체성을 인정받는다."},
                    {"label": "지금은 그런 기준이 너무 무거운 짐 같아.", "spoken": "지금은 그런 기준이 너무 무거운 짐 같아.", "delta": -4, "tag": "too_heavy", "hint": "중심을 내려놓으라는 말처럼 들린다."},
                ],
            },
            {
                "title": "조용한 동행",
                "location": "밤길",
                "background": "night_road.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "scene_prompt": "Elizabeth Proctor walking a quiet road at night with the player, restrained warmth, trust slowly growing",
                "narration": "함께 걷는 밤길은 이상하게도 덜 춥다. 엘리자베스는 드러내진 않지만, 네 곁을 안전한 침묵으로 느끼기 시작한다.",
                "setup": "챕터 마지막 장면. 그녀가 너를 회복의 동행으로 받아들일지 정해진다.",
                "opening_line": "당신 옆에 있으면 침묵도 무겁기만 하진 않네요. 그건 드문 일입니다.",
                "choices": [
                    {"label": "말이 없어도 괜찮은 관계가 오래가더라.", "spoken": "말이 없어도 괜찮은 관계가 오래가더라.", "delta": 8, "tag": "silence_is_safe", "hint": "함께 있는 것 자체가 위안이 된다."},
                    {"label": "당신이 편하다면, 난 그 속도를 따를게.", "spoken": "당신이 편하다면, 난 그 속도를 따를게.", "delta": 7, "tag": "follow_her_pace", "hint": "신뢰가 더 깊어진다."},
                    {"label": "이 침묵도 결국 답답하긴 하네.", "spoken": "이 침묵도 결국 답답하긴 하네.", "delta": -5, "tag": "called_it_burdensome", "hint": "겨우 열린 틈이 다시 닫힌다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 용서의 문턱",
        "summary": "엘리자베스는 용서를 강요받지 않으면서도, 회복의 가능성을 스스로 선택해야 한다.",
        "default_background": "prison.jpg",
        "default_character": ELIZABETH_NAME,
        "default_expression": "sad",
        "scenes": [
            {
                "title": "감옥의 밤",
                "location": "세일럼 감옥",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "sad",
                "scene_prompt": "Elizabeth Proctor in Salem prison at night, quiet strength and sorrow, dim lantern light",
                "narration": "차가운 감옥에서도 그녀는 쉽게 무너지지 않는다. 그러나 가까이서 보면, 단단함은 종종 깨지지 않으려는 고통과 비슷한 얼굴을 하고 있다.",
                "setup": "엘리자베스는 이제 용서가 타인을 위한 일이 아니라 자기 자신을 위한 일인지 고민한다.",
                "opening_line": "용서는 그 사람을 가볍게 풀어주는 일이라기보다, 내 손에 남은 쇠사슬을 보는 일 같아요.",
                "choices": [
                    {"label": "그래서 용서는 상대보다 먼저 자신을 위한 일일 수 있어.", "spoken": "그래서 용서는 상대보다 먼저 자신을 위한 일일 수 있어.", "delta": 8, "tag": "for_herself", "hint": "용서를 자기 회복의 언어로 이해한다."},
                    {"label": "용서하지 못해도 괜찮아. 다만 네 마음이 영원히 묶이진 않길 바라.", "spoken": "용서하지 못해도 괜찮아. 다만 네 마음이 영원히 묶이진 않길 바라.", "delta": 7, "tag": "unbound_heart", "hint": "강요 없이 회복을 말해준다."},
                    {"label": "그래도 결국 용서해야 끝나지 않겠어?", "spoken": "그래도 결국 용서해야 끝나지 않겠어?", "delta": -6, "tag": "pressured_forgive", "hint": "회복을 명령처럼 들었다."},
                ],
            },
            {
                "title": "존을 바라보며",
                "location": "감옥 면회실",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "neutral",
                "scene_prompt": "Elizabeth Proctor seeing John Proctor in prison, love, grief, and moral clarity intertwined",
                "narration": "존을 바라보는 그녀의 눈에는 여전히 사랑이 있다. 다만 그 사랑은 예전으로 돌아가자는 말이 아니라, 서로의 진실을 있는 그대로 보겠다는 결심에 가깝다.",
                "setup": "엘리자베스는 존을 놓아주는 것과 포기하는 것의 차이를 생각하고 있다.",
                "opening_line": "누군가를 놓아주는 일이 꼭 사랑이 없는 일은 아니겠지요.",
                "choices": [
                    {"label": "오히려 가장 깊은 사랑은 붙잡지 않는 데서 오기도 해.", "spoken": "오히려 가장 깊은 사랑은 붙잡지 않는 데서 오기도 해.", "delta": 8, "tag": "love_without_grip", "hint": "사랑의 더 성숙한 형태를 본다."},
                    {"label": "당신은 포기하는 게 아니라, 그 사람의 선택을 존중하는 거야.", "spoken": "당신은 포기하는 게 아니라, 그 사람의 선택을 존중하는 거야.", "delta": 7, "tag": "respect_his_choice", "hint": "스스로를 비겁하다고 여기지 않게 된다."},
                    {"label": "그래도 끝까지 붙잡아야 하는 거 아냐?", "spoken": "그래도 끝까지 붙잡아야 하는 거 아냐?", "delta": -5, "tag": "must_hold", "hint": "그녀의 방식의 사랑을 부정받는다."},
                ],
            },
            {
                "title": "자기 자신에게 내리는 판결",
                "location": "감옥 창가",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "scene_prompt": "Elizabeth Proctor by a prison window at dawn, finally turning compassion toward herself",
                "narration": "오랫동안 남을 평가하듯 자신을 엄격하게 재단해온 사람만이 가진 피로가 있다. 엘리자베스는 이제야 자기 자신에게도 조금의 자비가 필요하다는 걸 깨닫기 시작한다.",
                "setup": "이 장면은 그녀가 회복의 방향을 자기 자신에게까지 넓힐 수 있는지 가르는 분기점이다.",
                "opening_line": "남을 용서하는 일보다 어려운 건, 어쩌면 나 자신에게 지나치게 엄격했던 걸 인정하는 일일지도 모르겠어요.",
                "choices": [
                    {"label": "당신도 상처받은 사람이었지, 재판관이 아니었어.", "spoken": "당신도 상처받은 사람이었지, 재판관이 아니었어.", "delta": 9, "tag": "not_her_own_judge", "hint": "자기 처벌에서 벗어날 틈이 생긴다."},
                    {"label": "자비는 약함이 아니라 회복의 시작이야.", "spoken": "자비는 약함이 아니라 회복의 시작이야.", "delta": 8, "tag": "mercy_begins", "hint": "자기 연민을 긍정적으로 본다."},
                    {"label": "너무 스스로를 봐주는 것도 독이 될 수 있어.", "spoken": "너무 스스로를 봐주는 것도 독이 될 수 있어.", "delta": -6, "tag": "deny_self_mercy", "hint": "겨우 열린 회복의 문이 다시 좁아진다."},
                ],
            },
            {
                "title": "마지막 고요",
                "location": "새벽 직전 감옥",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "love",
                "scene_prompt": "Elizabeth Proctor in a final quiet prison dawn, serene emotional resolution, tragic hope",
                "narration": "모든 것이 끝나가는 시간인데도 그녀의 얼굴에는 이상한 평온이 돈다. 그 평온은 체념이 아니라, 고통 속에서도 끝내 자신을 잃지 않겠다는 의지에 가깝다.",
                "setup": "최종 장면 직전. 너의 말이 그녀의 엔딩 감정을 결정한다.",
                "opening_line": "끝이 가까워질수록 선명해지는 것도 있군요. 내가 무엇을 잃었는지보다, 무엇을 아직 지키고 있는지가.",
                "choices": [
                    {"label": "당신은 여전히 신뢰할 수 있는 사람이고, 그건 쉽게 무너지지 않아.", "spoken": "당신은 여전히 신뢰할 수 있는 사람이고, 그건 쉽게 무너지지 않아.", "delta": 9, "tag": "still_trustworthy", "hint": "자기 가치가 선명해진다."},
                    {"label": "당신 안에 남은 따뜻함이 결국 당신을 살릴 거야.", "spoken": "당신 안에 남은 따뜻함이 결국 당신을 살릴 거야.", "delta": 8, "tag": "warmth_remains", "hint": "희망 엔딩 쪽으로 기운다."},
                    {"label": "결국 누구도 예전으로 돌아가진 못하겠지.", "spoken": "결국 누구도 예전으로 돌아가진 못하겠지.", "delta": -5, "tag": "no_return", "hint": "회복보다 상실에 더 묶이게 된다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 4. 남겨진 봄",
        "summary": "엘리자베스 루트의 최종 장. 희망, 용서, 이별 엔딩으로 갈라진다.",
        "default_background": "farmhouse.jpg",
        "default_character": ELIZABETH_NAME,
        "default_expression": "love",
        "scenes": [
            {
                "title": "빈 집의 햇빛",
                "location": "프락터 집",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "scene_prompt": "Elizabeth Proctor in a quiet farmhouse after tragedy, morning sunlight, grief and resilience together",
                "narration": "모든 것이 지나간 뒤의 집은 전과 같지 않다. 그러나 빈자리가 곧 폐허는 아니다. 엘리자베스는 상실 속에서도 다시 살아갈 수 있는 사람처럼 서 있다.",
                "setup": "플레이어와의 관계가 높을수록 그녀는 더 따뜻하고 또렷하게 마음을 드러낸다.",
                "opening_line": "상처가 사라진 건 아니에요. 다만 이제 그 상처가 내 삶 전체를 대신 말하게 두고 싶진 않아요.",
                "choices": [
                    {"label": "그건 잊은 게 아니라, 상처보다 더 큰 사람이 되겠다는 뜻이네.", "spoken": "그건 잊은 게 아니라, 상처보다 더 큰 사람이 되겠다는 뜻이네.", "delta": 10, "tag": "greater_than_wound", "hint": "희망 엔딩에 강하게 가까워진다."},
                    {"label": "당신은 충분히 오래 버텼고, 이제 조금 더 살아도 돼.", "spoken": "당신은 충분히 오래 버텼고, 이제 조금 더 살아도 돼.", "delta": 8, "tag": "live_now", "hint": "회복을 허락받는 감각을 준다."},
                    {"label": "그래도 사람은 결국 상처대로 살게 되지 않나.", "spoken": "그래도 사람은 결국 상처대로 살게 되지 않나.", "delta": -7, "tag": "wound_defines", "hint": "회복 가능성을 꺾는다."},
                ],
            },
            {
                "title": "봄의 문장",
                "location": "집 앞 들판",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "love",
                "scene_prompt": "Elizabeth Proctor in a spring field outside the farmhouse, calm hope, gentle emotional closure",
                "narration": "바람은 여전히 차갑지만, 계절은 분명히 움직인다. 엘리자베스는 긴 겨울 끝에서 처음으로 앞으로의 시간을 생각한다.",
                "setup": "최종 선택. 누적 호감도에 따라 희망 엔딩, 용서 엔딩, 이별 엔딩이 결정된다.",
                "opening_line": "모든 것을 되돌릴 수는 없겠지요. 그래도 남은 삶을 어떻게 쓸지는 아직 정할 수 있어요.",
                "choices": [
                    {"label": "당신의 남은 삶엔 평온도, 사랑도 다시 올 수 있어.", "spoken": "당신의 남은 삶엔 평온도, 사랑도 다시 올 수 있어.", "delta": 10, "tag": "hope_ahead", "hint": "희망 엔딩으로 기운다."},
                    {"label": "용서는 이미 시작됐어. 이제 그걸 삶으로 옮기면 돼.", "spoken": "용서는 이미 시작됐어. 이제 그걸 삶으로 옮기면 돼.", "delta": 8, "tag": "forgiveness_lived", "hint": "용서 엔딩으로 기운다."},
                    {"label": "그저 조용히 혼자 사는 게 제일 나을지도 몰라.", "spoken": "그저 조용히 혼자 사는 게 제일 나을지도 몰라.", "delta": -8, "tag": "solitary_end", "hint": "이별 엔딩 쪽으로 기운다."},
                ],
            },
        ],
    },
]


# =========================================================
# 공통 유틸
# =========================================================

def get_stage(value: int) -> str:
    if value < 20:
        return "cold"
    if value < 50:
        return "neutral"
    if value < 80:
        return "smile"
    return "love"


def get_api_key() -> str:
    return st.secrets.get("OPENAI_API_KEY", "")


def get_client():
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def

