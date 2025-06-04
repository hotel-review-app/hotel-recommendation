import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(layout="centered", page_title="사용자 맞춤화 호텔 추천 시스템", page_icon="🏨")

# --- CSS 스타일 (배경색, 가운데 정렬, 폰트 크기 조정 등) ---
st.markdown("""
    <style>
    body {
        background-color: #f5f6fa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        text-align: center;
    }
    .stTextInput>div>div>input {
        font-size: 1.1rem;
        padding: 0.75rem;
        width: 500px;
        text-align: center;
    }
    .custom-caption {
        font-size: 14px;
        color: gray;
        margin-top: -10px;
    }
    .stCaption, .stMarkdown p {
        font-size: 17px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CSV 불러오기 ---
df = pd.read_csv('리뷰데이터_0519_2.csv')
df['tokens'] = df['tokens'].apply(eval)

# 📌 동의어 사전
synonym_dict = {
    '깨끗': ['깨끗하다', '청결하다', '깔끔하다', '위생적', '정돈되다', '청결', '청결함','청결한','깨끗한','깔끔한', '청소', '욕실깨끗', '컨디션', '위생상태', '깔끔히', '위생적이다', '위생관리', '깔끔'],
    '조용': ['조용하다', '고요하다', '방음', '소리없다', '주변조용', '소음없다', '적막하다', '소리안남', '평온하다', '조용히', '조용스러움'],
    '친절': ['친절하다', '상냥하다', '배려심', '도움되다', '유쾌하다', '감사하다', '직원', '서비스', '친절함', '응대좋다', '직원응대', '마음씨좋다', '미소', '우호적이다', '호의적이다', '신속하다', '민첩하다'],
    '가격': ['가성비', '합리적', '저렴하다', '할인받다', '가격', '가성', '저렴함', '가격대비', '가격만족', '가격좋다', '비용', '가격혜택', '싸다', '값이 낮다'],
    '편안': ['편안하다', '안락하다', '침구좋다', '포근하다', '숙면', '침대', '편하다', '쿠션감', '휴식', '잠잘옴', '푹쉬다', '편히', '고요하다', '적막하다', '차분하다', '안락하다', '평온하다'],
    '위치': ['가깝다', '위치', '근처', '접근성', '중심가', '역세권', '도보', '근접', '위치최고', '가까움', '인근', '교통편'],
    '조식': ['조식', '맛있다', '식사', '조식맛있다', '아침식사', '뷔페', '아침밥', '조식메뉴', '조식만족', '아침조식', '맛좋다', '풍미있다'],
    '넓다': ['넓다', '객실넓다', '화장실넓다', '공간넓다', '욕조넓다', '넓직하다', '넓음', '넒은', '넓은편', '넖은편', '광활하다'],
    '뷰': ['뷰', '풍경', '전망', '야경', '경치', '전망좋다', '뷰맛집', '시야', '오션뷰', '한강뷰', '아름답다'],
    '시설': ['시설', '신축', '인테리어', '수압', '샤워기', '청소상태'],
    '보안': ['보안', '안전하다', '키카드', '도어락', '경비', '안어', '리모델링', '새거', '새로지은', '모던', '쾌적하다', '시설좋다'],
    '욕실': ['욕실', '화장실', '샤워실', '욕조', '온수전성'],
    '소음': ['시끄럽다', '소음', '소리', '방음안됨', '방음부족', '소음심하다', '소리들리다', '주변시끄럽다', '소란스럽다', '떠들썩하다'],
    '체크인': ['체크인', '체크아웃', '입실', '퇴실', '입실시간', '대기시간', '입실대기'],
    '에어컨': ['에어컨', '냉방', '에어컨잘됨', '냉방잘됨'],
    '와이파이': ['와이파이', '인터넷', 'wifi', '무선인터넷'],
    '더럽다': ['지저분하다', '불결하다'],
    '좋다': ['훌륭하다', '우수하다'],
    '나쁘다': ['불량하다', '형편없다'],
    '가깝다': ['인접하다', '근접하다'],
    '춥다': ['쌀쌀하다', '차갑다'],
    '덥다': ['후덥지근하다', '무덥다'],
    '쾌적하다': ['상쾌하다', '기분좋다'],
    '흡연': ['흡연', '흡연실', '흡연가능', '비흡연', '금연실', '흡연구역', '담배냄새', '금연정책'],
    '분위기': ['분위기', '아늑하다', '감성', '무드등', '분위기좋다', '로맨틱하다', '조명', '조도', '조용한분위기'],
    '매트리스': ['매트리스', '쿠션감', '스프링', '침대', '침구']
}

    # --- 동의어 검색 함수 ---
def find_synonym_set(keyword, synonym_dict):
    for key, values in synonym_dict.items():
        if keyword == key or keyword in values:
            return [key] + values
    return [keyword]  # 사전에 없으면 입력어 하나만으로 검색

# --- UI 구성 ---
st.markdown("<h1 style='text-align: center;'>🔍 사용자 맞춤화 호텔 추천 시스템</h1>", unsafe_allow_html=True)
st.markdown("🕒 처음 실행 시 약간의 로딩 시간이 발생할 수 있습니다. 잠시만 기다려 주세요!")
st.markdown("<p style='text-align: center; color: gray; font-size: 17px;'>검색할 키워드를 입력하면, 긍정적인 리뷰가 많은 호텔을 추천해드립니다!</p>", unsafe_allow_html=True)

user_keyword = st.text_input("검색할 키워드를 입력하세요", "")
st.markdown("<p class='custom-caption'>※ 한 번에 하나의 키워드만 입력해 주세요 (예: 깨끗)</p>", unsafe_allow_html=True)

if user_keyword:
    target_keywords = find_synonym_set(user_keyword, synonym_dict)
    st.success(f"✅ '{user_keyword}' 키워드 세트: {target_keywords}")

    # 키워드 포함 여부
    df['키워드_포함'] = df['tokens'].apply(lambda tokens: any(k in tokens for k in target_keywords))

    # 긍정 리뷰 필터링
    df_positive = df[(df['감정'] == 'LABEL_2') & (df['키워드_포함'])]

    # 호텔별 리뷰 수
    result = df_positive.groupby('호텔명').size().reset_index(name='키워드_긍정_리뷰수')
    result = result.sort_values(by='키워드_긍정_리뷰수', ascending=False)

    st.markdown("### 📊 긍정 리뷰 수가 많은 호텔")
    st.dataframe(result, height=600, use_container_width=True)  # ✅ 전체 보여주도록 설정
