#Sangyel Tashi

# AI News Summarizer

> A real-time news summarization and discussion question generator built with Gradio and powered entirely by a local Ollama language model — no internet API keys required.  
> Designed for speed, clarity, and critical thinking.

---

## Key Features
Fetch top news from multiple New York Times sections  
3-paragraph summaries following AP style  
3 thought-provoking discussion questions per article  
Interactive & clean Gradio interface  
Completely local processing — runs on your own machine  

---

## Technologies Used
-  [Ollama](https://ollama.com/) — Local LLM for text generation  
-  [Gradio](https://www.gradio.app/) — Web-based UI  
-  Python — Backend logic and integration  

---

## How to Install & Run

1. Download the project folder to your computer.  

2. Install dependencies 
```bash
pip install -r requirements.txt
```
3. Install Ollama
- Download from [Ollama's official site](https://ollama.com/download)  
- Pull your preferred model (example: `llama2`):
```bash
ollama pull llama2
```
4. Run the app
```bash
python app.py
```

5. Open Gradio
- A local link will appear in the terminal  
- Click it to open the app in your browser  

---

## How It Works

```plaintext
Ollama AI model summarizes -> Gradio output
```

Workflow Steps:  
1. User selects a news section in Gradio.  
2. Python script creates a structured prompt for Ollama.  
3. Ollama LLM generates a 3-paragraph AP-style summary and 3 discussion questions.  
4. Gradio UI displays the results instantly.  

---

## Team Members
- Sangyel Tashi: create readme
- Josh Mckay: Summary
- Jinxin Dong: UI

---

## Gradio app public link
8/14/2025: https://70ac7bfc41adb34b1f.gradio.live

This share link expires in 1 week. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)
