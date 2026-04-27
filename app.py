import os
from flask import Flask, render_template, request, session
from groq import Groq

app = Flask(__name__)
app.secret_key = "tameem_secret_123"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    session.clear()
    return render_template("chatbot.html", messages=[])

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]
    if "messages" not in session:
        session["messages"] = []
    session["messages"].append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}
        ] + session["messages"]
    )
    answer = response.choices[0].message.content
    session["messages"].append({"role": "assistant", "content": answer})
    session.modified = True
    return render_template("chatbot.html", messages=session["messages"])

if __name__ == "__main__":
    app.run(debug=True)
