import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("chatbot.html", answer=None)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content
    return render_template("chatbot.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)