from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

PORT = os.getenv("PORT")

app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")   
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASS") 
app.config['MYSQL_DB'] = os.getenv("DB_DATABASE") 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)


@app.route('/create', methods=['POST'])
def createArticle():
    if request.method == 'POST':
        data = request.get_json()
        article_title = data['article_title']
        article_content = data['article_content']
        id_user = data['id_user']

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO article (article_title, article_content, id_user) VALUES (%s, %s, %s)", (article_title, article_content, id_user))
        db.connection.commit()
        cursor.close()

        return jsonify({
            'message': 'Data berhasil di tambahkan'
        })
    
@app.route('/read', methods=['GET'])
def getArticle():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM article")
    data = cursor.fetchall()
    cursor.close()

    articles = []
    for article in data:
        article_dict = {
            'article_title': article['article_title'],
            'article_content': article['article_content'],
            'id_user': article['id_user'],
            'createdAt': article['createdAt'],
            'updatedAt': article['updatedAt'],
        }
        articles.append(article_dict)

    return jsonify(articles)

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        data = request.get_json()
        article_title = data['article_title']
        article_content = data['article_content']
        id_user = data['id_user']

        cursor = db.connection.cursor()
        cursor.execute("UPDATE article SET article_title=%s, article_content=%s, user_id=%s WHERE id_article=%s", (article_title, article_content, id_user, id))
        db.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil diperbarui'})

# Endpoint untuk menghapus data
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM article WHERE id_article=%s", (id,))
    db.connection.commit()
    cursor.close()

    return jsonify({'message': 'Data berhasil dihapus'})

if __name__ == "__main__":
    try:
        print("Aplikasi berjalan di port:", PORT)
        app.run(debug=True, port=PORT)
    except Exception as e:
        print("Terjadi kesalahan:", str(e))