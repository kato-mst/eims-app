import streamlit as st
import pandas as pd
import random
import string
from streamlit_option_menu import option_menu

# ページ設定を「wide」に変更
st.set_page_config(layout="wide")

# 初期社員データ（サンプルデータ）
employee_data = [
    {"employee_id": "EMP00001", "name_kanji": "山田 太郎", "name_kana": "ヤマダ タロウ", "department": "営業", "email": "taro.yamada@example.com"},
    {"employee_id": "EMP00002", "name_kanji": "佐藤 花子", "name_kana": "サトウ ハナコ", "department": "経理", "email": "hanako.sato@example.com"}
]

# 社員ID生成関数
def generate_employee_id():
    return "EMP" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# 初期表示
if "current_view" not in st.session_state:
    st.session_state.current_view = "社員一覧"
if "employee_data" not in st.session_state:
    st.session_state.employee_data = employee_data

# メニュー
with st.sidebar:
    menu_options = ["社員一覧", "社員登録"]
    selected_option = option_menu("", menu_options, 
                                  icons=["list-task", "person-plus"],
                                  menu_icon="cast", default_index=menu_options.index(st.session_state.current_view))
    st.session_state.current_view = selected_option

# 社員一覧表示
if st.session_state.current_view == "社員一覧":
    st.title("社員一覧")

    df = pd.DataFrame(st.session_state.employee_data)
    df.set_index("employee_id", inplace=True)

    # ヘッダー
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 2, 4, 1, 1])
    col1.markdown("**社員ID**")
    col2.markdown("**名前**")
    col3.markdown("**フリガナ**")
    col4.markdown("**部署**")
    col5.markdown("**メールアドレス**")
    col6.markdown("**編集**")
    col7.markdown("**削除**")

    # 編集と削除のアイコン付きデータフレーム
    def edit_employee(index):
        st.session_state.edit_index = index

    def delete_employee(index):
        st.session_state.delete_index = index

    for idx, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 2, 2, 2, 4, 1, 1])
        col1.write(idx)
        col2.write(row["name_kanji"])
        col3.write(row["name_kana"])
        col4.write(row["department"])
        col5.write(row["email"])
        if col6.button("✏️", key=f"edit_{idx}"):
            edit_employee(idx)
        if col7.button("🗑️", key=f"delete_{idx}"):
            delete_employee(idx)

    # 編集モーダル
    if "edit_index" in st.session_state:
        index = st.session_state.edit_index
        data = df.loc[index]
        with st.form("edit_form"):
            name_kanji = st.text_input("名前（漢字）", value=data["name_kanji"])
            name_kana = st.text_input("名前（フリガナ）", value=data["name_kana"])
            department = st.text_input("部署", value=data["department"])
            email = st.text_input("メールアドレス", value=data["email"])
            submit_btn = st.form_submit_button("確定")
            cancel_btn = st.form_submit_button("キャンセル")
        if submit_btn:
            st.session_state.employee_data = [
                {"employee_id": emp["employee_id"], 
                 "name_kanji": name_kanji if emp["employee_id"] == index else emp["name_kanji"],
                 "name_kana": name_kana if emp["employee_id"] == index else emp["name_kana"],
                 "department": department if emp["employee_id"] == index else emp["department"],
                 "email": email if emp["employee_id"] == index else emp["email"]}
                for emp in st.session_state.employee_data
            ]
            del st.session_state.edit_index
        if cancel_btn:
            del st.session_state.edit_index

    # 削除モーダル
    if "delete_index" in st.session_state:
        index = st.session_state.delete_index
        st.warning(f"社員ID：{index}の情報を削除しますか？")
        col1, col2 = st.columns([1, 1])
        if col1.button("OK"):
            st.session_state.employee_data = [emp for emp in st.session_state.employee_data if emp["employee_id"] != index]
            del st.session_state.delete_index
        if col2.button("キャンセル"):
            del st.session_state.delete_index

# 社員登録
elif st.session_state.current_view == "社員登録":
    st.title("社員登録")
    with st.form("register_form"):
        name_kanji = st.text_input("名前（漢字）")
        name_kana = st.text_input("名前（フリガナ）")
        department = st.text_input("部署")
        email = st.text_input("メールアドレス")
        submit_btn = st.form_submit_button("登録")
    if submit_btn:
        new_employee = {
            "employee_id": generate_employee_id(),
            "name_kanji": name_kanji,
            "name_kana": name_kana,
            "department": department,
            "email": email
        }
        st.session_state.employee_data.append(new_employee)
        st.success("社員情報が登録されました。")