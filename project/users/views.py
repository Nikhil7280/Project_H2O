from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db
from project.models import User, Data
from project.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from project.users.picture_handler import add_profile_pic
import stripe
import pickle
import math
public_key='pk_test_51JqEebSEhjJ0OK35gH2wXCL17vaigmFloJ1dyEgpsYwLrwvqGT0PLlL3Fl7PASrPeXdfUkbZGTzyLc9h6qeacjyV00iyWEoBPG'
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"
users=Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account created successfully! You are now logged in as {user.username}",category='success')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



# login
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/data':
                next = url_for("users.data")

            return redirect(next)

    return render_template('login.html',form=form)



# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account (update UserForm)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)

@users.route('/payment_home')
def payment_home():
    return render_template('payment_home.html',public_key=public_key)


@users.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@users.route('/payment',methods=['POST'])
def payment():
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
       customer=customer.id, 
       ammount=1999,
       currency='usd',
       description='Pay!!'
    )

    return redirect(url_for('thankyou'))


@users.route('/data',methods=['GET','POST'])
@login_required
def data():
    return render_template("data.html")


@users.route('/getmlmodeldata',methods=['GET','POST'])
@login_required
def getmlmodeldata():
    per_18 = request.form["No. of persons < 18"] 
    per_19 = request.form["No. of persons > 18"]
    water_appli = request.form["No. of Water Using Appliances"]
    garden = request.form["Garden"]
    season = request.form["Season"]
    weather = request.form["Weather"]
    water_avai = request.form["Water Available In Different Sources"]
    region = request.form["Region"]
    holiday = request.form["Holiday"]

    if garden == 'yes':
        garden = 1
    else:
        garden = 0

    season = 0

    if weather.lower() == 'cloudy':
        weather = 0
    elif weather.lower() == 'cold':
        weather = 1
    elif weather.lower() == 'dry':
        weather = 2
    elif weather.lower() == 'hot':
        weather = 3
    elif weather.lower() == 'humid':
        weather = 4
    else:
        weather = 5

    region = 0

    if holiday == 'no':
        holiday = 0
    else:
        holiday = 1

    input_list = [per_18,per_19,water_appli,garden,season,weather,water_avai,region,holiday]

    with open("/home/sachin269/Desktop/hacknitr/project/users/model_pickle.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
        y_pred_from_pkl = pickle_model.predict([input_list])
    y_pred = 0.95*y_pred_from_pkl[0]
    y_pred = math.ceil(y_pred)
    return str(y_pred)

 