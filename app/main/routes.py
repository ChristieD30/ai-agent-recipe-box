from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Recipe
from datetime import datetime

# Create a Blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.updated_at.desc()).all()
        return render_template('main/index.html', recipes=recipes)
    return render_template('main/index.html')

@main.route('/recipe/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        
        if not name or not ingredients or not instructions:
            flash('All fields are required!', 'danger')
        else:
            # Create new recipe
            recipe = Recipe(
                name=name,
                ingredients=ingredients,
                instructions=instructions,
                user_id=current_user.id
            )
            db.session.add(recipe)
            db.session.commit()
            
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('main.index'))
            
    return render_template('main/add_recipe.html')

@main.route('/recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Ensure the recipe belongs to the current user
    if recipe.user_id != current_user.id:
        flash('You do not have permission to view this recipe.', 'danger')
        return redirect(url_for('main.index'))
        
    return render_template('main/view_recipe.html', recipe=recipe)

@main.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Ensure the recipe belongs to the current user
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        recipe.name = request.form.get('name', recipe.name)
        recipe.ingredients = request.form.get('ingredients', recipe.ingredients)
        recipe.instructions = request.form.get('instructions', recipe.instructions)
        recipe.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('main.view_recipe', recipe_id=recipe.id))
        
    return render_template('main/edit_recipe.html', recipe=recipe)

@main.route('/recipe/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Ensure the recipe belongs to the current user
    if recipe.user_id != current_user.id:
        flash('You do not have permission to delete this recipe.', 'danger')
        return redirect(url_for('main.index'))
    
    db.session.delete(recipe)
    db.session.commit()
    
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('main.index'))
