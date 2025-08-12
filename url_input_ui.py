"""
Jinxin Dong
Person 2: handles user input and interface (print directions and get url from input)
"""
import gradio as gr

def receive_url(url):
    if not (url and url.startswith(("http://", "https://"))):
        return "Please enter a valid URL (must start with http:// or https://)."
    return f"Got the URL: {url}. Ready to start summarizing!"

def create_url_input_interface():
    with gr.Blocks(title="AI News Article Summarizer") as demo:
        gr.Markdown("""# News Article URL Input
                    Paste the news article link you want to summarize below.""")
        
        with gr.Row():
            url_input = gr.Textbox(label="", placeholder="https://example.com", scale=9)
            submit_btn = gr.Button("Submit", scale=1)
        
        status_output = gr.Textbox(label="Status", interactive=False)
        
        submit_btn.click(receive_url, url_input, status_output)
        url_input.submit(receive_url, url_input, status_output)
    
    return demo
