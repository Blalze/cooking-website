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

    # Generate recipes with user-specified styles or requirements
    recipes = []
    for i in range(3):  # Generate three recipe variations
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a highly creative recipe generator. Your goal is to create recipes that match "
                    "the user's specified requirements or style as closely as possible. For example, if they specify "
                    "a Japanese dish, ensure the recipe aligns with Japanese cuisine and their provided details."
                )},
                {"role": "user", "content": f"Create a recipe based on these specifications: {ingredients}."}
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

    # Customize the recipe based on user feedback
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are a recipe customizer. Your task is to adjust recipes to meet the user's feedback "
                "and maintain the original style and flavor profile as much as possible."
            )},
            {"role": "user", "content": f"Here is the original recipe: {original_recipe}. Adjust it based on this feedback: {feedback}."}
        ]
    )
    customized_recipe = response['choices'][0]['message']['content'].strip()

    # Render the customized recipe
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
