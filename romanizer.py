from jieba import cut
from pypinyin import lazy_pinyin, Style
from unicodedata import normalize

ZH_SYMBOL = {
    '。': '. ',
    '，': ', ',
    '、': ', ',
    '「': " '",
    '」': "' ",
    '『': ' "',
    '』': '" ',
    '〈': " '",
    '〉': "' ",
    '《': ' "',
    '》': '" ',
    '【': " '",
    '】': "' ",
    '（': ' (',
    '）': ') ',
    '……': '...',
    '——': '—',
    '—': '-',
    '　': ' ',
    '；': '; ',
    '：': ': '
}

def convert_zh_pinyin(text):
    zh_split = list(cut(text))
    result = []
    for chunk in zh_split:
        py_chunk = lazy_pinyin(chunk, style=Style.TONE3, neutral_tone_with_five=True)
        result.append(''.join(py_chunk))
    join_result = join_zh_result(result)
    clean_result = clean_zh_result(join_result)
    return clean_result

# still has problem with % followed by word
def join_zh_result(text):
    new_list = []
    for index, chunk in enumerate(text):
        if chunk[:1].isalnum() and index >= 1 and text[index-1].isalnum():
            chunk = ''.join([' ', chunk])
        new_list.append(chunk)
    return ''.join(new_list).strip()

def clean_zh_result(text):
    for sym in ZH_SYMBOL:
        text = text.replace(sym, ZH_SYMBOL[sym])
    text = normalize('NFKC', text)
    return text