import streamlit as st
import pandas as pd
import datetime

# 1. إعدادات واجهة المنصة باللغة العربية
st.set_page_config(page_title="صندوق جماعة معلين بني بكر بن وائل", page_icon="💰", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) للغة العربية
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    div[data-testid="stSidebarUserContent"] { direction: rtl; }
    div[data-testid="stAppViewBlockContainer"] { direction: rtl; text-align: right; }
    h1, h2, h3, p, span, label { text-align: right !important; direction: rtl !important; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 نظام كشوفات وصندوق جماعة معلين بني بكر بن وائل")
st.write("منصة رقمية متكاملة لإدارة الاشتراكات، المصاريف، وحسابات الصندوق الجماعي.")

# 2. إدارة البيانات وحفظها مؤقتاً (بإمكانك ربطها بقاعدة بيانات لاحقاً)
if 'members' not in st.session_state:
    st.session_state.members = [
        {"المعرف": 101, "الاسم": "أحمد البكري", "الحالة": "نشط", "إجمالي الاشتراكات": 500},
        {"المعرف": 102, "الاسم": "محمد البكري", "الحالة": "نشط", "إجمالي الاشتراكات": 500},
        {"المعرف": 103, "الاسم": "خالد البكري", "الحالة": "متأخر", "إجمالي الاشتراكات": 200}
    ]

if 'transactions' not in st.session_state:
    st.session_state.transactions = [
        {"التاريخ": "2026-01-01", "النوع": "إيداع (اشتراك)", "المبلغ": 500, "التفاصيل": "اشتراك أحمد البكري"},
        {"التاريخ": "2026-01-02", "النوع": "إيداع (اشتراك)", "المبلغ": 500, "التفاصيل": "اشتراك محمد البكري"},
        {"التاريخ": "2026-01-05", "النوع": "إيداع (اشتراك)", "المبلغ": 200, "التفاصيل": "اشتراك جزئي خالد البكري"},
        {"التاريخ": "2026-01-10", "النوع": "مصروف (مساعدة)", "المبلغ": 400, "التفاصيل": "مساعدة عائلية طارئة"}
    ]

# 3. الحسابات المالية الإجمالية (الملخص التنفيذي)
df_trans = pd.DataFrame(st.session_state.transactions)
total_income = df_trans[df_trans['النوع'].str.contains("إيداع")]['المبلغ'].sum()
total_expense = df_trans[df_trans['النوع'].str.contains("مصروف")]['المبلغ'].sum()
current_balance = total_income - total_expense

# عرض الميزانية الحالية في الأعلى
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="رصيد الصندوق الحالي", value=f"{current_balance:,} ريال")
with col2:
    st.metric(label="إجمالي الإيداعات والاشتراكات", value=f"{total_income:,} ريال", delta_color="normal")
with col3:
    st.metric(label="إجمالي المصاريف والمساعدات", value=f"{total_expense:,} ريال")

st.markdown("---")

# 4. القائمة الجانبية للتنقل بين الأقسام
menu = ["📊 لوحة التحكم والكشوفات", "👤 إدارة أسماء الجماعة", "💸 تسجيل حركة مالية (قبض/صرف)"]
choice = st.sidebar.selectbox("قائمة الإدارة", menu)

# --- القسم الأول: لوحة التحكم والكشوفات ---
if choice == "📊 لوحة التحكم والكشوفات":
    st.subheader("📋 كشف الحركات المالية للصندوق")
    if not df_trans.empty:
        st.dataframe(df_trans, use_container_width=True)
    else:
        st.info("لا توجد حركات مالية مسجلة بعد.")
        
    st.subheader("👥 كشف حالة اشتراكات الأعضاء")
    df_members = pd.DataFrame(st.session_state.members)
    st.dataframe(df_members, use_container_width=True)

# --- القسم الثاني: إدارة أسماء الجماعة ---
elif choice == "👤 إدارة أسماء الجماعة":
    st.subheader("➕ إضافة فرد جديد للجماعة")
    with st.form("add_member_form"):
        new_id = st.number_input("رقم الهوية أو المعرف الداخلي", min_value=100, max_value=9999, step=1)
        new_name = st.text_input("اسم الفرد كاملاً")
        status = st.selectbox("حالة السداد التلقائية", ["نشط", "متأخر"])
        submitted = st.form_submit_button("حفظ الاسم في الكشف")
        
        if submitted and new_name:
            st.session_state.members.append({"المعرف": new_id, "الاسم": new_name, "الحالة": status, "إجمالي الاشتراكات": 0})
            st.success(f"تم إضافة {new_name} بنجاح إلى كشوفات الجماعة.")
            st.rerun()

# --- القسم الثالث: تسجيل حركة مالية ---
elif choice == "💸 تسجيل حركة مالية (قبض/صرف)":
    st.subheader("📝 تسجيل حركة مالية جديدة في الصندوق")
    with st.form("transaction_form"):
        t_type = st.selectbox("نوع المعاملة", ["إيداع (اشتراك)", "إيداع (تبرع)", "مصروف (مساعدة)", "مصروف (تشغيلي)"])
        t_amount = st.number_input("المبلغ (بالريال السعودي)", min_value=1, max_value=100000, step=50)
        t_details = st.text_input("تفاصيل الحركة (مثال: اشتراك فلان لشهر رجب / مساعدة زواج)")
        t_date = st.date_input("تاريخ المعاملة", datetime.date.today())
        
        submitted_trans = st.form_submit_button("اعتماد العملية المالية")
        
        if submitted_trans and t_details:
            # إضافة المعاملة للحسابات
            st.session_state.transactions.append({
                "التاريخ": str(t_date),
                "النوع": t_type,
                "المبلغ": t_amount,
                "التفاصيل": t_details
            })
            
            # إذا كان اشتراك لأحد الأعضاء، نقوم بتحديث إجمالي اشتراكاته تلقائياً
            if "اشتراك" in t_type:
                df_m = pd.DataFrame(st.session_state.members)
                # فحص مبسط إذا كان الاسم مذكور في التفاصيل لتحديث رصيده
                for member in st.session_state.members:
                    if member['الاسم'] in t_details:
                        member['إجمالي الاشتراكات'] += t_amount
                        member['الحالة'] = "نشط"
            
            st.success("تم تسجيل العملية المالية بنجاح وتحديث رصيد الصندوق الكلي.")
            st.rerun()
