import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# إعداد الصفحة وتصميمها لتناسب الجوال والكمبيوتر
st.set_page_config(page_title="نظام إدارة الديات - دخول آمن", page_icon="🔒", layout="wide")

# تعديل الاتجاه يدعم اللغة العربية (RTL) والمظهر
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1000px; }
    h1, h2, h3, p, label, span, div { text-align: right; direction: rtl; }
    div.stButton > button:first-child { background-color: #1E88E5; color:white; width: 100%; font-weight: bold; }
    .stTextInput>div>div>input { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- دالة لتشفير كلمة المرور لحمايتها في قاعدة البيانات ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- إنشاء وتجهيز قاعدة البيانات المحلية للموقع ---
def init_db():
    conn = sqlite3.connect('diya_secure_system.db', check_same_thread=False)
    cursor = conn.cursor()
    # جدول المستخدمين (الصلاحيات)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    # جدول الأعضاء
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, family_id TEXT, family_name TEXT)''')
    # جدول الديات
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, total_amount REAL, date TEXT)''')
    # جدول الكشوفات
    cursor.execute('''CREATE TABLE IF NOT EXISTS collection_sheets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, member_id INTEGER, required_amount REAL, is_paid INTEGER DEFAULT 0)''')
    
    # إنشاء مستخدم افتراضي (مدير النظام) إذا لم يكن موجوداً
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        # اسم المستخدم الافتراضي: admin | كلمة المرور الافتراضية: admin123
        hashed_password = make_hashes("admin123")
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', ?)", (hashed_password,))
        
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# --- إدارة جلسة تسجيل الدخول (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- شاشة تسجيل الدخول ---
if not st.session_state['logged_in']:
    st.title("🔒 تسجيل الدخول إلى النظام")
    st.subheader("هذا النظام محمي، الرجاء إدخال صلاحيات الوصول")
    
    with st.form(key='login_form'):
        username = st.text_input("اسم المستخدم:")
        password = st.text_input("كلمة المرور:", type="password")
        submit_button = st.form_submit_button(label="دخول")
        
        if submit_button:
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            if result and check_hashes(password, result[0]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()  # إعادة تحميل الصفحة للانتقال للبرنامج
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")

# --- لوحة التحكم الرئيسية (تفتح فقط بعد تسجيل الدخول الناجح) ---
else:
    # شريط علوي لترحيب المستخدم وزر تسجيل الخروج
    col_user, col_logout = st.columns([8, 2])
    with col_user:
        st.write(f"👤 مرحباً بك: **{st.session_state['username']}** (مدير النظام)")
    with col_logout:
        if st.button("تسجيل الخروج 🏃‍♂️"):
            st.session_state['logged_in'] = False
            st.rerun()
            
    st.title("⚖️ النظام الإلكتروني لإدارة وتقسيم ديات الجماعة")
    st.write("---")

    # --- القائمة الجانبية للتنقل ---
    menu = ["👥 إدارة وجدولة الأعضاء", "💰 إضافة قضية وتقسيم الدية", "📊 كشوفات السداد والتقارير", "⚙️ تغيير كلمة المرور"]
    choice = st.sidebar.radio("انتقل إلى:", menu)

    # --- 1. قسم إدارة الأعضاء ---
    if choice == "👥 إدارة وجدولة الأعضاء":
        st.header("👥 تسجيل أفراد الجماعة في الصندوق")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fam_name = st.text_input("اسم العائلة (الفخذ):")
        with col2:
            fam_id = st.text_input("رقم العائلة الموحد:")
        with col3:
            name = st.text_input("الاسم الكامل للمشترك:")
            
        if st.button("إضافة العضو الجديد إلى النظام"):
            if name and fam_id and fam_name:
                cursor.execute("INSERT INTO members (name, family_id, family_name) VALUES (?, ?, ?)", (name, fam_id, fam_name))
                conn.commit()
                st.success(f"تم تسجيل العضو: {name} بنجاح!")
            else:
                st.error("الرجاء تعبئة جميع الحقول المطلوبة.")

        st.subheader("📋 قائمة الأعضاء المسجلين حالياً")
        df_members = pd.read_sql_query("SELECT id AS [رقم العضو], name AS [الاسم الكامل], family_id AS [رقم العائلة], family_name AS [اسم العائلة] FROM members", conn)
        st.dataframe(df_members, use_container_width=True)

    # --- 2. قسم إضافة القضايا والتقسيم التلقائي ---
    elif choice == "💰 إضافة قضية وتقسيم الدية":
        st.header("💰 تسجيل قضية دية جديدة وتوزيعها بالتساوي")
        
        case_title = st.text_input("اسم القضية أو المتضرر (مثال: دية قضية فلان):")
        total_amount = st.number_input("المبلغ الإجمالي المطلوب كاملاً (بالريال):", min_value=0.0, step=1000.0)
        
        if st.button("حفظ القضية وتوليد كشف التقسيم التلقائي"):
            cursor.execute("SELECT COUNT(*) FROM members")
            members_count = cursor.fetchone()[0]
            
            if members_count == 0:
                st.error("خطأ: لا يوجد أعضاء مسجلين في النظام لتقسيم المبلغ عليهم!")
            elif case_title and total_amount > 0:
                individual_share = round(total_amount / members_count, 2)
                date_str = datetime.now().strftime("%Y-%m-%d")
                
                cursor.execute("INSERT INTO cases (title, total_amount, date) VALUES (?, ?, ?)", (case_title, total_amount, date_str))
                case_id = cursor.lastrowid
                
                cursor.execute("SELECT id FROM members")
                members = cursor.fetchall()
                for member in members:
                    cursor.execute("INSERT INTO collection_sheets (case_id, member_id, required_amount, is_paid) VALUES (?, ?, ?, 0)", 
                                   (case_id, member[0], individual_share))
                conn.commit()
                
                st.success(f"📊 تم تقسيم الدية بنجاح! إجمالي الأعضاء: {members_count} عضو | نصيب الفرد الواحد: {individual_share} ريال.")
            else:
                st.error("الرجاء إدخال اسم القضية وتحديد المبلغ.")

    # --- 3. قسم الكشوفات والتقارير ---
    elif choice == "📊 كشوفات السداد والتقارير":
        st.header("📊 كشوفات الجماعة والتحصيل")
        
        df_cases = pd.read_sql_query("SELECT id, title FROM cases", conn)
        if df_cases.empty:
            st.info("لا توجد قضايا مسجلة في النظام حتى الآن.")
        else:
            case_options = {row['title']: row['id'] for index, row in df_cases.iterrows()}
            selected_case_title = st.selectbox("اختر القضية لعرض كشفها المالي:", list(case_options.keys()))
            selected_case_id = case_options[selected_case_title]
            
            query = f"""
                SELECT cs.id AS [رقم السجل], m.name AS [الاسم الكامل], m.family_id AS [رقم العائلة], m.family_name AS [اسم العائلة], 
                       cs.required_amount AS [المبلغ المطلوب], 
                       CASE WHEN cs.is_paid = 1 THEN '✅ تم السداد' ELSE '❌ لم يتم السداد' END AS [حالة السداد]
                FROM collection_sheets cs
                JOIN members m ON cs.member_id = m.id
                WHERE cs.case_id = {selected_case_id}
            """
            df_report = pd.read_sql_query(query, conn)
            st.dataframe(df_report, use_container_width=True)
            
            st.subheader("🔄 تحديث حالة سداد لعضو")
            sheet_id_to_pay = st.number_input("أدخل (رقم السجل) الخاص بالشخص الذي سدد:", min_value=1, step=1)
            if st.button("تأكيد استلام المبلغ وتغيير الحالة إلى (تم السداد)"):
                cursor.execute("UPDATE collection_sheets SET is_paid = 1 WHERE id = ?", (sheet_id_to_pay,))
                conn.commit()
                st.success("تم تحديث حالة السداد بنجاح! يرجى إعادة اختيار القضية لتحديث الجدول المالي.")
                
            st.subheader("📥 تحميل الكشف")
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_report.to_excel(writer, index=False)
            
            st.download_button(
                label="تحميل هذا الكشف كملف Excel",
                data=buffer.getvalue(),
                file_name=f"كشف_{selected_case_title}.xlsx",
                mime="application/vnd.ms-excel"
            )

    # --- 4. قسم الإعدادات (تغيير كلمة المرور الافتراضية) ---
    elif choice == "⚙️ تغيير كلمة المرور":
        st.header("⚙️ تغيير كلمة مرور النظام")
        new_password = st.text_input("أدخل كلمة المرور الجديدة:", type="password")
        confirm_password = st.text_input("تأكيد كلمة المرور الجديدة:", type="password")
        
        if st.button("تحديث كلمة المرور"):
            if new_password and new_password == confirm_password:
                hashed_new = make_hashes(new_password)
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new, st.session_state['username']))
                conn.commit()
                st.success("🔒 تم تغيير كلمة المرور بنجاح! استخدم الكلمة الجديدة في المرة القادمة.")
            else:
                st.error("خطأ: كلمات المرور غير متطابقة أو فارغة.")
