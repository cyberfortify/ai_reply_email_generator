from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "your_open_api_key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    data = request.get_json()
    email_content = data.get('email', '')

    if not email_content:
        return jsonify({"error": "Email content is missing"}), 400

    prompt = f"Write a polite and professional reply to the following email:\n\n{email_content}\n\nReply:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": reply})

    except openai.error.OpenAIError as e:
        # Specific handling for quota errors
        if "exceeded your current quota" in str(e):
            return jsonify({"error": "You have exceeded your quota. Please check your OpenAI plan and billing details."}), 403
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
