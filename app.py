import streamlit as st
import pandas as pd
import random

# 1. إعدادات الواجهة الأساسية واللغة العربية الشاملة (RTL)
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL)، تكبير الأيقونات، الخطوط والتبويبات الشاملة
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        direction: rtl !important;
        text-align: right !important;
    }
    h1, h2, h3, h4, font, p, span, label {
        text-align: right !important;
        direction: rtl !important;
    }
    div[data-baseweb="tab-list"] {
        direction: rtl !important;
        justify-content: flex-start !important;
        gap: 15px !important;
    }
    div[data-baseweb="tab"] p {
        font-size: 20px !important; 
        font-weight: bold !important;
    }
    .stButton>button {
        width: 100%;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    .stat-box {
        background-color: #f8f9fa;
        border-right: 6px solid #2e7d32;
        padding: 20px;
        border-radius: 8px;
        text-align: right;
        margin-bottom: 15px;
        box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stMarkdownContainer"] { text-align: right !important; direction: rtl !important; }
    label[data-testid="stWidgetLabel"] { text-align: right !important; direction: rtl !important; font-size: 16px !important; font-weight: bold !important; }
    .delete-btn>div>button { background-color: #d32f2f !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة قواعد البيانات والمفاتيح لضمان ثبات الجلسة وعدم الاختفاء
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"admin": "123"}

if 'members_db' not in st.session_state:
    st.session_state.members_db = [
        {"الاسم": "أحمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "محمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "لا", "الجنس": "ذكر"},
        {"الاسم": "فاطمة المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "أنثى"}
    ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("🔐 لوحة تحكم نظام جماعة معلين الرقمي")
    
    u = st.text_input("اسم المستخدم الحالي:", key="login_u").strip()
    p = st.text_input("كلمة السر الحالية:", type="password", key="login_p").strip()
    
    if st.button("🔓 تسجيل الدخول الآمن للموقع", key="btn_login_submit"):
        if u in st.session_state.users_db and st.session_state.users_db[u] == p:
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح.")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة.")
else:
    # زر الخروج العلوي الآمن
    if st.button("🚪 خروج من النظام", key="btn_logout_top"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("⚖️ النظام الإلكتروني المطور لإدارة المستحقات - جماعة معلين")
    st.markdown("---")

    # 📊 لوحة الإحصائيات العامة المحدثة (محرك الصندوق التلقائي للـ 500 ريال)
    total = len(st.session_state.members_db)
    males = sum(1 for m in st.session_state.members_db if m.get("الجنس") == "ذكر")
    females = total - males
    paid = sum(1 for m in st.session_state.members_db if m.get("تم دفع الصندوق") == "نعم")
    not_paid = total - paid
    box_money = paid * 500  

    st.markdown("### 📊 لوحة الإحصائيات المالية والعامة الحالية للصندوق")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><span style="font-size:24px;">👥</span><br><b>إجمالي الأعضاء</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{total} فرد</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><span style="font-size:24px;">👨</span><br><b>عدد الذكور</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{males} ذكر</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><span style="font-size:24px;">👩</span><br><b>عدد الإناث</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{females} أنثى</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><span style="font-size:24px;">✅</span><br><b>المسجلين بالصندوق</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{paid} عضو</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><span style="font-size:24px;">❌</span><br><b>غير المسجلين</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{not_paid} فرد</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><span style="font-size:24px;">💰</span><br><b>ميزانية الصندوق</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{box_money:,} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # كتل التبويبات الأربعة المحمية كلياً ضد الانهيار
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 1. الحساب والتقسيم المالي", 
        "👥 2. إدارة وتعديل الأعضاء", 
        "📊 3. كشوفات التقارير والفرز", 
        "🔒 4. صلاحيات المستخدمين"
    ])

    # ==========================================
    # 💰 1. الحساب والتقسيم المالي المطور (فرز المبالغ الفوري والـ PDF)
    # ==========================================
    with tab1:
        st.subheader("💵 تقسيم مبلغ مالي معين بالتساوي مع تحديد نظام ترتيب كشف التقرير")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            amt = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال سعودي):", min_value=0.0, value=0.0, key="fin_amt_in")
        with col_m2:
            reason = st.text_input("سبب أو مناسبة أو عنوان هذا التقسيم المالي:", value="دية عاجلة", key="fin_reason_in")
            
        sort_fin_opt = st.selectbox("🎯 نظام ترتيب وفرز كشف التقرير المالي الحالي:", ["بدون ترتيب", "أبجدي (من أ إلى ي)", "حسب كود العائلة", "حسب الجنس", "عشوائي (خلط عشوائي للسجلات)"], key="sort_fin_selectbox_key")
        
        if amt > 0 and total > 0:
            share = amt / total
            st.metric("💰 الحصة المقررة السداد للفرد الواحد حالياً بالتساوي", f"{share:,.2f} ريال")
            
            df_calc = pd.DataFrame(st.session_state.members_db)
            df_calc["المبلغ المستحق سداده (ريال)"] = round(share, 2)
            
            # تطبيق خيارات الفرز المطلوبة الأربعة ديناميكياً
            if sort_fin_opt == "أبجدي (من أ إلى ي)":
                df_calc = df_calc.sort_values(by="الاسم")
            elif sort_fin_opt == "حسب كود العائلة":
                df_calc = df_calc.sort_values(by="كود العائلة")
            elif sort_opt == "حسب الجنس":
                df_calc = df_calc.sort_values(by="الجنس")
            elif sort_fin_opt == "عشوائي (خلط عشوائي للسجلات)":
                df_calc = df_calc.sample(frac=1, random_state=random.randint(1, 1000)).reset_index(drop=True)
                
            st.markdown("#### 📋 جدول المطالبات المالية الحالي بالفرز المختار:")
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
            
            h_rows_fin = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{r['الجنس']}</td><td>{share:,.2f} ريال</td></tr>" for _, r in df_calc.iterrows()])
            html_fin = f'<html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>body {{ font-family: "Arial", sans-serif; padding: 40px; text-align: right; background-color: #ffffff; }} .header-title {{ color: #b71c1c; text-align: center; border-bottom: 3px solid #b71c1c; padding-bottom: 12px; font-size: 24px; }} .summary-box {{ background-color: #f8f9fa; border-right: 6px solid #b71c1c; padding: 15px; margin: 20px 0; font-size: 16px; line-height: 1.8; }} table {{ width:100%; border-collapse:collapse; margin-top: 25px; }} th, td {{ border:1px solid #dddddd; padding:12px; font-size:15px; text-align: right; }} th {{ background-color: #b71c1c; color: white; font-weight: bold; }} tr:nth-child(even) {{ background-color: #f2f2f2; }} .print-button {{ display:block; width:100%; padding:15px; background-color:#1976d2; color:white; font-size:18px; font-weight:bold; text-align:center; border:none; border-radius:8px; cursor:pointer; margin-bottom:25px; }} @media print {{ .print-button {{ display:none; }} }} </style></head><body><button class="print-button" onclick="window.print()">🖨️ اضغط هنا الآن لحفظ وطباعة هذا التقرير المالي كملف PDF مفرز</button><h2 class="header-title">تقرير مالي رسمي خاص بتقسيم المستحقات - جماعة معلين</h2><div class="summary-box"><b>📌 موضوع ومناسبة التقسيم:</b> {reason}<br><b>💰 إجمالي المبلغ المالي المطلوب تقسيمه:</b> {amt:,.2f} ريال سعودي<br><b>👥 إجمالي عدد الأفراد المستحقين للسداد:</b> {total} فرد<br><b>🎯 نظام ترتيب وفرز الكشف المعتمد في هذا المستند:</b> {sort_fin_opt}<br><b>💵 المطالبة المالية المقررة للفرد الواحد:</b> {share:,.2f} ريال سعودي بالتساوي<br></div><table><thead><tr><th>اسم فرد الجماعة</th><th>كود عائلة العضو</th><th>الجنس</th><th>المبلغ المالي المستحق سداده</th></tr></thead><tbody>{h_rows_fin}</tbody></table><br><br><br><p style="text-align:center; font-size:12px; color:#555555;">مستند رسمي صادر إلكترونياً عن نظام إدارة شؤون جماعة معلين الرقمي</p></body></html>'
            
            st.markdown("---")
            st.download_button(f"📥 تحميل مستند تقرير تقسيم ({reason}) كـ PDF مفرز", data=html_fin, file_name=f"تقرير_تقسيم_{reason}.html", mime="text/html", key="dl_fin_pdf", use_container_width=True)

    # ==========================================
    # 👥 2. إدارة وتعديل الأعضاء وحذفهم (معالجة الأحداث الثابتة 100%)
    # ==========================================
