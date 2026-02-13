from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Folder Configuration
UPLOAD_FOLDER = "uploads"
DOCS_FOLDER = "docs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOCS_FOLDER"] = DOCS_FOLDER

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCS_FOLDER, exist_ok=True)


# -------------------------------
# Function to Generate Documentation
# -------------------------------
def generate_documentation(file_path):

    documentation = "Generated Documentation\n"
    documentation += "============================\n\n"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()

                # Detect Functions
                if line.startswith("def "):
                    documentation += f"Function Found: {line}\n"
                    documentation += "Description: This function performs a specific task.\n\n"

                # Detect Classes
                elif line.startswith("class "):
                    documentation += f"Class Found: {line}\n"
                    documentation += "Description: This class defines structure and behavior.\n\n"

    except Exception as e:
        documentation += f"Error reading file: {str(e)}"

    return documentation


# -------------------------------
# ROUTES
# -------------------------------

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Upload Page
@app.route("/upload")
def upload():
    return render_template("upload.html")


# Generate Documentation
@app.route("/generate", methods=["POST"])
def generate():

    if "codefile" not in request.files:
        return redirect("/upload")

    file = request.files["codefile"]

    if file.filename == "":
        return redirect("/upload")

    # Save uploaded file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Generate documentation
    documentation = generate_documentation(filepath)

    # Save documentation file
    doc_path = os.path.join(app.config["DOCS_FOLDER"], "documentation.txt")
    with open(doc_path, "w", encoding="utf-8") as doc_file:
        doc_file.write(documentation)

    # Send result to result.html
    return render_template("result.html", documentation=documentation)


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)