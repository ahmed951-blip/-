import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) وتحسين مظهر الواجهات والأزرار الإحصائية
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; }
    
    .main-btn>div>button { background-color: #2e7d32; color: white; padding: 10px; }
    .excel-btn>div>button { background-color: #1f7244; color: white; font-weight: bold; }
    .word-btn>div>button { background-color: #2b579a; color: white; font-weight: bold; }
    .pdf-btn>div>button { background-color: #b71c1c; color: white; border-radius: 8px; font-weight: bold; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; height: 38px; }
    
    .login-box { max-width: 450px; margin: 0 auto; padding: 25px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; justify-content: flex-start; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    
    .stat-box { background-color: #f8f9fa; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px; text-align: right; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة قواعد البيانات والمفاتيح في الذاكرة لضمان الاستقرار الشامل ومنع اختفاء البيانات
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"admin": "123"}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'members_db' not in st.session_state:
    st.session_state.members_db = [
        {"الاسم": "أحمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "محمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "لا", "الجنس": "ذكر"},
        {"الاسم": "فاطمة المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "أنثى"}
    ]

# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("🔐 تسجيل الدخول - نظام جماعة معلين")
    
    u_input = st.text_input("اسم المستخدم:", key="login_u").strip()
    p_input = st.text_input("كلمة السر:", type="password", key="login_p").strip()
    
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("دخول للنظام", key="login_action_btn"):
        if u_input in st.session_state.users_db and st.session_state.users_db[u_input] == p_input:
            st.session_state.logged_in = True
            st.success("تم التحقق بنجاح..")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 💻 واجـهـة الـمـوقـع بـعـد الـدخـول
# ==========================================
else:
    # زر تسجيل الخروج العلوي منفصل ومستقر
    if st.button("🚪 تسجيل الخروج", key="logout_action_btn"):
        st.session_state.logged_in = False
        st.rerun()
            
    st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
    st.markdown("---")

    # 📊 لوحة الإحصائيات العامة والمالية للموقع
    total_members = len(st.session_state.members_db)
    males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
    females = total_members - males
    paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
    not_paid = total_members - paid
    box_money = paid * 500

    st.markdown("### 📊 لوحة الإحصائيات العامة والمالية للموقع")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><b>👥 إجمالي الأعضاء</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{total_members}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><b>👨 عدد الذكور</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{males}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><b>👩 عدد الإناث</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{females}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><b>✅ مسجل بالصندوق</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{paid}</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><b>❌ غير مسجل</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{not_paid}</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><b>💰 مبلغ الصندوق</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{box_money:,.0f} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # تحويل الحالات الحالية لعرضها بوضوح
    df_current = pd.DataFrame(st.session_state.members_db)
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. حساب وتقسيم المبالغ", "👥 2. إدارة وإضافة الأعضاء", "📊 3. استخراج التقارير المتقدمة", "🔒 4. صلاحيات وحسابات المستخدمين"])

    # ------------------------------------------
    # التبويب الأول: الحسابات والتقسيم المالي
    # ------------------------------------------
    with tab1:
        st.subheader("💵 إدخال المبالغ وتقسيمها بالتساوي")
        if total_members > 0:
            col_m1, col_m2 = st.columns(2)
            with col_m1: total_amount = st.number_input("أدخل المبلغ المالي الإجمالي مراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=100.0, key="calc_amount_input")
            with col_m2: reason = st.text_input("سبب أو مناسبة التقسيم:", value="دية عامة", key="calc_reason_input")

            if total_amount > 0:
                share_per_member = total_amount / total_members
                st.markdown("### 📊 نتيجة التوزيع المالي الإجمالي:")
                col_s1, col_s2 = st.columns(2)
                with col_s1: st.metric(label="💰 نصيب الفرد الواحد الحالي", value=f"{share_per_member:,.2f} ريال")
                with col_s2: st.metric(label="👥 عدد الأفراد المستحقين الفعلي", value=f"{total_members} فرد")
                
                df_calc = df_current.copy()
                df_calc["المبلغ المستحق (ريال)"] = round(share_per_member, 2)
                st.dataframe(df_calc, use_container_width=True, hide_index=True)
        else: st.error("قائمة الأسماء فارغة.")

    # ------------------------------------------
    # التبويب الثاني: إدارة وإضافة الأعضاء (حل مشكلة عدم الاستجابة بشكل كامل)
    # ------------------------------------------
    with tab2:
        st.subheader("➕ إضافة عضو جديد لجماعة معلين")
        
        # حقول الإدخال مع ربطها بمعرفات فريدة مستقلة تماماً
        add_name = st.text_input("اسم العضو الثلاثي الكامل:", key="txt_add_name_unique")
        add_code = st.text_input("كود العائلة:", key="txt_add_code_unique")
        add_paid = st.selectbox("تم دفع مبلغ الصندوق؟", ["نعم", "لا"], key="sel_add_paid_unique")
        add_gender = st.selectbox("الجنس:", ["ذكر", "أنثى"], key="sel_add_gender_unique")
        
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("➕ تسجيل واعتماد العضو في النظام", key="execute_add_member_btn"):
            if add_name.strip() != "" and add_code.strip() != "":
                # التحقق الآمن من عدم التكرار
                if not any(d['الاسم'] == add_name.strip() for d in st.session_state.members_db):
                    st.session_state.members_db.append({
                        "الاسم": add_name.strip(),
                        "كود العائلة": add_code.strip().upper(),
                        "تم دفع الصندوق": add_paid,
                        "الجنس": add_gender
                    })
                    st.success("تم تسجيل العضو بنجاح في القائمة.")
                    st.rerun()
                else:
                    st.warning("هذا الاسم مسجل مسبقاً في النظام.")
            else:
                st.error("يرجى ملء حقول الاسم وكود العائلة أولاً لضمان إتمام الإضافة.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 قائمة الأعضاء المسجلين حالياً وخيار الحذف المباشر")
        
        # أخذ نسخة منفصلة مستقرة من قائمة البيانات قبل بدء عملية الحذف لمنع تجميد السيرفر
        members_list_copy = list(st.session_state.members_db)
        
        for idx, member in enumerate(members_list_copy):
            col_show, col_del_btn = st.columns([4, 1])
            with col_show:
                st.info(f"👤 **{member['الاسم']}** | 🏠 عائلة: {member['كود العائلة']} | 💰 الصندوق: {member['تم دفع الصندوق']} | 🧬 الجنس: {member['الجنس']}")
            with col_del_btn:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                # استخدام مفتاح (key) فريد جداً ومحمي يجمع اسم العضو ورقمه الترتيبي لمنع مشكلة Duplicate Widget ID
                if st.button("🗑️ حذف", key=f"delete_member_secure_id_{idx}_{member['الاسم'].replace(' ', '_')}", use_container_width=True):
                    # تصفية وإعادة بناء المصفوفة لحذف العضو المطلوب بأمان
                    st.session_state.members_db = [m for m in st.session_state.members_db if m["الاسم"] != member["الاسم"]]
                    st.success("تم حذف العضو المختار فوراً.")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

