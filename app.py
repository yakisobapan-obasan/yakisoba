import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# データベース接続
def get_db_connection():
    conn = sqlite3.connect("lyrics.db")
    conn.row_factory = sqlite3.Row
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

# 検索機能
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    conn = get_db_connection()
    lyrics = conn.execute(
        "SELECT * FROM lyrics WHERE song LIKE ? OR lyric LIKE ?",
        ('%' + query + '%', '%' + query + '%')
    ).fetchall()
    conn.close()
    return render_template("index.html", lyrics=lyrics)


# 編集機能（歌詞を取得）
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

# 削除機能
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM lyrics WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# API（JSON形式でデータ取得）
@app.route("/api/lyrics", methods=["GET"])
def api_lyrics():
    conn = get_db_connection()
    lyrics = conn.execute("SELECT * FROM lyrics").fetchall()
    conn.close()
    return jsonify([dict(row) for row in lyrics])

if __name__ == "__main__":
    app.run(debug=True)
