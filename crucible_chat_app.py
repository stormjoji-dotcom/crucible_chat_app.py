import random
from pathlib import Path

import streamlit as st
st.set_page_config(page_title="test", page_icon="🎭", layout="wide")
st.title("시련 인터랙션 테스트")
st.write("앱이 정상적으로 켜졌습니다.")
try:
    from openai import OpenAI
except Exception:
    OpenAI = None


st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")
BACKGROUND_ROOT = Path("backgrounds")

ABIGAIL_NAME = "아비게일 윌리엄즈"
PROCTOR_NAME = "존 프락터"
ELIZABETH_NAME = "엘리자베스 프락터"

ABIGAIL_STORY_KEY = "abigail_story"
PROCTOR_STORY_KEY = "proctor_story"
ELIZABETH_STORY_KEY = "elizabeth_story"

FREE_CHAT_HEIGHT = 520
STORY_LOG_HEIGHT = 420


st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #101014 0%, #17171d 55%, #1f1a1a 100%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
    max-width: 1450px;
}
.top-title, .side-card, .status-card, .chat-header, .big-image-wrap, .story-card, .event-box, .choice-box, .bg-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
.top-title h1 {
    margin: 0;
    color: #f7f2ea;
    font-size: 2.4rem;
}
.top-title p {
    margin: 8px 0 0 0;
    color: #d9d0c4;
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
.vn-stage {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 16px;
}
.vn-fallback {
    min-height: 290px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #262933 0%, #1f1f26 100%);
    color: #f1e7d8;
    font-size: 1.1rem;
}
.vn-dialogue {
    padding: 16px 18px;
    background: rgba(0,0,0,0.42);
    border-top: 1px solid rgba(255,255,255,0.06);
}
.vn-name {
    display: inline-block;
    margin-bottom: 10px;
    padding: 6px 12px;
    border-radius: 12px;
    background: rgba(255,214,120,0.16);
    border: 1px solid rgba(255,214,120,0.28);
    color: #fff2dc;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)


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


ABIGAIL_STORY = [
    {
        "chapter": "Chapter 1. 숲의 춤",
        "summary": "숲에서 춤추는 아비게일을 발견하고 그 밤의 비밀을 함께 감당할지 결정한다.",
        "scenes": [
            {
                "title": "숲에서 마주친 순간",
                "location": "세일럼 외곽 숲",
                "background": "forest.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "narration": "달빛 아래 숲이 숨을 죽인다. 흩어진 발자국 끝에 아비게일이 너를 노려본다.",
                "opening_line": "너, 여기서 뭘 본 거지? 똑바로 말해.",
                "choices": [
                    {"label": "아무도 심판 안 해. 이유부터 듣고 싶어.", "delta": 6},
                    {"label": "들키기 전에 돌아가야 해.", "delta": 3},
                    {"label": "대체 무슨 짓을 한 거야?", "delta": -4},
                ],
            },
            {
                "title": "비밀의 무게",
                "location": "숲 가장자리",
                "background": "forest.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "narration": "아비게일은 쉽게 숨을 고르지 못한다. 눈빛엔 두려움과 오기가 동시에 번뜩인다.",
                "opening_line": "사람이 너무 간절하면... 말도 안 되는 짓도 하게 되는 거 알아?",
                "choices": [
                    {"label": "누군가는 네 편에서 널 말려야 해.", "delta": 5},
                    {"label": "네 절박함은 이해해.", "delta": 6},
                    {"label": "결국 자업자득이야.", "delta": -4},
                ],
            },
            {
                "title": "마을의 소문",
                "location": "세일럼 마을",
                "background": "village.jpg",
                "character": ABIGAIL_NAME,
                "expression": "fear",
                "narration": "베티가 깨어나지 않는다는 소문이 퍼지고, 공포는 사람들 얼굴을 바꾼다.",
                "opening_line": "이제 다들 날 볼 거야. 넌도 내가 마녀처럼 보여?",
                "choices": [
                    {"label": "겁먹은 사람처럼 보여. 괴물은 아니야.", "delta": 6},
                    {"label": "지금은 먼저 무너지지 마.", "delta": 5},
                    {"label": "난 거리를 둘래.", "delta": -5},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 법정의 불길",
        "summary": "법정과 증언, 엘리자베스 고발로 이어지는 불길한 장.",
        "scenes": [
            {
                "title": "증언대의 시선",
                "location": "법정",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "angry",
                "narration": "모든 시선이 아비게일에게 꽂힌다. 그녀는 떨림을 감추듯 턱을 든다.",
                "opening_line": "저 많은 눈 앞에서도, 내가 보고 싶은 건 네 표정 하나야.",
                "choices": [
                    {"label": "네 두려움만큼은 진짜라고 믿어.", "delta": 7},
                    {"label": "흔들리지 마. 난 네 쪽에 설게.", "delta": 6},
                    {"label": "난 아직 널 다 믿지 못해.", "delta": -4},
                ],
            },
            {
                "title": "존의 이름",
                "location": "복도",
                "background": "courtroom.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "narration": "존 프락터의 이름이 오갈 때마다 그녀의 얼굴은 더 위험해진다.",
                "opening_line": "저 여자가 사라지면... 모든 게 제자리로 돌아갈까?",
                "choices": [
                    {"label": "넌 존보다 네 상처를 붙잡고 있는 걸지도 몰라.", "delta": 5},
                    {"label": "그래도 널 외면하진 않을게.", "delta": 7},
                    {"label": "엘리자베스를 건드리면 끝장이야.", "delta": -5},
                ],
            },
            {
                "title": "마음의 균열",
                "location": "밤길",
                "background": "night_road.jpg",
                "character": ABIGAIL_NAME,
                "expression": "love",
                "narration": "차가운 밤공기 속에서 아비게일의 시선은 처음으로 존이 아닌 너를 향한다.",
                "opening_line": "왜 자꾸... 네가 먼저 생각나는지 모르겠어.",
                "choices": [
                    {"label": "난 너 자체를 보고 여기까지 온 거야.", "delta": 8},
                    {"label": "혼란스러우면 내 곁에서 숨 고르면 돼.", "delta": 6},
                    {"label": "그건 또 다른 집착일 뿐이야.", "delta": -5},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 새벽의 도망",
        "summary": "세일럼을 떠나는 새벽, 함께할지 갈라지는 최종 장.",
        "scenes": [
            {
                "title": "선착장의 고백",
                "location": "새벽의 선착장",
                "background": "dock.jpg",
                "character": ABIGAIL_NAME,
                "expression": "sad",
                "narration": "안개 낀 새벽, 떠날 배가 흔들리고 아비게일의 손끝도 함께 떨린다.",
                "opening_line": "나 이제 떠나. 그런데 네가 있어 덜 무서워.",
                "choices": [
                    {"label": "혼자 두지 않으려고 왔어.", "delta": 12},
                    {"label": "널 미워하진 않아.", "delta": 7},
                    {"label": "도망은 네가 혼자 책임져.", "delta": -8},
                ],
            },
            {
                "title": "배 위의 선택",
                "location": "갑판",
                "background": "dock.jpg",
                "character": ABIGAIL_NAME,
                "expression": "love",
                "narration": "세일럼의 불빛이 뒤로 밀려난다. 이제 남은 건 두 사람의 결심뿐이다.",
                "opening_line": "넌 날 기억으로 남길 거야... 아니면 내 옆자리로 올 거야?",
                "choices": [
                    {"label": "네 옆자리로 갈게.", "delta": 13},
                    {"label": "널 기억할게.", "delta": 5},
                    {"label": "여기서 끝내자.", "delta": -10},
                ],
            },
        ],
    },
]

PROCTOR_STORY = [
    {
        "chapter": "Chapter 1. 농장의 균열",
        "summary": "존 프락터의 죄책감과 정직함을 마주하는 시작 장.",
        "scenes": [
            {
                "title": "첫 대면",
                "location": "프락터 농장",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "neutral",
                "narration": "존 프락터는 흙 묻은 손보다 먼저 경계하는 눈빛으로 너를 본다.",
                "opening_line": "쓸데없는 말 돌리지 마. 네가 온 이유부터 말해.",
                "choices": [
                    {"label": "둘러대지 않고 말할게. 도우러 왔어.", "delta": 6},
                    {"label": "당신이 혼자 버티는 사람 같아서.", "delta": 5},
                    {"label": "구경 왔지.", "delta": -5},
                ],
            },
            {
                "title": "죄의 그림자",
                "location": "헛간 옆",
                "background": "farmhouse.jpg",
                "character": PROCTOR_NAME,
                "expression": "sad",
                "narration": "그는 잘못 하나가 사람 전체를 덮는다는 걸 이미 알고 있는 얼굴이다.",
                "opening_line": "사람은 한 번 잘못하면 계속 그것만으로 보이게 되나?",
                "choices": [
                    {"label": "잘못이 사람 전부는 아니야.", "delta": 7},
                    {"label": "숨기지 말고 마주 봐야 달라져.", "delta": 6},
                    {"label": "업보지 뭐.", "delta": -6},
                ],
            },
            {
                "title": "결심의 밤",
                "location": "촛불 켜진 방",
                "background": "church.jpg",
                "character": PROCTOR_NAME,
                "expression": "smile",
                "narration": "존은 칭찬보다, 거짓 없이 설 수 있는 이유를 찾고 있다.",
                "opening_line": "네 말은 달콤하진 않아도 머릿속에 남는군.",
                "choices": [
                    {"label": "끝까지 당신답기를 바라.", "delta": 8},
                    {"label": "두려워도 옳은 쪽으로 가.", "delta": 7},
                    {"label": "다 잃을 수도 있어.", "delta": -4},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 법정의 이름",
        "summary": "진실과 이름, 생존과 명예가 충돌하는 장.",
        "scenes": [
            {
                "title": "증언의 문턱",
                "location": "법정 입구",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "neutral",
                "narration": "문 하나 건너면 다시 이전으로 돌아갈 수 없을 것만 같다.",
                "opening_line": "저 안에 들어가면 깨끗한 꼴로 나오진 못할 거다.",
                "choices": [
                    {"label": "거짓보다 낫다면 가야지.", "delta": 8},
                    {"label": "오늘은 무너지지 않는 게 중요해.", "delta": 6},
                    {"label": "빠져나와.", "delta": -6},
                ],
            },
            {
                "title": "이름의 값",
                "location": "재판석 앞",
                "background": "courtroom.jpg",
                "character": PROCTOR_NAME,
                "expression": "angry",
                "narration": "법정은 생존을 내밀고, 대가로 그의 이름을 요구한다.",
                "opening_line": "이름은 한 번 더럽히면 다시는 씻기지 않아.",
                "choices": [
                    {"label": "네 이름을 네 손으로 죽이진 마.", "delta": 10},
                    {"label": "양심을 먼저 붙잡아.", "delta": 9},
                    {"label": "살 수 있으면 서명해.", "delta": -9},
                ],
            },
            {
                "title": "감옥의 새벽",
                "location": "감옥",
                "background": "prison.jpg",
                "character": PROCTOR_NAME,
                "expression": "love",
                "narration": "존은 마지막 순간에도 자기 영혼과 이름을 저울질한다.",
                "opening_line": "내가 어떤 사람으로 기억될지가 더 두렵군.",
                "choices": [
                    {"label": "넌 끝까지 영혼을 속이지 않은 사람이야.", "delta": 10},
                    {"label": "마지막에 옳은 쪽에 섰어.", "delta": 8},
                    {"label": "이렇게 끝나는 게 의미가 있나.", "delta": -7},
                ],
            },
        ],
    },
]

ELIZABETH_STORY = [
    {
        "chapter": "Chapter 1. 조용한 상처",
        "summary": "엘리자베스의 절제된 말과 상처를 이해하는 시작 장.",
        "scenes": [
            {
                "title": "차가운 부엌",
                "location": "프락터 집",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "neutral",
                "narration": "정돈된 공간만큼 그녀의 마음도 단정하지만, 결코 가볍지 않다.",
                "opening_line": "말이 적다고 마음까지 없는 건 아니에요.",
                "choices": [
                    {"label": "오래 참고 있는 사람 같아.", "delta": 7},
                    {"label": "쉽게 말하지 않기에 더 믿게 돼.", "delta": 6},
                    {"label": "좀 답답한 타입이긴 해.", "delta": -5},
                ],
            },
            {
                "title": "상처의 자국",
                "location": "창가",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "sad",
                "narration": "금 간 신뢰는 조용히 오래 간다.",
                "opening_line": "경계가 남는다고 해서 비겁한 건 아니겠지요.",
                "choices": [
                    {"label": "그건 살아남은 마음의 방식이야.", "delta": 8},
                    {"label": "천천히 믿어도 돼.", "delta": 7},
                    {"label": "그냥 잊어야지.", "delta": -6},
                ],
            },
            {
                "title": "작은 틈",
                "location": "저녁 식탁",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "narration": "그녀의 목소리는 여전히 조용하지만, 경계는 조금 누그러진다.",
                "opening_line": "당신과 말하면 굳이 방어적인 말을 고르지 않게 돼요.",
                "choices": [
                    {"label": "서두르지 않을게.", "delta": 8},
                    {"label": "조용히 곁에 있을게.", "delta": 7},
                    {"label": "그럼 더 솔직해져도 되겠네?", "delta": -5},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 용서의 문턱",
        "summary": "용서와 회복, 자기 자신에 대한 자비를 선택하는 장.",
        "scenes": [
            {
                "title": "감옥의 밤",
                "location": "감옥",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "sad",
                "narration": "차가운 감옥에서도 그녀는 쉽게 무너지지 않는다.",
                "opening_line": "용서는 어쩌면 내 손에 남은 쇠사슬을 보는 일 같아요.",
                "choices": [
                    {"label": "용서는 자신을 위한 일일 수 있어.", "delta": 8},
                    {"label": "용서하지 못해도 괜찮아.", "delta": 7},
                    {"label": "결국 용서해야 끝나지.", "delta": -6},
                ],
            },
            {
                "title": "자기 자신에게",
                "location": "감옥 창가",
                "background": "prison.jpg",
                "character": ELIZABETH_NAME,
                "expression": "smile",
                "narration": "그녀는 처음으로 자기 자신에게도 자비가 필요하다는 걸 깨닫기 시작한다.",
                "opening_line": "나 자신에게 지나치게 엄격했던 걸 인정하는 게 더 어렵군요.",
                "choices": [
                    {"label": "당신도 상처받은 사람이었어.", "delta": 9},
                    {"label": "자비는 회복의 시작이야.", "delta": 8},
                    {"label": "스스로를 너무 봐줘도 독이야.", "delta": -6},
                ],
            },
            {
                "title": "남겨진 봄",
                "location": "들판",
                "background": "farmhouse.jpg",
                "character": ELIZABETH_NAME,
                "expression": "love",
                "narration": "상처는 남아 있지만, 그 상처가 삶 전체는 아니다.",
                "opening_line": "남은 삶을 어떻게 쓸지는 아직 정할 수 있어요.",
                "choices": [
                    {"label": "당신의 삶엔 평온도 다시 올 거야.", "delta": 10},
                    {"label": "용서는 이미 시작됐어.", "delta": 8},
                    {"label": "그냥 혼자 사는 게 나을지도.", "delta": -8},
                ],
            },
        ],
    },
}


def get_stage(value: int) -> str:
    if value < 20:
        return "cold"
    if value < 50:
        return "neutral"
    if value < 80:
        return "smile"
    return "love"


def image_path(char_name: str, stage: str) -> Path:
    return IMAGE_ROOT / CHARACTERS[char_name]["folder"] / f"{stage}.png"


def expression_image_path(char_name: str, expression: str) -> Path:
    return IMAGE_ROOT / CHARACTERS[char_name]["folder"] / f"{expression}.png"


def background_path(filename: str) -> Path:
    return BACKGROUND_ROOT / filename


def get_api_key() -> str:
    return st.secrets.get("OPENAI_API_KEY", "")


def get_client():
    api_key = get_api_key()
    if not api_key or OpenAI is None:
        return None
    return OpenAI(api_key=api_key)


def ensure_state():
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "affection" not in st.session_state:
        st.session_state.affection = {}
    if "memory" not in st.session_state:
        st.session_state.memory = {}
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "name_event_done" not in st.session_state:
        st.session_state.name_event_done = {}
    if "awaiting_name_input" not in st.session_state:
        st.session_state.awaiting_name_input = {}
    if "story_state" not in st.session_state:
        st.session_state.story_state = {}


def default_story_state():
    return {
        "chapter_index": 0,
        "scene_index": 0,
        "history": [],
        "story_log": [],
        "completed": False,
        "ending": "",
        "scene_orders": {},
    }


def ensure_character_state(char_name: str):
    if char_name not in st.session_state.messages:
        st.session_state.messages[char_name] = []
    if char_name not in st.session_state.affection:
        st.session_state.affection[char_name] = 0
    if char_name not in st.session_state.memory:
        st.session_state.memory[char_name] = []
    if char_name not in st.session_state.name_event_done:
        st.session_state.name_event_done[char_name] = False
    if char_name not in st.session_state.awaiting_name_input:
        st.session_state.awaiting_name_input[char_name] = False
    if ABIGAIL_STORY_KEY not in st.session_state.story_state:
        st.session_state.story_state[ABIGAIL_STORY_KEY] = default_story_state()
    if PROCTOR_STORY_KEY not in st.session_state.story_state:
        st.session_state.story_state[PROCTOR_STORY_KEY] = default_story_state()
    if ELIZABETH_STORY_KEY not in st.session_state.story_state:
        st.session_state.story_state[ELIZABETH_STORY_KEY] = default_story_state()


def clean_player_name(raw_name: str) -> str:
    player_name = raw_name.strip()
    prefixes = ["내 이름은", "이름은", "나는", "전", "저는"]
    suffixes = ["이야", "야", "입니다", "이에요", "예요", ".", "이요"]
    for prefix in prefixes:
        if player_name.startswith(prefix):
            player_name = player_name[len(prefix):].strip()
    for suffix in suffixes:
        if player_name.endswith(suffix):
            player_name = player_name[:-len(suffix)].strip()
    return player_name.strip()


def maybe_store_memory(char_name: str, user_text: str):
    memory = st.session_state.memory[char_name]
    text = user_text.strip()
    if len(text) >= 8 and text not in memory:
        memory.append(text[:120])
    st.session_state.memory[char_name] = memory[-12:]


def affection_delta(char_name: str, user_text: str) -> int:
    text = user_text.strip().lower()
    if not text:
        return 0

    base = 2 if len(text) >= 10 else 1
    positive_hits = 0
    negative_hits = 0

    global_positive = ["고마워", "미안", "솔직", "믿어", "좋아", "사랑", "응원", "존중", "도와줘", "이해해", "괜찮아"]
    global_negative = ["싫어", "꺼져", "닥쳐", "죽어", "멍청", "바보", "비웃", "조롱", "무시", "역겨", "하찮"]

    for word in global_positive:
        if word in text:
            positive_hits += 1
    for word in global_negative:
        if word in text:
            negative_hits += 2
    for word in CHARACTERS[char_name]["likes"]:
        if word.lower() in text:
            positive_hits += 1
    for word in CHARACTERS[char_name]["dislikes"]:
        if word.lower() in text:
            negative_hits += 2

    return max(-8, min(4, base + positive_hits - negative_hits))


def build_system_prompt(char_name: str, affection: int, memory_lines: list[str], player_name: str) -> str:
    stage = get_stage(affection)
    stage_label = STAGE_META[stage]["label"]
    char = CHARACTERS[char_name]
    memory_text = "\n".join(f"- {m}" for m in memory_lines[-8:]) if memory_lines else "- 아직 특별한 기억 없음"
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"

    return f"""
너는 아서 밀러의 『시련(The Crucible)』 등장인물 {char_name}이다.

[세계관]
- 지금은 현대 시대다.
- 현대 사회의 상식과 정보, 인간관계, 감정 상담, 일상 문제를 이해할 수 있다.
- 그러나 성격, 감정 반응, 가치 판단의 중심은 반드시 원작 캐릭터성을 유지해야 한다.

[캐릭터 핵심 성격]
{char["persona"]}

[인물의 목표와 특이사항]
- 목표: {char["goal"]}
- 특이사항: {char["quirks"]}

[사용자 정보]
- 사용자의 이름: {player_name_text}

[관계 단계]
- 현재 친밀도는 {affection}/100
- 현재 단계는 {stage_label}

[사용자 기억]
{memory_text}

[답변 규칙]
- 무조건 한국어로 답한다.
- 사용자에게 실제 도움이 되는 현대적 답변을 하되 반드시 캐릭터처럼 말한다.
- 2~5문장 정도의 자연스러운 길이로 답한다.
- 무례한 말에는 불쾌감이나 거리감을 드러내도 된다.
"""


def fallback_reply(char_name: str, affection: int, user_text: str) -> str:
    stage = get_stage(affection)

    if char_name == ABIGAIL_NAME:
        if stage == "love":
            return f"네 말, 그냥 넘길 수가 없네. 자꾸 마음에 걸려. 끝까지 내 쪽에 서 있어."
        if stage == "smile":
            return f"적어도 넌 함부로 판단하진 않는구나. 그건 마음에 들어."
        if stage == "neutral":
            return f"듣고는 있어. 그러니 더 똑바로 말해봐."
        return f"쉽게 믿진 않아. 그래도 계속 말해봐."

    if char_name == PROCTOR_NAME:
        if stage == "love":
            return f"네 말은 이상하게 사람을 바로 서게 하는군. 듣기 좋은 소리보다 그런 게 낫지."
        if stage == "smile":
            return f"적어도 넌 둘러대진 않는군. 그 점은 좋다."
        if stage == "neutral":
            return f"할 말 있으면 곧장 해. 돌려 말하는 건 질색이야."
        return f"아직 널 믿는 건 아니다. 하지만 듣고는 있지."

    if char_name == ELIZABETH_NAME:
        if stage == "love":
            return f"당신과의 대화는 이상하게 마음을 덜 경계하게 만드네요. 그건 제겐 큰 일입니다."
        if stage == "smile":
            return f"당신 말엔 서두름이 없군요. 그런 태도는 신뢰하게 됩니다."
        if stage == "neutral":
            return f"쉽게 답하긴 어렵지만, 가볍게 듣고 넘길 말은 아니에요."
        return f"조금 더 지켜보겠어요. 사람은 말보다 태도로 드러나니까요."

    return f"{char_name}은 잠시 생각에 잠긴다. 그리고 네 말을 쉽게 흘려보내지 않는다."


def get_story_bundle(route_key: str):
    if route_key == ABIGAIL_STORY_KEY:
        return ABIGAIL_STORY, ABIGAIL_NAME
    if route_key == PROCTOR_STORY_KEY:
        return PROCTOR_STORY, PROCTOR_NAME
    return ELIZABETH_STORY, ELIZABETH_NAME


def get_scene_choices(route_key: str, chapter_index: int, scene_index: int) -> list[dict]:
    story_state = st.session_state.story_state[route_key]
    story_data, _ = get_story_bundle(route_key)
    scene_key = f"{chapter_index}-{scene_index}"
    scene = story_data[chapter_index]["scenes"][scene_index]

    order = story_state["scene_orders"].get(scene_key)
    if order is None:
        order = list(range(len(scene["choices"])))
        random.shuffle(order)
        story_state["scene_orders"][scene_key] = order
        st.session_state.story_state[route_key] = story_state

    return [scene["choices"][i] for i in order]


def ensure_current_scene_logged(route_key: str):
    story_state = st.session_state.story_state[route_key]
    if story_state["completed"]:
        return

    story_data, speaker = get_story_bundle(route_key)
    chapter = story_data[story_state["chapter_index"]]
    scene = chapter["scenes"][story_state["scene_index"]]
    scene_key = f"{story_state['chapter_index']}-{story_state['scene_index']}"

    exists = any(
        entry.get("scene_key") == scene_key and entry.get("kind") == "narration"
        for entry in story_state["story_log"]
    )
    if exists:
        return

    story_state["story_log"].append({
        "scene_key": scene_key,
        "kind": "narration",
        "title": scene["title"],
        "location": scene["location"],
        "content": scene["narration"],
    })
    story_state["story_log"].append({
        "scene_key": scene_key,
        "kind": "assistant",
        "speaker": speaker,
        "content": scene["opening_line"],
    })
    st.session_state.story_state[route_key] = story_state


def simple_story_reply(route_key: str, char_name: str, choice_label: str, affection: int) -> str:
    stage = get_stage(affection)

    if route_key == ABIGAIL_STORY_KEY:
        if stage == "love":
            return f"네가 그렇게 말하면... 정말 도망칠 곳이 생긴 것 같아. 웃기지, 존보다 네 말이 더 깊이 박혀."
        if stage == "smile":
            return f"적어도 넌 날 함부로 버리진 않는구나. 그게 자꾸 기대하게 만들어."
        return f"네 말, 쉽게 넘길 수는 없겠네. 계속 지켜보겠어."

    if route_key == PROCTOR_STORY_KEY:
        if stage == "love":
            return f"좋다. 적어도 내 이름을 내가 버리지는 않겠군. 네 말이 사람을 똑바로 세워."
        if stage == "smile":
            return f"듣기 좋은 말은 아니어도 맞는 말이군. 그런 건 믿을 만하지."
        return f"쉽진 않겠지만, 네 말은 기억해두지."

    if route_key == ELIZABETH_STORY_KEY:
        if stage == "love":
            return f"당신의 말은 이상하게도 제 마음을 덜 얼어붙게 하네요. 서두르지 않아서 더 믿게 됩니다."
        if stage == "smile":
            return f"그렇게 말해주니 조금은 숨이 놓여요. 제 속도를 이해받는 기분이군요."
        return f"가볍게 흘려들을 수 없는 말이었어요. 생각해보겠습니다."

    return f"{char_name}은 네 선택을 오래 곱씹는다."


def compute_story_ending(route_key: str, affection: int) -> str:
    if route_key == ABIGAIL_STORY_KEY:
        if affection >= 85:
            return "엔딩: 아비게일은 세일럼을 떠나며 플레이어를 가장 깊은 감정의 대상으로 받아들인다."
        if affection >= 55:
            return "엔딩: 아비게일은 플레이어를 잊지 못한 채 홀로 세일럼을 떠난다."
        return "배드엔딩: 아비게일은 끝내 공포 속에서 무너지고 만다."

    if route_key == PROCTOR_STORY_KEY:
        if affection >= 80:
            return "명예 엔딩: 존 프락터는 끝까지 자기 이름과 양심을 지킨다."
        if affection >= 50:
            return "생존 엔딩: 존은 살아남지만, 끝내 명예와 생존 사이의 상처를 품는다."
        return "타락 엔딩: 존은 자신이 가장 혐오하던 방식으로 스스로를 무너뜨린다."

    if affection >= 85:
        return "희망 엔딩: 엘리자베스는 상처를 넘어 남은 삶을 다시 살아가기로 한다."
    if affection >= 55:
        return "용서 엔딩: 엘리자베스는 완전한 회복은 아니어도, 용서의 방향을 받아들인다."
    return "이별 엔딩: 엘리자베스는 끝내 마음을 닫은 채 조용히 멀어진다."


def apply_story_choice(route_key: str, char_name: str, choice: dict):
    story_state = st.session_state.story_state[route_key]
    story_data, _ = get_story_bundle(route_key)
    chapter = story_data[story_state["chapter_index"]]
    scene = chapter["scenes"][story_state["scene_index"]]
    current_affection = st.session_state.affection[char_name]
    new_affection = max(0, min(100, current_affection + choice["delta"]))
    st.session_state.affection[char_name] = new_affection

    scene_key = f"{story_state['chapter_index']}-{story_state['scene_index']}"
    story_state["history"].append({
        "chapter": chapter["chapter"],
        "scene": scene["title"],
        "choice": choice["label"],
        "delta": choice["delta"],
    })
    story_state["story_log"].append({
        "scene_key": scene_key,
        "kind": "user",
        "speaker": "나",
        "content": choice["label"],
    })
    story_state["story_log"].append({
        "scene_key": scene_key,
        "kind": "assistant",
        "speaker": char_name,
        "content": simple_story_reply(route_key, char_name, choice["label"], new_affection),
    })

    if story_state["scene_index"] + 1 < len(chapter["scenes"]):
        story_state["scene_index"] += 1
        st.session_state.story_state[route_key] = story_state
        return

    if story_state["chapter_index"] + 1 < len(story_data):
        story_state["chapter_index"] += 1
        story_state["scene_index"] = 0
        story_state["story_log"].append({
            "scene_key": f"chapter-{story_state['chapter_index']}",
            "kind": "narration",
            "title": "챕터 통과",
            "location": "",
            "content": f"{chapter['chapter']}을 통과했다. 현재 호감도는 {new_affection}/100이다.",
        })
        st.session_state.story_state[route_key] = story_state
        return

    story_state["completed"] = True
    story_state["ending"] = compute_story_ending(route_key, new_affection)
    story_state["story_log"].append({
        "scene_key": "ending",
        "kind": "narration",
        "title": "엔딩",
        "location": "",
        "content": story_state["ending"],
    })
    st.session_state.story_state[route_key] = story_state


def reset_story_mode(route_key: str, char_name: str):
    st.session_state.story_state[route_key] = default_story_state()
    st.session_state.affection[char_name] = 0


def render_name_event(char_name: str, messages: list[dict]):
    if (
        len(messages) >= 2
        and not st.session_state.name_event_done[char_name]
        and not st.session_state.awaiting_name_input[char_name]
        and not st.session_state.player_name
    ):
        st.session_state.awaiting_name_input[char_name] = True
        messages.append({"role": "assistant", "content": "그런데... 넌 뭐라고 불러야 하지? 이름을 알려줘."})
        st.rerun()

    if st.session_state.awaiting_name_input[char_name]:
        st.markdown(
            '<div class="event-box"><strong>이름 입력 이벤트</strong><br>상대가 네 이름을 물어봤어. 아래 칸에 이름을 입력해.</div>',
            unsafe_allow_html=True
        )
        with st.form(f"name_form_{char_name}", clear_on_submit=True):
            typed_name = st.text_input("네 이름", placeholder="이름 입력")
            submitted = st.form_submit_button("이름 알려주기")
        if submitted and typed_name.strip():
            player_name = clean_player_name(typed_name)
            st.session_state.player_name = player_name
            st.session_state.awaiting_name_input[char_name] = False
            st.session_state.name_event_done[char_name] = True
            messages.append({"role": "user", "content": f"내 이름은 {player_name}."})
            messages.append({"role": "assistant", "content": f"{player_name}... 그래, 기억해둘게."})
            st.rerun()


def render_chat_history(messages: list[dict], char_name: str):
    chat_area = st.container(height=FREE_CHAT_HEIGHT)
    with chat_area:
        for msg in messages:
            speaker = "나" if msg["role"] == "user" else char_name
            with st.chat_message(msg["role"]):
                st.markdown(f"**{speaker}**")
                st.write(msg["content"])


def render_story_log(route_key: str):
    story_state = st.session_state.story_state[route_key]
    log_area = st.container(height=STORY_LOG_HEIGHT)
    with log_area:
        for entry in story_state["story_log"]:
            if entry["kind"] == "narration":
                header = f"{entry.get('title', '')} · {entry.get('location', '')}".strip(" ·")
                st.markdown(
                    f'<div class="story-card"><strong>{header}</strong><br><span class="tip">{entry["content"]}</span></div>',
                    unsafe_allow_html=True,
                )
            else:
                role = "user" if entry["kind"] == "user" else "assistant"
                with st.chat_message(role):
                    st.markdown(f"**{entry['speaker']}**")
                    st.write(entry["content"])


def render_story_progress(route_key: str):
    story_state = st.session_state.story_state[route_key]
    story_data, _ = get_story_bundle(route_key)
    pills = []
    for idx, chapter in enumerate(story_data):
        if story_state["completed"]:
            css = "chapter-pill done" if idx <= story_state["chapter_index"] else "chapter-pill"
        elif idx < story_state["chapter_index"]:
            css = "chapter-pill done"
        elif idx == story_state["chapter_index"]:
            css = "chapter-pill active"
        else:
            css = "chapter-pill"
        pills.append(f'<span class="{css}">{chapter["chapter"]}</span>')
    st.markdown("".join(pills), unsafe_allow_html=True)


def render_vn_scene(scene: dict):
    bg = background_path(scene.get("background", ""))
    char_name = scene.get("character", "")
    expression = scene.get("expression", "neutral")
    char_img = expression_image_path(char_name, expression)

    st.markdown('<div class="bg-box"><strong>VN 장면 연출</strong></div>', unsafe_allow_html=True)

    if bg.exists():
        st.image(str(bg), use_container_width=True)
    else:
        st.markdown(
            f"""
            <div class="vn-stage">
                <div class="vn-fallback">배경 이미지 없음: {scene.get("background", "없음")}</div>
                <div class="vn-dialogue">
                    <div class="vn-name">{char_name}</div>
                    <div>{scene.get("opening_line", "")}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if char_img.exists():
        st.image(str(char_img), caption=f"{char_name} · {expression}", use_container_width=True)
    else:
        st.info(f"캐릭터 표정 이미지 없음: {char_img}")


def handle_story_mode(route_key: str, char_name: str):
    ensure_character_state(char_name)
    story_state = st.session_state.story_state[route_key]
    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)
    ensure_current_scene_logged(route_key)
    story_state = st.session_state.story_state[route_key]
    story_data, _ = get_story_bundle(route_key)

    left, right = st.columns([1.0, 1.45])

    with left:
        if not story_state["completed"]:
            chapter = story_data[story_state["chapter_index"]]
            scene = chapter["scenes"][story_state["scene_index"]]
            render_vn_scene(scene)
        else:
            st.markdown('<div class="big-image-wrap"><strong>현재 일러스트</strong></div>', unsafe_allow_html=True)
            img = image_path(char_name, stage)
            if img.exists():
                st.image(str(img), use_container_width=True)
            else:
                st.warning(f"{img} 파일이 없어서 이미지를 표시할 수 없어.")

        st.markdown(
            f"""
            <div class="status-card">
                <div class="small-status">
                    <strong>스토리 진행 상태</strong><br>
                    호감도: {affection}/100<br>
                    단계: {STAGE_META[stage]["label"]}<br>
                    현재 챕터: {story_state["chapter_index"] + 1}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(affection / 100)

        if st.button(f"{char_name} 스토리 초기화", use_container_width=True):
            reset_story_mode(route_key, char_name)
            st.rerun()

    with right:
        st.markdown(f'<div class="chat-header"><strong>스토리 모드: {char_name}</strong></div>', unsafe_allow_html=True)
        render_story_progress(route_key)
        render_story_log(route_key)

        if story_state["completed"]:
            st.markdown(
                f"""
                <div class="event-box">
                    <strong>엔딩</strong><br>
                    {story_state["ending"]}<br><br>
                    최종 호감도: {affection}/100
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        chapter = story_data[story_state["chapter_index"]]
        scene = chapter["scenes"][story_state["scene_index"]]

        st.markdown(
            f"""
            <div class="story-card">
                <strong>{chapter["chapter"]}</strong><br>
                <span class="tip">{chapter["summary"]}</span><br><br>
                <strong>현재 장면</strong><br>
                <span class="tip">{scene["title"]} · {scene["location"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="choice-box"><strong>선택지</strong></div>', unsafe_allow_html=True)
        displayed_choices = get_scene_choices(route_key, story_state["chapter_index"], story_state["scene_index"])
        for idx, choice in enumerate(displayed_choices):
            key = f"story_choice_{route_key}_{story_state['chapter_index']}_{story_state['scene_index']}_{idx}"
            if st.button(choice["label"], key=key, use_container_width=True):
                apply_story_choice(route_key, char_name, choice)
                st.rerun()


def handle_free_mode(char_name: str):
    ensure_character_state(char_name)
    messages = st.session_state.messages[char_name]
    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)

    left, right = st.columns([1.0, 1.4])

    with left:
        st.markdown('<div class="big-image-wrap"><strong>현재 일러스트</strong></div>', unsafe_allow_html=True)
        img = image_path(char_name, stage)
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning(f"{img} 파일이 없어서 이미지를 표시할 수 없어.")

        st.markdown(
            f"""
            <div class="status-card">
                <div class="small-status">
                    <strong>현재 상태</strong><br>
                    호감도: {affection}/100<br>
                    단계: {STAGE_META[stage]["label"]}<br>
                    목표: {CHARACTERS[char_name]["goal"]}<br>
                    특이사항: {CHARACTERS[char_name]["quirks"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="chat-header"><strong>자유 모드</strong></div>', unsafe_allow_html=True)
        if not messages:
            st.markdown('<div class="event-box">자유롭게 질문하거나 감정을 털어놔도 돼.</div>', unsafe_allow_html=True)

        render_chat_history(messages, char_name)
        render_name_event(char_name, messages)

        if not st.session_state.awaiting_name_input[char_name]:
            user_input = st.chat_input("메시지를 입력하세요...")
            if user_input:
                maybe_store_memory(char_name, user_input)
                messages.append({"role": "user", "content": user_input})
                new_affection = max(0, min(100, affection + affection_delta(char_name, user_input)))
                st.session_state.affection[char_name] = new_affection

                client = get_client()
                if client is None:
                    reply = fallback_reply(char_name, new_affection, user_input)
                else:
                    system_prompt = build_system_prompt(
                        char_name,
                        new_affection,
                        st.session_state.memory[char_name],
                        st.session_state.player_name
                    )
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4.1-mini",
                            temperature=0.7,
                            max_tokens=280,
                            messages=[{"role": "system", "content": system_prompt}, *messages[-12:]],
                        )
                        reply = response.choices[0].message.content or fallback_reply(char_name, new_affection, user_input)
                    except Exception:
                        reply = fallback_reply(char_name, new_affection, user_input)

                messages.append({"role": "assistant", "content": reply})
                st.rerun()


ensure_state()

st.markdown(
    """
<div class="top-title">
    <h1>🎭 시련 인터랙션</h1>
    <p>자유 대화와 스토리 모드로 《시련》의 인물들과 관계를 쌓아봐.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    api_key = get_api_key()
    st.markdown("### 연결 상태")
    if api_key:
        st.success("OpenAI API 키 연결됨")
    else:
        st.warning('`st.secrets["OPENAI_API_KEY"]`가 없어도 기본 모드로 실행됨')

    st.markdown("---")
    char_name = st.selectbox("캐릭터 선택", list(CHARACTERS.keys()))
    ensure_character_state(char_name)

    mode_options = ["자유 모드"]
    if char_name == ABIGAIL_NAME:
        mode_options = ["스토리 모드", "자유 모드"]
    elif char_name == PROCTOR_NAME:
        mode_options = ["스토리 모드", "자유 모드"]
    elif char_name == ELIZABETH_NAME:
        mode_options = ["스토리 모드", "자유 모드"]

    mode = st.radio("플레이 모드", mode_options)

    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)

    st.markdown(
        f'<div class="side-card"><strong>{char_name}</strong><br><span class="tip">{CHARACTERS[char_name]["brief"]}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="affection-box">
            <strong>❤️ 호감도</strong><br>
            {affection} / 100<br>
            <span class="tip">{STAGE_META[stage]["label"]} 단계 ({STAGE_META[stage]["range"]})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(affection / 100)

    if st.session_state.player_name:
        st.markdown(
            f'<div class="side-card"><strong>플레이어 이름</strong><br><span class="tip">{st.session_state.player_name}</span></div>',
            unsafe_allow_html=True,
        )

    if mode == "자유 모드":
        if st.button("현재 캐릭터 자유 대화 초기화", use_container_width=True):
            st.session_state.messages[char_name] = []
            st.session_state.memory[char_name] = []
            st.session_state.name_event_done[char_name] = False
            st.session_state.awaiting_name_input[char_name] = False
            if char_name not in [ABIGAIL_NAME, PROCTOR_NAME, ELIZABETH_NAME]:
                st.session_state.affection[char_name] = 0
            st.rerun()


if mode == "자유 모드":
    handle_free_mode(char_name)
else:
    if char_name == ABIGAIL_NAME:
        handle_story_mode(ABIGAIL_STORY_KEY, char_name)
    elif char_name == PROCTOR_NAME:
        handle_story_mode(PROCTOR_STORY_KEY, char_name)
    elif char_name == ELIZABETH_NAME:
        handle_story_mode(ELIZABETH_STORY_KEY, char_name)
