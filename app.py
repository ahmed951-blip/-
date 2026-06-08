import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
from datetime import datetime

# =========================
# WORD
# =========================
from docx import Document

# =========================
# PDF عربي
# =========================
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =========================
# EXCEL
# =========================
from openpyxl import Workbook

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="نظام جماعة معلين",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], .main {
    direction: rtl;
    text-align: right;
    background-color: #f5f7fb;
}

h1,h2,h3,h4,h5,h6{
    font-weight:bold;
}

.stButton > button{
    width:100%;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#1565c0,#1976d2);
    color:white;
    font-size:16px;
    font-weight:bold;
    padding:10px;
}

.stTextInput input,
.stNumberInput input{
    border-radius:10px;
}

.stat-card{
    background:linear-gradient(135deg,#1e3c72,#2a5298);
    color:white;
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 5px 20px rgba(0,0,0,0.15);
    margin-bottom:15px;
}

.login-box{
    background:white;
    padding:40px;
    border-radius:20px;
    box-shadow:0px 0px 20px rgba(0,0,0,0.1);
    margin-top:80px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# قاعدة البيانات
# =========================
conn = sqlite3.connect(
    "maalin.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# جدول الأعضاء
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    family_code TEXT,
    gender TEXT,
    paid TEXT,
    phone TEXT,
    notes TEXT,
    created_at TEXT
)
""")

# =========================
# جدول المستخدمين
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

conn.commit()

# =========================
# إنشاء حساب الأدمن
# =========================
cursor.execute("""
SELECT * FROM users
WHERE username='admin'
""")

admin = cursor.fetchone()

if not admin:

    cursor.execute("""
    INSERT INTO users(username,password,role)
    VALUES('admin','123','admin')
    """)

    conn.commit()

# =========================
# تحميل الأعضاء
# =========================
def load_members():

    return pd.read_sql(
        "SELECT * FROM members",
        conn
    )

# =========================
# إنشاء Excel
# =========================
def create_excel(df):

    output = BytesIO()

    wb = Workbook()

    ws = wb.active

    ws.title = "التقرير"

    ws.append(list(df.columns))

    for row in df.values.tolist():
        ws.append(row)

    wb.save(output)

    return output.getvalue()

# =========================
# إنشاء Word
# =========================
def create_word(df):

    doc = Document()

    doc.add_heading(
        "تقرير أعضاء جماعة معلين",
        level=1
    )

    table = doc.add_table(
        rows=1,
        cols=len(df.columns)
    )

    table.style = "Table Grid"

    hdr_cells = table.rows[0].cells

    for i, col in enumerate(df.columns):
        hdr_cells[i].text = str(col)

    for _, row in df.iterrows():

        cells = table.add_row().cells

        for i, value in enumerate(row):
            cells[i].text = str(value)

    output = BytesIO()

    doc.save(output)

    return output.getvalue()

# =========================
# إنشاء PDF عربي
# =========================
def create_pdf(df):

    output = BytesIO()

    pdfmetrics.registerFont(
        TTFont(
            'Arabic',
            'Amiri-Regular.ttf'
        )
    )

    doc = SimpleDocTemplate(
        output,
        pagesize=A4
    )

    elements = []

    styles = getSampleStyleSheet()

    title_text = "تقرير أعضاء جماعة معلين"

    reshaped = arabic_reshaper.reshape(
        title_text
    )

    bidi_text = get_display(
        reshaped
    )

    title = Paragraph(
        f"<font name='Arabic'>{bidi_text}</font>",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1,20))

    data = []

    headers = []

    for col in df.columns:

        reshaped_col = arabic_reshaper.reshape(
            str(col)
        )

        bidi_col = get_display(
            reshaped_col
        )

        headers.append(bidi_col)

    data.append(headers)

    for _, row in df.iterrows():

        row_data = []

        for item in row:

            reshaped_item = arabic_reshaper.reshape(
                str(item)
            )

            bidi_item = get_display(
                reshaped_item
            )

            row_data.append(bidi_item)

        data.append(row_data)

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('FONTNAME',(0,0),(-1,-1),'Arabic'),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('ALIGN',(0,0),(-1,-1),'RIGHT'),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ]))

    elements.append(table)

    doc.build(elements)

    return output.getvalue()

# =========================
# Session
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
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class='login-box'>
        <h1 style='text-align:center'>
        ⚖️ نظام جماعة معلين
        </h1>
        <p style='text-align:center'>
        تسجيل الدخول
        </p>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 اسم المستخدم")

        password = st.text_input(
            "🔑 كلمة المرور",
            type="password"
        )

        if st.button("🚀 دخول النظام"):

            cursor.execute("""
            SELECT * FROM users
            WHERE username=? AND password=?
            """, (username, password))

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.session_state.role = user[3]

                st.success("تم تسجيل الدخول")

                st.rerun()

            else:
                st.error("بيانات الدخول غير صحيحة")

# =========================
# النظام
# =========================
else:

    members_df = load_members()

    total = len(members_df)

    male_count = len(
        members_df[members_df["gender"] == "ذكر"]
    )

    female_count = len(
        members_df[members_df["gender"] == "أنثى"]
    )

    paid_count = len(
        members_df[members_df["paid"] == "نعم"]
    )

    not_paid_count = total - paid_count

