from langchain.tools import Tool
from ..utils.prompt_builder import build_prompt

def get_story_generator_tool(llm):
    def _generate(inputs):
        prompt = build_prompt(inputs["prompt"], inputs["genre"], inputs["tone"])
        return llm.invoke(prompt)  # for ChatGroq

    return Tool(
        name="StoryGenerator",
        func=_generate,
        description="Generates a well-structured story from a given prompt, genre, and tone."
    )
