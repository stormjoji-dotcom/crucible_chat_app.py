import random
from pathlib import Path

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")
ABIGAIL_NAME = "아비게일 윌리엄즈"
ABIGAIL_STORY_KEY = "abigail_story"
STORY_LOG_HEIGHT = 420
FREE_CHAT_HEIGHT = 520


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
    font-size: 2.4rem;
}
.top-title p {
    margin: 8px 0 0 0;
    color: #d9d0c4;
    font-size: 1rem;
}
.side-card, .status-card, .chat-header, .big-image-wrap, .story-card {
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
    font-size: 0.9rem;
    line-height: 1.5;
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
input {
    color: white !important;
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


ABIGAIL_CHAPTER_RULES = [
    {"threshold": 20, "bad_ending": "배드엔딩 1. 숲의 춤이 들통난 뒤 아비게일은 세일럼의 공포를 혼자 떠안는다. 너의 지지를 끝내 얻지 못한 그녀는 마녀사냥의 첫 표적이 되어 군중에게 붙잡힌다."},
    {"threshold": 40, "bad_ending": "배드엔딩 2. 법정의 힘을 손에 쥔 아비게일은 끝내 존 프락터에게 매달리지만, 돌아온 것은 보호가 아니라 더 잔혹한 마녀사냥뿐이다."},
    {"threshold": 75, "bad_ending": "배드엔딩 3. 덴포스 앞에서 끝내 흔들린 아비게일은 모든 책임을 뒤집어쓴 채 마녀로 규정되고, 재판의 불길 속에서 처형당한다."},
    {"threshold": 90, "bad_ending": ""},
]


ABIGAIL_STORY = [
    {
        "chapter": "Chapter 1. 숲의 춤",
        "summary": "희곡 1막처럼 숲에서 춤추는 아비게일을 발견하고, 그 밤의 비밀을 함께 감당할지 결정하는 장이다.",
        "scenes": [
            {
                "title": "숲에서 마주친 순간",
                "location": "세일럼 외곽 숲",
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
        "scenes": [
            {
                "title": "법정이 세워진 날",
                "location": "세일럼 회의실",
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
        "scenes": [
            {
                "title": "댄포스의 시선",
                "location": "법정 대기실",
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
        "scenes": [
            {
                "title": "도망칠 준비",
                "location": "새벽의 선착장",
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


def get_api_key() -> str:
    return st.secrets.get("OPENAI_API_KEY", "")


def get_client():
    api_key = get_api_key()
    if not api_key:
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
        "tags": [],
        "completed": False,
        "last_result": "",
        "ending": "",
        "ending_type": "",
        "failed_chapter": None,
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
    if char_name == ABIGAIL_NAME and ABIGAIL_STORY_KEY not in st.session_state.story_state:
        st.session_state.story_state[ABIGAIL_STORY_KEY] = default_story_state()


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

    provoking_patterns = ["왜 이렇게 멍청", "너 별로", "네 잘못", "웃기네", "한심", "구질", "역겹"]
    if any(pattern in text for pattern in provoking_patterns):
        negative_hits += 3

    return max(-8, min(4, base + positive_hits - negative_hits))


def clean_player_name(raw_name: str) -> str:
    player_name = raw_name.strip()
    prefixes = ["내 이름은", "이름은", "나는", "전", "저는"]
    suffixes = ["이야", "야", "입니다", "이에요", "예요", ".", "이요"]

    for prefix in prefixes:
        if player_name.startswith(prefix):
            player_name = player_name[len(prefix) :].strip()
    for suffix in suffixes:
        if player_name.endswith(suffix):
            player_name = player_name[: -len(suffix)].strip()
    return player_name.strip()


def get_story_snapshot() -> str:
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    if not story["history"]:
        return "아직 스토리 모드를 진행하지 않았다."
    return "\n".join(
        f"- {item['chapter']} / {item['scene']}: 선택 '{item['choice']}' / 호감도 변화 {item['delta']:+d}"
        for item in story["history"][-8:]
    )


def build_system_prompt(char_name: str, affection: int, memory_lines: list[str], player_name: str) -> str:
    stage = get_stage(affection)
    stage_label = STAGE_META[stage]["label"]
    char = CHARACTERS[char_name]
    memory_text = "\n".join(f"- {m}" for m in memory_lines[-8:]) if memory_lines else "- 아직 특별한 기억 없음"
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"

    story_block = ""
    if char_name == ABIGAIL_NAME:
        story = st.session_state.story_state[ABIGAIL_STORY_KEY]
        tags = ", ".join(story["tags"][-10:]) if story["tags"] else "없음"
        ending = story["ending"] if story["ending"] else "아직 엔딩 전"
        story_block = f"""
[스토리 모드 반영]
- 스토리 진행 기록:
{get_story_snapshot()}
- 아비게일이 플레이어에게서 받은 인상 태그: {tags}
- 현재 스토리 상태: {ending}
- 자유 모드에서는 이 누적 인상을 반드시 반영한다.
"""

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
- 이름을 알고 있다면 너무 남발하지 말고 자연스럽게 불러도 된다.

[관계 단계]
- 현재 친밀도는 {affection}/100
- 현재 단계는 {stage_label}
- 경계 단계에서는 차갑고 조심스럽다.
- 중립 단계에서는 객관적이지만 캐릭터성을 유지한다.
- 친근 단계에서는 더 솔직하고 가까워진다.
- 매우 친밀 단계에서는 애착, 보호욕, 집착, 온기 같은 캐릭터별 친밀한 반응이 강해진다.

[사용자 기억]
{memory_text}
{story_block}
[답변 규칙]
- 무조건 한국어로 답한다.
- 사용자에게 실제 도움이 되는 현대적 답변을 하되 반드시 캐릭터처럼 말한다.
- 2~5문장 정도의 자연스러운 길이로 답한다.
- 무례한 말에는 불쾌감이나 거리감을 드러내도 된다.
"""


def build_story_prompt(scene: dict, choice: dict, affection: int, player_name: str) -> str:
    stage = STAGE_META[get_stage(affection)]["label"]
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"
    tags = ", ".join(st.session_state.story_state[ABIGAIL_STORY_KEY]["tags"][-10:]) or "없음"
    return f"""
너는 아서 밀러의 『시련』의 아비게일 윌리엄즈다.

[상황]
- 챕터: {scene['chapter']}
- 장면: {scene['title']}
- 장소: {scene['location']}
- 장면 설명: {scene['setup']}
- 플레이어 이름: {player_name_text}
- 현재 호감도: {affection}/100 ({stage})
- 누적 인상 태그: {tags}

[플레이어 선택]
- 선택 내용: {choice['label']}
- 선택이 아비게일에게 준 인상: {choice['hint']}

[지켜야 할 변화]
- 챕터 1은 숲의 춤과 비밀 공유에 대한 긴장이다.
- 챕터 2는 법정이 세워지고 엘리자베스가 고발되며, 존 프락터를 향한 집착이 아직 강하다.
- 챕터 3에서 호감도 75 이상이 되면 존 프락터보다 플레이어 쪽으로 마음이 완전히 기울어야 한다.
- 챕터 4는 세일럼 탈출 직전, 플레이어를 미래에 포함시킬지 결정하는 단계다.

[답변 방식]
- 아비게일의 대사와 짧은 장면 반응을 함께 보여준다.
- 3~5문장 정도로 답한다.
- 무조건 한국어로 쓴다.
"""


def generate_story_reply(scene: dict, choice: dict, affection: int, player_name: str) -> str:
    client = get_client()
    if client is None:
        return "아비게일은 잠시 숨을 고른다. 네가 한 말을 쉽게 흘려보내지 못한 듯 눈빛이 흔들린다."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.85,
            max_tokens=260,
            messages=[{"role": "system", "content": build_story_prompt(scene, choice, affection, player_name)}],
        )
        return response.choices[0].message.content or "..."
    except Exception as exc:
        return f"아비게일의 반응을 불러오지 못했어: {exc}"


def get_scene_key(chapter_index: int, scene_index: int) -> str:
    return f"{chapter_index}-{scene_index}"


def get_scene_choices(chapter_index: int, scene_index: int) -> list[dict]:
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    scene_key = get_scene_key(chapter_index, scene_index)
    scene = ABIGAIL_STORY[chapter_index]["scenes"][scene_index]
    order = story["scene_orders"].get(scene_key)
    if order is None:
        order = list(range(len(scene["choices"])))
        random.shuffle(order)
        story["scene_orders"][scene_key] = order
        st.session_state.story_state[ABIGAIL_STORY_KEY] = story
    return [scene["choices"][idx] for idx in order]


def ensure_current_scene_logged():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    if story["completed"]:
        return

    chapter = ABIGAIL_STORY[story["chapter_index"]]
    scene = chapter["scenes"][story["scene_index"]]
    scene_key = get_scene_key(story["chapter_index"], story["scene_index"])

    if any(entry.get("scene_key") == scene_key and entry.get("kind") == "narration" for entry in story["story_log"]):
        return

    story["story_log"].append(
        {"scene_key": scene_key, "kind": "narration", "title": scene["title"], "location": scene["location"], "content": scene["narration"]}
    )
    story["story_log"].append(
        {"scene_key": scene_key, "kind": "narration", "title": "상황", "location": scene["location"], "content": scene["setup"]}
    )
    story["story_log"].append(
        {"scene_key": scene_key, "kind": "assistant", "speaker": ABIGAIL_NAME, "content": scene["opening_line"]}
    )
    st.session_state.story_state[ABIGAIL_STORY_KEY] = story


def determine_final_abigail_ending(affection: int) -> tuple[str, str]:
    if affection >= 100:
        return (
            "good_love_escape",
            "엔딩 2. 아비게일은 끝내 존 프락터를 놓고 플레이어를 사랑의 대상으로 택한다. 두 사람은 세일럼을 등지고 함께 도망치며, 서로에게 처음으로 거짓 없는 미래를 약속한다.",
        )
    return (
        "good_escape",
        "엔딩 1. 아비게일은 원작처럼 세일럼을 떠난다. 다만 이번에는 플레이어를 잊지 못한 채, 자신을 끝까지 이해했던 한 사람의 기억을 품고 도망친다.",
    )


def finish_with_bad_ending(chapter_index: int):
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    story["completed"] = True
    story["failed_chapter"] = chapter_index
    story["ending_type"] = f"bad_{chapter_index + 1}"
    story["ending"] = ABIGAIL_CHAPTER_RULES[chapter_index]["bad_ending"]
    story["story_log"].append(
        {
            "scene_key": "ending",
            "kind": "narration",
            "title": f"배드엔딩 {chapter_index + 1}",
            "location": "세일럼",
            "content": story["ending"],
        }
    )
    st.session_state.story_state[ABIGAIL_STORY_KEY] = story


def apply_story_choice(scene: dict, choice: dict):
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    current_affection = st.session_state.affection[ABIGAIL_NAME]
    new_affection = max(0, min(100, current_affection + choice["delta"]))
    st.session_state.affection[ABIGAIL_NAME] = new_affection
    scene_key = get_scene_key(story["chapter_index"], story["scene_index"])

    story["tags"].append(choice["tag"])
    story["history"].append({"chapter": scene["chapter"], "scene": scene["title"], "choice": choice["label"], "delta": choice["delta"]})
    story["story_log"].append({"scene_key": scene_key, "kind": "user", "speaker": "나", "content": choice.get("spoken", choice["label"])})

    reply = generate_story_reply(scene, choice, new_affection, st.session_state.player_name)
    story["last_result"] = reply
    story["story_log"].append({"scene_key": scene_key, "kind": "assistant", "speaker": ABIGAIL_NAME, "content": reply})

    chapter_index = story["chapter_index"]
    scene_count = len(ABIGAIL_STORY[chapter_index]["scenes"])

    if story["scene_index"] + 1 < scene_count:
        story["scene_index"] += 1
        st.session_state.story_state[ABIGAIL_STORY_KEY] = story
        return

    threshold = ABIGAIL_CHAPTER_RULES[chapter_index]["threshold"]
    if new_affection < threshold:
        st.session_state.story_state[ABIGAIL_STORY_KEY] = story
        finish_with_bad_ending(chapter_index)
        return

    if chapter_index == len(ABIGAIL_STORY) - 1:
        ending_type, ending_text = determine_final_abigail_ending(new_affection)
        story["completed"] = True
        story["ending_type"] = ending_type
        story["ending"] = ending_text
        story["story_log"].append(
            {
                "scene_key": "ending",
                "kind": "narration",
                "title": "최종 엔딩",
                "location": "새벽의 바다",
                "content": ending_text,
            }
        )
        st.session_state.story_state[ABIGAIL_STORY_KEY] = story
        return

    next_chapter = chapter_index + 1
    story["chapter_index"] = next_chapter
    story["scene_index"] = 0
    story["story_log"].append(
        {
            "scene_key": f"chapter-{next_chapter}",
            "kind": "narration",
            "title": "챕터 통과",
            "location": "",
            "content": f"{scene['chapter']}을 통과했다. 현재 호감도는 {new_affection}/100, 다음 챕터 목표는 {ABIGAIL_CHAPTER_RULES[next_chapter]['threshold']}이다.",
        }
    )
    st.session_state.story_state[ABIGAIL_STORY_KEY] = story


def reset_story_mode():
    st.session_state.story_state[ABIGAIL_STORY_KEY] = default_story_state()
    st.session_state.affection[ABIGAIL_NAME] = 0


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
        st.markdown('<div class="event-box"><strong>이름 입력 이벤트</strong><br>상대가 네 이름을 물어봤어. 아래 칸에 이름을 입력해.</div>', unsafe_allow_html=True)
        with st.form(f"name_form_{char_name}", clear_on_submit=True):
            typed_name = st.text_input("네 이름", placeholder="이름 입력")
            submitted = st.form_submit_button("이름 알려주기")
        if submitted and typed_name.strip():
            player_name = clean_player_name(typed_name)
            st.session_state.player_name = player_name
            st.session_state.awaiting_name_input[char_name] = False
            st.session_state.name_event_done[char_name] = True
            messages.append({"role": "user", "content": f"내 이름은 {player_name}."})
            messages.append({"role": "assistant", "content": f"{player_name}... 그래, 기억해둘게. 이제부턴 그렇게 부를게."})
            st.rerun()


def render_chat_history(messages: list[dict], char_name: str):
    chat_area = st.container(height=FREE_CHAT_HEIGHT)
    with chat_area:
        for msg in messages:
            speaker = "나" if msg["role"] == "user" else char_name
            with st.chat_message(msg["role"]):
                st.markdown(f"**{speaker}**")
                st.write(msg["content"])


def render_story_progress():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    pills = []
    for idx, chapter in enumerate(ABIGAIL_STORY):
        if story["completed"]:
            css = "chapter-pill done" if idx <= story["chapter_index"] else "chapter-pill"
        elif idx < story["chapter_index"]:
            css = "chapter-pill done"
        elif idx == story["chapter_index"]:
            css = "chapter-pill active"
        else:
            css = "chapter-pill"
        threshold = ABIGAIL_CHAPTER_RULES[idx]["threshold"]
        pills.append(f'<span class="{css}">{chapter["chapter"]} · 목표 {threshold}</span>')
    st.markdown("".join(pills), unsafe_allow_html=True)


def render_story_log():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    log_area = st.container(height=STORY_LOG_HEIGHT)
    with log_area:
        for entry in story["story_log"]:
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


def handle_story_mode():
    ensure_character_state(ABIGAIL_NAME)
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    affection = st.session_state.affection[ABIGAIL_NAME]
    stage = get_stage(affection)
    ensure_current_scene_logged()
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]

    left, right = st.columns([1.0, 1.45])

    with left:
        st.markdown('<div class="big-image-wrap"><strong>현재 일러스트</strong></div>', unsafe_allow_html=True)
        img = image_path(ABIGAIL_NAME, stage)
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning(f"{img} 파일이 없어서 이미지를 표시할 수 없어.")

        current_rule = ABIGAIL_CHAPTER_RULES[min(story["chapter_index"], len(ABIGAIL_CHAPTER_RULES) - 1)]
        st.markdown(
            f"""
            <div class="status-card">
                <div class="small-status">
                    <strong>스토리 진행 상태</strong><br>
                    호감도: {affection}/100<br>
                    단계: {STAGE_META[stage]["label"]}<br>
                    현재 챕터 목표 호감도: {current_rule['threshold']}<br>
                    현재 장면: {story['scene_index'] + 1} / {len(ABIGAIL_STORY[story['chapter_index']]['scenes']) if not story['completed'] else len(ABIGAIL_STORY[story['chapter_index']]['scenes'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(affection / 100)

        if st.button("아비게일 스토리 초기화", use_container_width=True):
            reset_story_mode()
            st.rerun()

    with right:
        st.markdown('<div class="chat-header"><strong>스토리 모드: 아비게일</strong></div>', unsafe_allow_html=True)
        render_story_progress()
        render_story_log()

        if story["completed"]:
            st.markdown(
                f"""
                <div class="event-box">
                    <strong>엔딩</strong><br>
                    {story["ending"]}<br><br>
                    최종 호감도: {affection}/100
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="event-box">이제 자유 모드로 가면, 이 스토리에서 쌓인 관계를 반영한 아비게일과 대화할 수 있어.</div>', unsafe_allow_html=True)
            return

        chapter = ABIGAIL_STORY[story["chapter_index"]]
        scene = chapter["scenes"][story["scene_index"]]
        scene_for_prompt = {"chapter": chapter["chapter"], "title": scene["title"], "location": scene["location"], "setup": scene["setup"]}
        threshold = ABIGAIL_CHAPTER_RULES[story["chapter_index"]]["threshold"]
        remaining = len(chapter["scenes"]) - (story["scene_index"] + 1)

        st.markdown(
            f"""
            <div class="story-card">
                <strong>{chapter["chapter"]}</strong><br>
                <span class="tip">{chapter["summary"]}</span><br><br>
                <strong>이번 챕터 목표</strong><br>
                <span class="tip">남은 장면 포함 호감도 {threshold} 이상 달성</span><br><br>
                <strong>현재 선택 장면</strong><br>
                <span class="tip">{scene["title"]} · {scene["location"]}</span><br>
                <span class="tip">이 장면 뒤 남은 질문 수: {remaining}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="choice-box"><strong>선택지</strong><br><span class="tip">좋은 선택의 위치는 장면마다 섞인다.</span></div>', unsafe_allow_html=True)
        displayed_choices = get_scene_choices(story["chapter_index"], story["scene_index"])
        for idx, choice in enumerate(displayed_choices):
            key = f"story_choice_{story['chapter_index']}_{story['scene_index']}_{idx}"
            if st.button(choice["label"], key=key, use_container_width=True):
                apply_story_choice(scene_for_prompt, choice)
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

        if char_name == ABIGAIL_NAME:
            story = st.session_state.story_state[ABIGAIL_STORY_KEY]
            story_note = story["ending"] if story["ending"] else "아직 스토리 모드 엔딩 전"
            st.markdown(
                f"""
                <div class="story-card">
                    <strong>스토리 모드 반영</strong><br>
                    <span class="tip">{story_note}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="chat-header"><strong>자유 모드</strong></div>', unsafe_allow_html=True)
        if not messages:
            st.markdown('<div class="event-box">자유롭게 질문해도 되고 감정을 털어놔도 돼. 스토리 모드에서 쌓인 관계가 말투와 태도에 반영된다.</div>', unsafe_allow_html=True)

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
                    reply = "지금은 OpenAI API 키가 연결되지 않아 대화를 이어갈 수 없어."
                else:
                    system_prompt = build_system_prompt(char_name, new_affection, st.session_state.memory[char_name], st.session_state.player_name)
                    with st.spinner(f"{char_name} 답변 생성 중..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4.1-mini",
                                temperature=0.7,
                                max_tokens=280,
                                messages=[{"role": "system", "content": system_prompt}, *messages[-12:]],
                            )
                            reply = response.choices[0].message.content or "..."
                        except Exception as exc:
                            reply = f"오류가 발생했어: {exc}"

                messages.append({"role": "assistant", "content": reply})
                st.rerun()


ensure_state()

st.markdown(
    """
<div class="top-title">
    <h1>🎭 시련 인터랙션</h1>
    <p>스토리 모드로 아비게일의 운명을 바꾸고, 자유 모드에서 달라진 관계의 캐릭터와 대화해봐.</p>
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
        st.warning('`st.secrets["OPENAI_API_KEY"]`가 필요해.')

    st.markdown("---")
    char_name = st.selectbox("캐릭터 선택", list(CHARACTERS.keys()))
    ensure_character_state(char_name)

    mode_options = ["자유 모드"]
    if char_name == ABIGAIL_NAME:
        mode_options = ["스토리 모드", "자유 모드"]
    mode = st.radio("플레이 모드", mode_options)

    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)

    st.markdown(f'<div class="side-card"><strong>{char_name}</strong><br><span class="tip">{CHARACTERS[char_name]["brief"]}</span></div>', unsafe_allow_html=True)
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
        st.markdown(f'<div class="side-card"><strong>플레이어 이름</strong><br><span class="tip">{st.session_state.player_name}</span></div>', unsafe_allow_html=True)

    if char_name == ABIGAIL_NAME:
        story = st.session_state.story_state[ABIGAIL_STORY_KEY]
        chapter_text = "완료" if story["completed"] else f"{story['chapter_index'] + 1} / {len(ABIGAIL_STORY)}"
        current_goal = ABIGAIL_CHAPTER_RULES[min(story["chapter_index"], len(ABIGAIL_CHAPTER_RULES) - 1)]["threshold"]
        st.markdown(
            f"""
            <div class="side-card">
                <strong>아비게일 스토리 진행</strong><br>
                <span class="tip">챕터: {chapter_text}</span><br>
                <span class="tip">현재 챕터 목표 호감도: {current_goal}</span><br>
                <span class="tip">누적 선택: {len(story["history"])}회</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if mode == "자유 모드":
        if st.button("현재 캐릭터 자유 대화 초기화", use_container_width=True):
            st.session_state.messages[char_name] = []
            st.session_state.memory[char_name] = []
            st.session_state.name_event_done[char_name] = False
            st.session_state.awaiting_name_input[char_name] = False
            if char_name != ABIGAIL_NAME:
                st.session_state.affection[char_name] = 0
            st.rerun()


if char_name == ABIGAIL_NAME and mode == "스토리 모드":
    handle_story_mode()
else:
    handle_free_mode(char_name)
