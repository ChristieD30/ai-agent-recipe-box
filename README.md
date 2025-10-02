# 🍳 Recipe Application

A user-friendly web application for managing your favorite recipes. Built with Python and Flask, this application allows you to create, view, edit, and delete recipes with ease.

## 🌟 Features

- User authentication (register and login)
- Create, view, edit, and delete recipes
- Store recipe ingredients and instructions
- Simple and intuitive web interface
- SQLite database for data storage

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone [your-repository-url]
   cd recipe_app
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

1. **Initialize the database**
   ```bash
   python init_db.py
   ```

2. **Start the development server**
   ```bash
   python run.py
   ```

3. **Open your web browser and visit**
   ```
   http://localhost:5000
   ```

## 📂 Project Structure

```
recipe_app/
├── app/
│   ├── __init__.py         # Application factory and extensions
│   ├── models.py           # Database models
│   ├── auth/               # Authentication routes
│   ├── main/               # Main application routes
│   └── templates/          # HTML templates
│       ├── auth/           # Authentication templates
│       └── main/           # Main application templates
├── instance/               # Database and instance folder
├── init_db.py              # Initialize the database
├── recipe_app.py           # Core application logic
├── requirements.txt        # Project dependencies
└── run.py                  # Application entry point
```

## 🔒 Authentication

The application includes user authentication:
- Register a new account
- Log in with your credentials
- Securely manage your own recipes

## 🍲 Using the Application

1. **Create an account** or **log in** if you already have one
2. **View all recipes** on the home page
3. **Add a new recipe** with ingredients and instructions
4. **Edit** or **delete** your own recipes
5. **Log out** when you're done

## 🛠️ Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Flask-Login](https://flask-login.readthedocs.io/) - User session management
- [Bootstrap](https://getbootstrap.com/) - Frontend framework (for responsive design)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all open-source contributors who made this project possible
- Inspired by home cooks and food enthusiasts everywhere!
