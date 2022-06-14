import streamlit as st
from cutlet import Cutlet
from wunsen import ThapSap

st.title('Wunsen Demo')

lang_option = st.selectbox('เลือกภาษา',
    ('ญี่ปุ่น | Japanese', 'เกาหลี | Korean', 'เวียดนาม | Vietnamese'))

need_romaji = False

match lang_option:
    case 'ญี่ปุ่น | Japanese':
        lang_selected = 'ja'
        ja_option = st.radio('ตัวเลือก',
            ('Hepburn romanization', 'Hepburn แบบไม่มี macron',
            'ญี่ปุ่น (ทดลอง)'))
        match ja_option:
            case 'Hepburn romanization':
                input_selected = 'Hepburn-macron'
                placeholder = 'ohayō'
            case 'Hepburn แบบไม่มี macron':
                input_selected = 'Hepburn-no diacritic'
                placeholder = 'ohayou'
            case 'ญี่ปุ่น (ทดลอง)':
                input_selected = 'Hepburn-no diacritic'
                placeholder = 'おはよう'
                need_romaji = True
    case 'เกาหลี | Korean':
        lang_selected = 'ko'
        input_selected = 'RR'
        placeholder = 'annyeonghaseyo'
    case 'เวียดนาม | Vietnamese':
        lang_selected = 'vi'
        input_selected = 'VA'
        placeholder = 'xin chào'

text = st.text_area('Input', max_chars=700, placeholder=placeholder)

if text is not None:
    
    thap_sap = ThapSap(lang_selected, input=input_selected)

    text_split = text.splitlines()
    
    if need_romaji:
        katsu = Cutlet()
        katsu.use_foreign_spelling = False
        text_split = [katsu.romaji(ja_line) for ja_line in text_split]

    for line in text_split:
        st.write(thap_sap.thap(line))

st.caption("""### หมายเหตุ

หน้านี้เป็นตัวทดลองของ [wunsen](https://github.com/cakimpei/wunsen) ควรตรวจสอบผลลัพธ์ก่อนนำไปใช้

ตัวเลือก "ญี่ปุ่น (ทดลอง)" ใช้ [Cutlet](https://github.com/polm/cutlet) เปลี่ยนจากญี่ปุ่นเป็นโรมาจิ แล้วค่อยเปลี่ยนเป็นไทย
""")