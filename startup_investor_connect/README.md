# Startup-Investor Connect Platform

This project is a web application designed to connect startups with potential investors. It allows startups to showcase their projects and funding needs while enabling investors to find suitable investment opportunities.

## Features

- **Homepage**: Introduction to the platform with navigation links.
- **User Registration**: Two types of users can register - Startups and Investors.
- **User Login**: Secure login for users with redirection based on user type.
- **Startup Dashboard**: Startups can view and filter investors by industry and funding range.
- **Investor Dashboard**: Investors can view and filter startups by industry and funding requirement.
- **Messaging System**: A built-in messaging interface for communication between startups and investors.

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: MySQL
- **Database Connectivity**: PyMySQL
- **Frontend**: HTML, CSS, JavaScript (optional)
- **CSS Framework**: Bootstrap (or any other framework for responsive design)

## Project Structure

```
startup-investor-connect
├── app
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   │   └── uploads
│   ├── templates
│   │   ├── base.html
│   │   ├── homepage.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── startup_dashboard.html
│   │   ├── investor_dashboard.html
│   │   └── messaging.html
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   └── utils.py
├── migrations
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd startup-investor-connect
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure the database settings in `config.py`.

4. Run the application:
   ```
   python run.py
   ```

5. Access the application in your web browser at `http://127.0.0.1:5000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.