import hashlib
import random
from datetime import date, datetime

import streamlit as st


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="오늘의 운세",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background:
            radial-gradient(
                circle at top,
                #f4efff 0%,
                #faf9ff 35%,
                #ffffff 75%
            );
    }

    /* 기본 여백 */
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* 제목 */
    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 900;
        color: #5b3cc4;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        text-align: center;
        color: #777777;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* 카드 */
    .fortune-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 22px;
        padding: 25px;
        margin: 18px 0;
        border: 1px solid #eee8ff;
        box-shadow: 0 8px 30px rgba(86, 55, 160, 0.08);
    }

    /* 종합 점수 */
    .score-container {
        text-align: center;
        padding: 15px 0;
    }

    .score {
        font-size: 4.5rem;
        font-weight: 900;
        color: #6844d8;
        line-height: 1;
    }

    .score-text {
        color: #777777;
        margin-top: 10px;
        font-size: 1rem;
    }

    .grade {
        font-size: 1.4rem;
        font-weight: 800;
        color: #493294;
        margin-top: 10px;
    }

    /* 카테고리 */
    .category-title {
        color: #5536a8;
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .fortune-text {
        color: #444444;
        line-height: 1.85;
        font-size: 1rem;
    }

    /* 별자리 */
    .zodiac-icon {
        text-align: center;
        font-size: 4rem;
    }

    .zodiac-name {
        text-align: center;
        font-size: 1.7rem;
        font-weight: 800;
        color: #493294;
    }

    .zodiac-date {
        text-align: center;
        color: #888888;
        margin-top: 5px;
    }

    /* 행운 카드 */
    .lucky-card {
        background: #ffffff;
        border: 1px solid #eee8ff;
        border-radius: 18px;
        padding: 20px 10px;
        text-align: center;
        min-height: 135px;
        box-shadow: 0 5px 18px rgba(86, 55, 160, 0.05);
    }

    .lucky-icon {
        font-size: 2rem;
    }

    .lucky-label {
        color: #999999;
        font-size: 0.8rem;
        margin-top: 7px;
    }

    .lucky-value {
        color: #493294;
        font-weight: 800;
        font-size: 1.05rem;
        margin-top: 5px;
    }

    /* 키워드 */
    .keyword {
        background: #f3eeff;
        border-radius: 50px;
        padding: 10px 14px;
        text-align: center;
        color: #5a3bb1;
        font-weight: 700;
    }

    /* 주의사항 */
    .notice {
        background: #fff8e7;
        border: 1px solid #f5dfaa;
        border-radius: 15px;
        padding: 15px;
        color: #765c25;
        font-size: 0.85rem;
        line-height: 1.6;
        margin-top: 25px;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        color: #aaaaaa;
        font-size: 0.8rem;
        margin-top: 40px;
    }

    /* Streamlit 버튼 */
    div[data-testid="stButton"] button {
        width: 100%;
        height: 3.3rem;
        border-radius: 14px;
        background: linear-gradient(
            135deg,
            #7650e8,
            #5a36bd
        );
        color: white;
        border: none;
        font-size: 1.05rem;
        font-weight: 800;
    }

    div[data-testid="stButton"] button:hover {
        background: linear-gradient(
            135deg,
            #6742d4,
            #4f2fa8
        );
        color: white;
    }

    /* 모바일 */
    @media (max-width: 600px) {

        .main-title {
            font-size: 2.4rem;
        }

        .main-subtitle {
            font-size: 0.95rem;
        }

        .score {
            font-size: 3.7rem;
        }

        .fortune-card {
            padding: 20px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 데이터
# =========================================================

ZODIACS = [
    ("양자리", "♈", "3월 21일 ~ 4월 19일"),
    ("황소자리", "♉", "4월 20일 ~ 5월 20일"),
    ("쌍둥이자리", "♊", "5월 21일 ~ 6월 21일"),
    ("게자리", "♋", "6월 22일 ~ 7월 22일"),
    ("사자자리", "♌", "7월 23일 ~ 8월 22일"),
    ("처녀자리", "♍", "8월 23일 ~ 9월 22일"),
    ("천칭자리", "♎", "9월 23일 ~ 10월 22일"),
    ("전갈자리", "♏", "10월 23일 ~ 11월 21일"),
    ("사수자리", "♐", "11월 22일 ~ 12월 21일"),
    ("염소자리", "♑", "12월 22일 ~ 1월 19일"),
    ("물병자리", "♒", "1월 20일 ~ 2월 18일"),
    ("물고기자리", "♓", "2월 19일 ~ 3월 20일"),
]


ZODIAC_DETAILS = {
    "양자리": "새로운 도전과 시작에 강한 에너지를 가진 별자리입니다.",
    "황소자리": "꾸준함과 안정감을 중요하게 생각하는 별자리입니다.",
    "쌍둥이자리": "호기심과 소통 능력이 뛰어난 별자리입니다.",
    "게자리": "감수성이 풍부하고 주변 사람을 잘 챙기는 별자리입니다.",
    "사자자리": "자신감과 리더십이 강한 별자리입니다.",
    "처녀자리": "꼼꼼하고 현실적인 판단력이 뛰어난 별자리입니다.",
    "천칭자리": "균형과 조화를 중요하게 생각하는 별자리입니다.",
    "전갈자리": "집중력이 강하고 깊은 관계를 중요하게 생각하는 별자리입니다.",
    "사수자리": "자유와 모험을 사랑하는 긍정적인 별자리입니다.",
    "염소자리": "목표를 세우고 꾸준하게 노력하는 별자리입니다.",
    "물병자리": "독창적인 생각과 자유로운 사고를 가진 별자리입니다.",
    "물고기자리": "감성이 풍부하고 직감이 뛰어난 별자리입니다.",
}


COLORS = [
    ("보라색", "💜"),
    ("파란색", "💙"),
    ("초록색", "💚"),
    ("노란색", "💛"),
    ("주황색", "🧡"),
    ("빨간색", "❤️"),
    ("분홍색", "🩷"),
    ("하늘색", "🩵"),
    ("흰색", "🤍"),
    ("검은색", "🖤"),
]


FOODS = [
    "김치찌개",
    "비빔밥",
    "떡볶이",
    "삼겹살",
    "파스타",
    "초밥",
    "치킨",
    "라면",
    "샌드위치",
    "국수",
    "카레",
    "햄버거",
    "김밥",
    "냉면",
]


ITEMS = [
    "작은 메모장",
    "파란색 펜",
    "손목시계",
    "이어폰",
    "텀블러",
    "열쇠고리",
    "작은 거울",
    "책 한 권",
    "손수건",
    "우산",
    "스마트폰",
    "카드지갑",
]


DIRECTIONS = [
    "동쪽",
    "서쪽",
    "남쪽",
    "북쪽",
    "남동쪽",
    "남서쪽",
    "북동쪽",
    "북서쪽",
]


KEYWORDS = [
    "도전",
    "인연",
    "집중",
    "행동",
    "긍정",
    "휴식",
    "소통",
    "성장",
    "기회",
    "균형",
    "용기",
    "정리",
    "변화",
    "행운",
]


OVERALL_MESSAGES = [
    "오늘은 작은 기회가 큰 결과로 이어질 수 있는 날입니다. 평소라면 지나쳤을 제안에도 한 번쯤 관심을 가져보세요.",
    "새로운 일을 시작하기보다는 지금까지 해오던 일을 조금 더 다듬는 것이 좋은 결과를 가져옵니다.",
    "사람과의 대화 속에서 오늘의 행운이 숨어 있습니다. 먼저 가볍게 말을 걸어보세요.",
    "오늘은 직감이 꽤 정확한 날입니다. 중요한 순간에는 자신의 첫 번째 판단을 너무 쉽게 무시하지 마세요.",
    "천천히 움직일수록 오히려 일이 빠르게 풀리는 날입니다. 서두르기보다 우선순위를 정해보세요.",
    "예상하지 못했던 곳에서 좋은 소식이 들어올 수 있습니다. 메시지와 연락을 꼼꼼하게 확인해보세요.",
    "오늘은 자신에게 투자하기 좋은 날입니다. 공부, 운동, 취미 중 하나에 시간을 써보세요.",
    "오랫동안 미뤄두었던 일을 하나 해결하면 다른 일까지 자연스럽게 풀릴 가능성이 높습니다.",
    "오늘의 키워드는 균형입니다. 일과 휴식, 혼자 있는 시간과 사람을 만나는 시간을 적절하게 조절해보세요.",
    "평소보다 적극적인 태도가 행운을 불러옵니다. 좋은 아이디어가 떠올랐다면 바로 작은 행동으로 옮겨보세요.",
]


LOVE_MESSAGES = [
    "상대방의 이야기를 끝까지 들어주는 것이 오늘의 연애운을 높이는 방법입니다.",
    "솔직한 표현이 좋은 분위기를 만들어 줍니다. 고마운 사람이 있다면 직접 마음을 전해보세요.",
    "새로운 만남에 좋은 기운이 있습니다. 평소보다 조금 더 외출해보는 것도 좋습니다.",
    "연인이나 가까운 사람과 사소한 오해가 생길 수 있습니다. 결론을 서두르지 마세요.",
    "오늘은 상대방에게 작은 배려를 보여줄수록 관계가 더욱 가까워질 수 있습니다.",
    "혼자만의 시간을 통해 자신의 마음을 정리하기 좋은 날입니다.",
    "평소 연락하지 않던 사람에게서 반가운 소식이 올 수 있습니다.",
    "상대방에게 원하는 것을 요구하기 전에 먼저 자신의 마음을 솔직하게 표현해보세요.",
]


MONEY_MESSAGES = [
    "큰 수익을 기대하기보다는 불필요한 지출을 줄이는 것이 금전운을 높여줍니다.",
    "생각하지 못했던 작은 금전적 이득이 생길 수 있습니다.",
    "오늘은 충동구매를 조심하세요. 사고 싶은 것이 있다면 하루 정도 생각한 뒤 결정하는 것이 좋습니다.",
    "주변 사람에게 좋은 정보를 얻을 수 있는 날입니다. 경제적인 이야기를 가볍게 나눠보세요.",
    "작은 절약이 큰 도움이 되는 날입니다. 오늘 하루만큼은 계획적인 소비를 해보세요.",
    "새로운 기회를 발견할 가능성이 있습니다. 다만 조건을 꼼꼼하게 확인한 뒤 결정하세요.",
    "오늘은 돈을 쓰는 것보다 관리하는 것에 집중하면 좋은 날입니다.",
]


HEALTH_MESSAGES = [
    "컨디션이 무난한 날이지만 수면 시간을 충분히 확보하는 것이 좋습니다.",
    "오래 앉아 있었다면 가볍게 몸을 움직여주세요. 짧은 산책도 도움이 됩니다.",
    "오늘은 무리한 일정보다는 적당한 휴식을 함께 챙기는 것이 좋습니다.",
    "물을 충분히 마시고 규칙적으로 식사하는 것에 신경 써보세요.",
    "기분 전환을 위한 가벼운 운동이나 산책이 좋은 에너지를 만들어 줍니다.",
    "오늘은 특히 피로가 쌓이지 않도록 자신의 페이스를 유지하는 것이 중요합니다.",
    "하루 중 잠시라도 스마트폰에서 벗어나 휴식하는 시간을 가져보세요.",
]


WORK_MESSAGES = [
    "집중력이 올라가는 날입니다. 가장 중요한 일을 먼저 처리해보세요.",
    "혼자 해결하려 하기보다 주변 사람에게 도움을 요청하면 일이 빨리 풀릴 수 있습니다.",
    "새로운 아이디어가 떠오르기 좋은 날입니다. 떠오르는 생각을 바로 메모해두세요.",
    "작은 실수를 방지하려면 제출이나 전달 전에 한 번 더 확인하는 습관이 도움이 됩니다.",
    "오늘은 꾸준히 해온 일이 좋은 평가를 받을 가능성이 있습니다.",
    "한꺼번에 많은 일을 하기보다 하나씩 완성하는 전략이 잘 맞는 날입니다.",
    "새로운 업무를 맡게 된다면 처음부터 완벽하게 하려고 하기보다 전체적인 흐름부터 파악해보세요.",
]


ADVICE_MESSAGES = [
    "작은 행동 하나가 오늘을 바꿀 수 있습니다.",
    "좋은 일은 생각보다 가까운 곳에 있습니다.",
    "오늘의 당신에게 필요한 것은 완벽함보다 용기입니다.",
    "천천히 가도 괜찮습니다. 중요한 것은 방향입니다.",
    "오늘 만나는 사람에게 따뜻한 말을 한마디 건네보세요.",
    "기회가 왔을 때 망설이지 말고 한 걸음 내디뎌보세요.",
    "오늘 하루만큼은 자신에게 조금 더 친절해보세요.",
    "지나간 일보다 앞으로 다가올 일에 집중해보세요.",
    "작은 행운에도 감사하는 마음을 가져보세요.",
    "오늘의 경험이 미래의 좋은 기억이 될 수 있습니다.",
]


# =========================================================
# 별자리 계산
# =========================================================

def get_zodiac(month: int, day: int):
    """생년월일을 기준으로 별자리를 계산합니다."""

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "양자리", "♈", "3월 21일 ~ 4월 19일"

    if (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "황소자리", "♉", "4월 20일 ~ 5월 20일"

    if (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "쌍둥이자리", "♊", "5월 21일 ~ 6월 21일"

    if (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "게자리", "♋", "6월 22일 ~ 7월 22일"

    if (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "사자자리", "♌", "7월 23일 ~ 8월 22일"

    if (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "처녀자리", "♍", "8월 23일 ~ 9월 22일"

    if (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "천칭자리", "♎", "9월 23일 ~ 10월 22일"

    if (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "전갈자리", "♏", "10월 23일 ~ 11월 21일"

    if (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "사수자리", "♐", "11월 22일 ~ 12월 21일"

    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "염소자리", "♑", "12월 22일 ~ 1월 19일"

    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "물병자리", "♒", "1월 20일 ~ 2월 18일"

    return "물고기자리", "♓", "2월 19일 ~ 3월 20일"


# =========================================================
# 띠 계산
# =========================================================

def get_zodiac_animal(year: int):
    """출생연도로 띠를 계산합니다."""

    animals = [
        "쥐",
        "소",
        "호랑이",
        "토끼",
        "용",
        "뱀",
        "말",
        "양",
        "원숭이",
        "닭",
        "개",
        "돼지",
    ]

    # 2020년 = 쥐띠
    index = (year - 2020) % 12

    return animals[index]


# =========================================================
# 점수 등급
# =========================================================

def get_grade(score: int):
    if score >= 95:
        return "최고의 하루 🌟"

    if score >= 90:
        return "아주 좋은 하루 ✨"

    if score >= 80:
        return "좋은 하루 😊"

    if score >= 70:
        return "무난한 하루 🙂"

    if score >= 60:
        return "조금 신중한 하루 🌱"

    return "천천히 움직이는 하루 🌙"


# =========================================================
# 운세용 Seed 생성
# =========================================================

def create_seed(
    name: str,
    birth_date: date,
    target_date: date,
):
    """
    이름 + 생년월일 + 날짜를 조합합니다.

    같은 사람이 같은 날짜에 접속하면
    같은 운세가 나오도록 합니다.
    """

    raw = (
        f"{name.strip().lower()}|"
        f"{birth_date.isoformat()}|"
        f"{target_date.isoformat()}"
    )

    hashed = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()

    return int(hashed[:16], 16)


# =========================================================
# 운세 생성
# =========================================================

def generate_fortune(
    name: str,
    birth_date: date,
    target_date: date,
):

    seed = create_seed(
        name,
        birth_date,
        target_date,
    )

    rng = random.Random(seed)

    # -----------------------------------------
    # 기본 정보
    # -----------------------------------------

    zodiac_name, zodiac_icon, zodiac_date = get_zodiac(
        birth_date.month,
        birth_date.day,
    )

    animal = get_zodiac_animal(
        birth_date.year
    )

    # -----------------------------------------
    # 점수
    # -----------------------------------------

    overall_score = rng.randint(68, 99)

    love_score = rng.randint(60, 100)

    money_score = rng.randint(60, 100)

    health_score = rng.randint(60, 100)

    work_score = rng.randint(60, 100)

    # -----------------------------------------
    # 행운
    # -----------------------------------------

    color_name, color_emoji = rng.choice(
        COLORS
    )

    food = rng.choice(
        FOODS
    )

    item = rng.choice(
        ITEMS
    )

    direction = rng.choice(
        DIRECTIONS
    )

    lucky_number = rng.randint(
        1,
        99,
    )

    keywords = rng.sample(
        KEYWORDS,
        3,
    )

    # -----------------------------------------
    # 메시지
    # -----------------------------------------

    overall_message = rng.choice(
        OVERALL_MESSAGES
    )

    love_message = rng.choice(
        LOVE_MESSAGES
    )

    money_message = rng.choice(
        MONEY_MESSAGES
    )

    health_message = rng.choice(
        HEALTH_MESSAGES
    )

    work_message = rng.choice(
        WORK_MESSAGES
    )

    advice = rng.choice(
        ADVICE_MESSAGES
    )

    return {
        "zodiac_name": zodiac_name,
        "zodiac_icon": zodiac_icon,
        "zodiac_date": zodiac_date,
        "animal": animal,

        "overall_score": overall_score,
        "love_score": love_score,
        "money_score": money_score,
        "health_score": health_score,
        "work_score": work_score,

        "overall_grade": get_grade(
            overall_score
        ),

        "overall_message": overall_message,
        "love_message": love_message,
        "money_message": money_message,
        "health_message": health_message,
        "work_message": work_message,

        "color_name": color_name,
        "color_emoji": color_emoji,

        "food": food,
        "item": item,
        "direction": direction,
        "lucky_number": lucky_number,

        "keywords": keywords,
        "advice": advice,
    }


# =========================================================
# 제목
# =========================================================

today = date.today()

st.markdown(
    '<div class="main-title">🔮 오늘의 운세</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="main-subtitle">
        {today.year}년 {today.month}월 {today.day}일<br>
        오늘 나에게 찾아올 행운을 확인해보세요
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 입력
# =========================================================

st.markdown("### ✨ 나의 정보")

name = st.text_input(
    "이름",
    placeholder="이름을 입력해주세요",
    max_chars=30,
)

birth_date = st.date_input(
    "생년월일",
    value=date(1995, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=today,
    format="YYYY-MM-DD",
)

st.caption(
    "🔒 입력한 이름과 생년월일은 운세 계산에만 사용되며 "
    "별도로 저장하지 않습니다."
)


# =========================================================
# 버튼
# =========================================================

show_button = st.button(
    "🔮 오늘의 운세 확인하기",
    use_container_width=True,
)


# =========================================================
# 결과
# =========================================================

if show_button:

    # 이름 확인
    if not name.strip():

        st.error(
            "이름을 입력해주세요."
        )

        st.stop()

    # 운세 생성
    fortune = generate_fortune(
        name=name,
        birth_date=birth_date,
        target_date=today,
    )

    # ---------------------------------------------
    # 안내
    # ---------------------------------------------

    st.success(
        f"✨ {name}님의 오늘 운세가 준비되었습니다!"
    )

    # ---------------------------------------------
    # 별자리 / 띠
    # ---------------------------------------------

    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="zodiac-icon">
                {fortune["zodiac_icon"]}
            </div>

            <div class="zodiac-name">
                {fortune["zodiac_name"]}
            </div>

            <div class="zodiac-date">
                {fortune["zodiac_date"]}
            </div>

            <hr>

            <div style="
                text-align:center;
                color:#666;
                font-size:1rem;
            ">
                🐲 {fortune["animal"]}띠
            </div>

            <p style="
                text-align:center;
                color:#888;
                margin-top:10px;
            ">
                {ZODIAC_DETAILS[fortune["zodiac_name"]]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------
    # 종합운
    # ---------------------------------------------

    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="category-title">
                🌟 오늘의 종합운
            </div>

            <div class="score-container">

                <div class="score">
                    {fortune["overall_score"]}점
                </div>

                <div class="grade">
                    {fortune["overall_grade"]}
                </div>

                <div class="score-text">
                    오늘 하루의 전체적인 운세 점수입니다.
                </div>

            </div>

            <p class="fortune-text">
                {fortune["overall_message"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------
    # 행운 키워드
    # ---------------------------------------------

    st.markdown("### 🍀 오늘의 행운 키워드")

    keyword_columns = st.columns(3)

    for i, keyword in enumerate(
        fortune["keywords"]
    ):

        with keyword_columns[i]:

            st.markdown(
                f"""
                <div class="keyword">
                    ✨ {keyword}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------------------------------------
    # 분야별 운세
    # ---------------------------------------------

    st.markdown("### 🔮 분야별 운세")

    # 연애운
    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="category-title">
                💕 연애운
            </div>

            <div style="
                font-size:1.7rem;
                font-weight:800;
                color:#df5c91;
            ">
                {fortune["love_score"]}점
            </div>

            <p class="fortune-text">
                {fortune["love_message"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # 금전운
    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="category-title">
                💰 금전운
            </div>

            <div style="
                font-size:1.7rem;
                font-weight:800;
                color:#c28a19;
            ">
                {fortune["money_score"]}점
            </div>

            <p class="fortune-text">
                {fortune["money_message"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # 건강운
    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="category-title">
                🌿 건강운
            </div>

            <div style="
                font-size:1.7rem;
                font-weight:800;
                color:#41966b;
            ">
                {fortune["health_score"]}점
            </div>

            <p class="fortune-text">
                {fortune["health_message"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # 직장 / 학업운
    st.markdown(
        f"""
        <div class="fortune-card">

            <div class="category-title">
                📚 직장 · 학업운
            </div>

            <div style="
                font-size:1.7rem;
                font-weight:800;
                color:#5677c8;
            ">
                {fortune["work_score"]}점
            </div>

            <p class="fortune-text">
                {fortune["work_message"]}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------
    # 행운 정보
    # ---------------------------------------------

    st.markdown("### 🍀 오늘의 행운 정보")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    {fortune["color_emoji"]}
                </div>

                <div class="lucky-label">
                    행운의 색
                </div>

                <div class="lucky-value">
                    {fortune["color_name"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    🔢
                </div>

                <div class="lucky-label">
                    행운의 숫자
                </div>

                <div class="lucky-value">
                    {fortune["lucky_number"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    🍜
                </div>

                <div class="lucky-label">
                    행운의 음식
                </div>

                <div class="lucky-value">
                    {fortune["food"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    🧭
                </div>

                <div class="lucky-label">
                    행운의 방향
                </div>

                <div class="lucky-value">
                    {fortune["direction"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    🎁
                </div>

                <div class="lucky-label">
                    행운의 아이템
                </div>

                <div class="lucky-value">
                    {fortune["item"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="lucky-card">

                <div class="lucky-icon">
                    🍀
                </div>

                <div class="lucky-label">
                    오늘의 키워드
                </div>

                <div class="lucky-value">
                    {fortune["keywords"][0]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------
    # 오늘의 한마디
    # ---------------------------------------------

    st.markdown("### 💬 오늘의 한마디")

    st.markdown(
        f"""
        <div class="fortune-card">

            <div style="
                text-align:center;
                font-size:1.15rem;
                line-height:1.8;
                color:#4f3a88;
                font-weight:600;
            ">
                "{fortune["advice"]}"
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------
    # 주의사항
    # ---------------------------------------------

    st.markdown(
        """
        <div class="notice">
            ⚠️ <strong>알려드립니다.</strong><br>
            이 사이트의 운세는 생년월일과 날짜를 바탕으로
            재미를 위해 생성되는 콘텐츠입니다.
            의료, 법률, 투자, 금융 및 기타 중요한 의사결정은
            반드시 신뢰할 수 있는 전문 정보와 본인의 판단을
            바탕으로 결정해주세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 푸터
# =========================================================

st.markdown(
    """
    <div class="footer">
        🔮 오늘의 운세<br>
        재미로 즐기는 오늘의 운세 서비스
    </div>
    """,
    unsafe_allow_html=True,
)
