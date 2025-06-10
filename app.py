import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

# データベース接続（なければ自動作成）
def get_db_connection():
    conn = sqlite3.connect("lyrics.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lyrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song TEXT NOT NULL,
            lyric TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# ホームページ（歌詞の表示 & 保存）
@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()
    if request.method == "POST":
        song = request.form["song"]
        lyric = request.form["lyric"]
        conn.execute("INSERT INTO lyrics (song, lyric) VALUES (?, ?)", (song, lyric))
        conn.commit()
    lyrics = conn.execute("SELECT * FROM lyrics").fetchall()
    conn.close()
    return render_template("index.html", lyrics=lyrics)

# 編集機能（可愛いボタン追加）
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    if request.method == "POST":
        song = request.form["song"]
        lyric = request.form["lyric"]
        conn.execute("UPDATE lyrics SET song = ?, lyric = ? WHERE id = ?", (song, lyric, id))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    lyric = conn.execute("SELECT * FROM lyrics WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", lyric=lyric)

# スタイリング（ふわふわボタン）
@app.route("/style.css")
def styles():
    return """
    .cute-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background: linear-gradient(45deg, #ff9aa2, #ffb7b2);
        border-radius: 30px;
        box-shadow: 3px 3px 10px rgba(255, 150, 150, 0.5);
        font-family: 'Pacifico', cursive;
        text-decoration: none;
        transition: all 0.3s ease-in-out;
    }
    .cute-button:hover {
        background: linear-gradient(45deg, #ff758c, #ff7eb3);
        transform: scale(1.05);
    }
    """

# ポート設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
