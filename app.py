from flask import Flask, render_template, request, session
import ollama
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

SYSTEM_PROMPT = (
    "Tum ek AI Python Guide ho. Sirf Python programming se related questions ke jawab do. "
    "Agar koi user kisi aur topic par sawal poochhe (jaise cricket, history, etc.), to politely mana karo "
    "aur bolo ki 'Main sirf Python ke sawalon ke jawab dene ke liye bana hoon'."
)

def get_llama_response(user_input):
    response = ollama.chat(
        model='tinyllama',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response['message']['content']

@app.route("/", methods=["GET", "POST"])
def index():
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        question = request.form["question"]
        answer = get_llama_response(question)

        session["history"].append({
            "question": question,
            "answer": answer
        })
        session.modified = True

    return render_template("index.html", history=session.get("history", []))

if __name__ == "__main__":
    app.run(debug=True)
