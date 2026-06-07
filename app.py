import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية وتنسيق المظهر
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق تصميم مرئي منظم من اليمين إلى اليسار (RTL) وتنسيق الأزرار والجداول
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 95%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; }
    .main-btn>div>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; border-radius: 5px; height: 38px; }
    .stTabs [data-baseweb="tab-list"] { direction: rtl; justify-content: flex-start; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# عنوان النظام الرئيسي
st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
st.markdown("---")

# 2. إدارة قاعدة البيانات المؤقتة (Session State)
# نستخدم هيكلة تحتوي على (الاسم، كود العائلة، حالة الدفع، الجنس)
if 'members_db' not in st.session_state:
    st.session_state.members_db = [
        {"الاسم": "أحمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "محمد المعلي", "كود العائلة": "A1", "تم دفع الصندوق": "لا", "الجنس": "ذكر"},
        {"الاسم": "فاطمة المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "أنثى"},
        {"الاسم": "سعيد المعلي", "كود العائلة": "B2", "تم دفع الصندوق": "نعم", "الجنس": "ذكر"},
        {"الاسم": "خالد المعلي", "كود العائلة": "C3", "تم دفع الصندوق": "لا", "الجنس": "ذكر"}
    ]

# تحويل البيانات الحالية إلى DataFrame لسهولة المعالجة والفرز
df_current = pd.DataFrame(st.session_state.members_db)

# إنشاء التبويبات لتنظيم واجهة الموقع بشكل مرتب ومنفصل
tab_calc, tab_manage, tab_reports = st.tabs([
    "💰 1. حساب وتقسيم المبالغ", 
    "👥 2. إدارة وإضافة الأعضاء", 
    "📊 3. التقارير والفرز المتقدم"
])

# ==========================================
# التبويب الأول: الحسابات والتقسيم المالي
# ==========================================
with tab_calc:
    st.subheader("💵 إدخال المبالغ وتقسيمها بالتساوي")
    total_members = len(st.session_state.members_db)
    st.info(f"📊 إجمالي عدد أعضاء الجماعة المسجلين حالياً: **{total_members} فرد**")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        total_amount = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=100.0)
    with col_m2:
        reason = st.text_input("سبب أو مناسبة التقسيم:", value="دية عامة")

    if total_amount > 0 and total_members > 0:
        share_per_member = total_amount / total_members
        
        # عرض الإحصائيات المالية
        st.markdown("### 📊 نتيجة التوزيع المالي الإجمالي:")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric(label="💰 نصيب الفرد الواحد من المبلغ", value=f"{share_per_member:,.2f} ريال")
        with col_s2:
            st.metric(label="👥 عدد الأفراد المستحقين", value=f"{total_members} فرد")
            
        # جدول الحصص
        df_calc = df_current.copy()
        df_calc["المبلغ المستحق (ريال)"] = round(share_per_member, 2)
        
        st.markdown("#### 📋 جدول تفصيل توزيع المستحقات:")
        st.dataframe(df_calc, use_container_width=True, hide_index=True)
    elif total_amount == 0:
        st.warning("يرجى كتابة مبلغ أكبر من الصفر لبدء حساب وتقسيم الحصص المالية.")

# ==========================================
# التبويب الثاني: إدارة وإضافة الأعضاء مع الحذف
# ==========================================
with tab_manage:
    st.subheader("➕ إضافة عضو جديد للجماعة")
    
    # واجهة الإدخال مرتبة على شكل أعمدة أفقية
    col_in1, col_in2, col_in3, col_in4 = st.columns([3, 2, 2, 2])
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
            # التحقق من عدم تكرار الاسم
            if not any(d['الاسم'] == mem_name.strip() for d in st.session_state.members_db):
                new_entry = {
                    "الاسم": mem_name.strip(),
                    "كود العائلة": mem_code.strip().upper(),
                    "تم دفع الصندوق": mem_paid,
                    "الجنس": mem_gender
                }
                st.session_state.members_db.append(new_entry)
                st.success(f"تم تسجيل العضو 【 {mem_name} 】 بنجاح في النظام.")
                st.rerun()
            else:
                st.warning("هذا الاسم مسجل مسبقاً في النظام.")
        else:
            st.error("يرجى ملء حقول الاسم وكود العائلة أولاً.")

    st.markdown("---")
    st.subheader("📋 قائمة التحكم بالأعضاء وحذفهم")
    
    if len(st.session_state.members_db) > 0:
        for idx, member in enumerate(st.session_state.members_db):
            col_show, col_del_btn = st.columns([6, 1])
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
# التبويب الثالث: التقارير والفرز المتقدم
# ==========================================
with tab_reports:
    st.subheader("📊 لوحة التقارير والفرز الذكي")
    
    if len(st.session_state.members_db) > 0:
        # خيارات التصفية والفرز
        st.markdown("#### 🔍 حدد خيارات الفرز والتصفية المخصصة لتوليد التقرير:")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sort_option = st.selectbox("🎯 طريقة ترتيب السجلات:", ["أبجدي (حسب الاسم)", "حسب كود العائلة", "بدون ترتيب"])
        with col_f2:
            filter_family = st.selectbox("🏠 تصفية حسب عائلة محددة:", ["الكل"] + list(df_current["كود العائلة"].unique()))
        with col_f3:
            filter_gender = st.selectbox("🧬 تصفية حسب الجنس:", ["الكل", "ذكر", "أنثى"])
            
        col_f4 = st.columns(1)[0]
        with col_f4:
            filter_paid = st.selectbox("💰 تصفية حسب حالة دفع الصندوق:", ["الكل", "نعم", "لا"])

        # تطبيق عمليات التصفية بناء على اختيارات المستخدم
        df_filtered = df_current.copy()
        
        if filter_family != "الكل":
            df_filtered = df_filtered[df_filtered["كود العائلة"] == filter_family]
            
        if filter_gender != "الكل":
            df_filtered = df_filtered[df_filtered["الجنس"] == filter_gender]
            
        if filter_paid != "الكل":
            df_filtered = df_filtered[df_filtered["تم دفع الصندوق"] == filter_paid]

        # تطبيق عمليات الترتيب والفرز
        if sort_option == "أبجدي (حسب الاسم)":
            df_filtered = df_filtered.sort_values(by="الاسم")
        elif sort_option == "حسب كود العائلة":
            df_filtered = df_filtered.sort_values(by="كود العائلة")

        # عرض التقرير المفلتر النهائي
        st.markdown(f"### 📋 التقرير الناتج ({len(df_filtered)} عضو مطابق للفلاتر):")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        # تصدير التقرير الحالي المفرز إلى كشف مالي متوافق مع Excel
        csv_report = df_filtered.to_csv(index=False).encode('utf-8-sig')
        
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        st.download_button(
            label="📥 تحميل هذا التقرير المفرز كملف Excel (CSV)",
            data=csv_report,
            file_name="تقرير_مفرز_جماعة_معلين.csv",
            mime='text/csv',
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("يرجى إضافة أعضاء أولاً في التبويب الثاني لتتمكن من إنشاء وتقسيم التقارير.")
