from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_from_directory,
)
import random
import time
import sys
import os

app = Flask(__name__)
# 定义50音图数据 (平假名, 片假名, 罗马音)
hiragana_katakana = [
    # あ行
    ("あ", "ア", "a"),
    ("い", "イ", "i"),
    ("う", "ウ", "u"),
    ("え", "エ", "e"),
    ("お", "オ", "o"),
    # か行
    ("か", "カ", "ka"),
    ("き", "キ", "ki"),
    ("く", "ク", "ku"),
    ("け", "ケ", "ke"),
    ("こ", "コ", "ko"),
    # さ行
    ("さ", "サ", "sa"),
    ("し", "シ", "shi"),
    ("す", "ス", "su"),
    ("せ", "セ", "se"),
    ("そ", "ソ", "so"),
    # た行
    ("た", "タ", "ta"),
    ("ち", "チ", "chi"),
    ("つ", "ツ", "tsu"),
    ("て", "テ", "te"),
    ("と", "ト", "to"),
    # な行
    ("な", "ナ", "na"),
    ("に", "ニ", "ni"),
    ("ぬ", "ヌ", "nu"),
    ("ね", "ネ", "ne"),
    ("の", "ノ", "no"),
    # は行
    ("は", "ハ", "ha"),
    ("ひ", "ヒ", "hi"),
    ("ふ", "フ", "fu"),
    ("へ", "ヘ", "he"),
    ("ほ", "ホ", "ho"),
    # ま行
    ("ま", "マ", "ma"),
    ("み", "ミ", "mi"),
    ("む", "ム", "mu"),
    ("め", "メ", "me"),
    ("も", "モ", "mo"),
    # や行
    ("や", "ヤ", "ya"),
    ("ゆ", "ユ", "yu"),
    ("よ", "ヨ", "yo"),
    # ら行
    ("ら", "ラ", "ra"),
    ("り", "リ", "ri"),
    ("る", "ル", "ru"),
    ("れ", "レ", "re"),
    ("ろ", "ロ", "ro"),
    # わ行
    ("わ", "ワ", "wa"),
    ("を", "ヲ", "wo"),
    ("ん", "ン", "n"),
]
stats = {"total": 0, "correct": 0, "start_time": None, "durations": []}

mistakes = []  # 词汇练习错题本
vocab_data = [
    ["あい", "愛", "爱"],
    ["あう", "会う", "遇见"],
    ["いえ", "家", "房子"],
    ["うえ", "上", "上面"],
    ["え", "絵", "画"],
    ["おい", "甥", "外甥"],
    ["おう", "追う", "追赶"],
    ["あお", "青", "蓝色"],
    ["かお", "顔", "脸"],
    ["あか", "赤", "红色"],
    ["あき", "秋", "秋天"],
    ["きかい", "機会", "机会"],
    ["きく", "聞く", "听，问"],
    ["かく", "書く", "写"],
    ["ケア", "ケア", "护理"],
    ["ココア", "ココア", "可可"],
    ["けさ", "今朝", "今天早上"],
    ["さく", "咲く", "开花"],
    ["しあい", "試合", "比赛"],
    ["いし", "石", "石头"],
    ["かす", "貸す", "借出"],
    ["すそ", "裾", "衣服下摆"],
    ["せかい", "世界", "世界"],
    ["そしき", "組織", "组织"],
    ["かた", "肩", "肩膀"],
    ["たかい", "高い", "高的"],
    ["いち", "位置", "位置"],
    ["ちいさい", "小さい", "小的"],
    ["あつい", "暑い", "热的"],
    ["いつつ", "五つ", "五个"],
    ["て", "手", "手"],
    ["あと", "後", "之后"],
]


def select_mode():
    print("\n请选择练习模式:")
    print("1: 平假名 → 片假名")
    print("2: 片假名 → 平假名")
    print("3: 混合模式")
    while True:
        choice = input("输入数字选择(1-3): ").strip()
        if choice in ["1", "2", "3"]:
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/src/<path:filename>")
def serve_static(filename):
    audio_path = os.path.join("src", filename)
    return send_from_directory(
        os.path.dirname(audio_path), os.path.basename(audio_path)
    )


