from flask import Flask, render_template, request, jsonify
import random
import time
app = Flask(__name__)
# 定义50音图数据 (平假名, 片假名, 罗马音)
hiragana_katakana = [
    # あ行
    ("あ", "ア", "a"), ("い", "イ", "i"), ("う", "ウ", "u"), ("え", "エ", "e"), ("お", "オ", "o"),
    # か行
    ("か", "カ", "ka"), ("き", "キ", "ki"), ("く", "ク", "ku"), ("け", "ケ", "ke"), ("こ", "コ", "ko"),
    # さ行
    ("さ", "サ", "sa"), ("し", "シ", "shi"), ("す", "ス", "su"), ("せ", "セ", "se"), ("そ", "ソ", "so"),
    # た行
    ("た", "タ", "ta"), ("ち", "チ", "chi"), ("つ", "ツ", "tsu"), ("て", "テ", "te"), ("と", "ト", "to"),
    # な行
    ("な", "ナ", "na"), ("に", "ニ", "ni"), ("ぬ", "ヌ", "nu"), ("ね", "ネ", "ne"), ("の", "ノ", "no"),
    # は行
    ("は", "ハ", "ha"), ("ひ", "ヒ", "hi"), ("ふ", "フ", "fu"), ("へ", "ヘ", "he"), ("ほ", "ホ", "ho"),
    # ま行
    ("ま", "マ", "ma"), ("み", "ミ", "mi"), ("む", "ム", "mu"), ("め", "メ", "me"), ("も", "モ", "mo"),
    # や行
    ("や", "ヤ", "ya"), ("ゆ", "ユ", "yu"), ("よ", "ヨ", "yo"),
    # ら行
    ("ら", "ラ", "ra"), ("り", "リ", "ri"), ("る", "ル", "ru"), ("れ", "レ", "re"), ("ろ", "ロ", "ro"),
    # わ行
    ("わ", "ワ", "wa"), ("を", "ヲ", "wo"), ("ん", "ン", "n")
]
def select_mode():
    print("\n请选择练习模式:")
    print("1: 平假名 → 片假名")
    print("2: 片假名 → 平假名")
    print("3: 混合模式")
    while True:
        choice = input("输入数字选择(1-3): ").strip()
        if choice in ['1', '2', '3']:
            return int(choice)
        print("无效输入，请重新选择")

def select_rows():
    print("请选择要学习的行(输入数字，多个用空格分隔，0表示全部):")
    print("1: あ行  2: か行  3: さ行  4: た行  5: な行")
    print("6: は行  7: ま行  8: や行  9: ら行  10: わ行")
    choices = input("你的选择: ").split()
    
    if "0" in choices:
        return hiragana_katakana
    
    selected = []
    for choice in choices:
        try:
            row_num = int(choice)
            if 1 <= row_num <= 10:
                start = (row_num - 1) * 5
                end = start + 5
                if row_num == 8:
                    selected.extend(hiragana_katakana[35:38])
                elif row_num == 10:
                    selected.extend(hiragana_katakana[40:43])
                else:
                    selected.extend(hiragana_katakana[start:end])
        except ValueError:
            pass
    
    return selected if selected else hiragana_katakana
def get_study_set(selected_rows):
    if not selected_rows or 0 in selected_rows:
        return hiragana_katakana
    
    study_set = []
    for row in selected_rows:
        if row == 8:  # や行
            study_set.extend(hiragana_katakana[35:38])
        elif row == 10:  # わ行
            study_set.extend(hiragana_katakana[40:43])
        else:
            start = (row - 1) * 5
            end = start + 5
            study_set.extend(hiragana_katakana[start:end])
    
    return study_set

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_session():
    rows = request.json.get('rows', [])
    mode = request.json.get('mode', 3)
    study_set = get_study_set(rows)
    return jsonify({
        'hiragana': [h for h,k,r in study_set],
        'katakana': [k for h,k,r in study_set],
        'romaji': [r for h,k,r in study_set],
        'success': True  # 添加成功标志
    })
@app.route('/check', methods=['POST'])
def check_answer():
    data = request.json
    question_type = data['question_type']  # 'hira' or 'kata'
    question = data['question']
    user_answer = data['answer'].strip()
    
    # 修复1：确保正确查找对应项
    target = next((item for item in hiragana_katakana 
                 if (question_type == 'hira' and item[0] == question) or
                 (question_type == 'kata' and item[1] == question)), None)
    
    if not target:
        return jsonify({'error': 'Invalid question'}), 400
    
    hira, kata, romaji = target
    
    # 修复2：修正验证逻辑
    if question_type == 'hira':
        is_correct = user_answer == kata
        correct_answer = kata
    else:
        is_correct = user_answer == hira
        correct_answer = hira
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,  # 现在会返回正确答案
        'romaji': romaji
    })

if __name__ == '__main__':
    app.run(debug=True)  # 开发模式