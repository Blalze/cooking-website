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

# Route to generate a recipe using OpenAI API
@app.route("/generate", methods=["POST"])
def generate_recipe():
    # Get ingredients from the form
    ingredients = request.form.get("ingredients")

    # Call the OpenAI API to generate a recipe
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model
        messages=[
            {"role": "system", "content": "You are a helpful recipe generator."},
            {"role": "user", "content": f"Generate a recipe using these ingredients: {ingredients}."}
        ]
    )

    # Extract the recipe from the response
    recipe = response['choices'][0]['message']['content'].strip()

    # Return the recipe
    return f"<h1>Generated Recipe</h1><p>{recipe}</p>"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
