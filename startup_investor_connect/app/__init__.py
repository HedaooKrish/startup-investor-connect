import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user, login_user
from startup_investor_connect.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = 'login'

    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Import models inside app context to avoid circular imports
    with app.app_context():
        from .models import User, Startup, Investor, Message
        db.create_all()

    @app.route('/')
    def index():
        return render_template('homepage.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        from .models import User, Startup, Investor  # Import models

        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            user_type = request.form['user_type']

            # Handle file upload
            file = request.files.get('cover_image')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None  # No file uploaded or invalid file

            # Create user
            user = User(username=username, password=password, user_type=user_type)
            db.session.add(user)
            db.session.commit()

            # Create startup or investor based on user type
            if user_type == 'startup':
                startup = Startup(
                    name=request.form['startup_name'],
                    description=request.form['description'],
                    funding_received=request.form['funding_received'],
                    looking_for_investors='looking_for_investors' in request.form,
                    cover_image=filename,
                    website_url=request.form['website_url'],
                    founder_details=request.form['founder_details'],
                    industry=request.form['industry'],
                    funding_required=request.form['funding_required'],
                    user_id=user.id
                )
                db.session.add(startup)
            elif user_type == 'investor':
                investor = Investor(
                    name=request.form['investor_name'],
                    type=request.form['type'],
                    investment_portfolio=request.form['investment_portfolio'],
                    total_funding_given=request.form['total_funding_given'],
                    industry=request.form['industry'],
                    funding_range_min=request.form['funding_range_min'],
                    funding_range_max=request.form['funding_range_max'],
                    cover_image=filename,
                    user_id=user.id
                )
                db.session.add(investor)

            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from .models import User
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Query the user from the database
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)  # Log the user in
                # Redirect based on user type
                if user.user_type == 'startup':
                    return redirect(url_for('startup_dashboard'))
                elif user.user_type == 'investor':
                    return redirect(url_for('investor_dashboard'))
            else:
                return render_template('login.html', error="Invalid username or password")

        return render_template('login.html')

    @app.route('/startup_dashboard', methods=['GET'])
    def startup_dashboard():
        from .models import Investor

        # Get filter parameters
        industry = request.args.get('industry')
        funding_range = request.args.get('funding_range')

        # Query investors with optional filters
        query = Investor.query
        if industry:
            query = query.filter_by(industry=industry)
        if funding_range:
            try:
                min_funding, max_funding = map(float, funding_range.split('-'))
                query = query.filter(Investor.funding_range_min >= min_funding, Investor.funding_range_max <= max_funding)
            except ValueError:
                pass  # Ignore invalid funding range input

        investors = query.all()
        return render_template('startup_dashboard.html', investors=investors)

    @app.route('/investor_dashboard', methods=['GET'])
    def investor_dashboard():
        from .models import Startup

        # Get filter parameters
        industry = request.args.get('industry')
        funding_required = request.args.get('funding_required')

        # Query startups with optional filters
        query = Startup.query
        if industry:
            query = query.filter_by(industry=industry)
        if funding_required:
            try:
                funding_required = float(funding_required)
                query = query.filter(Startup.funding_required >= funding_required)
            except ValueError:
                pass  # Ignore invalid funding required input

        startups = query.all()
        return render_template('investor_dashboard.html', startups=startups)

    @app.route('/startup/<int:startup_id>', methods=['GET', 'POST'])
    def view_startup(startup_id):
        from .models import Startup, Message
        startup = Startup.query.get_or_404(startup_id)

        if request.method == 'POST':
            sender_id = session.get('user_id')  # Get sender_id from session
            if not sender_id:
                return "User not logged in", 403  # Handle unauthenticated users

            message_content = request.form['message']
            message = Message(sender_id=sender_id, receiver_id=startup.user_id, message=message_content)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('view_startup', startup_id=startup_id))

        return render_template('view_startup.html', startup=startup)

    @app.route('/investor/<int:investor_id>', methods=['GET', 'POST'])
    def view_investor(investor_id):
        from .models import Investor, Message
        investor = Investor.query.get_or_404(investor_id)

        if request.method == 'POST':
            sender_id = session.get('user_id')  # Get sender_id from session
            if not sender_id:
                return "User not logged in", 403  # Handle unauthenticated users

            message_content = request.form['message']
            message = Message(sender_id=sender_id, receiver_id=investor.user_id, message=message_content)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('view_investor', investor_id=investor_id))

        return render_template('view_investor.html', investor=investor)

    @app.route('/messages', methods=['GET'])
    def messages():
        from .models import Message, User, Startup
        user_id = session.get('user_id')  # Get the logged-in user's ID
        if not user_id:
            return "User not logged in", 403  # Handle unauthenticated users

        # Query messages where the logged-in user is the sender or receiver
        received_messages = Message.query.filter_by(receiver_id=user_id).all()
        sent_messages = Message.query.filter_by(sender_id=user_id).all()

        # Include sender details (startup name if available)
        messages_with_details = []
        for msg in received_messages + sent_messages:
            sender_user = User.query.get(msg.sender_id)
            sender_startup = Startup.query.filter_by(user_id=msg.sender_id).first()
            sender_name = sender_startup.name if sender_startup else sender_user.username

            messages_with_details.append({
                "message": msg.message,
                "timestamp": msg.timestamp,
                "sender": sender_name,
                "receiver": User.query.get(msg.receiver_id).username
            })

        return render_template('messages.html', messages=messages_with_details)

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
