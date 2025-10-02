import sqlite3
from datetime import datetime
from tabulate import tabulate

class RecipeApp:
    def __init__(self, db_name=None):
        import os
        # Use DB_PATH environment variable if set, otherwise use default or provided db_name
        self.db_path = os.getenv('DB_PATH', db_name or 'recipes.db')
        self.conn = None
        self.cursor = None
        self.current_user = None
        self.setup_database()

    def connect(self):
        """Establish a connection to the SQLite database."""
        # Ensure the directory exists
        import os
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)) or '.', exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def setup_database(self):
        """Create the necessary tables if they don't exist."""
        self.connect()
        
        # Create users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )''')
        
        # Create recipes table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_created TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        self.conn.commit()

    def create_user(self, name, email):
        """Create a new user."""
        try:
            self.cursor.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )
            self.conn.commit()
            print(f"User '{name}' created successfully!")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print("Error: Email already exists!")
            return None

    def login(self, email):
        """Login a user by email."""
        self.cursor.execute('SELECT id, name FROM users WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        if user:
            self.current_user = {'id': user[0], 'name': user[1]}
            print(f"Welcome back, {user[1]}!")
            return True
        print("User not found. Please create an account first.")
        return False

    def add_recipe(self, name, ingredients, instructions):
        """Add a new recipe for the current user."""
        if not self.current_user:
            print("Please login first!")
            return
            
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(
            '''INSERT INTO recipes 
               (name, date_created, ingredients, instructions, user_id)
               VALUES (?, ?, ?, ?, ?)''',
            (name, date_created, ingredients, instructions, self.current_user['id'])
        )
        self.conn.commit()
        print(f"Recipe '{name}' added successfully!")

    def list_recipes(self):
        """List all recipes for the current user."""
        if not self.current_user:
            print("Please login first!")
            return
            
        self.cursor.execute(
            'SELECT id, name, date_created FROM recipes WHERE user_id = ?',
            (self.current_user['id'],)
        )
        recipes = self.cursor.fetchall()
        
        if not recipes:
            print("No recipes found!")
            return
            
        print("\nYour Recipes:")
        print(tabulate(
            [[idx+1, name, date] for idx, (_, name, date) in enumerate(recipes)],
            headers=['#', 'Recipe Name', 'Date Created'],
            tablefmt='grid'
        ))

    def view_recipe(self, recipe_id):
        """View details of a specific recipe."""
        if not self.current_user:
            print("Please login first!")
            return
            
        self.cursor.execute(
            'SELECT name, date_created, ingredients, instructions FROM recipes WHERE id = ? AND user_id = ?',
            (recipe_id, self.current_user['id'])
        )
        recipe = self.cursor.fetchone()
        
        if not recipe:
            print("Recipe not found!")
            return
            
        name, date_created, ingredients, instructions = recipe
        print("\n" + "="*50)
        print(f"Recipe: {name}")
        print(f"Created on: {date_created}")
        print("\nIngredients:")
        print(ingredients)
        print("\nInstructions:")
        print(instructions)
        print("="*50 + "\n")

def main():
    app = RecipeApp()
    
    print("\n=== Welcome to Recipe App ===\n")
    
    while True:
        if not app.current_user:
            print("\n1. Create Account")
            print("2. Login")
            print("3. Exit")
            
            choice = input("\nChoose an option (1-3): ")
            
            if choice == '1':
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                app.create_user(name, email)
            elif choice == '2':
                email = input("Enter your email: ")
                app.login(email)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n1. Add Recipe")
            print("2. List My Recipes")
            print("3. View Recipe Details")
            print("4. Logout")
            
            choice = input("\nChoose an option (1-4): ")
            
            if choice == '1':
                name = input("Enter recipe name: ")
                ingredients = input("Enter ingredients (comma separated): ")
                instructions = input("Enter instructions: ")
                app.add_recipe(name, ingredients, instructions)
            elif choice == '2':
                app.list_recipes()
            elif choice == '3':
                try:
                    recipe_id = int(input("Enter recipe number to view: "))
                    app.view_recipe(recipe_id)
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == '4':
                print(f"Goodbye, {app.current_user['name']}!")
                app.current_user = None
            else:
                print("Invalid choice. Please try again.")
    
    app.close()

if __name__ == "__main__":
    main()
