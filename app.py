import os
from flask import Flask, render_template, request

# Initialize Flask application
app = Flask(__name__)

# Home route to render the HTML form
@app.route("/")
def home():
    return render_template("index.html")

# Route to generate a recipe (mock response for now)
@app.route("/generate", methods=["POST"])
def generate_recipe():
    # Get ingredients from the form
    ingredients = request.form.get("ingredients")

    # Mocked response instead of calling OpenAI API
    recipe = f"This is a mock recipe using the following ingredients: {ingredients}. Enjoy your meal!"

    # Return the mock recipe
    return f"<h1>Generated Recipe</h1><p>{recipe}</p>"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
