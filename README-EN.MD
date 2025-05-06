# Japanese Hiragana/Katakana Learning Tool

## Overview

This project provides an interactive Japanese kana (hiragana/katakana) learning application with the following features:

- Random character generation for hiragana ↔ katakana conversion practice
- Real-time performance tracking (accuracy and response time)
- Vocabulary practice module with customizable word lists
- Audio pronunciation support (added 2025/5/6)
- Web-based and terminal interfaces

Note: This tool focuses on character recognition rather than writing practice.

## Installation

### For End Users
Download the pre-built executable:
- [GitHub Releases](https://github.com/liuxiangchao369/japanese-50-tone-practice/releases)
- [Mirror (China)](https://gitee.com/MorWin/japanese-50-tone-practice/releases/)

Run `JapanesePractice.exe` and access:
[http://localhost:5000](http://127.0.0.1:5000)

### For Developers
Python environment setup:
```bash
pip install -r requirements.txt
# or minimal installation
pip install Flask==3.1.0
```

## Usage

### Terminal Version
```bash
python src/hiragana_katakana_trainer_terminal.py
```

### Web Version (Recommended)
```bash
python app.py
```
Access via browser: [http://localhost:5000](http://127.0.0.1:5000)

## Screenshot
![Application Screenshot](src/app.png)

## Building Executable
```bash
pip install pyinstaller
pyinstaller --onefile \
            --add-data "src;src" \
            --add-data "templates;templates" \
            --add-data "static;static" \
            --name JapanesePractice \
            app.py
```


