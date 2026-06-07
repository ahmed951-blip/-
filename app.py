import streamlit as st
import pandas as pd

# إعدادات الواجهة الأساسية واللغة العربية
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; }
    .stat-box { background-color: #f8f9fa; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px; text-align: right; margin-bottom: 15px; }
    .edit-btn>div>button { background-color: #f57c00; color: white; }
    .delete-btn>div>button { background-color: #d32f2f; color: white; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الجلسة وقاعدة البيانات في المتصفح لمنع التجميد وثبات الحسابات
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

# متغير لمتابعة العضو الذي يتم تعديله حالياً
if 'editing_member_idx' not in st.session_state:
    st.session_state.editing_member_idx = None

# شاشة تسجيل الدخول
if not st.session_state.logged_in:
    st.subheader("🔐 تسجيل الدخول - نظام جماعة معلين")
    u = st.text_input("اسم المستخدم:", key="login_username_key").strip()
    p = st.text_input("كلمة السر:", type="password", key="login_password_key").strip()
    if st.button("دخول للنظام", key="login_submit_btn_key"):
        if u in st.session_state.users_db and st.session_state.users_db[u] == p:
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح.")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
else:
    # شريط الخروج العلوي
    if st.button("🚪 تسجيل الخروج من النظام", key="logout_top_btn_key"):
        st.session_state.logged_in = False
        st.session_state.editing_member_idx = None
        st.rerun()

    st.title("⚖️ النظام الإلكتروني - جماعة معلين")
    st.markdown("---")

    # حساب الإحصائيات العامة والمالية بدقة (تحديث فوري لـ 500 ريال عند اختيار نعم)
    df = pd.DataFrame(st.session_state.members_db)
    total = len(df)
    males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
    females = total - males
    paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
    not_paid = total - paid
    box_money = paid * 500  # إضافة 500 ريال تلقائياً لكل من حالته "نعم"

    # عرض لوحة الإحصائيات بوضوح
    st.markdown("### 📊 إحصائيات الصندوق العامة المحدثة")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><b>👥 إجمالي الأعضاء</b><br><span style="font-size:20px; color:#2e7d32;">{total}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><b>👨 عدد الذكور</b><br><span style="font-size:20px; color:#2e7d32;">{males}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><b>👩 عدد الإناث</b><br><span style="font-size:20px; color:#2e7d32;">{females}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><b>✅ مسجل بالصندوق</b><br><span style="font-size:20px; color:#2e7d32;">{paid}</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><b>❌ غير مسجل</b><br><span style="font-size:20px; color:#2e7d32;">{not_paid}</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><b>💰 ميزانية الصندوق</b><br><span style="font-size:20px; color:#2e7d32;">{box_money:,} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # إنشاء التبويبات الـ 4
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. التقسيم المالي", "👥 2. إدارة وتعديل الأعضاء", "📊 3. التقارير والفرز", "🔒 4. حسابات المستخدمين"])

    # 1. التقسيم المالي وتوليد التقرير المخصص
    with tab1:
        st.subheader("💵 تقسيم المبالغ بالتساوي وتوليد المستند")
        amt = st.number_input("المبلغ الإجمالي المراد تقسيمه (ريال):", min_value=0.0, value=0.0, key="finance_amount_input_key")
        reason = st.text_input("سبب أو مناسبة التقسيم المالي:", value="دية عاجلة", key="finance_reason_input_key")
        
        if amt > 0 and total > 0:
            share = amt / total
            st.metric("💰 نصيب الفرد الواحد الحالي", f"{share:,.2f} ريال")
            df_calc = df.copy()
            df_calc["المبلغ المستحق"] = round(share, 2)
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
            
            # بناء صفحة تقرير التقسيم
            h_rows_fin = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{share:,.2f} ريال</td></tr>" for _, r in df_calc.iterrows()])
            html_fin = f"""<html dir="rtl"><head><meta charset="utf-8"></head><body onload="window.print()"><h2>تقرير تقسيم المستحقات المالي - جماعة معلين</h2><p><b>المناسبة:</b> {reason} | <b>المبلغ الإجمالي:</b> {amt:,.2f} ريال</p><table border="1" cellpadding="10" style="border-collapse:collapse; width:100%;"><thead><tr style="background:#b71c1c; color:white;"><th>اسم فرد الجماعة</th><th>كود العائلة</th><th>المبلغ المستحق سداده</th></tr></thead><tbody>{h_rows_fin}</tbody></table></body></html>"""
            st.download_button(f"📥 تحميل تقرير تقسيم ({reason}) كـ PDF", data=html_fin, file_name=f"تقرير_تقسيم_{reason}.html", mime="text/html", key="download_financial_pdf_btn_key")

    # 2. إدارة الأعضاء (تحرير وتعديل البيانات بالكامل + إضافة وحذف)
    with tab2:
        if st.session_state.editing_member_idx is not None:
            st.subheader("📝 تحرير وتعديل بيانات العضو")
            current_member_data = st.session_state.members_db[st.session_state.editing_member_idx]
            
            edit_name = st.text_input("تعديل الاسم الكامل:", value=current_member_data["الاسم"], key="mem_edit_name_field")
            edit_code = st.text_input("تعديل كود العائلة:", value=current_member_data["كود العائلة"], key="mem_edit_code_field")
            edit_paid = st.selectbox("تعديل حالة دفع الصندوق (+500 ريال عند اختيار نعم):", ["نعم", "لا"], index=["نعم", "لا"].index(current_member_data["تم دفع الصندوق"]), key="mem_edit_paid_field")
            edit_gender = st.selectbox("تعديل الجنس:", ["Ref_ذكر", "ذكر", "أنثى"], index=1, key="mem_edit_gender_field")
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 حفظ التعديلات الجديدة", key="save_edited_member_btn"):
                    if edit_name.strip() and edit_code.strip():
                        st.session_state.members_db[st.session_state.editing_member_idx] = {
                            "الاسم": edit_name.strip(),
                            "كود العائلة": edit_code.strip().upper(),
                            "تم دفع الصندوق": edit_paid,
                            "الجنس": edit_gender
                        }
                        st.session_state.editing_member_idx = None
                        st.success("تم تحرير وتحديث بيانات العضو بنجاح.")
                        st.rerun()
                    else:
                        st.error("يرجى عدم ترك حقول الاسم أو الكود فارغة.")
            with col_cancel:
                if st.button("❌ إلغاء التعديل", key="cancel_edited_member_btn"):
                    st.session_state.editing_member_idx = None
                    st.rerun()
        else:
            st.subheader("➕ إضافة عضو جديد للجماعة")
            n_name = st.text_input("اسم العضو الكامل:", key="mem_add_name_field")
            n_code = st.text_input("كود العائلة الحالي:", key="mem_add_code_field")
            n_paid = st.selectbox("تم دفع مبلغ الصندوق؟ (سيضيف 500 ريال للصندوق تلقائياً عند اختيار نعم):", ["نعم", "لا"], key="mem_add_paid_field")
            n_gender = st.selectbox("الجنس الحالي:", ["ذكر", "أنثى"], key="mem_add_gender_field")
            
            if st.button("➕ تسجيل العضو في النظام", key="execute_add_member_action_btn"):
                if n_name.strip() and n_code.strip():
                    if not any(d['الاسم'] == n_name.strip() for d in st.session_state.members_db):
                        st.session_state.members_db.append({"الاسم": n_name.strip(), "كود العائلة": n_code.strip().upper(), "تم دفع الصندوق": n_paid, "الجنس": n_gender})
                        st.success("تم تسجيل العضو بنجاح وتحديث أموال الصندوق.")
                        st.rerun()
                    else: st.warning("الاسم مسجل مسبقاً.")
                else: st.error("يرجى ملء الحقول.")

        st.markdown("---")
        st.subheader("📋 قائمة التحكم بالأعضاء (تحرير / حذف)")
        for idx, m in enumerate(list(st.session_state.members_db)):
            col_txt, col_edit, col_del = st.columns(3)
            with col_txt:
                st.info(f"👤 {m['الاسم']} | عائلة: {m['كود العائلة']} | صندوق: {m['تم دفع الصندوق']} | جنس: {m['الجنس']}")
            
            with col_edit:
                st.markdown('<div class="edit-btn">', unsafe_allow_html=True)
                if st.button("📝 تحرير", key=f"edit_member_id_{idx}_{m['الاسم'].replace(' ', '_')}", use_container_width=True):
                    st.session_state.editing_member_idx = idx
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col_del:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                # تم ضبط المحاذاة والمسافات البرمجية الأربعة للأمر هنا بدقة تامة وبدون أي تداخل
