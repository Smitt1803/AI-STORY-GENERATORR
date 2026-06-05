# from langchain.tools import Tool

# def get_title_generator_tool(llm):
#     def generate_title(story_text):
#         prompt = (
#             "Generate a creative and fitting title for the following story. "
#             "Make sure it's short, expressive, and captures the story’s theme.\n\n"
#             f"{story_text}"
#         )
#         return llm.invoke(prompt)

#     return Tool(
#         name="TitleGenerator",
#         func=generate_title,
#         description="Generates a suitable story title from the story content."
#     )


from langchain.tools import Tool

def get_title_generator_tool(llm):
    """Create a tool for generating a title for a story"""
    
    def generate_title(story_text):
        """Generate an appropriate title for the story"""
        
        # Extract the first few paragraphs to analyze
        story_preview = story_text[:1000]
        
        # Build the prompt for title generation
        prompt = (
            f"As a professional editor, please create a compelling and appropriate title for the following story."
            f"The title should be catchy, relevant to the content, and ideally 2-7 words long."
            f"Do not use generic titles like 'The Story' or 'A Tale'."
            f"Here's the beginning of the story:\n\n{story_preview}\n\n"
            f"Generate only the title, with no additional explanation or commentary:"
        )
        
        # Use the language model to generate the title
        return llm.invoke(prompt)
    
    return Tool(
        name="TitleGenerator",
        func=generate_title,
        description="Generates an appropriate title for a story based on its content."
    )