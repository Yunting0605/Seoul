import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 網頁基本設定
st.set_page_config(page_title="首爾行程規劃大師", layout="wide", page_icon="🇰🇷")

# 2. 初始化行程資料 (讓您可以直接在網頁編輯)
if 'itinerary_df' not in st.session_state:
    st.session_state.itinerary_df = pd.DataFrame([
        {"天數": "Day 1", "時間": "14:00", "行程內容": "抵達並入住高麗亞那酒店", "備註": "機場巴士 6701"},
        {"天數": "Day 2", "時間": "10:00", "行程內容": "景福宮、北村韓屋村", "備註": "穿韓服免門票"},
        {"天數": "Day 3", "時間": "11:00", "行程內容": "東廟假日市集", "備註": "週日限定"},
        {"天數": "Day 4", "時間": "12:00", "行程內容": "春川辣炒雞排午餐 + 南怡島", "備註": "搭 ITX 青春號"},
        {"天數": "Day 5", "行程內容": "弘大、梨大商圈購物", "備註": ""},
        {"天數": "Day 6", "行程內容": "樂天超市採買後前往機場", "備註": ""},
    ])

# 3. 側邊欄選單
with st.sidebar:
    st.title("🇰🇷 旅遊管理後台")
    menu = st.radio("功能導覽", ["📝 編輯行程", "🌦️ 即時天氣", "📍 Naver 地圖", "💰 旅費記帳", "🗣️ 韓語助手"])
    st.divider()
    st.write(f"📅 今日日期: {datetime.now().strftime('%Y-%m-%d')}")
    st.info("💡 提醒：編輯完行程請點擊『儲存變更』。")

# --- 功能 1：編輯行程 (網頁排行程) ---
if menu == "📝 編輯行程":
    st.header("🗓️ 規劃您的首爾行程")
    st.write("您可以直接點擊下方表格修改內容，或使用右側按鈕新增/刪除行。")
    
    # 使用 st.data_editor 達成網頁編輯功能
    edited_df = st.data_editor(
        st.session_state.itinerary_df, 
        num_rows="dynamic", 
        use_container_width=True
    )

    if st.button("💾 儲存變更"):
        st.session_state.itinerary_df = edited_df
        st.success("行程已成功儲存！(重新整理前有效)")

# --- 功能 2：即時天氣 (AccuWeather 連結) ---
elif menu == "🌦️ 即時天氣":
    st.header("🌦️ 首爾即時天氣預報")
    st.link_button("🌡️ 開啟 AccuWeather 詳細預報 (點我)", 
                   "https://www.accuweather.com/zh/kr/seoul/226081/daily-weather-forecast/226081",
                   use_container_width=True)
    st.divider()
    st.metric("首爾今日預估", "-2 °C", "-5 °C")
    st.warning("🧣 提醒：1月份首爾極度寒冷，請備妥發熱衣與羽絨衣。")

# --- 功能 3：Naver Map 導航 ---
elif menu == "📍 Naver 地圖":
    st.header("📍 Naver Map 景點導航")
    spots = {
        "🏨 高麗亞那酒店": "https://naver.me/G9R6p3Nf",
        "🥘 春川明洞雞排街": "https://naver.me/xXrk8Yf6",
        "🌳 南怡島碼頭": "https://naver.me/IFj6q9H4"
    }
    for name, url in spots.items():
        st.link_button(name, url, use_container_width=True)

# --- 功能 4：旅費記帳 (匯率 46) ---
elif menu == "💰 旅費記帳":
    st.header("💰 旅費記帳 (1 TWD ≈ 46 KRW)")
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    with st.form("expense_form"):
        item = st.text_input("花費項目")
        amount = st.number_input("金額 (KRW)", min_value=0, step=1000)
        if st.form_submit_button("新增支出"):
            st.session_state.expenses.append({"項目": item, "韓元": amount, "台幣": round(amount/46)})
    
    if st.session_state.expenses:
        st.table(pd.DataFrame(st.session_state.expenses))
        total_krw = sum(x['韓元'] for x in st.session_state.expenses)
        st.metric("總支出 (台幣)", f"NT$ {int(total_krw/46):,}")

# --- 功能 5：韓語助手 ---
elif menu == "🗣️ 韓語助手":
    st.header("🗣️ 點餐溝通不求人")
    st.code("닭갈비 4인분 주세요. (請給我4份辣炒雞排)", language="text")
    st.code("볶음밥 2인분 볶아주세요. (請幫我們炒2份飯)", language="text")
    st.code("물 좀 주세요. (請給我水)", language="text")
