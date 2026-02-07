"""
Machine Learning module for AI-powered task predictions.
This module provides functions for predicting task priority, categorizing tasks,
and estimating task difficulty using NLP with TextBlob.
"""

from textblob import TextBlob

# Keywords that indicate high priority
HIGH_PRIORITY_KEYWORDS = [
    'urgent', 'asap', 'immediately', 'critical', 'emergency', 
    'deadline', 'important', 'priority', 'must', 'required'
]

# Keywords that indicate low priority
LOW_PRIORITY_KEYWORDS = [
    'maybe', 'someday', 'later', 'eventually', 'whenever',
    'optional', 'nice to have', 'if possible'
]

# Category keywords mapping
CATEGORY_KEYWORDS = {
    'Work': ['meeting', 'report', 'email', 'presentation', 'project', 'client', 'deadline', 'office'],
    'Personal': ['grocery', 'shopping', 'home', 'family', 'personal', 'self'],
    'Health': ['doctor', 'gym', 'exercise', 'medicine', 'health', 'workout', 'fitness'],
    'Finance': ['bill', 'payment', 'bank', 'money', 'budget', 'tax', 'invoice'],
    'Learning': ['study', 'learn', 'course', 'book', 'read', 'tutorial', 'practice'],
    'Social': ['call', 'meet', 'party', 'friend', 'birthday', 'event'],
}

# Keywords indicating task complexity/difficulty
HARD_TASK_KEYWORDS = [
    'research', 'analyze', 'design', 'implement', 'develop', 'create',
    'complex', 'detailed', 'comprehensive', 'extensive', 'thorough',
    'integrate', 'optimize', 'refactor', 'architect', 'debug',
    'investigate', 'evaluate', 'configure', 'deploy', 'migrate'
]

MEDIUM_TASK_KEYWORDS = [
    'update', 'modify', 'review', 'prepare', 'organize', 'schedule',
    'write', 'draft', 'plan', 'coordinate', 'arrange', 'setup'
]

EASY_TASK_KEYWORDS = [
    'quick', 'simple', 'easy', 'basic', 'check', 'confirm',
    'send', 'reply', 'call', 'buy', 'get', 'pick up',
    'remind', 'note', 'list'
]

# Multi-step indicators
MULTI_STEP_INDICATORS = [
    'then', 'after', 'before', 'finally', 'first', 'next',
    'step', 'phase', 'stage', 'and then', 'followed by'
]


def predict_priority(title: str, description: str = '') -> str:
    """
    Predict the priority of a task based on its title and description.
    
    Args:
        title: The task title
        description: The task description
        
    Returns:
        str: 'low', 'medium', or 'high'
    """
    text = (title + ' ' + description).lower()
    
    # Check for high priority keywords
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in text:
            return 'high'
    
    # Check for low priority keywords
    for keyword in LOW_PRIORITY_KEYWORDS:
        if keyword in text:
            return 'low'
    
    return 'medium'


def categorize_task(title: str, description: str = '') -> str:
    """
    Categorize a task based on its title and description.
    
    Args:
        title: The task title
        description: The task description
        
    Returns:
        str: The predicted category
    """
    text = (title + ' ' + description).lower()
    
    # Count matches for each category
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            category_scores[category] = score
    
    # Return the category with the highest score
    if category_scores:
        return max(category_scores, key=category_scores.get)
    
    return 'General'


def ensure_nltk_data():
    """Ensure required NLTK data is downloaded."""
    import nltk
    required_resources = ['punkt_tab', 'averaged_perceptron_tagger_eng']
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource else f'taggers/{resource}')
        except (LookupError, AttributeError):
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass


def estimate_difficulty(title: str, description: str = '') -> dict:
    """
    Estimate task difficulty using NLP analysis with TextBlob.
    
    Analyzes:
    - Complexity keywords
    - Text length and word count
    - Sentence structure
    - Multi-step indicators
    - Subjectivity (more subjective = potentially more complex)
    
    Args:
        title: The task title
        description: The task description
        
    Returns:
        dict: Contains 'level' (easy/medium/hard), 'score' (1-10), and 'reasons'
    """
    ensure_nltk_data()
    text = (title + ' ' + description).strip()
    text_lower = text.lower()
    
    # Initialize score (1-10 scale)
    score = 5.0
    reasons = []
    
    # Use TextBlob for NLP analysis
    try:
        blob = TextBlob(text)
    except Exception:
        # Fallback if TextBlob initialization fails
        return {
            'level': 'medium',
            'score': 5.0,
            'reasons': ["AI analysis unavailable"]
        }
    
    # 1. Analyze word count
    word_count = len(blob.words)
    if word_count > 20:
        score += 1.5
        reasons.append(f"Detailed description ({word_count} words)")
    elif word_count > 10:
        score += 0.5
    elif word_count < 5:
        score -= 1.0
        reasons.append("Brief task")
    
    # 2. Check for complexity keywords
    hard_matches = sum(1 for kw in HARD_TASK_KEYWORDS if kw in text_lower)
    medium_matches = sum(1 for kw in MEDIUM_TASK_KEYWORDS if kw in text_lower)
    easy_matches = sum(1 for kw in EASY_TASK_KEYWORDS if kw in text_lower)
    
    if hard_matches > 0:
        score += hard_matches * 1.0
        reasons.append(f"Complex action words detected ({hard_matches})")
    if medium_matches > 0:
        score += medium_matches * 0.3
    if easy_matches > 0:
        score -= easy_matches * 0.5
        if not reasons:
            reasons.append("Simple action words")
    
    # 3. Check for multi-step indicators
    multi_step_count = sum(1 for indicator in MULTI_STEP_INDICATORS if indicator in text_lower)
    if multi_step_count > 0:
        score += multi_step_count * 0.7
        reasons.append(f"Multi-step task ({multi_step_count} steps)")
    
    # 4. Analyze sentence count (more sentences = more complex)
    sentence_count = len(blob.sentences)
    if sentence_count > 3:
        score += 1.0
        reasons.append(f"Multiple requirements ({sentence_count} sentences)")
    
    # 5. Analyze subjectivity (subjective tasks can be harder to complete)
    subjectivity = blob.sentiment.subjectivity
    if subjectivity > 0.6:
        score += 0.5
        reasons.append("Subjective/creative task")
    
    # 6. Check for technical terms (noun phrases that might be technical)
    noun_phrases = blob.noun_phrases
    technical_indicators = ['api', 'database', 'server', 'code', 'system', 'algorithm', 'function']
    technical_count = sum(1 for np in noun_phrases for ti in technical_indicators if ti in np.lower())
    if technical_count > 0:
        score += technical_count * 0.5
        reasons.append("Technical terminology detected")
    
    # Clamp score between 1 and 10
    score = max(1.0, min(10.0, score))
    
    # Determine difficulty level
    if score <= 3.5:
        level = 'easy'
    elif score <= 6.5:
        level = 'medium'
    else:
        level = 'hard'
    
    # Add default reason if none
    if not reasons:
        reasons.append("Standard task complexity")
    
    return {
        'level': level,
        'score': round(score, 1),
        'reasons': reasons
    }
