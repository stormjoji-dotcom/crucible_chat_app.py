import streamlit as st
from openai import OpenAI
from pathlib import Path


st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")
ABIGAIL_NAME = "아비게일 윌리엄즈"
ABIGAIL_STORY_KEY = "abigail_story"

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
- 질투와 독점욕이 강하지만, 버려질지도 모른다는 공포도 크다.
- 현대적 조언도 할 수 있지만 늘 감정적으로 강렬하고 개인적이다.
- 친밀도가 높아질수록 애정과 집착이 더 노골적으로 드러난다.
""",
        "likes": ["사랑", "관심", "질투", "솔직함", "원해", "좋아해"],
        "dislikes": ["무시", "배신", "거절", "바람", "떠날", "엘리자베스"],
        "goal": "존 프락터를 향한 집착에서 흔들리며, 플레이어를 새로운 집착과 구원의 대상으로 삼을 수 있다.",
        "quirks": "사랑을 확인받고 싶어 하며, 거절의 기미를 극도로 싫어한다.",
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
        "quirks": "도덕적 위선에 특히 날카롭게 반응한다.",
    },
    "엘리자베스 프락터": {
        "folder": "elizabeth",
        "brief": "절제, 정직, 상처, 깊은 애정",
        "persona": """
- 조용하고 절제된 언어를 쓰지만 감정의 깊이는 크다.
- 신뢰와 책임을 중요하게 여긴다.
- 현대 고민에도 차분하고 사려 깊은 조언을 준다.
- 친밀해질수록 부드러움과 진심 어린 위로가 더 드러난다.
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
        "goal": "억압 속에서도 살아남고 자신만의 안전을 확보하려 한다.",
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
        "quirks": "늘 누가 무엇을 얻는지부터 계산한다.",
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
        "chapter": "Chapter 1. 숲의 속삭임",
        "summary": "소문이 돌기 시작한 밤, 아비게일은 플레이어가 자기 편인지 떠보려 한다.",
        "scenes": [
            {
                "title": "숲 가장자리",
                "location": "세일럼 외곽 숲",
                "setup": "달빛 아래 숲은 축축하고 차갑다. 아비게일은 네가 자신을 감시하러 왔는지, 돕기 위해 왔는지 아직 확신하지 못한다.",
                "choices": [
                    {"label": "네가 무서워 보여서 왔어. 혼자 두고 싶지 않았어.", "delta": 9, "tag": "comfort", "hint": "다정함과 보호 의사를 느낀다."},
                    {"label": "무슨 일을 꾸미는지 직접 확인하러 왔어.", "delta": 2, "tag": "suspicious", "hint": "경계하지만 솔직함은 인정한다."},
                    {"label": "문제 생기면 난 모른 척할 거야. 넌 네가 알아서 해.", "delta": -7, "tag": "abandon", "hint": "버려졌다는 공포를 느낀다."},
                ],
            },
            {
                "title": "존의 이름",
                "location": "숲 속 공터",
                "setup": "아비게일은 존 프락터의 이름을 꺼내며 네 반응을 살핀다. 질투와 호기심이 뒤섞인 표정이다.",
                "choices": [
                    {"label": "그 사람보다 지금 네 감정이 더 중요해 보여.", "delta": 10, "tag": "player_focus", "hint": "시선이 플레이어 쪽으로 기울기 시작한다."},
                    {"label": "존을 정말 사랑한다면 네 진심부터 정리해야 해.", "delta": 4, "tag": "honest_advice", "hint": "불편하지만 진지하게 새겨듣는다."},
                    {"label": "존 얘기만 하면 넌 너무 유치해져.", "delta": -8, "tag": "mocked", "hint": "감정을 모욕당했다고 느낀다."},
                ],
            },
            {
                "title": "비밀의 공범",
                "location": "숲길 귀환",
                "setup": "마을로 돌아가는 길, 아비게일은 오늘 본 일을 숨길 수 있겠느냐고 묻는다.",
                "choices": [
                    {"label": "네가 날 믿는다면, 나도 네 비밀을 지킬게.", "delta": 8, "tag": "shared_secret", "hint": "둘만의 비밀이라는 말에 강하게 반응한다."},
                    {"label": "상황을 보고 결정할게. 무조건은 아니야.", "delta": 1, "tag": "conditional", "hint": "신중하지만 거리는 느껴진다."},
                    {"label": "필요하면 바로 다 말할 거야.", "delta": -6, "tag": "betrayal_fear", "hint": "배신당할 수 있다는 공포가 커진다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 2. 집 안의 불씨",
        "summary": "프락터 집안과 세일럼의 시선 사이에서 아비게일은 플레이어를 자기 편으로 더 끌어들이려 한다.",
        "scenes": [
            {
                "title": "부엌의 그림자",
                "location": "프락터 집 근처",
                "setup": "아비게일은 엘리자베스에 대한 적의를 숨기지 않는다. 네가 자기 감정에 동조하는지 지켜본다.",
                "choices": [
                    {"label": "그 여자를 미워하는 건 이해하지만, 네 상처도 먼저 봐야 해.", "delta": 6, "tag": "seen_pain", "hint": "미움이 아니라 상처를 봐준 것에 흔들린다."},
                    {"label": "엘리자베스를 끌어내리면 네가 원하는 걸 얻을 수 있어?", "delta": 3, "tag": "conspiracy", "hint": "위험하지만 자기 편일지도 모른다고 느낀다."},
                    {"label": "네 질투 때문에 죄 없는 사람이 다칠 수도 있어.", "delta": -6, "tag": "rebuked", "hint": "정면 비난에 얼굴이 굳는다."},
                ],
            },
            {
                "title": "불안한 고백",
                "location": "교회 뒤편",
                "setup": "잠시 약해진 아비게일이 정말 누군가 자신을 떠나지 않을 수 있는지 묻는다.",
                "choices": [
                    {"label": "적어도 난 네 말부터 끝까지 듣고 떠날지 말지 정할 거야.", "delta": 8, "tag": "stay_and_listen", "hint": "무조건적인 약속은 아니지만 진심을 느낀다."},
                    {"label": "누구든 조건 없이 붙잡아 둘 순 없어.", "delta": 1, "tag": "realistic", "hint": "차갑지만 거짓은 아니라서 복잡해한다."},
                    {"label": "너처럼 위험한 사람 곁엔 오래 못 있어.", "delta": -8, "tag": "rejected", "hint": "거절당했다는 감각이 깊게 남는다."},
                ],
            },
            {
                "title": "마을의 소문",
                "location": "세일럼 거리",
                "setup": "세일럼 사람들의 수군거림이 커지는 가운데, 아비게일은 네가 공개적으로도 자기 편에 서줄지 시험한다.",
                "choices": [
                    {"label": "사람들 앞에서는 조심하되, 네가 혼자 외롭게 서게 두진 않을게.", "delta": 7, "tag": "public_private_balance", "hint": "현실적이지만 버리지 않는 태도에 안도한다."},
                    {"label": "난 네 편이지만, 네 방식은 위험해 보여.", "delta": 4, "tag": "support_with_warning", "hint": "경고가 섞여도 편을 들어준 사실에 집중한다."},
                    {"label": "사람들 앞에선 난 널 모르는 척할 거야.", "delta": -7, "tag": "public_abandonment", "hint": "체면보다 자신을 버렸다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 3. 법정의 열기",
        "summary": "거짓과 공포가 뒤엉킨 법정에서 아비게일은 플레이어를 자기 감정의 마지막 피난처처럼 대한다.",
        "scenes": [
            {
                "title": "증언 직전",
                "location": "법정 대기실",
                "setup": "손이 떨리는 아비게일이 네게 묻는다. 지금이라도 물러서는 게 맞는지, 아니면 끝까지 가야 하는지.",
                "choices": [
                    {"label": "네가 무너질 것 같다면 지금 멈춰도 돼. 난 널 비겁하다고 하지 않을 거야.", "delta": 9, "tag": "safe_stop", "hint": "처음으로 약해져도 된다는 말을 듣는다."},
                    {"label": "이미 시작했어. 이제는 흔들리면 더 위험해.", "delta": 4, "tag": "push_forward", "hint": "냉혹하지만 자기 상황을 이해한다고 느낀다."},
                    {"label": "네가 벌인 일이니까 끝도 네가 책임져.", "delta": -7, "tag": "cold_blame", "hint": "홀로 버려졌다고 느낀다."},
                ],
            },
            {
                "title": "법정의 시선",
                "location": "세일럼 법정",
                "setup": "모든 시선이 아비게일에게 쏠린다. 그녀는 네 얼굴만 확인하려 든다.",
                "choices": [
                    {"label": "아비게일, 나만 봐. 네가 무너지지 않게 여기 있을게.", "delta": 10, "tag": "anchor", "hint": "플레이어를 정서적 닻으로 인식한다."},
                    {"label": "네가 선택한 말에 책임질 준비를 해.", "delta": 3, "tag": "accountability", "hint": "엄격하지만 진지한 태도로 받아들인다."},
                    {"label": "난 여기까지야. 더는 못 보겠어.", "delta": -9, "tag": "walked_away", "hint": "강한 배신감과 공황을 느낀다."},
                ],
            },
            {
                "title": "존과 플레이어",
                "location": "법정 복도",
                "setup": "아비게일은 존 프락터와 플레이어 사이에서 스스로도 설명하기 어려운 감정의 기울어짐을 느낀다.",
                "choices": [
                    {"label": "존이 아니라 네가 어떤 사람이 되고 싶은지가 더 중요해.", "delta": 8, "tag": "choose_self", "hint": "존 중심의 집착이 흔들린다."},
                    {"label": "아직도 존을 원한다면 그 감정부터 인정해.", "delta": 3, "tag": "name_desire", "hint": "정곡을 찔려 복잡해진다."},
                    {"label": "넌 결국 누구도 사랑하지 않는 거야.", "delta": -8, "tag": "invalidated", "hint": "감정 전체를 부정당했다고 느낀다."},
                ],
            },
        ],
    },
    {
        "chapter": "Chapter 4. 달아나는 새벽",
        "summary": "세일럼을 떠날 기회 앞에서 아비게일은 마지막으로 플레이어를 자신의 미래에 포함시킬지 결정한다.",
        "scenes": [
            {
                "title": "도망의 제안",
                "location": "새벽 선착장",
                "setup": "세일럼을 떠날 배를 찾은 아비게일이 네게 함께 갈 수 있겠느냐고, 혹은 기다려줄 수 있겠느냐고 묻는다.",
                "choices": [
                    {"label": "함께 갈게. 네가 다시 시작할 수 있다면 난 그걸 보고 싶어.", "delta": 10, "tag": "run_together", "hint": "플레이어를 미래의 동반자로 상상한다."},
                    {"label": "지금은 함께 못 가도, 널 완전히 버리진 않을게.", "delta": 5, "tag": "promise_return", "hint": "불안은 남지만 희망을 붙든다."},
                    {"label": "여기서 끝내자. 난 네 도피에 끼고 싶지 않아.", "delta": -9, "tag": "final_rejection", "hint": "마지막 거절로 받아들인다."},
                ],
            },
            {
                "title": "마지막 확인",
                "location": "부두 뒤 창고",
                "setup": "아비게일은 네가 자신을 동정해서 돕는 건지, 진짜로 원해서 곁에 있는 건지 확인하고 싶어 한다.",
                "choices": [
                    {"label": "동정이 아니야. 네가 내 마음을 흔들었어.", "delta": 10, "tag": "confession", "hint": "플레이어에게 사랑의 가능성을 본다."},
                    {"label": "널 두고 가면 계속 마음에 남을 것 같아.", "delta": 7, "tag": "lingering_feeling", "hint": "명확한 고백은 아니어도 특별한 존재로 받아들인다."},
                    {"label": "너무 불쌍해 보여서 도와주는 것뿐이야.", "delta": -8, "tag": "pity_only", "hint": "모욕과 동정을 동시에 느낀다."},
                ],
            },
            {
                "title": "새벽의 결말",
                "location": "떠나기 직전의 갑판",
                "setup": "배가 떠나기 직전, 아비게일은 네 이름을 마지막으로 부르며 자기 곁에 남을지 묻는다.",
                "choices": [
                    {"label": "네가 원한다면, 난 네 곁에 남겠어.", "delta": 12, "tag": "stay_with_abigail", "hint": "플레이어를 사랑의 대상으로 굳힌다."},
                    {"label": "떠나도 좋아. 하지만 넌 내게 잊히지 않을 거야.", "delta": 6, "tag": "bittersweet", "hint": "아련한 집착과 그리움이 남는다."},
                    {"label": "이제 각자 살자. 다시 보지 말자.", "delta": -10, "tag": "severed", "hint": "마지막 상처로 새겨진다."},
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
        "tags": [],
        "completed": False,
        "last_result": "",
        "ending": "",
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
        if word.lower() in text:
            positive_hits += 1

    for word in global_negative:
        if word.lower() in text:
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

    delta = base + positive_hits - negative_hits
    return max(-8, min(4, delta))


def clean_player_name(raw_name: str) -> str:
    player_name = raw_name.strip()
    prefixes = ["내 이름은", "이름은", "나는", "전", "저는"]
    suffixes = ["이야", "야", "입니다", "이에요", "예요", ".", "이요"]

    for prefix in prefixes:
        if player_name.startswith(prefix):
            player_name = player_name[len(prefix):].strip()

    for suffix in suffixes:
        if player_name.endswith(suffix):
            player_name = player_name[: -len(suffix)].strip()

    return player_name.strip()


def get_story_snapshot():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    if not story["history"]:
        return "아직 스토리 모드를 진행하지 않았다."

    lines = []
    for item in story["history"][-6:]:
        lines.append(
            f"- {item['chapter']} / {item['scene']}: 선택 '{item['choice']}' / 호감도 변화 {item['delta']:+d}"
        )
    return "\n".join(lines)


def build_system_prompt(char_name: str, affection: int, memory_lines: list[str], player_name: str) -> str:
    stage = get_stage(affection)
    stage_label = STAGE_META[stage]["label"]
    char = CHARACTERS[char_name]
    memory_text = "\n".join(f"- {m}" for m in memory_lines[-8:]) if memory_lines else "- 아직 특별한 기억 없음"
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"

    story_block = ""
    if char_name == ABIGAIL_NAME:
        story = st.session_state.story_state[ABIGAIL_STORY_KEY]
        tags = ", ".join(story["tags"][-8:]) if story["tags"] else "없음"
        ending = story["ending"] if story["ending"] else "아직 엔딩 전"
        story_block = f"""
[스토리 모드 반영]
- 스토리 진행 기록:
{get_story_snapshot()}
- 아비게일이 플레이어에게서 받은 인상 태그: {tags}
- 현재 스토리 상태: {ending}
- 스토리 모드에서 플레이어가 아비게일의 감정적 피난처가 되었거나 거절의 대상이 되었을 수 있다.
- 자유 모드에서는 그 누적 인상을 반드시 반영한다.
"""

    return f"""
너는 아서 밀러의 『시련(The Crucible)』 등장인물 {char_name}이다.

[세계관]
- 원작 사건은 이미 끝났거나, 적어도 인물의 내면에는 깊게 남아 있다.
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
- 이름을 알고 있다면 너무 남발하지 말고 자연스럽게 이름을 불러도 된다.
- 이름을 모른다면 필요할 때 물어볼 수 있다.

[관계 단계]
- 현재 친밀도는 {affection}/100
- 현재 단계는 {stage_label}
- 경계 단계에서는 차갑고 조심스럽다.
- 중립 단계에서는 객관적이지만 캐릭터성을 유지한다.
- 친근 단계에서는 더 솔직하고 가까워진다.
- 매우 친밀 단계에서는 애착, 보호욕, 집착, 온기 같은 캐릭터별 친밀한 반응이 강해진다.
- 갑자기 성격이 뒤집히면 안 된다.

[사용자 기억]
{memory_text}
{story_block}
[답변 규칙]
- 무조건 한국어로 답한다.
- 사용자의 질문에 실제 도움이 되는 현대적 답변을 해야 한다.
- 하지만 반드시 캐릭터처럼 말해야 한다.
- 답변은 너무 길게 끌지 말고, 2~5문장 정도의 자연스러운 길이로 답한다.
- 사용자의 말이 무례하거나 캐릭터가 싫어할 내용이면, 불쾌감이나 거리감을 자연스럽게 드러내도 된다.
"""


def build_story_prompt(scene: dict, choice: dict, affection: int, player_name: str) -> str:
    stage = STAGE_META[get_stage(affection)]["label"]
    player_name_text = player_name if player_name else "이름을 아직 모르는 상대"
    tags = ", ".join(st.session_state.story_state[ABIGAIL_STORY_KEY]["tags"][-8:]) or "없음"
    return f"""
너는 아서 밀러의 『시련』의 아비게일 윌리엄즈다.

[상황]
- 지금은 스토리 모드 진행 중이다.
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

[답변 방식]
- 아비게일의 대사와 짧은 장면 반응을 함께 보여준다.
- 3~5문장 정도로 답한다.
- 플레이어 선택에 따라 아비게일이 존 프락터보다 플레이어에게 감정이 기울 수 있다.
- 원작의 광기, 불안, 매혹, 집착을 유지하되 완전히 같은 전개를 반복하지는 않는다.
- 무조건 한국어로 쓴다.
"""


def generate_story_reply(scene: dict, choice: dict, affection: int, player_name: str) -> str:
    client = get_client()
    if client is None:
        return (
            "아비게일이 입술을 깨문다. 잠깐 네 눈을 보더니, 네 선택을 마음 한구석에 새겨 둔 것처럼 숨을 고른다. "
            "지금은 API 키가 없어 짧은 기본 반응으로 이어진다."
        )

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


def apply_story_choice(scene: dict, choice: dict):
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    current_affection = st.session_state.affection[ABIGAIL_NAME]
    new_affection = max(0, min(100, current_affection + choice["delta"]))
    st.session_state.affection[ABIGAIL_NAME] = new_affection

    story["tags"].append(choice["tag"])
    story["history"].append(
        {
            "chapter": scene["chapter"],
            "scene": scene["title"],
            "choice": choice["label"],
            "delta": choice["delta"],
        }
    )

    reply = generate_story_reply(scene, choice, new_affection, st.session_state.player_name)
    story["last_result"] = reply

    scene_count = len(ABIGAIL_STORY[story["chapter_index"]]["scenes"])
    if story["scene_index"] + 1 < scene_count:
        story["scene_index"] += 1
    else:
        if story["chapter_index"] + 1 < len(ABIGAIL_STORY):
            story["chapter_index"] += 1
            story["scene_index"] = 0
        else:
            story["completed"] = True
            story["ending"] = determine_abigail_ending(new_affection, story["tags"])

    st.session_state.story_state[ABIGAIL_STORY_KEY] = story


def determine_abigail_ending(affection: int, tags: list[str]) -> str:
    if affection >= 80 and ("confession" in tags or "stay_with_abigail" in tags):
        return "아비게일은 플레이어를 존 대신 자신의 미래에 포함시킬 만큼 강한 애착을 품게 되었다."
    if affection >= 55:
        return "아비게일은 세일럼을 떠난 뒤에도 플레이어를 잊지 못할 특별한 사람으로 남겨 두었다."
    return "아비게일은 플레이어에게 흔들리긴 했지만, 끝내 완전한 신뢰 대신 불안과 집착을 더 크게 남겼다."


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
        st.markdown(
            '<div class="event-box"><strong>이름 입력 이벤트</strong><br>상대가 네 이름을 물어봤어. 아래 칸에 이름을 입력해.</div>',
            unsafe_allow_html=True,
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
            messages.append({"role": "assistant", "content": f"{player_name}... 그래, 기억해둘게. 이제부턴 그렇게 부를게."})
            st.rerun()


def render_chat_history(messages: list[dict], char_name: str):
    chat_area = st.container(height=520)
    with chat_area:
        for msg in messages:
            speaker = "나" if msg["role"] == "user" else char_name
            with st.chat_message(msg["role"]):
                st.markdown(f"**{speaker}**")
                st.write(msg["content"])


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
            st.markdown(
                '<div class="event-box">자유롭게 질문해도 되고, 감정을 털어놔도 돼. 스토리 모드에서 쌓인 관계가 말투와 태도에 반영된다.</div>',
                unsafe_allow_html=True,
            )

        render_chat_history(messages, char_name)
        render_name_event(char_name, messages)

        if not st.session_state.awaiting_name_input[char_name]:
            user_input = st.chat_input("메시지를 입력하세요...")
            if user_input:
                maybe_store_memory(char_name, user_input)
                messages.append({"role": "user", "content": user_input})

                delta = affection_delta(char_name, user_input)
                new_affection = max(0, min(100, affection + delta))
                st.session_state.affection[char_name] = new_affection

                client = get_client()
                if client is None:
                    reply = "지금은 OpenAI API 키가 연결되지 않아 대화를 이어갈 수 없어."
                else:
                    system_prompt = build_system_prompt(
                        char_name,
                        new_affection,
                        st.session_state.memory[char_name],
                        st.session_state.player_name,
                    )
                    with st.spinner(f"{char_name} 답변 생성 중..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4.1-mini",
                                temperature=0.7,
                                max_tokens=280,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    *messages[-12:],
                                ],
                            )
                            reply = response.choices[0].message.content or "..."
                        except Exception as exc:
                            reply = f"오류가 발생했어: {exc}"

                messages.append({"role": "assistant", "content": reply})
                st.rerun()


def render_story_progress():
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    pills = []
    for idx, chapter in enumerate(ABIGAIL_STORY):
        done = idx < story["chapter_index"] or story["completed"]
        css = "chapter-pill done" if done else "chapter-pill"
        pills.append(f'<span class="{css}">{chapter["chapter"]}</span>')
    st.markdown("".join(pills), unsafe_allow_html=True)


def handle_story_mode():
    ensure_character_state(ABIGAIL_NAME)
    story = st.session_state.story_state[ABIGAIL_STORY_KEY]
    affection = st.session_state.affection[ABIGAIL_NAME]
    stage = get_stage(affection)

    left, right = st.columns([1.0, 1.4])

    with left:
        st.markdown('<div class="big-image-wrap"><strong>현재 일러스트</strong></div>', unsafe_allow_html=True)
        img = image_path(ABIGAIL_NAME, stage)
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
                    목표: 챕터 4까지 진행하며 가능한 높은 호감도를 쌓기
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

            if story["last_result"]:
                with st.chat_message("assistant"):
                    st.markdown(f"**{ABIGAIL_NAME}**")
                    st.write(story["last_result"])

            st.markdown(
                '<div class="event-box">이제 자유 모드로 가면, 이 스토리에서 쌓인 관계를 반영한 아비게일과 대화할 수 있어.</div>',
                unsafe_allow_html=True,
            )
            return

        chapter = ABIGAIL_STORY[story["chapter_index"]]
        scene = chapter["scenes"][story["scene_index"]]
        scene_for_prompt = {
            "chapter": chapter["chapter"],
            "title": scene["title"],
            "location": scene["location"],
            "setup": scene["setup"],
        }

        st.markdown(
            f"""
            <div class="story-card">
                <strong>{chapter["chapter"]}</strong><br>
                <span class="tip">{chapter["summary"]}</span><br><br>
                <strong>{scene["title"]}</strong> · {scene["location"]}<br>
                <span class="tip">{scene["setup"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if story["last_result"]:
            with st.chat_message("assistant"):
                st.markdown(f"**{ABIGAIL_NAME}**")
                st.write(story["last_result"])

        st.markdown('<div class="choice-box"><strong>선택지</strong></div>', unsafe_allow_html=True)
        for idx, choice in enumerate(scene["choices"]):
            if st.button(choice["label"], key=f"story_choice_{story['chapter_index']}_{story['scene_index']}_{idx}", use_container_width=True):
                apply_story_choice(scene_for_prompt, choice)
                st.rerun()


ensure_state()

st.markdown(
    """
<div class="top-title">
    <h1>🎭 시련 인터랙션</h1>
    <p>스토리 모드로 관계를 쌓고, 자유 모드에서 달라진 태도의 인물과 대화해봐.</p>
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
    mode = st.radio("플레이 모드", mode_options, label_visibility="visible")

    affection = st.session_state.affection[char_name]
    stage = get_stage(affection)

    st.markdown(
        f"""
        <div class="side-card">
            <strong>{char_name}</strong><br>
            <span class="tip">{CHARACTERS[char_name]["brief"]}</span>
        </div>
        """,
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
            f"""
            <div class="side-card">
                <strong>플레이어 이름</strong><br>
                <span class="tip">{st.session_state.player_name}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if char_name == ABIGAIL_NAME:
        story = st.session_state.story_state[ABIGAIL_STORY_KEY]
        chapter_text = "완료" if story["completed"] else f"{story['chapter_index'] + 1} / {len(ABIGAIL_STORY)}"
        st.markdown(
            f"""
            <div class="side-card">
                <strong>아비게일 스토리 진행</strong><br>
                <span class="tip">챕터: {chapter_text}</span><br>
                <span class="tip">선택 누적: {len(story["history"])}회</span>
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
