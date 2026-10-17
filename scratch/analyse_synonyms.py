import json
import urllib.request
import urllib.parse
import os
import concurrent.futures
from queue import Queue

VOCAB_PATH = "d:/extension English/BOT-idicator/extension English/data/vocabulary.json"

def fetch_synonyms(word):
    url = f"https://api.datamuse.com/words?rel_syn={urllib.parse.quote(word)}"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return word, [item['word'] for item in data if 'word' in item]
    except Exception as e:
        return word, None

def main():
    if not os.path.exists(VOCAB_PATH):
        print("Vocabulary file not found!")
        return
        
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
        
    entries = vocab.get("data", [])
    unique_words = sorted(list(set(e["word"].lower().strip() for e in entries)))
    
    print(f"Total entries: {len(entries)}")
    print(f"Total unique words: {len(unique_words)}")
    
    word_set = set(unique_words)
    synonym_map = {}
    
    print("Fetching synonyms from Datamuse...")
    start_time = time.time() if 'time' in globals() else 0
    import time
    start_time = time.time()
    
    # Using ThreadPoolExecutor for fast network requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_synonyms, unique_words)
        
        for idx, (word, syns) in enumerate(results):
            if syns:
                # Filter to only synonyms that are in our vocabulary AND not equal to the word itself
                in_vocab_syns = [s for s in syns if s.lower().strip() in word_set and s.lower().strip() != word]
                if in_vocab_syns:
                    synonym_map[word] = in_vocab_syns
            
            if (idx + 1) % 500 == 0:
                print(f"Processed {idx + 1}/{len(unique_words)} words...")

    duration = time.time() - start_time
    print(f"Finished fetching in {duration:.2f} seconds.")
    print(f"Words with synonyms in vocabulary: {len(synonym_map)}")
    
    # Save the mapped synonyms
    output_path = "d:/extension English/BOT-idicator/extension English/data/synonyms.json"
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(synonym_map, f_out, ensure_ascii=False, indent=2)
    print(f"Saved synonyms to {output_path}")

if __name__ == "__main__":
    main()
