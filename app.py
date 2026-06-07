import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية لتتناسب مع اللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) للواجهة وتلوين أزرار الحذف
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 90%; }
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label { text-align: right; direction: rtl; width: 100%; }
    div[data-testid="stTextInput"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; }
    .main-btn>div>button { background-color: #2e7d32; color: white; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# عنوان التطبيق الرئيسي
st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم المستحقات - جماعة معلين")
st.markdown("---")

# إنشاء تبويبين لتنظيم الواجهة
tab1, tab2 = st.tabs(["💰 حساب وتقسيم المبالغ", "👥 إدارة أسماء الجماعة (إضافة وحذف)"])

# إدارة حالة التطبيق (Session State) لحفظ الأسماء المسجلة
if 'members' not in st.session_state:
    st.session_state.members = ["أحمد المعلي", "محمد المعلي", "سعيد المعلي", "علي المعلي", "خالد المعلي"]

# التبويب الثاني: إدارة الأسماء (الإضافة والحذف المباشر)
with tab2:
    st.subheader("👥 لوحة التحكم في أفراد جماعة معلين")
    
    # نموذج إضافة عضو جديد
    col_input, col_add_btn = st.columns([3, 1])
    with col_input:
        new_member = st.text_input("إضافة اسم فرد جديد للجماعة:", key="add_input", placeholder="اكتب الاسم الثلاثي هنا...")
    with col_add_btn:
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        add_clicked = st.button("➕ إضافة الفرد", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if add_clicked:
            if new_member.strip() != "":
                if new_member.strip() not in st.session_state.members:
                    st.session_state.members.append(new_member.strip())
                    st.success(f"تمت إضافة {new_member} بنجاح.")
                    st.rerun()
                else:
                    st.warning("هذا الاسم موجود بالفعل في القائمة.")
            else:
                st.error("يرجى كتابة اسم صحيح.")

    st.markdown("### 📋 قائمة الأعضاء المسجلين حالياً والتحكم بها:")
    st.caption("يمكنك حذف أي عضو بالضغط على زر الحذف الأحمر بجانب اسمه وتحديث الحسابات فوراً.")
    
    # عرض الأسماء الحالية على شكل جدول مرن يحتوي أزرار الحذف
    if len(st.session_state.members) > 0:
        for idx, member in enumerate(st.session_state.members):
            col_name, col_del = st.columns([3, 1])
            with col_name:
                st.info(f"👤 {member}")
            with col_del:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button(f"🗑️ حذف", key=f"del_{idx}", use_container_width=True):
                    removed_member = st.session_state.members.pop(idx)
                    st.success(f"تم حذف {removed_member} من النظام.")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("لا يوجد أي أعضاء مسجلين في القائمة حالياً. يرجى إضافة أعضاء للبدء.")

# التبويب الأول: الحسابات والتقسيم المالي الديناميكي
with tab1:
    total_members = len(st.session_state.members)
    
    st.subheader("💵 إدخل المبالغ المراد تقسيمها")
    st.info(f"📊 عدد أفراد الجماعة المستحقين حالياً في النظام: **{total_members} فرد**")
    
    # حقول الإدخال المالي
    total_amount = st.number_input("أدخل المبلغ المالي الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, step=50.0)
    reason = st.text_input("سبب أو نوع التقسيم (مثال: دية، عانية، مساهمة دورية):", value="دية عامة")

    if total_amount > 0 and total_members > 0:
        # العملية الحسابية للتقسيم بالتساوي بناء على العدد المحدث
        share_per_member = total_amount / total_members
        
        st.markdown("### 📊 نتيجة التوزيع المالي الدقيق:")
        
        # مربعات العرض الرقمية الإحصائية
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric(label="💰 نصيب الفرد الواحد الحالي", value=f"{share_per_member:,.2f} ريال")
        with col_stat2:
            st.metric(label="👥 إجمالي عدد المستحقين الفعلي", value=f"{total_members} أفراد")
            
        # إنشاء جدول التوزيع الديناميكي
        distribution_data = {
            "اسم الفرد من جماعة معلين": st.session_state.members,
            "المبلغ المستحق (ريال)": [round(share_per_member, 2)] * total_members
        }
        df = pd.DataFrame(distribution_data)
        
        st.markdown("#### 📋 جدول تفصيل التوزيع:")
        st.dataframe(df, use_container_width=True)
        
        # ميزة بديلة ذكية ومستقرة للتقارير: تصدير ملف كشف الحساب والجدول متوافق تماماً مع إكسيل وباللغة العربية
        st.markdown("### 🖨️ طباعة وتصدير السجلات والمستندات")
        
        # تحويل الجدول لملف CSV يدعم العربية بشكل كامل عبر ترميز utf-8-sig
        csv = df.to_csv(index=False).encode('utf-8-sig')
        
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        st.download_button(
            label="📥 تحميل كشف التوزيع المالي المحدث لـ Excel (CSV)",
            data=csv,
            file_name=f"تقرير_تقسيم_{reason}_جماعة_معلين.csv",
            mime='text/csv',
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif total_amount == 0:
        st.warning("يرجى كتابة مبلغ أكبر من الصفر في الحقل أعلاه لحساب حصص الأفراد وتفعيل التقرير للتحميل.")
    elif total_members == 0:
        st.error("قائمة الأسماء فارغة حالياً. لا توجد أسماء لتقسيم المبلغ المالي عليها، يرجى إضافة أفراد للجماعة أولاً.")
