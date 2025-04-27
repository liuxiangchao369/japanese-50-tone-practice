import random
import time

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

def main():
    print("日语50音练习程序 (按Q退出)")
    print("=" * 30)
    
    study_set = select_rows()
    total = 0
    correct = 0
    mode = select_mode()
    total_time = 0  # 新增总时间统计
    while True:
        hira, kata, romaji  = random.choice(study_set)
        start_time = time.time()  # 记录开始时间
        if mode == 1 or (mode == 3 and random.random() < 0.5):
            print(f"\n平假名: {hira}")
            user_answer = input("片假名: ").strip()
            if user_answer.lower() == 'q' or user_answer == 'Ｑ':
                break
            if user_answer == kata:
                print("正确!")
                correct += 1
            else:
                print(f"错误! 正确答案: {kata} (罗马音: {romaji})")  # 添加罗马音
        else:
            print(f"\n片假名: {kata}")
            user_answer = input("平假名: ").strip()
            if user_answer.lower() == 'q' or user_answer == 'Ｑ':
                break
            if user_answer == hira:
                print("正确!")
                correct += 1
            else:
                print(f"错误! 正确答案: {hira}")
        
        total += 1
        elapsed = time.time() - start_time  # 计算耗时
        total_time += elapsed
        accuracy = (correct / total) * 100 if total > 0 else 0
        avg_time = total_time / total if total > 0 else 0
        print(f"正确率: {accuracy:.1f}% | 平均响应: {avg_time:.1f}s ({correct}/{total})")

if __name__ == "__main__":
    main()