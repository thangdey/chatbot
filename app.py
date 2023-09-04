import json
from difflib import get_close_matches
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

knowledge_base = load_knowledge_base('knowledge_base.json')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    user_input = data['user_input']
    
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        response = {'bot_response': answer}
    else:
        response = {'bot_response': 'Tôi chưa được lập trình để trả lời tình huống này!'}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)