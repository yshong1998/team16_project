from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.9wggmul.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reviewWritePage.html')
def reviewwritepage():
    return render_template('reviewWritePage.html')


@app.route('/reviewPage.html')
def reviewpage():
    return render_template('reviewPage.html')

@app.route('/etcReview.html')
def etcReview():
    return render_template('etcReview.html')


@app.route('/computerReview.html')
def computerReview():
    return render_template('computerReview.html')


@app.route('/smartPhoneReview.html')
def smartPhoneReview():
    return render_template('smartPhoneReview.html')


@app.route('/smartWatchReview.html')
def smartWatchReview():
    return render_template('smartWatchReview.html')

@app.route('/TabletReview.html')
def TabletReview():
    return render_template('TabletReview.html')

@app.route("/review", methods=["POST"])
def web_review_post():
    review_receive = request.form['review_give']
    star_receive = request.form['star_give']
    title_receive = request.form['title_give']
    password_receive = request.form['password_give']
    writer_receive = request.form['writer_give']
    board_receive = request.form['board_give']
    image_receive = request.form['image_give']
    doc = {
        'review':review_receive,
        'star':star_receive,
        'title':title_receive,
        'board':board_receive,
        'writer':writer_receive,
        'password':password_receive,
        'image_URL':image_receive
    }
    db.review.insert_one(doc)
    return jsonify({'msg':'리뷰가 등록되었습니다!'})

@app.route("/delete", methods=["POST"])
def web_delete_review():
    title_receive = request.form['title_give']
    print(title_receive + "asd")
    db.review.delete_one({'title': title_receive})
    return jsonify({'msg':'리뷰가 삭제되었습니다!'})

@app.route("/update", methods=["POST"])
def web_update_review():
    title_receive = request.form['title_give']
    password_receive = request.form['password_give']
    print(title_receive, password_receive)
    # review_list = list(db.review.find({}, {'_id': False}))
    return
    # doc = {
    #     'review': review_receive,
    #     'star': star_receive,
    #     'title': title_receive,
    #     'board': board_receive,
    #     'writer': writer_receive,
    #     'password': password_receive,
    #     'image_URL': image_receive
    # }
    # db.review.update_one(doc)
    # return jsonify({'msg':'리뷰가 삭제되었습니다!'})


@app.route("/review", methods=["GET"])
def web_review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews':review_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4300, debug=True)
