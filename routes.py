from flask import Flask, render_template, request, flash, redirect, url_for
from microblog.forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/')
def homepage():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")


