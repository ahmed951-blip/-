
import streamlit as st
import pandas as pd
import base64

# 1. إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) وتنظيم الخطوط والأزرار
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; }
    .main-btn>div>button { background-color: #2e7d32; color: white; border-radius: 8px; padding: 10px; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; border-radius: 5px; height: 38px; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; justify-content: flex-start; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# عنوان التطبيق الرئيسي
st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
st.markdown("---")

# 2. إدارة قاعدة البيانات المؤقتة في الذاكرة الحالية للبرنامج
if 'members_db' not in st.session_state:
    st.session_state.members_db = [
        {"الاسم": "أحمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "محمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "لا", "الجنس": "ذكر"},
        {"الاسم": "فاطمة المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "أنثى"},
        {"الاسم": "سعيد المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "خالد المعلي", "كود العائلة": "C3", "تم دفع الصندوق": "لا", "الجنس": "ذكر"}
    ]

# تحويل البيانات إلى جدول pandas
df_current = pd.DataFrame(st.session_state.members_db)

# إنشاء التبويبات الثلاثة لتنظيم الموقع
tab_calc, tab_manage, tab_reports = st.tabs([
    "💰 1. حساب وتقسيم المبالغ", 
    "👥 2. إدارة وإضافة الأعضاء", 
    "📊 3. التقارير والفرز المتقدم (PDF)"
])

# ==========================================
# التبويب الأول: الحسابات والتقسيم المالي
# ==========================================
with tab_calc:
    st.subheader("💵 إدخال المبالغ وتقسيمها بالتساوي على الجميع")
    total_members = len(st.session_state.members_db)
    st.info(f"📊 إجمالي عدد أعضاء الجماعة المسجلين في النظام: **{total_members} فرد**")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        total_amount = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=100.0)
    with col_m2:
        reason = st.text_input("سبب أو مناسبة التقسيم:", value="دية عامة")

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

# ==========================================
# التبويب الثاني: إدارة وإضافة الأعضاء مع خيار الحذف
# ==========================================
with tab_manage:
    st.subheader("➕ إضافة عضو جديد للجماعة")
    
    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    with col_in1:
        mem_name = st.text_input("اسم العضو الثلاثي:", placeholder="مثال: علي محمد المعلي")
    with col_in2:
        mem_code = st.text_input("كود العائلة:", placeholder="مثال: A1")
    with col_in3:
        mem_paid = st.selectbox("تم دفع مبلغ الصندوق؟", ["نعم", "لا"])
    with col_in4:
        mem_gender = st.selectbox("الجنس:", ["ذكر", "أنثى"])
        
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    add_btn = st.button("➕ تسجيل العضو في النظام")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if add_btn:
        if mem_name.strip() != "" and mem_code.strip() != "":
            if not any(d['الاسم'] == mem_name.strip() for d in st.session_state.members_db):
                new_entry = {
                    "الاسم": mem_name.strip(),
                    "كود العائلة": mem_code.strip().upper(),
                    "تم دفع الصندوق": mem_paid,
                    "الجنس": mem_gender
                }
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
            col_show, col_del_btn = st.columns([5, 1])
            with col_show:
                st.info(f"👤 **{member['الاسم']}** | 🏠 كود العائلة: {member['كود العائلة']} | 💰 دفع الصندوق: {member['تم دفع الصندوق']} | 🧬 الجنس: {member['الجنس']}")
            with col_del_btn:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("🗑️ حذف", key=f"del_mem_{idx}", use_container_width=True):
                    removed = st.session_state.members_db.pop(idx)
                    st.success(f"تم حذف {removed['الاسم']} بنجاح.")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("لا يوجد أعضاء مسجلين حالياً.")

# ==========================================
# التبويب الثالث: التقارير والفرز المتقدم وتصدير PDF
# ==========================================
with tab_reports:
    st.subheader("📊 لوحة التقارير والفرز وتصدير كشف الأسماء")
    
    if len(st.session_state.members_db) > 0:
        st.markdown("#### 🔍 حدد خيارات ترتيب وفلترة كشف أسماء الجماعة المستخرجة:")
        
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            sort_option = st.selectbox("🎯 خيار فرز وترتيب القائمة:", ["أبجدي (حسب الاسم)", "حسب كود العائلة", "حسب الجنس", "بدون ترتيب"])
        with col_f2:
            filter_family = st.selectbox("🏠 تصفية لعائلة محددة:", ["الكل"] + list(df_current["كود العائلة"].unique()))
        with col_f3:
            filter_gender = st.selectbox("🧬 تصفية للجنس:", ["الكل", "ذكر", "أنثى"])
        with col_f4:
            filter_paid = st.selectbox("💰 دفع الصندوق:", ["الكل", "نعم", "لا"])
            
        # تطبيق عمليات التصفية والفلترة
        df_filtered = df_current.copy()
        if filter_family != "الكل":
            df_filtered = df_filtered[df_filtered["كود العائلة"] == filter_family]
        if filter_gender != "الكل":
            df_filtered = df_filtered[df_filtered["الجنس"] == filter_gender]
        if filter_paid != "الكل":
            df_filtered = df_filtered[df_filtered["تم دفع الصندوق"] == filter_paid]

        # تطبيق خيارات الترتيب والفرز المطلوبة (أبجدي، عائلة، جنس)
        if sort_option == "أبجدي (حسب الاسم)":
            df_filtered = df_filtered.sort_values(by="الاسم")
        elif sort_option == "حسب كود العائلة":
            df_filtered = df_filtered.sort_values(by="كود العائلة")
        elif sort_option == "حسب الجنس":
            df_filtered = df_filtered.sort_values(by="الجنس")

        # عرض الكشف المصفى والمرتب أمام المستخدم
        st.markdown(f"### 📋 كشف الأسماء المفرز الحالي ({len(df_filtered)} عضو مطابق):")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        # دالة ذكية لتوليد ملف PDF متوافق 100% مع اللغة العربية والاتجاهات
        def convert_df_to_pdf_html(dataframe, current_sort):
            rows_html = ""
            for index, row in dataframe.iterrows():
                rows_html += f"""
                <tr>
                    <td>{row['الاسم']}</td>
                    <td>{row['كود العائلة']}</td>
                    <td>{row['تم دفع الصندوق']}</td>
                    <td>{row['الجنس']}</td>
                </tr>
                """
            
            html_content = f"""
            <html dir="rtl" lang="ar">
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Arial', sans-serif; text-align: right; padding: 30px; direction: rtl; }}
                    h2 {{ color: #2e7d32; border-bottom: 3px solid #2e7d32; padding-bottom: 12px; text-align: center; }}
                    .meta-info {{ margin-bottom: 25px; font-size: 15px; background: #f9f9f9; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                    th, td {{ border: 1px solid #cccccc; padding: 12px; text-align: right; font-size: 14px; }}
                    th {{ background-color: #2e7d32; color: white; font-weight: bold; }}
                    tr:nth-child(even) {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h2>تقرير كشف أسماء جماعة معلين الرسمي</h2>
                <div class="meta-info">
                    <strong>آلية الفرز المتبعة:</strong> {current_sort}<br>
                    <strong>عدد أفراد الجماعة المشمولين في التقرير:</strong> {len(dataframe)} فرد مسجل<br>
                </div>
                <table>
                    <thead>
