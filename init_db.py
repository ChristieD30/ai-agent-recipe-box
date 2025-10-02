import sqlite3

def init_db():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist (same as in recipe_app.py)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date_created TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Check if we already have sample data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Add sample user
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Sample User", "sample@example.com")
        )
        user_id = cursor.lastrowid
        
        # Add sample recipes
        sample_recipes = [
            ("Pasta Carbonara", 
             "Spaghetti, Eggs, Pancetta, Parmesan, Black Pepper, Salt",
             "1. Cook pasta\n2. Fry pancetta\n3. Mix eggs and cheese\n4. Combine everything"),
            ("Chicken Curry",
             "Chicken, Curry Powder, Coconut Milk, Onion, Garlic, Rice",
             "1. Cook chicken\n2. Sauté onions and garlic\n3. Add curry powder\n4. Add coconut milk\n5. Simmer and serve with rice")
        ]
        
        for name, ingredients, instructions in sample_recipes:
            cursor.execute('''
                INSERT INTO recipes (name, date_created, ingredients, instructions, user_id)
                VALUES (?, datetime('now'), ?, ?, ?)
            ''', (name, ingredients, instructions, user_id))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data!")
