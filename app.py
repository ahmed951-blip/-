import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) وتنظيم الخطوط والأزرار والواجهات بشكل مستقر
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; }
    .main-btn>div>button { background-color: #2e7d32; color: white; border-radius: 8px; padding: 10px; }
    .excel-btn>div>button { background-color: #1f7244; color: white; border-radius: 8px; font-weight: bold; }
    .word-btn>div>button { background-color: #2b579a; color: white; border-radius: 8px; font-weight: bold; }
    .pdf-btn>div>button { background-color: #b71c1c; color: white; border-radius: 8px; font-weight: bold; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; border-radius: 5px; height: 38px; }
    .login-box { max-width: 450px; margin: 0 auto; padding: 25px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; justify-content: flex-start; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة قاعدة البيانات الأساسية للمسؤولين والأعضاء (Session State)
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "123", "role": "مسؤول رئيسي"}
    }

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

# حساب الإحصائيات العامة الديناميكية لإظهارها بالأعلى دائماً
total_registered_members = len(st.session_state.members_db)
# افتراضياً: يتم حساب المبالغ المتوفرة بالصندوق بناءً على من قام بالدفع (500 ريال لكل من دفع "نعم")
total_fund_amount = sum(500 for member in st.session_state.members_db if member["تم دفع الصندوق"] == "نعم")

# ==========================================
# 📊 الإحصائيات العامة الثابتة في أعلى الموقع لجميع الزوار
# ==========================================
st.markdown("### 📊 إحصائيات صندوق جماعة معلين العامة")
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.metric(label="👥 إجمالي الأعضاء المسجلين حالياً", value=f"{total_registered_members} فرد")
with col_top2:
    st.metric(label="💰 إجمالي المبلغ المتوفر بالصندوق (تقديري)", value=f"{total_fund_amount:,.2f} ريال")
st.markdown("---")


# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
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
                st.success("تم التحقق بنجاح.. جاري الدخول")
                st.rerun()
            else:
                st.error("كلمة السر التي أدخلتها غير صحيحة.")
        else:
            st.error("اسم المستخدم غير مسجل بالنظام.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 💻 واجـهـة الـمـوقـع الـرئـيـسـيـة بـعـد الـدخـول
# ==========================================
else:
    # شريط علوي لعرض اسم المستخدم الحالي وزر تسجيل الخروج
    col_header, col_logout = st.columns()
    with col_header:
        st.subheader(f"👋 مرحباً بك: {st.session_state.current_user} ({st.session_state.user_role})")
    with col_logout:
        if st.button("🚪 تسجيل الخروج", key="logout_btn_top"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.user_role = ""
            st.rerun()
            
    st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
    st.markdown("---")

    # تحويل قاعدة البيانات الحالية إلى DataFrame لسهولة العرض والفرز
    df_current = pd.DataFrame(st.session_state.members_db)

    # إنشاء التبويبات الأربعة الثابتة والمستقرة لتفادي انهيار الصفحة وعيوب العرض
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 1. حساب وتقسيم المبالغ", 
        "👥 2. إدارة وإضافة الأعضاء", 
        "📊 3. استخراج التقارير المتقدمة",
        "🔒 4. صلاحيات وحسابات المستخدمين"
    ])

    # ------------------------------------------
    # التبويب الأول: الحسابات والتقسيم المالي
    # ------------------------------------------
    with tab1:
        st.subheader("💵 إدخال المبالغ وتقسيمها بالتساوي")
        total_members = len(st.session_state.members_db)
        st.info(f"📊 إجمالي عدد أعضاء الجماعة المستحقين للتقسيم: **{total_members} فرد**")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            total_amount = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=100.0, key="calc_amount_input")
        with col_m2:
            reason = st.text_input("سبب أو مناسبة التقسيم:", value="دية عامة", key="calc_reason_input")

        if total_amount > 0 and total_members > 0:
            share_per_member = total_amount / total_members
            st.markdown("### 📊 نتيجة التوزيع المالي الإجمالي:")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric(label="💰 نصيب الفرد الواحد الحالي", value=f"{share_per_member:,.2f} ريال")
            with col_s2:
                st.metric(label="👥 عدد الأفراد المستحقين الفعلي", value=f"{total_members} فرد")
                
            df_calc = df_current.copy()
            df_calc["المبلغ المستحق (ريال)"] = round(share_per_member, 2)
            st.markdown("#### 📋 جدول تفصيل توزيع المستحقات:")
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
        elif total_amount == 0:
            st.warning("يرجى كتابة مبلغ أكبر من الصفر لبدء حساب وتقسيم الحصص المالية.")

    # ------------------------------------------
    # التبويب الثاني: إدارة وإضافة الأعضاء
    # ------------------------------------------
    with tab2:
        st.subheader("➕ إضافة عضو جديد لجماعة معلين")
        col_in1, col_in2, col_in3, col_in4 = st.columns(4)
        with col_in1:
            mem_name = st.text_input("اسم العضو الثلاثي:", placeholder="مثال: علي محمد المعلي", key="add_mem_name")
        with col_in2:
            mem_code = st.text_input("كود العائلة:", placeholder="مثال: A1", key="add_mem_code")
        with col_in3:
            mem_paid = st.selectbox("تم دفع مبلغ الصندوق؟", ["نعم", "لا"], key="add_mem_paid")
        with col_in4:
            mem_gender = st.selectbox("الجنس:", ["ذكر", "أنثى"], key="add_mem_gender")
            
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        add_btn = st.button("➕ تسجيل العضو في النظام", key="submit_new_member_btn")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if add_btn:
            if mem_name.strip() != "" and mem_code.strip() != "":
                if not any(d['الاسم'] == mem_name.strip() for d in st.session_state.members_db):
                    new_entry = {"الاسم": mem_name.strip(), "كود العائلة": mem_code.strip().upper(), "تم دفع الصندوق": mem_paid, "الجنس": mem_gender}
                    st.session_state.members_db.append(new_entry)
                    st.success(f"تم تسجيل العضو 【 {mem_name} 】 بنجاح.")
                    st.rerun()
                else:
                    st.warning("هذا الاسم مسجل مسبقاً في النظام.")
            else:
                st.error("يرجى ملء حقول الاسم وكود العائلة أولاً.")

        st.markdown("---")
        st.subheader("📋 قائمة التحكم بالأعضاء وحذفهم المباشر")
        if len(st.session_state.members_db) > 0:
            for idx, member in enumerate(st.session_state.members_db):
                col_show, col_del_btn = st.columns()
                with col_show:
                    st.info(f"👤 **{member['الاسم']}** | 🏠 كود العائلة: {member['كود العائلة']} | 💰 دفع الصندوق: {member['تم دفع الصندوق']} | 🧬 الجنس: {member['الجنس']}")
                with col_del_btn:
                    st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                    if st.button("🗑️ حذف", key=f"del_mem_secure_{idx}", use_container_width=True):
                        st.session_state.members_db.pop(idx)
                        st.success(f"تم الحذف بنجاح.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("لا يوجد أعضاء مسجلين حالياً.")

