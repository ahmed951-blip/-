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
        st.rerun()

    st.title("⚖️ النظام الإلكتروني - جماعة معلين")
    st.markdown("---")

    # حساب الإحصائيات العامة والمالية بدقة
    df = pd.DataFrame(st.session_state.members_db)
    total = len(df)
    males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
    females = total - males
    paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
    not_paid = total - paid
    box_money = paid * 500

    # عرض لوحة الإحصائيات بوضوح
    st.markdown("### 📊 إحصائيات الصندوق العامة")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><b>👥 إجمالي الأعضاء</b><br><span style="font-size:20px; color:#2e7d32;">{total}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><b>👨 عدد الذكور</b><br><span style="font-size:20px; color:#2e7d32;">{males}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><b>👩 عدد الإناث</b><br><span style="font-size:20px; color:#2e7d32;">{females}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><b>✅ مسجل بالصندوق</b><br><span style="font-size:20px; color:#2e7d32;">{paid}</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><b>❌ غير مسجل</b><br><span style="font-size:20px; color:#2e7d32;">{not_paid}</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><b>💰 ميزانية الصندوق</b><br><span style="font-size:20px; color:#2e7d32;">{box_money:,} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # إنشاء التبويبات الـ 4
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. التقسيم المالي", "👥 2. إدارة الأعضاء", "📊 3. التقارير والفرز", "🔒 4. حسابات المستخدمين"])

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

    # 2. إدارة الأعضاء (الإضافة والحذف الفوري)
    with tab2:
        st.subheader("➕ إضافة عضو جديد للجماعة")
        n_name = st.text_input("اسم العضو الكامل:", key="mem_add_name_field")
        n_code = st.text_input("كود العائلة الحالي:", key="mem_add_code_field")
        n_paid = st.selectbox("تم دفع الصندوق؟", ["نعم", "لا"], key="mem_add_paid_field")
        n_gender = st.selectbox("الجنس الحالي:", ["ذكر", "أنثى"], key="mem_add_gender_field")
        
        if st.button("➕ تسجيل العضو في النظام", key="execute_add_member_action_btn"):
            if n_name.strip() and n_code.strip():
                if not any(d['الاسم'] == n_name.strip() for d in st.session_state.members_db):
                    st.session_state.members_db.append({"الاسم": n_name.strip(), "كود العائلة": n_code.strip().upper(), "تم دفع الصندوق": n_paid, "الجنس": n_gender})
                    st.success("تم تسجيل العضو بنجاح.")
                    st.rerun()
                else: st.warning("الاسم مسجل مسبقاً.")
            else: st.error("يرجى ملء الحقول.")

        st.markdown("---")
        st.subheader("📋 قائمة الأعضاء الحالية وخيار الحذف")
        for idx, m in enumerate(list(st.session_state.members_db)):
            col_txt, col_btn = st.columns([4, 1])
            col_txt.info(f"👤 {m['الاسم']} | عائلة: {m['كود العائلة']} | صندوق: {m['تم دفع الصندوق']} | جنس: {m['الجنس']}")
            if col_btn.button("🗑️ حذف العضو", key=f"del_member_id_secure_{idx}_{m['الاسم'].replace(' ', '_')}"):
                st.session_state.members_db = [item for item in st.session_state.members_db if item["الاسم"] != m["الاسم"]]
                st.success("تم الحذف بنجاح.")
                st.rerun()

    # 3. لوحة التقارير والفرز المتقدم (تم إضافة خيار فرز وتصفية الجنس بنجاح)
    with tab3:
        st.subheader("📊 الفرز واستخراج الكشوفات والتقارير الشاملة")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sort_opt = st.selectbox("ترتيب كشف الأسماء حسب:", ["أبجدي", "كود العائلة", "بدون ترتيب"], key="reports_sort_option_select")
        with col_f2:
            gender_filter = st.selectbox("تصفية وفلترة حسب الجنس:", ["الكل", "ذكر", "أنثى"], key="reports_gender_filter_select")
        with col_f3:
            paid_filter = st.selectbox("تصفية حسب دفع الصندوق:", ["الكل", "نعم", "لا"], key="reports_paid_filter_select")
        
        # تطبيق الفلترة والترتيب بناء على الاختيارات الجديدة ديناميكياً
        df_rep = df.copy()
        if gender_filter != "الكل":
            df_rep = df_rep[df_rep["الجنس"] == gender_filter]
        if paid_filter != "الكل":
            df_rep = df_rep[df_rep["تم دفع الصندوق"] == paid_filter]
            
        if sort_opt == "أبجدي": 
            df_rep = df_rep.sort_values(by="الاسم")
        elif sort_opt == "كود العائلة": 
            df_rep = df_rep.sort_values(by="كود العائلة")
        
        st.dataframe(df_rep, use_container_width=True, hide_index=True)
        st.markdown("---")
        
        cb1, cb2, cb3 = st.columns(3)
        # Excel
        csv = df_rep.to_csv(index=False).encode('utf-8-sig')
        cb1.download_button("📥 تحميل كشف كملف Excel", data=csv, file_name="تقرير_جماعة_معلين.csv", mime="text/csv", key="excel_download_action_key")
        
        # Word
        w_text = f"تقرير كشف أسماء جماعة معلين المفرز\nإجمالي الأفراد في الكشف: {len(df_rep)}\n\n"
        for _, r in df_rep.iterrows(): w_text += f"- {r['الاسم']} | عائلة: {r['كود العائلة']} | صندوق: {r['تم دفع الصندوق']} | جنس: {r['الجنس']}\n"
        cb2.download_button("📥 تحميل كشف كمستند Word", data=w_text.encode('utf-8-sig'), file_name="تقرير_جماعة_معلين.doc", mime="application/msword", key="word_download_action_key")
        
        # PDF
        h_rows = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{r['تم دفع الصندوق']}</td><td>{r['الجنس']}</td></tr>" for _, r in df_rep.iterrows()])
        html = f"""<html dir="rtl"><head><meta charset="utf-8"></head><body onload="window.print()"><h2>تقرير كشف أسماء جماعة معلين</h2><table border="1" cellpadding="10" style="border-collapse:collapse; width:100%;"><thead><tr style="background:#2e7d32; color:white;"><th>الاسم</th><th>العائلة</th><th>الصندوق</th><th>الجنس</th></tr></thead><tbody>{h_rows}</tbody></table></body></html>"""
        cb3.download_button("📥 تحميل للطباعة كـ PDF", data=html, file_name="تقرير_جماعة_معلين_PDF.html", mime="text/html", key="pdf_download_action_key")

