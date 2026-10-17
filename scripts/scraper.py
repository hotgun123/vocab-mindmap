import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

WORDS_FILE = "word_list.txt"
OUTPUT_FILE = "../data/vocabulary.json"

def scrape_cambridge(word):
    url = f"https://dictionary.cambridge.org/vi/dictionary/english-vietnamese/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {word}: Status {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        entries = []
        
        # Dictionary blocks usually have class 'pr dictionary' or 'di-body'
        # To be safe, we can find all '.dsense' blocks directly
        
        for entry_idx, sense in enumerate(soup.select('.dsense')):
            # Find the closest parent that contains the headword, or fallback to the main headword of the page
            parent_entry = sense.find_previous(class_='di-head')
            
            headword_elem = parent_entry.select_one('.dhw') if parent_entry else soup.select_one('.dhw')
            headword = headword_elem.text.strip() if headword_elem else word
            
            pos_elem = parent_entry.select_one('.dpos') if parent_entry else soup.select_one('.dpos')
            pos = pos_elem.text.strip() if pos_elem else "unknown"
            
            phonetic_elem = parent_entry.select_one('.ipa.dipa') if parent_entry else soup.select_one('.ipa.dipa')
            phonetic = f"/{phonetic_elem.text.strip()}/" if phonetic_elem else ""
            
            # Definition EN
            def_elem = sense.select_one('.def.ddef_d')
            if not def_elem:
                continue
            definition = def_elem.text.strip()
            
            # Translation VI
            trans_elem = sense.select_one('.trans.dtrans')
            if not trans_elem:
                continue
            translation = trans_elem.text.strip()
            
            # Example EN
            eg_elem = sense.select_one('.eg.deg')
            example_en = eg_elem.text.strip() if eg_elem else ""
            
            # Bỏ qua nếu không có đủ data cần thiết
            if not definition or not translation or not example_en:
                continue
                
            entry_id = f"{headword}_{pos}_{entry_idx}".replace(" ", "_")
            
            entries.append({
                "id": entry_id,
                "word": headword,
                "pos": pos,
                "phonetic": phonetic,
                "definition_en": definition,
                "translation_vi": translation,
                "example_en": example_en,
                "example_vi": "", # Cambridge VI dictionary doesn't always have VI translation for examples
                "difficulty": 1, # Default
                "tags": [],
                "related_meanings": []
            })
                
        return entries
        
    except Exception as e:
        print(f"Error scraping {word}: {e}")
        return []

def main():
    if not os.path.exists(WORDS_FILE):
        print(f"{WORDS_FILE} not found!")
        return
        
    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
        
    # Remove duplicates
    words = list(dict.fromkeys(words))
    
    print(f"Found {len(words)} unique words to scrape.")
    
    all_entries = []
    
    for i, word in enumerate(words):
        print(f"Scraping [{i+1}/{len(words)}]: {word}...")
        
        entries = scrape_cambridge(word)
        all_entries.extend(entries)
        
        # Rate limiting
        time.sleep(random.uniform(1, 3))
        
    # Post-processing: Add related meanings
    for i, entry in enumerate(all_entries):
        # Tìm các entries cùng word
        related = [e['id'] for e in all_entries if e['word'] == entry['word'] and e['id'] != entry['id']]
        entry['related_meanings'] = related
        
    # Build final JSON structure
    output_data = {
        "version": "1.0",
        "totalWords": len(words),
        "totalEntries": len(all_entries),
        "data": all_entries
    }
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"\nDone! Scraped {len(all_entries)} entries for {len(words)} words.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
