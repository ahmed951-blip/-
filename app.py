import streamlit as st
from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

# إعدادات الصفحة
st.set_page_config(page_title="BLIP Image Captioning", page_icon="🖼️", layout="centered")

st.title("🖼️ BLIP Image Captioning App")
st.write("قم برفع صورة أو وضع رابط صورة للحصول على وصف تلقائي لمحتواها باستخدام نموذج BLIP.")

# تحميل النموذج والمشغل (Processor) وتخزينهما في الذاكرة المؤقتة لسرعة الأداء
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

try:
    processor, model = load_model()
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل النموذج: {e}")

# خيارات إدخال الصورة
option = st.radio("اختر طريقة إدخال الصورة:", ("رفع ملف صورة", "إدخال رابط صورة"))

raw_image = None

if option == "رفع ملف صورة":
    uploaded_file = st.file_uploader("اختر صورة...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            raw_image = Image.open(uploaded_file).convert('RGB')
        except Exception as e:
            st.error(f"عذراً، تعذر قراءة الملف المرفوع: {e}")

elif option == "إدخال رابط صورة":
    url = st.text_input("أدخل رابط الصورة المباشر (URL):", "")
    if url:
        try:
            # إضافة User-Agent لتجنب حظر الطلب من بعض المواقع
            headers = {"User-Agent": "Mozilla/5.0"}
            raw_image = Image.open(requests.get(url, stream=True, headers=headers).raw).convert('RGB')
        except Exception as e:
            st.error(f"تعذر تحميل الصورة من الرابط. تأكد من أن الرابط مباشر وصحيح. الخطأ: {e}")

# معالجة الصورة وتوليد الوصف
if raw_image is not None:
    st.image(raw_image, caption="الصورة المستخدمة", use_container_width=True)
    
    with st.spinner("جاري تحليل الصورة وتوليد الوصف..."):
        try:
            # معالجة الصورة بدون نص توجيهي (الوصف المطلق)
            inputs = processor(raw_image, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            # عرض النتيجة
            st.success("✨ تم توليد الوصف بنجاح!")
            st.subheader("الوصف (Caption):")
            st.info(caption)
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء توليد الوصف: {e}")
