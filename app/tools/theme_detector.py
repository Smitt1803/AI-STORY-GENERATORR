from langchain.tools import Tool
import re

def get_theme_tool():
    """Create an enhanced tool for detecting themes in story text"""
    
    def detect_themes(text):
        """Detect common themes in the story with improved accuracy"""
        # More comprehensive keyword list with contextual patterns
        themes_keywords = {
            "Love": [r"\blove\b", r"\bromance\b", r"\bheart\b", r"passion", r"affection", r"relationship", 
                     r"embrace", r"kiss", r"lover", r"romantic"],
            "Adventure": [r"\bjourney\b", r"\bquest\b", r"\bexplore\b", r"\bdiscover", r"adventure", 
                         r"expedition", r"voyage", r"wilderness", r"explore"],
            "Mystery": [r"\bmystery\b", r"\bclue\b", r"detective", r"solve", r"secret", r"enigma", 
                       r"investigation", r"unknown", r"puzzle", r"mysterious"],
            "Conflict": [r"\bbattle\b", r"\bfight\b", r"\bwar\b", r"conflict", r"struggle", r"tension", 
                        r"argument", r"feud", r"rivalry", r"confrontation"],
            "Redemption": [r"\bforgiv", r"\bredeem", r"salvation", r"atone", r"second chance", r"repent", 
                          r"mistake", r"forgiveness", r"restore", r"amend"],
            "Coming of Age": [r"\bgrow\b", r"\bmature\b", r"youth", r"adolescen", r"lesson", r"learn", 
                             r"childhood", r"adult", r"transition", r"development"],
            "Loss": [r"\bdeath\b", r"\bgrief\b", r"mourn", r"lost", r"absence", r"tragedy", 
                    r"bereavement", r"sorrow", r"missing", r"gone"],
            "Identity": [r"\bidentity\b", r"\bself\b", r"discover", r"who am I", r"true self", r"person", 
                        r"belong", r"authentic", r"heritage", r"origin"],
            "Good vs Evil": [r"\bhero\b", r"\bvillain\b", r"\bgood\b", r"\bevil\b", r"dark", r"light", 
                            r"moral", r"corrupt", r"justice", r"wrong"],
            "Power": [r"\bcontrol\b", r"\bpower\b", r"authority", r"rule", r"dominate", r"influence", 
                     r"strength", r"mighty", r"command", r"govern"],
            "Nature": [r"\bnature\b", r"\bwild\b", r"forest", r"natural", r"earth", r"environment", 
                      r"wilderness", r"animal", r"plant", r"ecological"],
            "Technology": [r"\bmachine\b", r"\bdigital\b", r"tech", r"future", r"robot", r"computer", 
                          r"artificial", r"electronic", r"virtual", r"cyber"],
            "Family": [r"\bfamily\b", r"\bparent", r"child", r"sibling", r"mother", r"father", 
                      r"brother", r"sister", r"relative", r"heritage"],
            "Friendship": [r"\bfriend\b", r"\bcompanion", r"ally", r"comrade", r"bond", r"loyalty", 
                          r"trust", r"support", r"together", r"camaraderie"],
            "Betrayal": [r"\bbetray", r"\bdeceive", r"treachery", r"backstab", r"disloyal", r"trust", 
                         r"traitor", r"betray", r"unfaithful", r"false"],
            "Sacrifice": [r"\bsacrifice", r"\bgive up", r"surrender", r"offering", r"martyrdom", 
                         r"selfless", r"cost", r"price", r"forsake", r"altruism"],
            "Transformation": [r"transform", r"change", r"metamorphosis", r"evolution", r"convert", 
                              r"alter", r"shift", r"transition", r"growth", r"rebirth"]
        }
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Score themes using regex pattern matching
        theme_scores = {}
        for theme, patterns in themes_keywords.items():
            # Count matches across all patterns for this theme
            score = sum(len(re.findall(pattern, text_lower)) for pattern in patterns)
            if score > 0:
                theme_scores[theme] = score
        
        # Add contextual analysis for major themes
        # Check for love story context
        if re.search(r"fell in love|love story|romantic|relationship", text_lower):
            theme_scores["Love"] = theme_scores.get("Love", 0) + 3
            
        # Check for adventure context
        if re.search(r"set out on|began (a|the) journey|embarked on|quest", text_lower):
            theme_scores["Adventure"] = theme_scores.get("Adventure", 0) + 3
            
        # Check for coming of age context
        if re.search(r"grew up|matured|learned (about|that)|realized", text_lower):
            theme_scores["Coming of Age"] = theme_scores.get("Coming of Age", 0) + 3
            
        # Return the top themes (up to 5)
        top_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        return [theme for theme, _ in top_themes] if top_themes else ["Universal", "Human Experience"]
    
    return Tool(
        name="ThemeDetector",
        func=detect_themes,
        description="Identifies common literary themes present in a story with improved pattern matching."
    )