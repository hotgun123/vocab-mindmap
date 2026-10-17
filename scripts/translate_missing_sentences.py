import json
import os
import sys
import urllib.parse
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

CACHE_PATH = os.path.join(DATA_DIR, 'sentence_translations_cache.json')
VOCAB_JSON_PATH = os.path.join(DATA_DIR, 'topics_vocabulary.json')
VOCAB_JS_PATH = os.path.join(DATA_DIR, 'topics_vocab_data.js')

# Load cache
trans_cache = {}
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, 'r', encoding='utf-8') as f:
            trans_cache = json.load(f)
    except Exception as e:
        print("Error loading cache:", e)

print(f"Initial cache entries: {len(trans_cache)}")

def translate(text):
    text = text.strip()
    if not text:
        return ""
    if text in trans_cache and trans_cache[text]:
        return trans_cache[text]
    
    # 1. Chrome Extension translate API
    try:
        url = 'https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=en&tl=vi&q=' + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0:
                res_text = data[0] if isinstance(data[0], str) else data[0][0]
                trans_cache[text] = res_text
                return res_text
    except Exception:
        pass

    # 2. Fallback: MyMemory API
    try:
        url = f'https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|vi'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            res_text = data['responseData']['translatedText']
            if res_text and 'MYMEMORY WARNING' not in res_text:
                trans_cache[text] = res_text
                return res_text
    except Exception:
        pass

    return ""

# Load topics_vocabulary.json
with open(VOCAB_JSON_PATH, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

# Collect missing sentences
missing_sents = set()
for item in vocab_data['words']:
    for ex in item.get('examples', []):
        en = ex.get('en', '').strip()
        if en:
            if en in trans_cache and trans_cache[en]:
                ex['vi'] = trans_cache[en]
            elif not ex.get('vi'):
                missing_sents.add(en)

print(f"Unique sentences to translate: {len(missing_sents)}")

if missing_sents:
    sent_list = list(missing_sents)
    start_t = time.time()
    completed = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        for en, vi in zip(sent_list, executor.map(translate, sent_list)):
            completed += 1
            if vi:
                trans_cache[en] = vi
            if completed % 200 == 0 or completed == len(sent_list):
                print(f"Translated: {completed}/{len(sent_list)} ({time.time() - start_t:.1f}s)")
                # Periodically save cache snapshot
                if completed % 1000 == 0:
                    snapshot = dict(trans_cache)
                    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
                        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    # Final save cache
    snapshot = dict(trans_cache)
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"Saved cache with {len(snapshot)} entries.")

# Fill translations into vocabulary
total_filled = 0
for item in vocab_data['words']:
    for ex in item.get('examples', []):
        en = ex.get('en', '').strip()
        if not ex.get('vi') and en in trans_cache:
            ex['vi'] = trans_cache[en]
        if ex.get('vi'):
            total_filled += 1

print(f"Total example sentences with Vietnamese translation: {total_filled}")

# Save JSON
with open(VOCAB_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(vocab_data, f, ensure_ascii=False, indent=2)
print("Updated topics_vocabulary.json")

# Save JS for local file:// usage
with open(VOCAB_JS_PATH, 'w', encoding='utf-8') as f:
    f.write("// Auto-generated vocabulary by topics dataset\n")
    f.write("window.VOCAB_TOPICS_METADATA = " + json.dumps({
        "version": "1.0",
        "totalWords": len(vocab_data['words']),
        "topicGroups": vocab_data['topicGroups']
    }, ensure_ascii=False) + ";\n\n")
    f.write("window.VOCAB_WORDS = " + json.dumps(vocab_data['words'], ensure_ascii=False) + ";\n")
print("Updated topics_vocab_data.js")
