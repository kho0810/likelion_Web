from flask import render_template, Flask, request, redirect
from app import app
import urllib2
from bs4 import BeautifulSoup
from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
    SubmitField, validators, ValidationError


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


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
