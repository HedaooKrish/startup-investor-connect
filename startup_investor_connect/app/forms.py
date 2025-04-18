from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField, FileField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional, Email, EqualTo

class StartupRegistrationForm(FlaskForm):
    startup_name = StringField('Startup Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    funding_received = DecimalField('Funding Received', validators=[DataRequired()])
    looking_for_investors = BooleanField('Looking for Investors')
    cover_image = FileField('Cover Image', validators=[Optional()])
    website_url = StringField('Website URL', validators=[DataRequired(), URL()])
    founder_details = StringField('Founder Details', validators=[DataRequired()])
    industry = SelectField('Industry', choices=[('Fintech', 'Fintech'), ('Edtech', 'Edtech'), ('Healthtech', 'Healthtech'), ('Other', 'Other')], validators=[DataRequired()])
    funding_required = DecimalField('Funding Required', validators=[DataRequired()])
    submit = SubmitField('Register Startup')

class InvestorRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    type = RadioField('Type', choices=[('Individual', 'Individual'), ('Company', 'Company')], validators=[DataRequired()])
    investment_portfolio = TextAreaField('Investment Portfolio', validators=[Optional()])
    total_funding_given = DecimalField('Total Funding Given', validators=[DataRequired()])
    industry_involved = StringField('Industry Involved', validators=[DataRequired()])
    funding_range_willing_to_invest = StringField('Funding Range Willing to Invest', validators=[DataRequired()])
    cover_image = FileField('Cover Image', validators=[Optional()])
    submit = SubmitField('Register Investor')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('startup', 'Startup'), ('investor', 'Investor')], validators=[DataRequired()])
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Register')