import streamlit as st
from cutlet import Cutlet
from korean_romanizer.romanizer import Romanizer
from wunsen import ThapSap

st.title('Wunsen Demo')

lang_option = st.selectbox('เลือกภาษา',
    ('ญี่ปุ่น | Japanese', 'เกาหลี | Korean', 'เวียดนาม | Vietnamese'))

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
                input_selected = 'JAPANESE'
                placeholder = 'おはよう'
    case 'เกาหลี | Korean':
        lang_selected = 'ko'
        ko_option = st.radio('ตัวเลือก',
            ('Revised Romanization', 'ฮันกึล (ทดลอง)'))
        match ko_option:
            case 'Revised Romanization':
                input_selected = 'RR'
                placeholder = 'annyeonghaseyo'
            case 'ฮันกึล (ทดลอง)':
                input_selected = 'HANGUL'
                placeholder = '안녕하세요'
    case 'เวียดนาม | Vietnamese':
        lang_selected = 'vi'
        input_selected = 'VA'
        placeholder = 'xin chào'

text = st.text_area('Input', max_chars=700, placeholder=placeholder)

match input_selected:
    case 'JAPANESE':
        katsu = Cutlet()
        katsu.use_foreign_spelling = False
        thap_sap = ThapSap(lang_selected, input='Hepburn-no diacritic')
        st.write(thap_sap.thap(katsu.romaji(text)))
    case 'HANGUL':
        r = Romanizer(text)
        thap_sap = ThapSap(lang_selected)
        st.write(thap_sap.thap(r.romanize()))
    case _:
        thap_sap = ThapSap(lang_selected, input=input_selected)
        st.write(thap_sap.thap(text))

st.caption("""### หมายเหตุ

หน้านี้เป็นตัวทดลองของ [wunsen](https://github.com/cakimpei/wunsen) ควรตรวจสอบผลลัพธ์ก่อนนำไปใช้

ตัวเลือก "ญี่ปุ่น (ทดลอง)" ใช้ [Cutlet](https://github.com/polm/cutlet) เปลี่ยนจากญี่ปุ่นเป็นโรมาจิ แล้วค่อยเปลี่ยนเป็นไทย
ส่วนตัวเลือก "ฮันกึล (ทดลอง)" ใช้ [korean-romanizer](https://github.com/osori/korean-romanizer) เปลี่ยนจากฮันกึลเป็นตัวโรมัน แล้วเปลี่ยนเป็นไทย

[app source](https://github.com/cakimpei/wunsen-demo)
""")