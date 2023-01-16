from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from key import *
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib

ca = certifi.where()
app = Flask(__name__, template_folder="templates")

client = MongoClient('mongodb+srv://test:sparta@cluster0.dhd2t83.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')


@app.route("/review", methods=["POST"])
def s3_upload_img():
    review_route = request.form['image_give']
    title = request.form['title_give']
    data = open(review_route + title, 'rb')
    # data = open(review_route + f + '.jpg', 'rb')
    s3.Bucket(BUCKET_NAME).put_object(
        Key=title, Body=data, ContentType='image/jpg')

    return jsonify({'msg': '등록완료'})


@app.route('/login.html')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register.html')
def register():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})


    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')


    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:

        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


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
    return


@app.route("/review", methods=["GET"])
def web_review_get():
    review_list = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews':review_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4300, debug=True)
