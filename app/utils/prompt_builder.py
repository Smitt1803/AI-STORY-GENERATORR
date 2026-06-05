def build_prompt(prompt, genre, tone, style="No preference", story_length="Medium", include_twist=False, 
                protagonist_description=None, setting=None):
    """Build a comprehensive prompt for story generation"""
    
    # Map story length to approximate word count
    length_map = {
        "Very Short": "300-500 words",
        "Short": "800-1200 words",
        "Medium": "1500-2500 words",
        "Long": "3000-5000 words",
        "Very Long": "7000-10000 words"
    }
    
    # Build the base prompt
    base_prompt = (
        f"You are a professional fiction author known for emotional, character-driven storytelling.\n"
        f"Write a {length_map.get(story_length, 'medium-length')} story in the **{genre}** genre with a **{tone}** tone.\n"
    )
    
    # Add style preference if specified
    if style and style != "No preference":
        base_prompt += f"Use a **{style}** writing style with appropriate narrative techniques.\n"
    
    # Add protagonist details if available
    if protagonist_description:
        base_prompt += f"The protagonist has the following characteristics: {protagonist_description}\n"
    
    # Add setting if specified
    if setting:
        base_prompt += f"The story is set in {setting}.\n"
    
    # Add plot twist instruction if requested
    if include_twist:
        base_prompt += "Include a surprising but logical plot twist near the end of the story.\n"
    
    # Add structural guidelines
    base_prompt += (
        f"\n### Core Idea:\n{prompt}\n\n"
        f"### Structure:\n"
        f"- Start with an engaging hook that establishes setting and character.\n"
        f"- Introduce conflict (inner or relational) that creates tension.\n"
        f"- Develop the character's journey and emotional transformation.\n"
        f"- Build toward a climactic moment.\n"
        f"- End with a meaningful resolution or revelation.\n\n"
        f"### Writing Guidelines:\n"
        f"- Use vivid, sensory descriptions.\n"
        f"- Balance dialogue, action, and introspection.\n"
        f"- Create realistic, flawed characters with clear motivations.\n"
        f"- Maintain consistent pacing and tone.\n"
        f"- Show rather than tell emotional states and character development.\n\n"
        f"### Write the story now:\n"
    )
    
    return base_prompt





















# def build_prompt(prompt, genre, tone):
#     return (
#         f"You are a professional fiction author known for emotional, character-driven storytelling.\n"
#         f"Write a short story in the **{genre}** genre with a **{tone}** tone.\n"
#         f"Focus on emotional depth, character relationships, and a satisfying resolution.\n\n"
#         f"### Core Idea:\n{prompt}\n\n"
#         f"### Structure:\n- Start with the protagonist's setting and desire.\n"
#         f"- Introduce conflict (inner or relational).\n"
#         f"- Show emotional transformation.\n"
#         f"- End with a meaningful resolution or twist.\n\n"
#         f"### Write the story now:\n"
#     )