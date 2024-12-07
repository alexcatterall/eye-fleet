from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    try:
        # Prepare the conversation history for Ollama
        ollama_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma2:2b",
                "messages": ollama_messages
            },
            stream=True
        )
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    if 'message' in json_response:
                        full_response += json_response['message']['content']
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse line as JSON: {line}")

        return jsonify({"generated_text": full_response})

    except requests.RequestException as e:
        return jsonify({"error": f"Error communicating with Ollama API: {str(e)}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error parsing Ollama API response: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5328)

