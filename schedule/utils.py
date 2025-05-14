import re

import fasttext

model = fasttext.load_model("fasttext_models/lid.176.bin")
COMMON_ENGLISH_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
    'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
    'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
    'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
    'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
    'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
    'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
    'give', 'day', 'most', 'us', 'something', 'thing', 'other'
}


def detect_lang_fasttext(text):
    prediction = model.predict(text)
    lang = prediction[0][0].replace("__label__", "")
    confidence = prediction[1][0]
    return lang, confidence


def is_meaningful(text, allowed_langs=('en', 'ru'), confidence_threshold=0.5):
    tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_ratio = sum(1 for t in tokens if t in COMMON_ENGLISH_WORDS) / max(1, len(tokens))
    print(f'Word ratio: {word_ratio:.2f}')
    if word_ratio > 0.5:
        return True
    lang, conf = detect_lang_fasttext(text)
    print(f'Detected: {lang} ({conf:.2f})')
    return lang in allowed_langs and conf >= confidence_threshold
