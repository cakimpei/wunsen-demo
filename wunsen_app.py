import streamlit as st
from cutlet import Cutlet
from wunsen import ThapSap

st.title('Wunsen Demo')

lang_option = st.selectbox('เลือกภาษา',
    ('จีนกลาง | Mandarin', 'ญี่ปุ่น | Japanese',
    'เกาหลี | Korean', 'เวียดนาม | Vietnamese'))

need_romaji = False
need_sandhi = True

match lang_option:
    case 'จีนกลาง | Mandarin':
        lang_selected = 'zh'
        input_selected = 'Pinyin-number'
        zh_option = st.radio('รูปแบบการทับศัพท์',
            ('หลักเกณฑ์การทับศัพท์ภาษาจีน',
            'เกณฑ์การถ่ายทอดเสียงภาษาจีนแมนดารินด้วยอักขรวิธีไทย'))
        match zh_option:
            case 'หลักเกณฑ์การทับศัพท์ภาษาจีน':
                system_selected = 'RI49'
                placeholder = 'ni3 hao3'
            case 'เกณฑ์การถ่ายทอดเสียงภาษาจีนแมนดารินด้วยอักขรวิธีไทย':
                system_selected = 'THC43'
                placeholder = 'ni3 hao3'
        sandhi_option = st.radio(
            'การเปลี่ยนวรรณยุกต์เสียงสามที่อยู่หน้าเสียงสามเป็นเสียงสอง',
            ('เปลี่ยน', 'ไม่เปลี่ยน'))
        match sandhi_option:
            case 'เปลี่ยน':
                need_sandhi = True
            case 'ไม่เปลี่ยน':
                need_sandhi = False
    case 'ญี่ปุ่น | Japanese':
        lang_selected = 'ja'
        system_selected = 'ORS61'
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
        system_selected = 'RI55'
        placeholder = 'annyeonghaseyo'
    case 'เวียดนาม | Vietnamese':
        lang_selected = 'vi'
        input_selected = 'VA'
        system_selected = 'RI55'
        placeholder = 'xin chào'

text = st.text_area('Input', max_chars=700, placeholder=placeholder)

if text is not None:
    
    thap_sap = ThapSap(lang_selected, system=system_selected,
        input=input_selected)
    
    if lang_selected == 'zh':
        thap_sap = ThapSap(lang_selected, system=system_selected,
            input=input_selected, option={'sandhi': need_sandhi})

    text_split = text.splitlines()
    
    if need_romaji:
        katsu = Cutlet()
        katsu.use_foreign_spelling = False
        text_split = [katsu.romaji(ja_line) for ja_line in text_split]

    for line in text_split:
        st.write(thap_sap.thap(line))

st.caption("""### หมายเหตุ

หน้านี้เป็นตัวทดลองของ [wunsen](https://github.com/cakimpei/wunsen) ควรตรวจสอบผลลัพธ์ก่อนนำไปใช้

wunsen ไม่มีส่วนเกี่ยวข้องกับผู้กำหนดแนวทางการทับศัพท์แต่อย่างใด

ตัวเลือก "ญี่ปุ่น (ทดลอง)" ใช้ [Cutlet](https://github.com/polm/cutlet) เปลี่ยนจากญี่ปุ่นเป็นโรมาจิ แล้วค่อยเปลี่ยนเป็นไทย
""")