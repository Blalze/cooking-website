import os
from flask import Flask, render_template, request, send_file
import openai
from io import BytesIO

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
    ingredients = request.form.get("ingredients")

    # Call the OpenAI API to generate three recipes
    recipes = []
    for i in range(3):
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

# Route to handle customization requests
@app.route("/customize", methods=["POST"])
def customize_recipe():
    original_recipe = request.form.get("original_recipe")
    feedback = request.form.get("feedback")

    # Use OpenAI API to customize the recipe based on feedback
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative recipe customizer."},
            {"role": "user", "content": f"Here is the original recipe: {original_recipe}. Customize it based on this feedback: {feedback}."}
        ]
    )
    customized_recipe = response['choices'][0]['message']['content'].strip()

    # Render the homepage with the updated recipe
    return render_template("index.html", customized_recipe=customized_recipe)

# Route to handle recipe download
@app.route("/download", methods=["POST"])
def download_recipe():
    recipe = request.form.get("recipe")
    filename = "recipe.txt"

    # Create a downloadable text file
    file_data = BytesIO()
    file_data.write(recipe.encode("utf-8"))
    file_data.seek(0)

    return send_file(
        file_data,
        as_attachment=True,
        download_name=filename,
        mimetype="text/plain"
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
