from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

openai.api_key = 'your-api-key'

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

def evaluate_answer(student_answer, context):
    prompt = f"""
    학생의 실험 보고서 답변을 평가하고 피드백을 제공해 주세요.
    실험 맥락: {context}
    학생의 답변: {student_answer}

    1. 답변의 장점:
    2. 답변의 단점:
    3. 보강점 안내:
    """
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    context = data['context']
    student_answers = data['answers']
    feedback = {stage: evaluate_answer(answer, context) for stage, answer in student_answers.items()}
    return jsonify(feedback)

if __name__ == '__main__':
    app.run(debug=True)
