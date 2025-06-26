import requests
import re

def generate_blog(user_prompt):
    prompt = (
        f"Write a blog post on the topic: '{user_prompt}' in 200-300 words. "
        "Start with a suitable title on its own line, followed by the full blog body."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code == 200:
            raw_text = response.json().get("response", "").strip()
            raw_text = re.sub(r"Word Count:\s*\d+\)?$", "", raw_text).strip()
            lines = raw_text.split("\n", 1)
            title = lines[0].strip("# ").strip()
            if title.lower().startswith("title:") or title.lower().startswith("title-"):
                title = title[6:].strip()

            body = lines[1].strip() if len(lines) > 1 else ""
            if body.lower().startswith("blog body -"):  
                body = body[11:].strip()

            if not body:
                body = raw_text
                if not title or title.lower() == user_prompt.lower():
                    title = user_prompt.title()

            return {"title": title, "body": body}
        else:
            return {"title": None, "body": "There was an error generating the blog."}
    except Exception as e:
        return {"title": None, "body": f"Exception: {str(e)}"}
