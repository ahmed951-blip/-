import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="نظام جماعة معلين",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# تصميم عربي
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stButton button {
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# قاعدة البيانات
# =========================
DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn

conn = get_db()
cur = conn.cursor()

# =========================
# إنشاء الجداول
# =========================
def init_db():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        national_id TEXT,
        family_code TEXT,
        gender TEXT,
        paid TEXT,
        created_at TEXT
    )
    """)

    conn.commit()

init_db()

# =========================
# تشفير كلمة المرور
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# إنشاء أدمن افتراضي
# =========================
def create_admin():

    cur.execute("SELECT * FROM users WHERE username='admin'")
    admin = cur.fetchone()

    if not admin:
        cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("admin", hash_password("123"), "admin"))

        conn.commit()

create_admin()

# =========================
# Session State
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================
# تسجيل الدخول
# =========================
def login():

    st.title("🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):

        cur.execute("""
        SELECT username, password, role
        FROM users
        WHERE username=?
        """, (username,))

        user = cur.fetchone()

        if user and user[1] == hash_password(password):

            st.session_state.logged_in = True
            st.session_state.username = user[0]
            st.session_state.role = user[2]

            st.success("تم تسجيل الدخول بنجاح")
            st.rerun()

        else:
            st.error("بيانات غير صحيحة")

# =========================
# تسجيل الخروج
# =========================
def logout():
    if st.sidebar.button("🚪 تسجيل خروج"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# تشغيل النظام
# =========================
if not st.session_state.logged_in:
    login()
    st.stop()

logout()

# =========================
# واجهة بعد الدخول
# =========================
st.title("⚖️ نظام جماعة معلين")

st.info(f"مرحباً {st.session_state.username} 👋")
