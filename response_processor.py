"""
Response processing and naturalization
"""

import re
from config import HELPFUL_CONTACTS


def clean_bullet_formatting(text: str) -> str:
    """
    Clean and standardize bullet point formatting.
    Removes mixed bullet styles and standardizes to clean format.
    
    Args:
        text: Text with potential bullet points
        
    Returns:
        Cleaned text with standardized bullet points
    """
    # Replace mixed bullet formats with clean ones
    # Remove "• *" patterns and similar
    text = re.sub(r'•\s*\*\s*', '• ', text)
    text = re.sub(r'•\s*•\s*', '• ', text)
    text = re.sub(r'-\s*\*\s*', '• ', text)
    text = re.sub(r'\*\s*•\s*', '• ', text)
    
    # Standardize all bullet markers to "•"
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    
    # Remove extra spaces after bullets
    text = re.sub(r'•\s+', '• ', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def format_as_bullets(text: str, max_bullets: int = 5) -> str:
    """
    Convert long paragraphs into bullet points if needed.
    
    Args:
        text: Text to format
        max_bullets: Maximum number of bullet points
        
    Returns:
        Formatted text with bullet points
    """
    # Clean existing bullet formatting first
    text = clean_bullet_formatting(text)
    
    # If already has bullets or is short, return as is
    if len(text) < 200 or ('•' in text and text.count('\n') > 1):
        return text
    
    # Split by sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    # If we have multiple meaningful sentences, convert to bullets
    if len(sentences) > 2:
        bullets = []
        for i, sentence in enumerate(sentences[:max_bullets]):
            if sentence:
                bullets.append(f"• {sentence}")
        if bullets:
            return "\n".join(bullets)
    
    return text


def fix_emoji_alignment(text: str) -> str:
    """
    Fix emoji and text alignment issues - ensure emojis stay with their text.
    
    Args:
        text: Text with potential emoji alignment issues
        
    Returns:
        Text with fixed emoji alignment
    """
    # Fix emojis that are on separate lines from their text
    # Pattern: emoji on one line, text on next line
    text = re.sub(r'([🚀✨💼👥📞📧💡🌐😊☀️])\s*\n\s*([A-Za-z])', r'\1 \2', text)
    
    # Fix emojis at end of lines that should be with next line
    text = re.sub(r'([🚀✨💼👥📞📧💡🌐😊☀️])\s*\n', r' \1\n', text)
    
    # Ensure emojis have space after them if followed by text
    text = re.sub(r'([🚀✨💼👥📞📧💡🌐😊☀️])([A-Za-z])', r'\1 \2', text)
    
    # Remove multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix bullet points with emojis - ensure emoji is on same line as bullet
    lines = text.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            fixed_lines.append('')
            continue
        
        # If line starts with emoji and next line is bullet, combine them
        if i < len(lines) - 1 and re.match(r'^[🚀✨💼👥📞📧💡🌐😊☀️]', line):
            next_line = lines[i + 1].strip()
            if next_line.startswith('•'):
                # Combine emoji with bullet
                fixed_lines.append(line + ' ' + next_line)
                lines[i + 1] = ''  # Mark next line as processed
                continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def make_response_natural(answer: str, question: str) -> str:
    """
    Post-process response to make it more natural, concise, and engaging.
    
    Args:
        answer: Generated answer text
        question: User's question
        
    Returns:
        Naturalized and formatted answer text
    """
    # Replace boring/robotic phrases with engaging alternatives
    replacements = {
        "I'm sorry, but the provided context does not contain": 
            "I don't have that info, but",
        "the provided context does not contain": 
            "I don't have that available, but",
        "I cannot find information about": 
            "I'm not certain about",
        "Based on the provided context": 
            "Based on what I know",
        "According to the provided context": 
            "From what I can see",
        "the context does not": 
            "I don't have that detail, but",
        "Sure, I can help you with that": 
            "Absolutely! 😊",
        "Here's how": 
            "Here's how",
        "Here's what": 
            "Here's what",
    }
    
    answer_lower = answer.lower()
    for robotic_phrase, natural_phrase in replacements.items():
        if robotic_phrase.lower() in answer_lower:
            pattern = re.compile(re.escape(robotic_phrase), re.IGNORECASE)
            answer = pattern.sub(natural_phrase, answer)
    
    # Clean and format bullet points
    answer = clean_bullet_formatting(answer)
    answer = format_as_bullets(answer)
    
    # Add emojis contextually and engagingly
    question_lower = question.lower()
    
    # Remove standalone emoji lines and attach them properly
    answer = fix_emoji_alignment(answer)
    
    # Service-related questions - add engaging emoji
    if any(word in question_lower for word in ['service', 'offer', 'provide', 'what do you']):
        if not any(emoji in answer for emoji in ['🚀', '✨', '💼']):
            if answer.startswith('•'):
                answer = '🚀 ' + answer
            elif len(answer) < 150:
                answer = answer.rstrip('.!?') + ' ✨'
    
    # Contact/HR related - add contact emojis inline
    if any(word in question_lower for word in ['contact', 'phone', 'email', 'hr', 'reach']):
        answer = answer.replace('+91', '📞 +91')
        answer = answer.replace(' hr@', ' 📧 hr@')
        answer = answer.replace('@empiric', '📧 @empiric')
    
    # Job/career related - make it engaging
    job_keywords = [
        'job', 'career', 'vacancy', 'opening', 'position', 
        'hire', 'employment', 'hr', 'apply'
    ]
    if any(keyword in question_lower for keyword in job_keywords):
        if "hr@" not in answer.lower() and "6355" not in answer:
            if any(phrase in answer.lower() for phrase in [
                "don't have", "not certain", "not available"
            ]):
                answer += (
                    f"\n\n💡 Need more info? Contact HR:\n"
                    f"• 📞 {HELPFUL_CONTACTS['hr']['phone']}\n"
                    f"• 📧 {HELPFUL_CONTACTS['hr']['email']}\n"
                    f"• 🌐 Check career page for openings"
                )
    
    # Make opening more engaging
    if answer.startswith('Sure') or answer.startswith('Here'):
        # Add friendly emoji at start
        if not answer[0] in ['🚀', '✨', '💼', '👥', '📞', '💡']:
            answer = '😊 ' + answer
    
    # Limit response length - keep it concise and engaging
    if len(answer) > 500:
        lines = answer.split('\n')
        if len(lines) > 8:
            answer = '\n'.join(lines[:8]) + '\n\n...'
    
    return answer

