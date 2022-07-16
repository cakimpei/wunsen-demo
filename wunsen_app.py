import streamlit as st
from pypinyin import lazy_pinyin, Style
from cutlet import Cutlet
from korean_romanizer.romanizer import Romanizer
from wunsen import ThapSap

st.title('Wunsen Demo')

lang_option = st.selectbox('เลือกภาษา',
    ('จีนกลาง | Mandarin', 'ญี่ปุ่น | Japanese',
    'เกาหลี | Korean', 'เวียดนาม | Vietnamese'))

need_pinyin = False
need_sandhi = True
need_romaji = False
need_romaja = False

match lang_option:
    case 'จีนกลาง | Mandarin':
        lang_selected = 'zh'
        input_selected = 'Pinyin-number'
        zh_input = st.radio('ตัวเลือก input',
            ('พินอิน+เลขวรรณยุกต์', 'จีน > พินอิน > ไทย (ทดลอง)'))
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
        match zh_input:
            case 'พินอิน+เลขวรรณยุกต์':
                sandhi_option = st.radio(
                    'เปลี่ยนวรรณยุกต์เสียงสามที่อยู่หน้าเสียงสามเป็นเสียงสอง',
                    ('เปลี่ยน', 'ไม่เปลี่ยน'))
                match sandhi_option:
                    case 'เปลี่ยน':
                        need_sandhi = True
                    case 'ไม่เปลี่ยน':
                        need_sandhi = False
            case 'จีน > พินอิน > ไทย (ทดลอง)':
                placeholder = '你好'
                need_pinyin = True
                need_sandhi = False
    case 'ญี่ปุ่น | Japanese':
        lang_selected = 'ja'
        system_selected = 'ORS61'
        ja_option = st.radio('ตัวเลือก input',
            ('Hepburn romanization', 'Hepburn แบบไม่มี macron',
            'ญี่ปุ่น > Hepburn > ไทย (ทดลอง)'))
        match ja_option:
            case 'Hepburn romanization':
                input_selected = 'Hepburn-macron'
                placeholder = 'ohayō'
            case 'Hepburn แบบไม่มี macron':
                input_selected = 'Hepburn-no diacritic'
                placeholder = 'ohayou'
            case 'ญี่ปุ่น > Hepburn > ไทย (ทดลอง)':
                input_selected = 'Hepburn-no diacritic'
                placeholder = 'おはよう'
                need_romaji = True
    case 'เกาหลี | Korean':
        lang_selected = 'ko'
        system_selected = 'RI55'
        input_selected = 'RR'
        ko_option = st.radio('ตัวเลือก',
            ('Revised Romanization', 'ฮันกึล > RR > ไทย (ทดลอง)'))
        match ko_option:
            case 'Revised Romanization':
                placeholder = 'annyeonghaseyo'
            case 'ฮันกึล > RR > ไทย (ทดลอง)':
                placeholder = '안녕하세요'
                need_romaja = True
    case 'เวียดนาม | Vietnamese':
        lang_selected = 'vi'
        input_selected = 'VA'
        system_selected = 'RI55'
        placeholder = 'xin chào'

text = st.text_area('ข้อความ', max_chars=700, placeholder=placeholder)

if text is not None:
    
    thap_sap = ThapSap(lang_selected, system=system_selected,
        input=input_selected)
    
    if lang_selected == 'zh':
        thap_sap = ThapSap(lang_selected, system=system_selected,
            input=input_selected, option={'sandhi': need_sandhi})

    text_split = text.splitlines()

    if need_pinyin:
        new_text_split = []
        for zh_line in text_split:
            zh_text = lazy_pinyin(zh_line, style=Style.TONE3, tone_sandhi=True)
            new_text_split.append(' '.join(zh_text))
        text_split = new_text_split
    elif need_romaji:
        katsu = Cutlet()
        katsu.use_foreign_spelling = False
        text_split = [katsu.romaji(ja_line) for ja_line in text_split]
    elif need_romaja:
        new_text_split = []
        for ko_line in text_split:
            kr = Romanizer(ko_line)
            new_text_split.append(kr.romanize())
        text_split = new_text_split

    for line in text_split:
        st.write(thap_sap.thap(line))

st.caption("""### หมายเหตุ

หน้านี้เป็นตัวทดลองของ [wunsen](https://github.com/cakimpei/wunsen) ควรตรวจสอบผลลัพธ์ก่อนนำไปใช้

wunsen ไม่มีส่วนเกี่ยวข้องกับผู้กำหนดแนวทางการทับศัพท์แต่อย่างใด

ตัวเลือก "(ทดลอง)" ใช้ python-pinyin, Cutlet, korean-romanizer เปลี่ยนจากภาษาต้นทางเป็นตัวอักษรโรมัน แล้วค่อยเปลี่ยนเป็นไทย

[source](https://github.com/cakimpei/wunsen-heroku)
""")