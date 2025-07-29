import time

import streamlit as st
from utils import submit_score, get_user_info,get_testname, extract_params_from_url

st.set_page_config(page_title="IronMan答题工具", page_icon="🤖", layout="centered")

st.title("IronMan答题工具 🤖")
st.markdown("By口天吴")

# 添加自定义CSS样式
st.markdown("""
<style>
div.stButton > button:first-child {
    width: auto;
    margin: 5px;
}
div.stButton > button:first-child[kind="secondary"] {
    background-color: #4CAF50;
    color: white;
}
div.stButton > button:first-child[kind="primary"] {
    background-color: #008CBA;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'quiz_url' not in st.session_state:
    st.session_state.quiz_url = ""
if 'result' not in st.session_state:
    st.session_state.result = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# 主内容区域
st.header("输入链接")

# 在主区域添加输入框
st.markdown("""
<style>
.quiz-url-textarea {
    font-size: 1.2em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

quiz_url = st.text_area("请输入答题链接：", height=150, value=st.session_state.quiz_url, key="quiz_url_input")


col1, col2 = st.columns(2)
with col1:
    if st.button("开始答题"):
        if not quiz_url.strip():
            st.warning("请输入有效的答题链接")
        else:
            st.session_state.quiz_url = quiz_url
            with st.spinner("正在提交答题成绩..."):
                response1 = submit_score(quiz_url)
                st.session_state.result = response1
            # with st.spinner("正在获取用户信息..."):


# with col2:
#     if st.button("获取用户信息"):
#         if not quiz_url.strip():
#             st.warning("请输入有效的答题链接")
#         else:
#             st.session_state.quiz_url = quiz_url


# 显示结果
if st.session_state.result:
    st.subheader("答题结果")
    result = st.session_state.result
    try:
        if result and result.json()['success']:
            st.success("答题成功：您的成绩是100分！！\n快去铁人app中查看答题成绩！！")
            response2 = get_user_info(quiz_url)
            st.session_state.user_info = response2
            response3 = get_testname(quiz_url)
            st.session_state.testname = response3

        else:
            st.error("答题失败，请检查输入的链接。")
    except Exception as e:
        st.warning("请求失败: 请检查输入的链接。")
# 显示用户信息结果
if st.session_state.user_info:
    user_response2 = st.session_state.user_info
    user_response3 = st.session_state.testname
    try:
        user_info = user_response2.json()
        partyMemName = user_info.get("data", {}).get("partyMemName")
        orgName = user_info.get("data", {}).get("orgName")

        st.subheader("用户信息")
        if  partyMemName and orgName:
            st.info(f"用户信息：{partyMemName} {orgName}")
        else:
            st.warning("请求失败: 注：\n1.如果是第一次答题，无法获取用户信息是正常的，不影响答题。\n2.纪检每月一学无法获取用户信息是正常的，不影响答题。\n请直接点击开始答题，再获取用户信息。")

    except Exception as e:
        st.warning("请求失败: 注：\n1.如果是第一次答题，无法获取用户信息是正常的，不影响答题。\n2.纪检每月一学无法获取用户信息是正常的，不影响答题。\n请直接点击开始答题，再获取用户信息。")

    st.subheader("考卷信息")
    testname_info = user_response3.json()
    testName = testname_info.get("data", {}).get("testName")
    st.info(f"考卷信息：{testName}")

# """将用户信息、考卷信息保存在文件中"""
    with open("user_info.txt", "a") as f:
        f.write(f"答题时间：{time.strftime('%Y-%m-%d %H:%M:%S') }\n")
        # f.write(f"答题时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n")
        f.write(f"用户信息：{partyMemName} {orgName}\n")
        f.write(f"考卷信息：{testName}\n")
        f.write(f"答题链接：{quiz_url}\n\n\n")

# 使用说明
with st.expander("使用说明"):
    st.markdown("""
    1. 在上方输入框中粘贴答题链接，然后点击答题即可。
    2. "用户信息"可以查看当前答题的用户信息，获取不到也不影响答题。
    3. 以下两种情况，可能无法获取用户信息，请直接点击开始答题，再获取用户信息： 1.第一次答题，无法获取用户信息是正常的，不影响答题。2.纪检每月一学无法获取用户信息是正常的，不影响答题。    
    4. 答题完成后请到铁人APP中查看成绩
    """)




# # 技术信息
# with st.expander("技术信息"):
#     if st.session_state.quiz_url:
#         with st.spinner("解析链接参数..."):
#             try:
#                 params = extract_params_from_url(st.session_state.quiz_url)
#                 st.json(params)
#             except:
#                 st.info("请输入有效的链接以查看参数信息")