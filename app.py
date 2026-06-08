import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
from datetime import datetime
from docx import Document
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook

# =========================================================
# إعداد الصفحة
# =========================================================
st.set_page_config(
    page_title="نظام جماعة معلين الاحترافي",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], .main {
    direction: rtl !important;
    text-align: right !important;
}

h1,h2,h3,h4,h5,h6,p,span,label {
    text-align:right !important;
    direction:rtl !important;
}

div[data-baseweb="tab-list"]{
    direction: rtl !important;
}

.stButton > button{
    width:100%;
    border-radius:10px;
    font-size:16px;
    font-weight:bold;
}

.stat-card{
    background:#f8f9fa;
    border-right:5px solid #2e7d32;
    padding:20px;
    border-radius:12px;
    margin-bottom:10px;
    box-shadow:0px 0px 5px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# قاعدة البيانات SQLite
# =========================================================
conn = sqlite3.connect("maalin.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء جدول الأعضاء
cursor.execute("""
CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    family_code TEXT,
    paid TEXT,
    gender TEXT,
    phone TEXT,
    notes TEXT,
    created_at TEXT
)
""")

# المستخدمين
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

conn.commit()

# إنشاء الأدمن الافتراضي
cursor.execute("SELECT * FROM users WHERE username='admin'")
admin_exist = cursor.fetchone()

if not admin_exist:
    cursor.execute("""
    INSERT INTO users(username,password,role)
    VALUES('admin','123','مدير')
    """)
    conn.commit()

# =========================================================
# دوال
# =========================================================
def load_members():
    query = "SELECT * FROM members"
    df = pd.read_sql(query, conn)
    return df


def create_excel(df):

    output = BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "الأعضاء"

    ws.append(list(df.columns))

    for row in df.values.tolist():
        ws.append(row)

    wb.save(output)

    return output.getvalue()


def create_word(df):

    doc = Document()

    doc.add_heading(
        'تقرير أعضاء جماعة معلين',
        level=1
    )

    table = doc.add_table(
        rows=1,
        cols=len(df.columns)
    )

    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells

    for i, col in enumerate(df.columns):
        hdr_cells[i].text = str(col)

    for _, row in df.iterrows():

        row_cells = table.add_row().cells

        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    output = BytesIO()
    doc.save(output)

    return output.getvalue()


def create_pdf(df):

    output = BytesIO()

    pdf = SimpleDocTemplate(
        output,
        pagesize=A4
    )

    elements = []

    styles = getSampleStyleSheet()

    title = Paragraph(
        "تقرير أعضاء جماعة معلين",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    data = [list(df.columns)]

    for _, row in df.iterrows():
        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))

    elements.append(table)

    pdf.build(elements)

    return output.getvalue()

# =========================================================
# Session
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================================================
# تسجيل الدخول
# =========================================================
if not st.session_state.logged_in:

    st.title("🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    if st.button("دخول النظام"):

        cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        if user:

            st.session_state.logged_in = True
            st.session_state.role = user[3]

            st.success("تم تسجيل الدخول")
            st.rerun()

        else:
            st.error("بيانات الدخول غير صحيحة")

# =========================================================
# النظام الرئيسي
# =========================================================
else:

    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("🚪 خروج"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("⚖️ نظام جماعة معلين الاحترافي")

    df = load_members()

    total = len(df)

    paid = len(df[df["paid"] == "نعم"])

    not_paid = total - paid

    males = len(df[df["gender"] == "ذكر"])

    females = len(df[df["gender"] == "أنثى"])

    fund = paid * 500

    st.markdown("## 📊 الإحصائيات")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.markdown(f"""
    <div class='stat-card'>
    👥<br>
    إجمالي الأعضاء
    <h2>{total}</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class='stat-card'>
    👨
    <h2>{males}</h2>
    ذكور
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class='stat-card'>
    👩
    <h2>{females}</h2>
    إناث
    </div>
    """, unsafe_allow_html=True)

    c4.markdown(f"""
    <div class='stat-card'>
    ✅
    <h2>{paid}</h2>
    مسدد
    </div>
    """, unsafe_allow_html=True)

    c5.markdown(f"""
    <div class='stat-card'>
    ❌
    <h2>{not_paid}</h2>
    غير مسدد
    </div>
    """, unsafe_allow_html=True)

    c6.markdown(f"""
    <div class='stat-card'>
    💰
    <h2>{fund:,}</h2>
    ريال
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 إدارة الأعضاء",
        "📊 التقارير",
        "💰 التقسيم المالي",
        "🔍 البحث والفلترة",
        "🔐 المستخدمين"
    ])

    # =====================================================
    # إدارة الأعضاء
    # =====================================================
    with tab1:

        st.subheader("➕ إضافة عضو")

        with st.form("add_member"):

            name = st.text_input("الاسم")

            family = st.text_input("كود العائلة")

            phone = st.text_input("رقم الجوال")

            gender = st.selectbox(
                "الجنس",
                ["ذكر", "أنثى"]
            )

            paid_status = st.selectbox(
                "تم الدفع",
                ["نعم", "لا"]
            )

            notes = st.text_area("ملاحظات")

            submit = st.form_submit_button("إضافة")

            if submit:

                cursor.execute("""
                INSERT INTO members(
                    name,
                    family_code,
                    paid,
                    gender,
                    phone,
                    notes,
                    created_at
                )
                VALUES(?,?,?,?,?,?,?)
                """, (
                    name,
                    family,
                    paid_status,
                    gender,
                    phone,
                    notes,
                    datetime.now().strftime("%Y-%m-%d")
                ))

                conn.commit()

                st.success("تمت إضافة العضو")

                st.rerun()

        st.markdown("---")

        st.subheader("✏️ تعديل وحذف الأعضاء")

        members = load_members()

        for _, row in members.iterrows():

            with st.expander(f"👤 {row['name']}"):

                new_name = st.text_input(
                    "الاسم",
                    row["name"],
                    key=f"name_{row['id']}"
                )

                new_family = st.text_input(
                    "كود العائلة",
                    row["family_code"],
                    key=f"family_{row['id']}"
                )

                new_phone = st.text_input(
                    "الجوال",
                    row["phone"],
                    key=f"phone_{row['id']}"
                )

                new_gender = st.selectbox(
                    "الجنس",
                    ["ذكر","أنثى"],
                    index=0 if row["gender"]=="ذكر" else 1,
                    key=f"gender_{row['id']}"
                )

                new_paid = st.selectbox(
                    "الدفع",
                    ["نعم","لا"],
                    index=0 if row["paid"]=="نعم" else 1,
                    key=f"paid_{row['id']}"
                )

                new_notes = st.text_area(
                    "ملاحظات",
                    row["notes"],
                    key=f"notes_{row['id']}"
                )

                cc1, cc2 = st.columns(2)

                with cc1:

                    if st.button(
                        "💾 حفظ التعديل",
                        key=f"save_{row['id']}"
                    ):

                        cursor.execute("""
                        UPDATE members
                        SET
                        name=?,
                        family_code=?,
                        paid=?,
                        gender=?,
                        phone=?,
                        notes=?
                        WHERE id=?
                        """, (
                            new_name,
                            new_family,
                            new_paid,
                            new_gender,
                            new_phone,
                            new_notes,
                            row["id"]
                        ))

                        conn.commit()

                        st.success("تم التعديل")

                        st.rerun()

                with cc2:

                    if st.button(
                        "🗑️ حذف",
                        key=f"delete_{row['id']}"
                    ):

                        cursor.execute("""
                        DELETE FROM members
                        WHERE id=?
                        """, (row["id"],))

                        conn.commit()

                        st.warning("تم الحذف")

                        st.rerun()

    # =====================================================
    # التقارير
    # =====================================================
    with tab2:

        st.subheader("📊 التقارير")

        report_df = load_members()

        st.dataframe(
            report_df,
            use_container_width=True
        )

        excel_file = create_excel(report_df)

        st.download_button(
            "📥 تحميل Excel",
            excel_file,
            "report.xlsx"
        )

        word_file = create_word(report_df)

        st.download_button(
            "📥 تحميل Word",
            word_file,
            "report.docx"
        )

        pdf_file = create_pdf(report_df)

        st.download_button(
            "📥 تحميل PDF",
            pdf_file,
            "report.pdf"
        )

    # =====================================================
    # التقسيم المالي
    # =====================================================
    with tab3:

        st.subheader("💰 التقسيم المالي")

        amount = st.number_input(
            "المبلغ الإجمالي",
            min_value=0.0
        )

        reason = st.text_input(
            "سبب التقسيم"
        )

        if amount > 0 and total > 0:

            share = amount / total

            st.metric(
                "المبلغ المستحق للفرد",
                f"{share:,.2f} ريال"
            )

            calc_df = load_members()

            calc_df["المبلغ المستحق"] = round(
                share,
                2
            )

            st.dataframe(calc_df)

    # =====================================================
    # البحث
    # =====================================================
    with tab4:

        st.subheader("🔍 البحث والفلترة")

        keyword = st.text_input("ابحث بالاسم")

        search_df = load_members()

        if keyword:

            search_df = search_df[
                search_df["name"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            search_df,
            use_container_width=True
        )

    # =====================================================
    # المستخدمين
    # =====================================================
    with tab5:

        st.subheader("🔐 إدارة المستخدمين")

        with st.form("user_form"):

            u = st.text_input("اسم المستخدم")

            p = st.text_input(
                "كلمة المرور",
                type="password"
            )

            role = st.selectbox(
                "الصلاحية",
                ["مدير","موظف"]
            )

            submit_user = st.form_submit_button(
                "إضافة مستخدم"
            )

            if submit_user:

                cursor.execute("""
                INSERT INTO users(username,password,role)
                VALUES(?,?,?)
                """, (u,p,role))

                conn.commit()

                st.success("تم إضافة المستخدم")

        users_df = pd.read_sql(
            "SELECT username,role FROM users",
            conn
        )

        st.dataframe(
            users_df,
            use_container_width=True
        )