@app.route("/start", methods=["POST"])
def start_session():
    rows = request.json.get("rows", [])
    mode = request.json.get("mode", 3)
    study_set = get_study_set(rows)
    return jsonify(
        {
            "hiragana": [h for h, k, r in study_set],
            "katakana": [k for h, k, r in study_set],
            "romaji": [r for h, k, r in study_set],
            "success": True,  # 添加成功标志
        }
    )


@app.route("/check", methods=["POST"])
def check_answer():
    data = request.json
    question_type = data["question_type"]  # 'hira' or 'kata'
    question = data["question"]
    user_answer = data["answer"].strip()
    mode = data.get("mode", 1)  # Default to mode 1 if not specified
    if mode == 4:
        for h, k, r in hiragana_katakana:
            if user_answer == h:
                return jsonify({"correct": True, "correct_answer": h, "romaji": r})
        return jsonify({"correct": False, "correct_answer": None, "romaji": None})
    # 修复1：确保正确查找对应项
    target = next(
        (
            item
            for item in hiragana_katakana
            if (question_type == "hira" and item[0] == question)
            or (question_type == "kata" and item[1] == question)
        ),
        None,
    )

    if not target:
        return jsonify({"error": "Invalid question"}), 400

    hira, kata, romaji = target

    # 修复2：修正验证逻辑
    if question_type == "hira":
        is_correct = user_answer == kata
        correct_answer = kata
    else:
        is_correct = user_answer == hira
        correct_answer = hira

    return jsonify(
        {
            "correct": is_correct,
            "correct_answer": correct_answer,  # 现在会返回正确答案
            "romaji": romaji,
        }
    )


@app.route("/word")
def word_practice():
    return render_template(
        "word.html",
        modes=[
            (1, "平假名→日本語漢字"),
            (2, "中文→日本語漢字"),
            (3, "日本語漢字→中文"),
        ],
        vocab=vocab_data,
    )


@app.route("/word/practice", methods=["POST"])
def word_practice_session():
    global stats, mistakes

    mode = int(request.form.get("mode", 1))
    is_correct = None  # Initialize variable
    # Check previous answer
    if "answer" in request.form and stats["start_time"]:
        stats["total"] += 1
        is_correct = request.form["answer"] == request.form["prev_answer"]
        stats["correct"] += int(is_correct)
        stats["durations"].append(time.time() - stats["start_time"])

    # Generate new question
    question, answer = generate_question(mode)
    stats["start_time"] = time.time()
    # In word_practice_session()
    if "answer" in request.form and not is_correct:
        mistakes.append(
            {
                "question": request.form["prev_question"],
                "correct": request.form["prev_answer"],
                "user_answer": request.form["answer"],
            }
        )

    # Add to render_template()
    mistakes = mistakes[-5:]  # Show last 5 mistakes

    return render_template(
        "word.html",
        question=question,
        answer=answer,
        is_correct=is_correct if "answer" in request.form else None,
        prev_answer=request.form.get("prev_answer", ""),
        accuracy=f"{stats['correct']}/{stats['total']}",
        avg_time=(
            f"{sum(stats['durations'])/len(stats['durations']):.1f}"
            if stats["durations"]
            else "-"
        ),
        mode=mode,
        modes=[
            (1, "平假名→日本語漢字"),
            (2, "中文→日本語漢字"),
            (3, "日本語漢字→中文"),
        ],
        mistakes=mistakes[-5:] if mistakes else [],
    )


@app.route("/word/add", methods=["GET", "POST"])
def add_vocab():
    if request.method == "POST":
        new_word = [
            request.form["hiragana"],
            request.form["kanji"],
            request.form["meaning"],
        ]
        vocab_data.append(new_word)
        return redirect(url_for("word_practice"))
    return render_template("add_vocab.html", vocab=vocab_data)


def generate_question(mode):
    item = random.choice(vocab_data)
    if mode == 1:
        return f"写出「{item[0]}」对应的日本語漢字", item[1]
    elif mode == 2:
        return f"写出「{item[2]}」对应的日本語漢字", item[1]
    else:
        return f"写出「{item[1]}」对应的中文意思", item[2]


if __name__ == "__main__":
    app.run(debug=True)  # 开发模式
