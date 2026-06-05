from langchain.tools import Tool

def get_style_enhancer_tool(llm):
    """Create a tool for enhancing the writing style of a story"""
    
    def enhance_style(inputs):
        """Enhance the writing style of a story based on the specified style"""
        story = inputs["story"]
        style = inputs["style"]
        
        # Build the prompt for style enhancement
        prompt = (
            f"As a professional editor, please enhance the following story to better match "
            f"a {style} writing style. Maintain the plot, characters, and core elements, "
            f"but adjust the language, sentence structure, and narrative techniques to "
            f"better reflect a {style} style.\n\n"
            f"Here's the story to enhance:\n\n{story}\n\n"
            f"Please provide the enhanced version with {style} styling:"
        )
        
        # Use the language model to enhance the style
        return llm.invoke(prompt)
    
    return Tool(
        name="StyleEnhancer",
        func=enhance_style,
        description="Enhances the writing style of a story according to a specified style."
    )