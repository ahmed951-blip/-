import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) وتحسين مظهر البطاقات الإحصائية والأزرار
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; }
    
    .main-btn>div>button { background-color: #2e7d32; color: white; padding: 10px; }
    .excel-btn>div>button { background-color: #1f7244; color: white; font-weight: bold; }
    .word-btn>div>button { background-color: #2b579a; color: white; font-weight: bold; }
    .pdf-btn>div>button { background-color: #b71c1c; color: white; font-weight: bold; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; height: 38px; }
    .edit-btn>div>button { background-color: #f57c00; color: white; border: none; height: 38px; }
    
    .login-box { max-width: 450px; margin: 0 auto; padding: 25px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; justify-content: flex-start; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    
    .stat-card { background-color: #f8f9fa; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); margin-bottom: 10px; text-align: right; }
    .stat-title { font-size: 14px; color: #6c757d; font-weight: bold; }
    .stat-value { font-size: 22px; color: #2e7d32; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة قاعدة البيانات الأساسية في الذاكرة (Session State)
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"admin": {"password": "123", "role": "مسؤول رئيسي"}}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""

if 'members_db' not in st.session_state:
    st.session_state.members_db = [
        {"الاسم": "أحمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "محمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "لا", "الجنس": "ذكر"},
        {"الاسم": "فاطمة المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "أنثى"}
    ]

if 'editing_idx' not in st.session_state:
    st.session_state.editing_idx = None

# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("🔐 تسجيل الدخول للوحة التحكم")
    
    username_input = st.text_input("اسم المستخدم:", key="login_username").strip()
    password_input = st.text_input("كلمة السر:", type="password", key="login_password").strip()
    
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    login_btn = st.button("دخول للنظام")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if login_btn:
        if username_input in st.session_state.users_db:
            if st.session_state.users_db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.current_user = username_input
                st.session_state.user_role = st.session_state.users_db[username_input]["role"]
                st.success("تم الدخول بنجاح..")
                st.rerun()
            else: st.error("كلمة السر غير صحيحة.")
        else: st.error("اسم المستخدم غير مسجل.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 💻 واجـهـة الـمـوقـع بـعـد الـدخـول
# ==========================================
else:
    # تم ضبط وتحديد رقم 2 لإنشاء عمودين متناسقين تماماً
    col_header, col_logout = st.columns(2)
    with col_header: st.subheader(f"👋 مرحباً بك: {st.session_state.current_user} ({st.session_state.user_role})")
    with col_logout:
        if st.button("🚪 تسجيل الخروج", key="logout_btn_top"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.user_role = ""
            st.session_state.editing_idx = None
            st.rerun()
            
    st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
    st.markdown("---")

    # 📊 لوحة الإحصائيات العامة والمالية للموقع
    total_registered_members = len(st.session_state.members_db)
    total_males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
    total_females = sum(1_for_m_in_st.session_state.members_db_if_m["الجنس"] == "أنثى")
    total_paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
    total_not_paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "لا")
    total_fund_amount = total_paid * 500

    st.markdown("### 📊 لوحة الإحصائيات العامة والمالية للموقع")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.markdown(f'<div class="stat-card"><div class="stat-title">👥 إجمالي الأعضاء</div><div class="stat-value">{total_registered_members}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><div class="stat-title">👨 عدد الذكور</div><div class="stat-value">{total_males}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><div class="stat-title">👩 عدد الإناث</div><div class="stat-value">{total_females}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card"><div class="stat-title">✅ المسجلين بالصندوق</div><div class="stat-value">{total_paid}</div></div>', unsafe_allow_html=True)
    with c5: st.markdown(f'<div class="stat-card"><div class="stat-title">❌ غير المسجلين بالصندوق</div><div class="stat-value">{total_not_paid}</div></div>', unsafe_allow_html=True)
    with c6: st.markdown(f'<div class="stat-card"><div class="stat-title">💰 ميزانية الصندوق</div><div class="stat-value">{total_fund_amount:,.0f} ر.س</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    df_current = pd.DataFrame(st.session_state.members_db)
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. حساب وتقسيم المبالغ", "👥 2. إدارة وإضافة الأعضاء", "📊 3. استخراج التقارير المتقدمة", "🔒 4. صلاحيات وحسابات المستخدمين"])

    # ------------------------------------------
    # التبويب الأول: الحسابات والتقسيم المالي
    # ------------------------------------------
    with tab1:
        st.subheader("💵 إدخال المبالغ وتقسيمها بالتساوي")
        if total_registered_members > 0:
            col_m1, col_m2 = st.columns(2)
            with col_m1: total_amount = st.number_input("أدخل المبلغ المالي الإجمالي (ريال):", min_value=0.0, value=0.0, step=100.0, key="calc_amount_input")
            with col_m2: reason = st.text_input("سبب أو مناسبة التقسيم:", value="دية عامة", key="calc_reason_input")

            if total_amount > 0:
                share_per_member = total_amount / total_registered_members
                st.markdown("### 📊 نتيجة التوزيع المالي الإجمالي:")
                col_s1, col_s2 = st.columns(2)
                with col_s1: st.metric(label="💰 نصيب الفرد الواحد الحالي", value=f"{share_per_member:,.2f} ريال")
                with col_s2: st.metric(label="👥 عدد الأفراد المستحقين الفعلي", value=f"{total_registered_members} فرد")
                df_calc = df_current.copy()
                df_calc["المبلغ المستحق (ريال)"] = round(share_per_member, 2)
                st.dataframe(df_calc, use_container_width=True, hide_index=True)
        else: st.error("قائمة الأسماء فارغة.")

    # ------------------------------------------
    # التبويب الثاني: إدارة وإضافة الأعضاء (إصلاح الأقواس الحاسم للأعضاء)
    # ------------------------------------------
    with tab2:
        if st.session_state.editing_idx is not None:
            st.subheader("📝 تعديل بيانات العضو الحالي")
            edit_data = st.session_state.members_db[st.session_state.editing_idx]
            
            e_name = st.text_input("الاسم الثلاثي المحدث:", value=edit_data["الاسم"], key="input_edit_name")
            e_code = st.text_input("كود العائلة المحدث:", value=edit_data["كود العائلة"], key="input_edit_code")
            e_paid = st.selectbox("حالة الصندوق:", ["نعم", "لا"], index=["نعم", "لا"].index(edit_data["تم دفع الصندوق"]), key="select_edit_paid")
            e_gender = st.selectbox("الجنس:", ["ذكر", "أنثى"], index=["ذكر", "أنثى"].index(edit_data["الجنس"]), key="select_edit_gender")
            
            col_ef1, col_ef2 = st.columns(2)
            with col_ef1:
                if st.button("💾 حفظ التعديلات المحدثة", key="btn_save_member_changes"):
                    if e_name.strip() != "" and e_code.strip() != "":
                        st.session_state.members_db[st.session_state.editing_idx] = {
                            "الاسم": e_name.strip(),
                            "كود العائلة": e_code.strip().upper(),
                            "تم دفع الصندوق": e_paid,
                            "الجنس": e_gender
                        }
                        st.session_state.editing_idx = None
                        st.success("تم تحديث البيانات.")
                        st.rerun()
            with col_ef2:
                if st.button("❌ إلغاء التعديل", key="btn_cancel_member_edit"):
                    st.session_state.editing_idx = None
                    st.rerun()
        else:
