import streamlit as st
import pandas as pd
from io import BytesIO
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# =========================================================
# إعداد الصفحة
# =========================================================
st.set_page_config(
    page_title="نظام جماعة معلين",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# تنسيق RTL
# =========================================================
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"], .main {
    direction: rtl !important;
    text-align: right !important;
}

h1,h2,h3,h4,h5,h6,p,span,label {
    text-align: right !important;
    direction: rtl !important;
}

div[data-baseweb="tab-list"]{
    direction: rtl !important;
}

.stButton>button{
    width:100%;
    font-size:16px;
    font-weight:bold;
    border-radius:10px;
}

.stat-box{
    background:#f8f9fa;
    border-right:5px solid #2e7d32;
    padding:20px;
    border-radius:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# قواعد البيانات
# =========================================================
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": "123"
    }

if "members_db" not in st.session_state:
    st.session_state.members_db = [
        {
            "الاسم": "أحمد المعلي",
            "كود العائلة": "A1",
            "تم دفع الصندوق": "نعم",
            "الجنس": "ذكر"
        },
        {
            "الاسم": "فاطمة المعلي",
            "كود العائلة": "B2",
            "تم دفع الصندوق": "لا",
            "الجنس": "أنثى"
        }
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# دوال التقارير
# =========================================================
def create_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="التقرير")

    return output.getvalue()


def create_word(df):
    doc = Document()

    doc.add_heading('تقرير أعضاء جماعة معلين', level=1)

    table = doc.add_table(rows=1, cols=len(df.columns))

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
        styles['Title']
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
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ]))

    elements.append(table)

    pdf.build(elements)

    return output.getvalue()

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

    if st.button("دخول"):

        if (
            username in st.session_state.users_db
            and
            st.session_state.users_db[username] == password
        ):

            st.session_state.logged_in = True
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

    st.title("⚖️ نظام جماعة معلين الرقمي")

    st.markdown("---")

    # =====================================================
    # الإحصائيات
    # =====================================================
    total = len(st.session_state.members_db)

    paid = sum(
        1 for m in st.session_state.members_db
        if m["تم دفع الصندوق"] == "نعم"
    )

    money = paid * 500

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class='stat-box'>
    👥<br>
    إجمالي الأعضاء<br>
    <h2>{total}</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class='stat-box'>
    ✅<br>
    المسددين<br>
    <h2>{paid}</h2>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class='stat-box'>
    💰<br>
    ميزانية الصندوق<br>
    <h2>{money:,} ريال</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================
    # التبويبات
    # =====================================================
    tab1, tab2, tab3 = st.tabs([
        "👥 إدارة الأعضاء",
        "📊 التقارير",
        "💰 التقسيم المالي"
    ])

    # =====================================================
    # إدارة الأعضاء
    # =====================================================
    with tab1:

        st.subheader("➕ إضافة عضو")

        name = st.text_input("اسم العضو")

        code = st.text_input("كود العائلة")

        paid_status = st.selectbox(
            "حالة الدفع",
            ["نعم", "لا"]
        )

        gender = st.selectbox(
            "الجنس",
            ["ذكر", "أنثى"]
        )

        if st.button("إضافة عضو"):

            if name and code:

                st.session_state.members_db.append({
                    "الاسم": name,
                    "كود العائلة": code,
                    "تم دفع الصندوق": paid_status,
                    "الجنس": gender
                })

                st.success("تمت إضافة العضو")
                st.rerun()

            else:
                st.error("يجب تعبئة جميع الحقول")

        st.markdown("---")

        st.subheader("✏️ تحرير وحذف الأعضاء")

        for i, member in enumerate(st.session_state.members_db):

            with st.expander(f"👤 {member['الاسم']}"):

                new_name = st.text_input(
                    "الاسم",
                    value=member["الاسم"],
                    key=f"name_{i}"
                )

                new_code = st.text_input(
                    "كود العائلة",
                    value=member["كود العائلة"],
                    key=f"code_{i}"
                )

                new_paid = st.selectbox(
                    "الدفع",
                    ["نعم", "لا"],
                    index=0 if member["تم دفع الصندوق"] == "نعم" else 1,
                    key=f"paid_{i}"
                )

                new_gender = st.selectbox(
                    "الجنس",
                    ["ذكر", "أنثى"],
                    index=0 if member["الجنس"] == "ذكر" else 1,
                    key=f"gender_{i}"
                )

                colu1, colu2 = st.columns(2)

                with colu1:
                    if st.button("💾 حفظ التعديل", key=f"save_{i}"):

                        st.session_state.members_db[i] = {
                            "الاسم": new_name,
                            "كود العائلة": new_code,
                            "تم دفع الصندوق": new_paid,
                            "الجنس": new_gender
                        }

                        st.success("تم تحديث البيانات")
                        st.rerun()

                with colu2:
                    if st.button("🗑️ حذف العضو", key=f"delete_{i}"):

                        st.session_state.members_db.pop(i)

                        st.warning("تم حذف العضو")
                        st.rerun()

    # =====================================================
    # التقارير
    # =====================================================
    with tab2:

        st.subheader("📊 التقارير")

        df = pd.DataFrame(st.session_state.members_db)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        excel_file = create_excel(df)

        st.download_button(
            label="📥 تحميل Excel",
            data=excel_file,
            file_name="report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        word_file = create_word(df)

        st.download_button(
            label="📥 تحميل Word",
            data=word_file,
            file_name="report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        pdf_file = create_pdf(df)

        st.download_button(
            label="📥 تحميل PDF",
            data=pdf_file,
            file_name="report.pdf",
            mime="application/pdf"
        )

    # =====================================================
    # التقسيم المالي
    # =====================================================
    with tab3:

        st.subheader("💰 تقسيم مبلغ مالي")

        amount = st.number_input(
            "المبلغ الإجمالي",
            min_value=0.0
        )

        if amount > 0 and total > 0:

            share = amount / total

            st.metric(
                "المبلغ المستحق لكل فرد",
                f"{share:,.2f} ريال"
            )

            calc_df = pd.DataFrame(
                st.session_state.members_db
            )

            calc_df["المبلغ المستحق"] = round(
                share,
                2
            )

            st.dataframe(
                calc_df,
                use_container_width=True,
                hide_index=True
            )
