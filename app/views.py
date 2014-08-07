from flask import render_template, Flask, request, redirect, url_for, current_app
from app import app
import urllib2
from bs4 import BeautifulSoup
from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
    SubmitField, validators, ValidationError, IntegerField
from google.appengine.ext import db
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ContactForm(Form):
    name = TextField("Name", [validators.Required("Please enter your name.")])
    email = TextField(
        "Email", [validators.Required("Please enter email address."),
                  validators.Email("Please enter valid email address.")])
    subject = TextField(
        "Subject", [validators.Required("Please enter a subject.")])
    message = TextAreaField(
        "Message", [validators.Required("Please enter a subject.")])
    submit = SubmitField("Send")


class Tweet(db.Model):
    photo = db.BlobProperty()
    comment = db.StringProperty()

    def setPhoto(self, filestream):
        self.photo = db.Blob(filestream)

    def setExif(self, exif):
        self.exif = json.dumps(exif)

    def getExif(self):
        return json.loads(self.exif)


class TweetURL(object):
    url = ''
    comment = ''


@app.route('/')
@app.route('/index')
def index():
    a = 123
    b = [123, '353', 'abc']

    return render_template('index.html', a=a, b=b, c='ccc')


@app.route('/hi', methods=['GET', 'POST'])
def hi():
    get = None
    post1 = None
    post2 = None

    if request.method == 'GET':
        get = request.args.get("get1")
    if request.method == 'POST':
        post1 = request.form.get("post1")
        post2 = request.form.get("post2")

    return render_template('hi.html',
                           get_val=get, post_val1=post1, post_val2=post2)


@app.route('/first', methods=['GET'])
def first():
    if request.method == 'GET':
        get = request.args.get("get")
        if request.args.get("google"):
            return redirect('https://www.google.co.kr/?gws_rd=ssl#\
                newwindow=1&q=' + get)
        if request.args.get("naver"):
            return redirect('http://search.naver.com/search.naver?where=\
                nexearch&query=' + get)
        if request.args.get("daum"):
            return redirect('http://search.daum.net/search?w=tot&DA=YZR&t\
                __nil_searchbox=btn&sug=&o=&q=' + get)

    return render_template('first.html')


@app.route('/second', methods=['GET'])
def second():
    if request.method == 'GET' and request.args:
        htmlSource = request.args.get("url")
        # url exception
        if htmlSource[0:7] != "http://":
            return render_template("second.html")

        tagName = request.args.get("tagName")
        if request.args.get("classTag"):
            tagName = "." + tagName
        if request.args.get("idTag"):
            tagName = "#" + tagName

        htmltext = urllib2.urlopen(htmlSource).read()
        soup = BeautifulSoup(htmltext, from_encoding="utf-8")

        arr = []

        for tag in soup.select(tagName):
            arr.append(tag.get_text())

        return render_template('second.html', arr=arr)
    else:
        return render_template('second.html')


@app.route('/index1')
def index1():
    return render_template('index1.html')


@app.route('/third', methods=['GET', 'POST'])
def third():
    form = ContactForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('third.html', form=form)
        else:
            return "Nice to meet you, " + form.name.data + "!"
    return render_template('third.html', form=form)


class NaverForm(Form):
    genre = IntegerField(
        "genre", [validators.Required("Please enter genre number.")])
    submit = SubmitField("Send")


@app.route('/forth', methods=['GET', 'POST'])
def forth():
    form = NaverForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('forth.html', form=form)
        else:
            # crawl
            url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(form.genre.data)
            htmltext = urllib2.urlopen(url).read()
            soup = BeautifulSoup(htmltext, from_encoding="utf-8")

            arr = []
            # arr1 = []
            titles = soup.find_all('a', 'nclicks(fls.list)')
            for tag in titles:
                # arr1.append(len(tag.get_text()))
                if len(tag.get_text()) > 2:
                    arr.append(tag.get_text())

            return render_template('forth.html', arr=arr[:10], form=form,
                                   titles=titles)

    return render_template('forth.html', form=form)


@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    if request.form:
        upload_data = Tweet()

        if request.files.get('photo'):
            post_photo = request.files.get('photo')
            filestream = post_photo.read()
            upload_data.photo = db.Blob(filestream)
            # print post_photo

        post_comment = request.form.get('comment')
        upload_data.comment = post_comment
        upload_data.put()

    tweetURLs = []
    for tweet in Tweet.all():
        tweetURL = TweetURL()
        if tweet.photo:
            tweetURL.url = url_for("show", key=tweet.key())
        tweetURL.comment = tweet.comment
        tweetURLs.append(tweetURL)

    return render_template('tweet.html', tweetURLs=tweetURLs)


@app.route('/show/<key>', methods=['GET'])
def show(key):
    uploaded_data = db.get(key)
    return current_app.response_class(uploaded_data.photo)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
