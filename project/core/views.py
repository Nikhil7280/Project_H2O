from flask import render_template,request,Blueprint

core=Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('index.html')

@core.route('/info')
def info():   
    # general info about company
    return render_template('info.html')

@core.route('/contactus')
def contactus():
    return render_template('contactus.html')