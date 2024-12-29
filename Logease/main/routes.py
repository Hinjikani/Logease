from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/homepage')
def home():
    return render_template('homepage.html')