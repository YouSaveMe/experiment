from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

key = os.getenv('open_ai')
client = OpenAI(api_key=key)

app = Flask(__name__)
CORS(app)

def evaluate_answer(stage, student_answer, context):
    prompt = f"""
    학생의 실험 보고서 답변을 평가하고 피드백을 제공해 주세요.
    실험 맥락: {context}
    실험 단계: {stage}
    학생의 답변: {student_answer}

    1. 답변의 장점:
    2. 답변의 단점:
    3. 보강점 안내:
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_data = {
            "stage": stage,
            "content": completion.choices[0].message.content,  # 'content' 속성에 직접 접근
            "model": completion.model,
            "object_type": completion.object
        }
        return response_data
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return {"error": str(e)}


@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.get_json()
        context = data['context']
        student_answers = data['answers']
        feedback = {stage: evaluate_answer(stage, answer, context) for stage, answer in student_answers.items()}
        return jsonify(feedback)
    except Exception as e:
        print(f"Error in evaluate endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
