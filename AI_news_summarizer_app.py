# credits to Josh Mckay, Sangyel Tashi, Jinxin Dong
#refercence Professor.Jairam

#Import Library
import subprocess
import gradio as gr
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Josh & Jinxin KEY
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")
NYT_URL = "https://api.nytimes.com/svc/topstories/v2"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "mistral"

# Jinxin: Fetch webpage text
def fetch_article_text(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text() for p in paragraphs)
    except Exception as e:
        return f"Error fetching article text: {e}"

# Josh: Ollama URL summary
def get_summary_from_url(url):
    text = fetch_article_text(url)
    try:
        res = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": f"Summarize:\n{text}", "stream": False})
        return res.json().get("response", "No summary generated")
    except Exception as e:
        return f"Error generating summary: {e}"

# Jinxin: Batch URL summary
def receive_urls_summarize(urls_text):
    urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
    if not urls:
        return "Please enter at least one valid URL.", ""
    
    all_summaries = []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            all_summaries.append(f"{url} → Invalid URL")
            continue
        summary = get_summary_from_url(url)
        all_summaries.append(f"{url}\n{summary}\n{'-'*40}")
    
    status = f"Processed {len(urls)} URL(s)."
    return status, "\n".join(all_summaries)

# Josh and Jinxin NYT top stories
if not NYT_API_KEY:
    raise ValueError("Please set your NYT_API_KEY in the .env file.")

def get_top_stories(section="home", limit=3):
    try:
        res = requests.get(f"{NYT_URL}/{section}.json", params={"api-key": NYT_API_KEY})
        res.raise_for_status()
        data = res.json()
        return [
            {"title": a["title"], "abstract": a["abstract"], "url": a["url"]}
            for a in data.get("results", [])[:limit]
        ]
    except Exception as e:
        print(f"Error fetching NYT data: {e}")
        return []

def summarize_article(title, abstract):
    prompt = f"Summarize the news article titled '{title}': {abstract}"
    try:
        res = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": prompt, "stream": False})
        return res.json().get("response", "No summary generated")
    except Exception as e:
        return f"Error summarizing article: {e}"

def generate_discussion_questions(title, abstract):
    prompt = f"Based on the article '{title}' ({abstract}), create 3 thought-provoking discussion questions."
    try:
        res = requests.post(OLLAMA_API, json={"model": MODEL, "prompt": prompt, "stream": False})
        return res.json().get("response", "No questions generated")
    except Exception as e:
        return f"Error generating questions: {e}"

def process_news(section):
    articles = get_top_stories(section)
    if not articles:
        return "No articles found. Please try a different section or check your API key."
    
    output = ""
    for a in articles:
        summary = summarize_article(a["title"], a["abstract"])
        questions = generate_discussion_questions(a["title"], a["abstract"])
        output += f"## {a['title']}\n\n"
        output += f"{a['abstract']}\n\n"
        output += f"Summary:\n{summary}\n\n"
        output += f"Discussion Questions:\n{questions}\n\n"
        output += f"Read more: {a['url']}\n\n{'-'*40}\n\n"
    return output

#Jinxin: Gradio UI
with gr.Blocks(title="AI News Summarizer") as demo:
    gr.Markdown("AI News Summarizer & Discussion")

    with gr.Tab("NYT Top Stories"):
        section = gr.Dropdown(
            choices=["home", "world", "business", "technology"],
            value="home",
            label="Select News Section"
        )
        run_btn = gr.Button("Get & Analyze News")
        output_md = gr.Markdown()
        run_btn.click(process_news, inputs=section, outputs=output_md)

    with gr.Tab("Custom URL Summarizer"):
        url_input = gr.Textbox(
            label="Article URLs",
            placeholder="https://example.com/\nhttps://another.com/",
            lines=5
        )
        submit_btn = gr.Button("Submit")
        status_output = gr.Textbox(label="Status", interactive=False)
        summary_output = gr.Textbox(label="Article Summaries", interactive=False, lines=20)
        submit_btn.click(receive_urls_summarize, inputs=url_input, outputs=[status_output, summary_output])
        url_input.submit(receive_urls_summarize, inputs=url_input, outputs=[status_output, summary_output])

if __name__ == "__main__":
    demo.launch(share = True)
