from langchain.tools import Tool
from transformers import pipeline

_summarizer_pipe = None


def get_summarizer_pipe():
    global _summarizer_pipe
    if _summarizer_pipe is None:
        _summarizer_pipe = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return _summarizer_pipe

def get_summary_tool():
    def summarize(text: str):
        summarizer_pipe = get_summarizer_pipe()
        return summarizer_pipe(
            text[:1000],
            max_length=1000,
            min_length=30,
            do_sample=False,
        )[0]["summary_text"]

    return Tool(
        name="SummaryGenerator",
        func=summarize,
        description="Summarizes a given story."
    )
