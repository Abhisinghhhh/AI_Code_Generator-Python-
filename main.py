import os
import requests
import re


def clean_code(code):
    """
    Remove markdown code fences (``` or ```python) from the generated code.
    """
    # Remove starting ``` or ```python and any trailing newlines/spaces
    code = re.sub(r"^\s*```(?:python)?\s*\n?", "", code)
    # Remove ending ```
    code = re.sub(r"\n?\s*```$", "", code)
    return code.strip()

def generate_code(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a Python code generator. Only return Python code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    code = response.json()["choices"][0]["message"]["content"]
    print("Raw generated code:\n", code)  # Debug print raw output
    cleaned = clean_code(code)
    print("\nCleaned code:\n", cleaned)   # Debug print cleaned code
    return cleaned

if __name__ == "__main__":
    user_prompt = input("🔍 Enter what Python code you want: ")

    generated_code = generate_code(user_prompt)

    if generated_code:
        print("\n✅ Generated Code:\n")
        print(generated_code)

        run = input("\n⚠️ Do you want to run this code? (yes/no): ").strip().lower()
        if run == "yes":
            print("\n▶️ Output:\n")
            exec(generated_code)
