#credits to Josh Mckay, Sangyel Tashi, Jinxin Dong

#Josh Mckay
import subprocess

def get_summary_from_url(url):
    result = subprocess.run(
            ["ollama", "run", "llama2", f"Summarize the following article briefly:\n\n{url}"],
            capture_output=True,
            text=True,
            check=True,
        )
    return result.stdout.strip()

#Jinxin Dong
import gradio as gr

def receive_url_summarize(url):
    if not (url and url.startswith(("http://", "https://"))):
        return "Please enter a valid URL (must start with http:// or https://).", ""
    summary = get_summary_from_url(url)
    status = f"Got the URL: {url}. Summary generated."
    return status, summary

def create_url_input_interface():
    with gr.Blocks(title="AI News Article Summarizer") as demo:
        gr.Markdown("# News Article URL Input\nPaste the news article link you want to summarize below.")

        with gr.Row():
            url_input = gr.Textbox(label="Article URL", placeholder="https://example.com/", scale=9)
            submit_btn = gr.Button("Submit", scale=1)

        status_output = gr.Textbox(label="Status", interactive=False)
        summary_output = gr.Textbox(label="Article Summary", interactive=False, lines=10)

        submit_btn.click(receive_url_summarize, inputs=url_input, outputs=[status_output, summary_output])
        url_input.submit(receive_url_summarize, inputs=url_input, outputs=[status_output, summary_output])

    return demo

if __name__ == "__main__":
    demo = create_url_input_interface()
    demo.launch()