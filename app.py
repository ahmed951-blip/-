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

# 2. إدارة قاعدة البيانات الثابتة في الذاكرة لمنع تجميد المتصفح
if 'users_list' not in st.session_state:
    st.session_state.users_list = [
        {"اسم المستخدم": "admin", "كلمة السر": "123", "الصلاحية": "مسؤول رئيسي"}
    ]

if 'members_list' not in st.session_state:
    st.session_state.members_list = [
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
    st.subheader("🔐 تسجيل الدخول - نظام جماعة معلين")
    u = st.text_input("اسم المستخدم:", key="login_u").strip()
    p = st.text_input("كلمة السر:", type="password", key="login_p").strip()
    if st.button("دخول للنظام", key="btn_login_submit"):
        # التحقق الآمن من مصفوفة المستخدمين الحية
        user_match = any(user["اسم المستخدم"] == u and user["كلمة السر"] == p for user in st.session_state.users_list)
        if user_match:
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح.")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غير صحيحة.")
else:
    # شريط تسجيل الخروج العلوي المستقر
    if st.button("🚪 تسجيل الخروج من النظام", key="btn_logout_top"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("⚖️ النظام الإلكتروني - جماعة معلين")
    st.markdown("---")

    # 📊 لوحة الإحصائيات العامة والمالية (محرك احتساب الـ 500 ريال التلقائي الفوري)
    df_base = pd.DataFrame(st.session_state.members_list)
    
    total = len(df_base) if not df_base.empty else 0
    males = sum(1 for m in st.session_state.members_list if m.get("الجنس") == "ذكر")
    females = total - males
    paid = sum(1 for m in st.session_state.members_list if m.get("تم دفع الصندوق") == "نعم")
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

    # إنشاء التبويبات القياسية المحمية وعزل العمليات بالكامل
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
            
            df_calc = pd.DataFrame(st.session_state.members_list)
            df_calc["المبلغ المستحق سداده (ريال)"] = round(share, 2)
            st.dataframe(df_calc, use_container_width=True, hide_index=True)
            
            h_rows_fin = "".join([f"<tr><td>{r['الاسم']}</td><td>{r['كود العائلة']}</td><td>{share:,.2f} ريال</td></tr>" for _, r in df_calc.iterrows()])
            html_fin = f'<html dir="rtl" lang="ar"><head><meta charset="utf-8"><style>body {{ font-family: "Arial", sans-serif; padding: 40px; text-align: right; background-color: #ffffff; }} .header-title {{ color: #b71c1c; text-align: center; border-bottom: 3px solid #b71c1c; padding-bottom: 12px; font-size: 24px; }} .summary-box {{ background-color: #f8f9fa; border-right: 6px solid #b71c1c; padding: 15px; margin: 20px 0; font-size: 16px; line-height: 1.8; }} table {{ width:100%; border-collapse:collapse; margin-top: 25px; }} th, td {{ border:1px solid #dddddd; padding:12px; font-size:15px; text-align: right; }} th {{ background-color: #b71c1c; color: white; font-weight: bold; }} tr:nth-child(even) {{ background-color: #f2f2f2; }} .print-button {{ display:block; width:100%; padding:15px; background-color:#1976d2; color:white; font-size:18px; font-weight:bold; text-align:center; border:none; border-radius:8px; cursor:pointer; margin-bottom:25px; }} @media print {{ .print-button {{ display:none; }} }} </style></head><body><button class="print-button" onclick="window.print()">🖨️ اضغط هنا الآن لحفظ هذا التقرير المالي كملف PDF</button><h2 class="header-title">تقرير مالي رسمي خاص بتقسيم المستحقات - جماعة معلين</h2><div class="summary-box"><b>📌 موضوع ومناسبة التقسيم:</b> {reason}<br><b>💰 إجمالي المبلغ المالي المطلوب تقسيمه:</b> {amt:,.2f} ريال سعودي<br><b>👥 إجمالي عدد الأفراد المستحقين للسداد:</b> {total} فرد<br><b>💵 المطالبة المالية المقررة للفرد الواحد:</b> {share:,.2f} ريال سعودي بالتساوي<br></div><table><thead><tr><th>اسم فرد الجماعة</th><th>كود عائلة العضو</th><th>المبلغ المالي المستحق سداده</th></tr></thead><tbody>{h_rows_fin}</tbody></table><br><br><br><p style="text-align:center; font-size:12px; color:#555555;">مستند رسمي صادر إلكترونياً عن نظام إدارة شؤون جماعة معلين الرقمي</p></body></html>'
            st.download_button(f"📥 تحميل مستند تقرير تقسيم ({reason}) كـ PDF مخصص", data=html_fin, file_name=f"تقرير_تقسيم_{reason}.html", mime="text/html", key="dl_fin_pdf", use_container_width=True)

    # ------------------------------------------
    # 2. تبويب التعديل والتحرير والإضافة للأعضاء (بواسطة محررات الخلايا المباشرة الفعالة 100%)
    # ------------------------------------------
    with tab2:
        st.subheader("👥 لوحة التحكم الفورية بأعضاء جماعة معلين")
        st.markdown("💡 **طريقة العمل الحية والمضمونة:**")
        st.caption("1. للإضافة: اضغط على زر **(➕ Add row)** الموجود في أسفل الجدول واكتب بيانات العضو الجديد مباشرة بداخل الخلية.")
        st.caption("2. للتحرير والتعديل: اضغط مرتين على أي خانة (الاسم، العائلة، الصندوق، الجنس) وعدلها فوراً.")
        st.caption("3. للحذف: حدد السطر المُراد التخلص منه واضغط على زر الحذف في كيبورد جهازك أو علامة السلة.")
        
        df_members_editor = pd.DataFrame(st.session_state.members_list)
        
        # محرر الخلايا الذكي لمنع حدوث تجميد أو حظر للجلسة في السيرفرات
        edited_members_df = st.data_editor(
            df_members_editor,
            num_rows="dynamic",
            use_container_width=True,
            key="members_live_data_editor",
            column_config={
                "تم دفع الصندوق": st.column_config.SelectboxColumn(options=["نعم", "لا"]),
                "الجنس": st.column_config.SelectboxColumn(options=["ذكر", "أنثى"])
            }
        )
        
        # حفظ التغييرات الحية تلقائياً بداخل ذاكرة السيستم دون تعليق
        if not edited_members_df.equals(df_members_editor):
            st.session_state.members_list = edited_members_df.to_dict(orient="records")
            st.success("تم حفظ وتحديث مصفوفة الأعضاء وأموال الصندوق تلقائياً.")
            st.rerun()

    # ------------------------------------------
    # 3. تبويب لوحة التقارير والفرز المتقدم (تصدير كشوفات فرز الجنس و Excel/Word/PDF)
    # ------------------------------------------
    with tab3:
        st.subheader("📊 الفرز المتقدم واستخراج الكشوفات والتقارير الشاملة")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: sort_opt = st.selectbox("ترتيب كشف الأسماء والتقرير حسب:", ["بدون ترتيب", "أبجدي", "كود العائلة"], key="sort_sel")
        with col_f2: gender_filter = st.selectbox("تصفية وفلترة السجلات حسب الجنس:", ["الكل", "ذكر", "أنثى"], key="gender_sel")
        with col_f3: paid_filter = st.selectbox("تصفية الكشوفات حسب دفع الصندوق:", ["الكل", "نعم", "لا"], key="paid_sel")
        
        df_rep = pd.DataFrame(st.session_state.members_list)
        
