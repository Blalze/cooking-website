import os
from flask import Flask, render_template, request
import openai

# Initialize Flask application
app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Home route to render the HTML form
@app.route("/")
def home():
    return render_template("index.html")

# Route to generate multiple recipes using OpenAI API
@app.route("/generate", methods=["POST"])
def generate_recipe():
    # Get ingredients from the form
    ingredients = request.form.get("ingredients")

    # Call the OpenAI API to generate three different recipes
    recipes = []
    for i in range(3):  # Generate three variations
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative recipe generator."},
                {"role": "user", "content": f"Generate a unique recipe using these ingredients: {ingredients}."}
            ]
        )
        recipes.append(response['choices'][0]['message']['content'].strip())

    # Render the recipes on the homepage
    return render_template("index.html", recipes=recipes)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
