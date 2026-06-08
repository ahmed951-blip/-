# app.py

import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime
from io import BytesIO

# -----------------------------

# إعداد الصفحة

# -----------------------------

st.set_page_config(
page_title="نظام جماعة معلين",
page_icon="⚖️",
layout="wide"
)

# -----------------------------

# CSS عربي

# -----------------------------

st.markdown("""

<style>
html, body, [class*="css"]{
    direction: rtl;
    text-align:right;
}

.stButton button{
    width:100%;
    border-radius:8px;
    font-weight:bold;
}

.metric-box{
    background:#f8f9fa;
    border-right:5px solid #198754;
    padding:10px;
    border-radius:8px;
}
</style>

""", unsafe_allow_html=True)

# -----------------------------

# قاعدة البيانات

# -----------------------------

DB = "database.db"

def get_connection():
return sqlite3.connect(DB, check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

# -----------------------------

# إنشاء الجداول

# -----------------------------

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS members(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
family_code TEXT,
gender TEXT,
paid TEXT,
created_at TEXT
)
""")

conn.commit()

# -----------------------------

# تشفير كلمة المرور

# -----------------------------

def hash_password(password):
return hashlib.sha256(password.encode()).hexdigest()

# إنشاء مدير افتراضي

cur.execute("SELECT * FROM users WHERE username='admin'")
admin = cur.fetchone()

if not admin:
cur.execute(
"""
INSERT INTO users(username,password,role)
VALUES(?,?,?)
""",
(
"admin",
hash_password("123"),
"admin"
)
)
conn.commit()

# -----------------------------

# Session

# -----------------------------

if "logged_in" not in st.session_state:
st.session_state.logged_in = False

if "username" not in st.session_state:
st.session_state.username = ""

if "role" not in st.session_state:
st.session_state.role = ""

# -----------------------------

# تسجيل الدخول

# -----------------------------

if not st.session_state.logged_in:

```
st.title("🔐 تسجيل الدخول")

username = st.text_input("اسم المستخدم")

password = st.text_input(
    "كلمة المرور",
    type="password"
)

if st.button("دخول"):

    cur.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cur.fetchone()

    if user:
        st.session_state.logged_in = True
        st.session_state.username = user[1]
        st.session_state.role = user[3]
        st.rerun()
    else:
        st.error("بيانات الدخول غير صحيحة")

st.stop()
```

# -----------------------------

# خروج

# -----------------------------

if st.sidebar.button("🚪 تسجيل خروج"):
st.session_state.logged_in = False
st.rerun()

st.title("⚖️ نظام جماعة معلين")

# -----------------------------

# قراءة البيانات

# -----------------------------

df = pd.read_sql_query(
"SELECT * FROM members",
conn
)

total = len(df)

males = len(
df[df["gender"] == "ذكر"]
) if not df.empty else 0

females = len(
df[df["gender"] == "أنثى"]
) if not df.empty else 0

paid = len(
df[df["paid"] == "نعم"]
) if not df.empty else 0

unpaid = total - paid

# -----------------------------

# الإحصائيات

# -----------------------------

st.subheader("📊 لوحة التحكم")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("إجمالي الأعضاء", total)
c2.metric("الذكور", males)
c3.metric("الإناث", females)
c4.metric("المسددين", paid)
c5.metric("غير المسددين", unpaid)

# -----------------------------

# التبويبات

# -----------------------------

tab1,tab2,tab3 = st.tabs(
[
"👥 الأعضاء",
"📊 التقارير",
"🔒 المستخدمون"
]
)

# -----------------------------

# إدارة الأعضاء

# -----------------------------

with tab1:

```
st.subheader("إضافة عضو")

with st.form("add_member"):

    name = st.text_input("الاسم")

    family = st.text_input("كود العائلة")

    gender = st.selectbox(
        "الجنس",
        ["ذكر","أنثى"]
    )

    paid_status = st.selectbox(
        "الصندوق",
        ["نعم","لا"]
    )

    submit = st.form_submit_button(
        "➕ إضافة"
    )

    if submit:

        cur.execute(
            """
            INSERT INTO members
            (
                name,
                family_code,
                gender,
                paid,
                created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                name,
                family,
                gender,
                paid_status,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
            )
        )

        conn.commit()

        st.success("تمت الإضافة")

        st.rerun()

st.divider()

search = st.text_input("🔍 بحث")

view = df.copy()

if search:
    view = view[
        view["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    view,
    use_container_width=True
)
```

# -----------------------------

# التقارير

# -----------------------------

with tab2:

```
st.subheader("Excel")

if not df.empty:

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "📥 تحميل Excel",
        data=buffer.getvalue(),
        file_name="members.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
```

# -----------------------------

# المستخدمون

# -----------------------------

with tab3:

```
if st.session_state.role != "admin":
    st.warning("للإدارة فقط")
else:

    new_user = st.text_input(
        "اسم المستخدم الجديد"
    )

    new_pass = st.text_input(
        "كلمة المرور",
        type="password"
    )

    if st.button("إضافة مستخدم"):

        try:

            cur.execute(
                """
                INSERT INTO users(
                    username,
                    password,
                    role
                )
                VALUES(?,?,?)
                """,
                (
                    new_user,
                    hash_password(
                        new_pass
                    ),
                    "user"
                )
            )

            conn.commit()

            st.success("تمت الإضافة")

        except:
            st.error("المستخدم موجود")
```
