from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        genai.configure(api_key="AIzaSyACwhkVuzzzK4tXoSarhqaL9Y4CJ-FUc3M")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 0,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            safety_settings=safety_settings,
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        response_text = response.text

    return render_template('index.html', response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=11000)
