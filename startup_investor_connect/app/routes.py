from flask import render_template, redirect, url_for, request, flash, session
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Startup, Investor, Message

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        if user_type == 'startup':
            new_user = Startup(
                name=form.startup_name.data,
                description=form.description.data,
                funding_received=form.funding_received.data,
                looking_for_investors=form.looking_for_investors.data,
                cover_image=form.cover_image.data,
                website_url=form.website_url.data,
                founder_details=form.founder_details.data,
                industry=form.industry.data,
                funding_required=form.funding_required.data
            )
        else:
            new_user = Investor(
                name=form.name.data,
                type=form.investor_type.data,
                investment_portfolio=form.investment_portfolio.data,
                total_funding_given=form.total_funding_given.data,
                industry_involved=form.industry_involved.data,
                funding_range=form.funding_range.data,
                cover_image=form.cover_image.data
            )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            flash('Login successful!', 'success')
            return redirect(url_for('startup_dashboard') if user.user_type == 'startup' else url_for('investor_dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/startup_dashboard')
def startup_dashboard():
    investors = Investor.query.all()
    return render_template('startup_dashboard.html', investors=investors)

@app.route('/investor_dashboard')
def investor_dashboard():
    startups = Startup.query.all()
    return render_template('investor_dashboard.html', startups=startups)

@app.route('/messaging')
def messaging():
    return render_template('messaging.html')