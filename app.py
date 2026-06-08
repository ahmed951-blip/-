import streamlit as st
import pandas as pd
import random

# =========================================================
# إعدادات الصفحة
# =========================================================
st.set_page_config(
    page_title="نظام جماعة معلين الرقمي",
    page_icon="⚖️",
    layout="wide"
)

# =========================================================
# تنسيق RTL كامل
# =========================================================
st.markdown("""
<style>

/* دعم RTL كامل */
html, body, [data-testid="stAppViewContainer"], .main {
    direction: rtl !important;
    text-align: right !important;
}

/* الخطوط والعناوين */
h1, h2, h3, h4, h5, h6, p, span, label {
    direction: rtl !important;
    text-align: right !important;
}

/* التبويبات */
div[data-baseweb="tab-list"] {
    direction: rtl !important;
    gap: 10px !important;
}

div[data-baseweb="tab"] p {
    font-size: 18px !important;
    font-weight: bold !important;
}

/* الأزرار */
.stButton > button {
    width: 100%;
    font-size: 17px !important;
    font-weight: bold !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* الإحصائيات */
.stat-box {
    background-color: #f8f9fa;
    border-right: 6px solid #2e7d32;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.08);
}

/* الجداول */
table {
    direction: rtl !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# قواعد البيانات الوهمية
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
            "الاسم": "محمد المعلي",
            "كود العائلة": "A1",
            "تم دفع الصندوق": "لا",
            "الجنس": "ذكر"
        },
        {
            "الاسم": "فاطمة المعلي",
            "كود العائلة": "B2",
            "تم دفع الصندوق": "نعم",
            "الجنس": "أنثى"
        }
    ]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# صفحة تسجيل الدخول
# =========================================================
if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.title("🔐 نظام جماعة معلين الرقمي")

    username = st.text_input(
        "اسم المستخدم",
        key="login_user"
    )

    password = st.text_input(
        "كلمة المرور",
        type="password",
        key="login_pass"
    )

    if st.button("🔓 تسجيل الدخول"):

        if (
            username in st.session_state.users_db
            and
            st.session_state.users_db[username] == password
        ):

            st.session_state.logged_in = True
            st.success("✅ تم تسجيل الدخول بنجاح")
            st.rerun()

        else:
            st.error("❌ بيانات الدخول غير صحيحة")

# =========================================================
# النظام الرئيسي
# =========================================================
else:

    # زر الخروج
    _, logout_col = st.columns([8, 1])

    with logout_col:

        if st.button("🚪 خروج"):

            st.session_state.logged_in = False
            st.rerun()

    st.title("⚖️ النظام الإلكتروني لإدارة جماعة معلين")

    st.markdown("---")

    # =====================================================
    # الإحصائيات
    # =====================================================
    total = len(st.session_state.members_db)

    males = sum(
        1 for m in st.session_state.members_db
        if m["الجنس"] == "ذكر"
    )

    females = sum(
        1 for m in st.session_state.members_db
        if m["الجنس"] == "أنثى"
    )

    paid = sum(
        1 for m in st.session_state.members_db
        if m["تم دفع الصندوق"] == "نعم"
    )

    not_paid = total - paid

    box_money = paid * 500

    st.subheader("📊 الإحصائيات العامة")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.markdown(f"""
    <div class="stat-box">
    👥<br>
    <b>إجمالي الأعضاء</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {total}
    </span>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="stat-box">
    👨<br>
    <b>عدد الذكور</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {males}
    </span>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="stat-box">
    👩<br>
    <b>عدد الإناث</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {females}
    </span>
    </div>
    """, unsafe_allow_html=True)

    c4.markdown(f"""
    <div class="stat-box">
    ✅<br>
    <b>المسجلين بالصندوق</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {paid}
    </span>
    </div>
    """, unsafe_allow_html=True)

    c5.markdown(f"""
    <div class="stat-box">
    ❌<br>
    <b>غير المسجلين</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {not_paid}
    </span>
    </div>
    """, unsafe_allow_html=True)

    c6.markdown(f"""
    <div class="stat-box">
    💰<br>
    <b>ميزانية الصندوق</b><br>
    <span style="font-size:22px;color:#2e7d32;">
    {box_money:,} ر.س
    </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================
    # التبويبات
    # =====================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 التقسيم المالي",
        "👥 إدارة الأعضاء",
        "📊 التقارير",
        "🔐 المستخدمين"
    ])

    # =====================================================
    # التبويب الأول
    # =====================================================
    with tab1:

        st.subheader("💵 تقسيم مبلغ مالي")

        amount = st.number_input(
            "أدخل المبلغ الإجمالي",
            min_value=0.0,
            value=0.0
        )

        reason = st.text_input(
            "سبب التقسيم",
            value="دية عامة"
        )

        if amount > 0 and total > 0:

            share = amount / total

            st.metric(
                "💰 حصة الفرد الواحد",
                f"{share:,.2f} ريال"
            )

            df = pd.DataFrame(st.session_state.members_db)

            df["المبلغ المستحق"] = round(share, 2)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            csv = df.to_csv(index=False).encode("utf-8-sig")

            st.download_button(
                "📥 تحميل التقرير CSV",
                csv,
                file_name="financial_report.csv",
                mime="text/csv"
            )

    # =====================================================
    # التبويب الثاني
    # =====================================================
    with tab2:

        st.subheader("👥 إضافة عضو جديد")

        new_name = st.text_input(
            "اسم العضو"
        )

        new_code = st.text_input(
            "كود العائلة"
        )

        new_paid = st.selectbox(
            "تم دفع الصندوق؟",
            ["نعم", "لا"]
        )

        new_gender = st.selectbox(
            "الجنس",
            ["ذكر", "أنثى"]
        )

        if st.button("➕ إضافة العضو"):

            if new_name.strip() and new_code.strip():

                st.session_state.members_db.append({
                    "الاسم": new_name.strip(),
                    "كود العائلة": new_code.strip(),
                    "تم دفع الصندوق": new_paid,
                    "الجنس": new_gender
                })

                st.success("✅ تمت إضافة العضو")
                st.rerun()

            else:
                st.error("❌ يرجى تعبئة جميع الحقول")

        st.markdown("---")

        st.subheader("📋 قائمة الأعضاء")

        if len(st.session_state.members_db) > 0:

            for i, member in enumerate(st.session_state.members_db):

                c1, c2, c3, c4, c5 = st.columns([3,2,2,2,1])

                c1.write(member["الاسم"])
                c2.write(member["كود العائلة"])
                c3.write(member["تم دفع الصندوق"])
                c4.write(member["الجنس"])

                with c5:

                    if st.button("🗑️", key=f"delete_{i}"):

                        st.session_state.members_db.pop(i)

                        st.warning(
                            f"تم حذف العضو {member['الاسم']}"
                        )

                        st.rerun()

    # =====================================================
    # التبويب الثالث
    # =====================================================
    with tab3:

        st.subheader("📊 التقارير والفرز")

        report_df = pd.DataFrame(
            st.session_state.members_db
        )

        if not report_df.empty:

            pay_filter = st.selectbox(
                "فلترة حسب الدفع",
                ["الكل", "نعم", "لا"]
            )

            gender_filter = st.selectbox(
                "فلترة حسب الجنس",
                ["الكل", "ذكر", "أنثى"]
            )

            filtered_df = report_df.copy()

            if pay_filter != "الكل":

                filtered_df = filtered_df[
                    filtered_df["تم دفع الصندوق"] == pay_filter
                ]

            if gender_filter != "الكل":

                filtered_df = filtered_df[
                    filtered_df["الجنس"] == gender_filter
                ]

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

            csv_report = filtered_df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "📥 تحميل التقرير",
                csv_report,
                file_name="members_report.csv",
                mime="text/csv"
            )

        else:
            st.info("لا توجد بيانات")

    # =====================================================
    # التبويب الرابع
    # =====================================================
    with tab4:

        st.subheader("🔐 إدارة المستخدمين")

        new_user = st.text_input(
            "اسم المستخدم الجديد"
        )

        new_pass = st.text_input(
            "كلمة المرور",
            type="password"
        )

        if st.button("✅ إنشاء المستخدم"):

            if new_user.strip() and new_pass.strip():

                if new_user in st.session_state.users_db:

                    st.error("المستخدم موجود مسبقاً")

                else:

                    st.session_state.users_db[new_user] = new_pass

                    st.success(
                        f"✅ تم إنشاء المستخدم {new_user}"
                    )

            else:
                st.error("يرجى تعبئة جميع الحقول")

        st.markdown("---")

        st.subheader("👤 المستخدمون الحاليون")

        users_df = pd.DataFrame({
            "اسم المستخدم":
            list(st.session_state.users_db.keys())
        })

        st.dataframe(
            users_df,
            use_container_width=True,
            hide_index=True
        )
