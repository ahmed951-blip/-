import streamlit as st
import pandas as pd

# 1. إعدادات الواجهة الأساسية واللغة العربية (RTL)
st.set_page_config(page_title="نظام جماعة معلين الرقمي", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] { text-align: right; direction: rtl; }
    div[data-testid="stNumberInput"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label { text-align: right; direction: rtl; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 8px; }
    .stat-box { background-color: #f8f9fa; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px; text-align: right; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الجلسة وقاعدة البيانات الآمنة (Session State) لمنع تجميد المتصفح
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

if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None

# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول (لوحة الإحصائيات مخفية بالكامل قبل الدخول)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("🔐 تسجيل الدخول - نظام جماعة معلين")
    u = st.text_input("اسم المستخدم:", key="login_u").strip()
    p = st.text_input("كلمة السر:", type="password", key="login_p").strip()
    if st.button("دخول للنظام", key="btn_login_submit"):
        if u in st.session_state.users_db and st.session_state.users_db[u] == p:
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح.")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
else:
    # شريط تسجيل الخروج العلوي المستقر
    if st.button("🚪 تسجيل الخروج من النظام", key="btn_logout_top"):
        st.session_state.logged_in = False
        st.session_state.editing_index = None
        st.rerun()

    st.title("⚖️ النظام الإلكتروني - جماعة معلين")
    st.markdown("---")

    # 📊 لوحة الإحصائيات العامة والمالية (محرك الصندوق التلقائي للـ 500 ريال)
    total = len(st.session_state.members_db)
    males = sum(1 for m in st.session_state.members_db if m["الجنس"] == "ذكر")
    females = total - males
    paid = sum(1 for m in st.session_state.members_db if m["تم دفع الصندوق"] == "نعم")
    not_paid = total - paid
    box_money = paid * 500  

    st.markdown("### 📊 إحصائيات الصندوق العامة المحدثة")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.markdown(f'<div class="stat-box"><b>👥 إجمالي الأعضاء</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{total}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><b>👨 عدد الذكور</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{males}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><b>👩 عدد الإناث</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{females}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><b>✅ مسجل بالصندوق</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{paid}</span></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-box"><b>❌ غير مسجل</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{not_paid}</span></div>', unsafe_allow_html=True)
    c6.markdown(f'<div class="stat-box"><b>💰 ميزانية الصندوق</b><br><span style="font-size:20px; color:#2e7d32; font-weight:bold;">{box_money:,} ر.س</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # إنشاء التبويبات الأربعة الثابتة والمحمية
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. التقسيم المالي", "👥 2. إدارة وتعديل الأعضاء", "📊 3. التقارير والفرز المتقدم", "🔒 4. صلاحيات وحسابات المستخدمين"])

    # ------------------------------------------
    # 1. تبويب التقسيم المالي وإصدار مستند PDF الفوري المخصص
    # ------------------------------------------
    with tab1:
        st.subheader("💵 تقسيم المبالغ بالتساوي وتوليد مستند التقسيم المخصص")
        amt = st.number_input("المبلغ الإجمالي المراد تقسيمه على الجماعة (ريال):", min_value=0.0, value=0.0, key="fin_amt_in")
        reason = st.text_input("سبب أو مناسبة هذا التقسيم المالي الجديد:", value="دية عامة", key="fin_reason_in")
        
        if amt > 0 and total > 0:
            share = amt / total
            st.metric("💰 نصيب الفرد الواحد من هذا التقسيم", f"{share:,.2f} ريال")
            
            df_calc = pd.DataFrame(st.session_state.members_db)
            df_calc["المبلغ المستحق سداده (ريال)"] = round(share, 2)
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
            
            h_rows_fin = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{share:,.2f} ريال</td></tr>" for _, r in df_calc.iterrows()])
            html_fin = f'<html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>body {{ font-family: "Arial", sans-serif; padding: 40px; text-align: right; background-color: #ffffff; }} .header-title {{ color: #b71c1c; text-align: center; border-bottom: 3px solid #b71c1c; padding-bottom: 12px; font-size: 24px; }} .summary-box {{ background-color: #f8f9fa; border-right: 6px solid #b71c1c; padding: 15px; margin: 20px 0; font-size: 16px; line-height: 1.8; }} table {{ width:100%; border-collapse:collapse; margin-top: 25px; }} th, td {{ border:1px solid #dddddd; padding:12px; font-size:15px; text-align: right; }} th {{ background-color: #b71c1c; color: white; font-weight: bold; }} tr:nth-child(even) {{ background-color: #f2f2f2; }} .print-button {{ display:block; width:100%; padding:15px; background-color:#1976d2; color:white; font-size:18px; font-weight:bold; text-align:center; border:none; border-radius:8px; cursor:pointer; margin-bottom:25px; }} @media print {{ .print-button {{ display:none; }} }} </style></head><body><button class="print-button" onclick="window.print()">🖨️ اضغط هنا الآن لحفظ هذا التقرير المالي كملف PDF</button><h2 class="header-title">تقرير مالي رسمي خاص بتقسيم المستحقات - جماعة معلين</h2><div class="summary-box"><b>📌 موضوع ومناسبة التقسيم:</b> {reason}<br><b>💰 إجمالي المبلغ المالي المطلوب تقسيمه:</b> {amt:,.2f} ريال سعودي<br><b>👥 إجمالي عدد الأفراد المستحقين للسداد:</b> {total} فرد<br><b>💵 المطالبة المالية المقررة للفرد الواحد:</b> {share:,.2f} ريال سعودي بالتساوي<br></div><table><thead><tr><th>اسم فرد الجماعة</th><th>كود عائلة العضو</th><th>المبلغ المالي المستحق سداده</th></tr></thead><tbody>{h_rows_fin}</tbody></table><br><br><br><p style="text-align:center; font-size:12px; color:#555555;">مستند رسمي صادر إلكترونياً عن نظام إدارة شؤون جماعة معلين الرقمي</p></body></html>'
            st.download_button(f"📥 تحميل مستند تقرير تقسيم ({reason}) كـ PDF مخصص", data=html_fin, file_name=f"تقرير_تقسيم_{reason}.html", mime="text/html", key="dl_fin_pdf", use_container_width=True)

    # ------------------------------------------
    # 2. تبويب إدارة وتعديل الأعضاء (إضافة مباشرة وتعديل فوري حر ومضمون 100%)
    # ------------------------------------------
    with tab2:
        if st.session_state.editing_index is not None:
            st.subheader("📝 تحرير وتعديل بيانات العضو")
            m_edit = st.session_state.members_db[st.session_state.editing_index]
            
            e_name = st.text_input("تعديل الاسم الكامل للعضو:", value=m_edit["الاسم"], key="e_name_in")
            e_code = st.text_input("تعديل كود العائلة المقررة:", value=m_edit["كود العائلة"], key="e_code_in")
            e_paid = st.selectbox("تعديل حالة دفع الصندوق (+500 ريال عند نعم):", ["نعم", "لا"], index=["نعم", "لا"].index(m_edit["تم دفع الصندوق"]), key="e_paid_in")
            e_gender = st.selectbox("تعديل نوع الجنس المعتمد:", ["ذكر", "أنثى"], index=["ذكر", "أنثى"].index(m_edit["الجنس"]), key="e_gender_in")
            
            if st.button("💾 حفظ التعديلات الجديدة للعضو", key="btn_save_edit"):
                if e_name.strip() and e_code.strip():
                    st.session_state.members_db[st.session_state.editing_index] = {"الاسم": e_name.strip(), "كود العائلة": e_code.strip().upper(), "تم دفع الصندوق": e_paid, "الجنس": e_gender}
                    st.session_state.editing_index = None
                    st.success("تم تحديث بيانات العضو بنجاح.")
                    st.rerun()
                else: st.error("يرجى ملء الحقول.")
            if st.button("❌ إلغاء عملية التعديل والعودة", key="btn_cancel_edit"):
                st.session_state.editing_index = None
                st.rerun()
        else:
            st.subheader("➕ إضافة عضو جديد للجماعة")
            n_name = st.text_input("اسم العضو الثلاثي الكامل الجديد:", key="n_name_in")
            n_code = st.text_input("كود العائلة الخاص بالعضو الجديد:", key="n_code_in")
            n_paid = st.selectbox("تم دفع مبلغ الصندوق؟ (سيضيف 500 ريال للصندوق فوراً عند نعم):", ["نعم", "لا"], key="n_paid_in")
            n_gender = st.selectbox("الجنس المعتمد:", ["ذكر", "أنثى"], key="n_gender_in")
            
            if st.button("➕ تسجيل واعتماد العضو في النظام", key="btn_add_member"):
                if n_name.strip() and n_code.strip():
                    if not any(d['الاسم'] == n_name.strip() for d in st.session_state.members_db):
                        st.session_state.members_db.append({"الاسم": n_name.strip(), "كود العائلة": n_code.strip().upper(), "تم دفع الصندوق": n_paid, "الجنس": n_gender})
