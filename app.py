import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية متوافقة مع اللغة العربية (RTL)
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

# 2. تهيئة قاعدة البيانات في الذاكرة لضمان ثبات وحفظ البيانات
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

if 'editing_member_idx' not in st.session_state:
    st.session_state.editing_member_idx = None

# ==========================================
# 🔐 شـاشـة تـسـجـيـل الـدخـول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
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
    col_out_1, col_out_2 = st.columns(2)
    with col_out_2:
        if st.button("🚪 تسجيل الخروج من النظام", key="logout_top_btn_key", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.editing_member_idx = None
            st.rerun()

    st.title("⚖️ النظام الإلكتروني - جماعة معلين")
    st.markdown("---")

    # حساب الإحصائيات العامة والمالية ديناميكياً (إضافة 500 ريال فورا لكل حالة نعم)
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

    # جلب البيانات الحية المباشرة
    df_main_live = pd.DataFrame(st.session_state.members_db)

    # إنشاء التبويبات القياسية المستقرة
    tab1, tab2, tab3, tab4 = st.tabs(["💰 1. التقسيم المالي الجديد", "👥 2. إدارة وتعديل الأعضاء", "📊 3. التقارير والفرز المتقدم", "🔒 4. صلاحيات وحسابات المستخدمين"])

    # ------------------------------------------
    # 1. التقسيم المالي وإصدار تقرير PDF فوري مخصص للعملية المالية
    # ------------------------------------------
    with tab1:
        st.subheader("💵 تقسيم المبالغ بالتساوي وتوليد مستند التقسيم المخصص")
        amt = st.number_input("المبلغ الإجمالي المراد تقسيمه على الجماعة (ريال):", min_value=0.0, value=0.0, key="finance_amount_input_key")
        reason = st.text_input("سبب أو مناسبة هذا التقسيم المالي الجديد:", value="دية عامة", key="finance_reason_input_key")
        
        if amt > 0 and total > 0:
            share = amt / total
            st.metric("💰 نصيب الفرد الواحد من هذا التقسيم", f"{share:,.2f} ريال")
            
            df_calc = df_main_live.copy()
            df_calc["المبلغ المستحق سداده (ريال)"] = round(share, 2)
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
            
            h_rows_fin = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{share:,.2f} ريال</td></tr>" for _, r in df_calc.iterrows()])
            html_fin = f'<html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>body {{ font-family: "Arial", sans-serif; padding: 40px; text-align: right; background-color: #ffffff; }} .header-title {{ color: #b71c1c; text-align: center; border-bottom: 3px solid #b71c1c; padding-bottom: 12px; font-size: 24px; }} .summary-box {{ background-color: #f8f9fa; border-right: 6px solid #b71c1c; padding: 15px; margin: 20px 0; font-size: 16px; line-height: 1.8; }} table {{ width:100%; border-collapse:collapse; margin-top: 25px; }} th, td {{ border:1px solid #dddddd; padding:12px; font-size:15px; text-align: right; }} th {{ background-color: #b71c1c; color: white; font-weight: bold; }} tr:nth-child(even) {{ background-color: #f2f2f2; }} .print-button {{ display:block; width:100%; padding:15px; background-color:#1976d2; color:white; font-size:18px; font-weight:bold; text-align:center; border:none; border-radius:8px; cursor:pointer; margin-bottom:25px; }} @media print {{ .print-button {{ display:none; }} }} </style></head><body><button class="print-button" onclick="window.print()">🖨️ اضغط هنا الآن لحفظ هذا التقرير المالي كملف PDF</button><h2 class="header-title">تقرير مالي رسمي خاص بتقسيم المستحقات - جماعة معلين</h2><div class="summary-box"><b>📌 موضوع ومناسبة التقسيم:</b> {reason}<br><b>💰 إجمالي المبلغ المالي المطلوب تقسيمه:</b> {amt:,.2f} ريال سعودي<br><b>👥 إجمالي عدد الأفراد المستحقين للسداد:</b> {total} فرد<br><b>💵 المطالبة المالية المقررة للفرد الواحد:</b> {share:,.2f} ريال سعودي بالتساوي<br></div><table><thead><tr><th>اسم فرد الجماعة</th><th>كود عائلة العضو</th><th>المبلغ المالي المستحق سداده</th></tr></thead><tbody>{h_rows_fin}</tbody></table><br><br><br><p style="text-align:center; font-size:12px; color:#555555;">مستند رسمي صادر إلكترونياً عن نظام إدارة شؤون جماعة معلين الرقمي</p></body></html>'
            
            st.download_button(f"📥 تحميل مستند تقرير تقسيم ({reason}) كـ PDF مخصص", data=html_fin, file_name=f"تقرير_تقسيم_{reason}.html", mime="text/html", key="download_financial_pdf_btn_key", use_container_width=True)

    # ------------------------------------------
    # 2. إدارة وتعديل وتحرير بيانات الأعضاء (إضافة مباشرة وتعديل فوري حر بدون استمارات معلقة)
    # ------------------------------------------
    with tab2:
        if st.session_state.editing_member_idx is not None:
            st.subheader("📝 تحرير وتعديل بيانات العضو")
            current_member_data = st.session_state.members_db[st.session_state.editing_member_idx]
            
            # حقول حرة مباشرة لحل مشكلة تجميد الأزرار وحفظ التحرير فوراً
            edit_name = st.text_input("تعديل الاسم الكامل للعضو:", value=current_member_data["الاسم"], key="field_edit_name")
            edit_code = st.text_input("تعديل كود العائلة المقررة:", value=current_member_data["كود العائلة"], key="field_edit_code")
            edit_paid = st.selectbox("تعديل حالة دفع الصندوق (+500 ريال عند نعم):", ["نعم", "لا"], index=["نعم", "لا"].index(current_member_data["تم دفع الصندوق"]), key="field_edit_paid")
            edit_gender = st.selectbox("تعديل نوع الجنس المعتمد:", ["ذكر", "أنثى"], index=["ذكر", "أنثى"].index(current_member_data["الجنس"]), key="field_edit_gender")
            
            c_save, c_cancel = st.columns(2)
            with c_save:
                if st.button("💾 اعتماد وحفظ التعديلات", key="btn_save_member_changes_final"):
                    if edit_name.strip() and edit_code.strip():
                        st.session_state.members_db[st.session_state.editing_member_idx] = {
                            "الاسم": edit_name.strip(), "كود العائلة": edit_code.strip().upper(), "تم دفع الصندوق": edit_paid, "الجنس": edit_gender
                        }
                        st.session_state.editing_member_idx = None
                        st.success("تم تحديث البيانات المحدثة.")
                        st.rerun()
                    else: st.error("الحقول مطلوبة.")
            with c_cancel:
                if st.button("❌ إلغاء التعديل", key="btn_cancel_member_edit_final"):
                    st.session_state.editing_member_idx = None
                    st.rerun()
        else:
            st.subheader("➕ إضافة عضو جديد لجماعة معلين")
