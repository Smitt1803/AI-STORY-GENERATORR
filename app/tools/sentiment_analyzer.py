from langchain.tools import Tool
from transformers import pipeline

_sentiment_analyzer = None


def get_sentiment_analyzer():
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = pipeline("sentiment-analysis")
    return _sentiment_analyzer

def get_sentiment_tool():
    """Create a tool for analyzing the sentiment of story text"""
    
    def analyze_sentiment(text):
        """Analyze the sentiment of the provided text"""
        sentiment_analyzer = get_sentiment_analyzer()

        # For longer texts, split into chunks and analyze
        if len(text) > 512:  # Typical token limit for transformer models
            chunks = [text[i:i+512] for i in range(0, len(text), 512)]
            results = [sentiment_analyzer(chunk)[0] for chunk in chunks]
            
            # Average the sentiment scores
            total_score = sum(r['score'] for r in results)
            avg_score = total_score / len(results)
            
            # Determine overall sentiment
            if avg_score >= 0.6:
                overall_sentiment = "positive"
            elif avg_score <= 0.4:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
                
            return {
                "sentiment": overall_sentiment,
                "score": avg_score,
                "confidence": sum(r['score'] for r in results) / len(results)
            }
        else:
            result = sentiment_analyzer(text)[0]
            return {
                "sentiment": result['label'].lower(),
                "score": result['score'],
                "confidence": result['score']
            }
    
    return Tool(
        name="SentimentAnalyzer",
        func=analyze_sentiment,
        description="Analyzes the emotional tone and sentiment of a story."
    )
