import streamlit as st
import requests
from PIL import Image
from transformers import pipeline

# 1. إعدادات واجهة الموقع
st.set_page_config(page_title="محلل الصور الذكي", page_icon="🖼️")
st.title("🖼️ تطبيق وصف الصور التلقائي (BLIP)")
st.write("ارفع صورة من جهازك أو وضع رابطاً مباشراً لصورة ليقوم الذكاء الاصطناعي بوصفها.")

# 2. تحميل النموذج باسم المهمة الجديد المعتمد في مكتبة transformers
@st.cache_resource
def get_caption_pipeline():
    # تم تحديث اسم المهمة إلى image-text-to-text لتجنب الخطأ السابق تماماً
    return pipeline("image-text-to-text", model="Salesforce/blip-image-captioning-base")

try:
    captioner = get_caption_pipeline()
except Exception as e:
    st.error(f"فشل في تحميل نموذج الذكاء الاصطناعي: {e}")

# 3. خيارات إدخال الصورة
choice = st.radio("اختر طريقة إدخال الصورة:", ["رفع ملف صورة", "إدخال رابط صورة"])
img_input = None

if choice == "رفع ملف صورة":
    uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            img_input = Image.open(uploaded_file).convert("RGB")
        except:
            st.error("خطأ في قراءة ملف الصورة.")

else:
    url_input = st.text_input("أدخل رابط الصورة المباشر:")
    if url_input:
        try:
            # إضافة حماية للروابط لمنع حظر خوادم Streamlit
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url_input, stream=True, headers=headers)
            img_input = Image.open(response.raw).convert("RGB")
        except:
            st.error("تعذر تحميل الصورة من هذا الرابط. تأكد أنه رابط مباشر ينتهي بـ .jpg أو .png")

# 4. معالجة الصورة وإظهار النتيجة فوراً
if img_input:
    st.image(img_input, caption="الصورة التي تم إدخالها", use_container_width=True)
    
    with st.spinner("جاري تحليل الصورة وتوليد الوصف..."):
        try:
            # توليد الوصف
            result = captioner(img_input)
            caption_text = result[0]['generated_text']
            
            # عرض النتيجة للمستخدم
            st.success("✨ تم تحليل الصورة بنجاح!")
            st.subheader("الوصف باللغة الإنجليزية:")
            st.code(caption_text, language="text")
        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الصورة: {e}")
