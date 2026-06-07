import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) وتحسين مظهر الواجهات والأزرار الإحصائية والمالية
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

# 2. تهيئة قاعدة البيانات الأساسية في الذاكرة (Session State)
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

# حساب الإحصائيات العامة والمالية للموقع
total_members = len(st.session_state.members_db)
males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
females = total_members - males
paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
not_paid = total_members - paid
box_money = paid * 500

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
        else: st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 💻 واجـهـة الـمـوقـع بـعـد الـدخـول
# ==========================================
else:
    if st.button("🚪 تسجيل الخروج", key="logout_action_btn"):
        st.session_state.logged_in = False
        st.rerun()
            
    st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
    st.markdown("---")

    # 📊 عرض لوحة الإحصائيات العامة والمالية
    st.markdown("### 📊 لوحة الإحصائيات العامة والمالية للموقع")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><b>👥 إجمالي الأعضاء</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{total_members}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><b>👨 عدد الذكور</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{males}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><b>👩 عدد الإناث</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{females}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><b>✅ مسجل بالصندوق</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{paid}</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><b>❌ غير مسجل</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{not_paid}</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><b>💰 مبلغ الصندوق</b><br><span style="font-size:22px; color:#2e7d32; font-weight:bold;">{box_money:,.0f} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    df_current = pd.DataFrame(st.session_state.members_db)
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. حساب وتقسيم المبالغ الجديد", "👥 2. إدارة وإضافة الأعضاء", "📊 3. استخراج التقارير المتقدمة", "🔒 4. صلاحيات وحسابات المستخدمين"])

    # ------------------------------------------
    # التبويب الأول: تقسيم المبالغ الجديد والتقرير الخاص بالتقسيم
    # ------------------------------------------
    with tab1:
        st.subheader("💵 إضافة وتقسيم مبلغ مالي جديد على الجماعة بالتساوي")
        if total_members > 0:
            col_m1, col_m2 = st.columns(2)
            with col_m1: 
                total_amount = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=100.0, key="calc_amount_input_unique")
            with col_m2: 
                reason = st.text_input("سبب أو مناسبة هذا التقسيم المالي:", value="دية عاجلة", key="calc_reason_input_unique")

            if total_amount > 0:
                share_per_member = total_amount / total_members
                st.markdown("### 📊 نتيجة احتساب حصص التوزيع المالي الحالي:")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1: st.metric(label="💰 نصيب الفرد الواحد من هذا المبلغ", value=f"{share_per_member:,.2f} ريال")
                with col_s2: st.metric(label="👥 إجمالي عدد أفراد الجماعة المستحقين", value=f"{total_members} فرد")
                
                df_calc = df_current.copy()
                df_calc["المبلغ المطلوب سداده (ريال)"] = round(share_per_member, 2)
                
                st.markdown("#### 📋 كشف تفصيلي بتوزيع المبالغ الحالية:")
                st.dataframe(df_calc, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("### 🖨️ طباعة المستند والتقرير الخاص بهذا التقسيم المالي")
                st.caption("اضغط على الزر الأحمر بالأسفل، لفتح نافذة طباعة مستند الـ PDF الخاص بهذا التقسيم بالتحديد.")
                
                # تم حل مشكلة الـ f-string السابقة عبر تجزئة بناء القوالب بشكل هندسي بسيط ونظيف
                pdf_rows_html = ""
                for _, r in df_calc.iterrows():
                    pdf_rows_html += f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{share_per_member:,.2f} ريال</td></tr>"
                
                # تجميع تقرير ملف الطباعة النهائي
                financial_pdf_report = '<html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>'
                financial_pdf_report += "body { font-family: 'Arial', sans-serif; padding: 40px; text-align: right; background-color: #ffffff; } "
                financial_pdf_report += ".header-title { color: #b71c1c; text-align: center; border-bottom: 3px solid #b71c1c; padding-bottom: 12px; font-size: 24px; } "
                financial_pdf_report += f".summary-box {{ background-color: #f8f9fa; border-right: 6px solid #b71c1c; padding: 15px; margin: 20px 0; font-size: 16px; line-height: 1.8; }} "
                financial_pdf_report += "table { width:100%; border-collapse:collapse; margin-top: 25px; } "
                financial_pdf_report += "th, td { border:1px solid #dddddd; padding:12px; font-size:15px; text-align: right; } "
                financial_pdf_report += "th { background-color: #b71c1c; color: white; font-weight: bold; } "
                financial_pdf_report += "tr:nth-child(even) { background-color: #f2f2f2; } "
                financial_pdf_report += ".print-button { display:block; width:100%; padding:15px; background-color:#1976d2; color:white; font-size:18px; font-weight:bold; text-align:center; border:none; border-radius:8px; cursor:pointer; margin-bottom:25px; } "
                financial_pdf_report += "@media print { .print-button { display:none; } } "
                financial_pdf_report += f'</style></head><body><button class="print-button" onclick="window.print()">🖨️ اضغط هنا الآن لحفظ هذا التقرير المالي كملف PDF</button>'
                financial_pdf_report += f'<h2 class="header-title">تقرير مالي رسمي خاص بتقسيم المستحقات - جماعة معلين</h2>'
                financial_pdf_report += f'<div class="summary-box"><b>📌 موضوع ومناسبة التقسيم:</b> {reason}<br><b>💰 إجمالي المبلغ المالي المطلوب تقسيمه:</b> {total_amount:,.2f} ريال سعودي<br><b>👥 إجمالي عدد الأفراد المسجلين والمستحقين للسداد:</b> {total_members} فرد<br><b>💵 المطالبة المالية المقررة الفرد الواحد:</b> {share_per_member:,.2f} ريال سعودي بالتساوي<br></div>'
