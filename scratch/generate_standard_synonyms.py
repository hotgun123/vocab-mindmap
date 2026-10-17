import json
import os
import urllib.request
import urllib.parse
import concurrent.futures
import time
import threading
from nltk.corpus import wordnet as wn

VOCAB_PATH = "d:/extension English/BOT-idicator/extension English/data/vocabulary.json"
OUTPUT_PATH = "d:/extension English/BOT-idicator/extension English/data/synonyms.json"

# Thread-safe cache for Datamuse API calls
cache_lock = threading.Lock()
datamuse_cache = {}

def get_wordnet_pos(pos_str):
    pos_str = pos_str.lower()
    if 'adjective' in pos_str or pos_str == 'adj':
        return wn.ADJ
    elif 'noun' in pos_str or pos_str == 'n':
        return wn.NOUN
    elif 'verb' in pos_str or pos_str == 'v':
        return wn.VERB
    elif 'adverb' in pos_str or pos_str == 'adv':
        return wn.ADV
    return None

def get_datamuse_pos_tag(pos_str):
    pos_str = pos_str.lower()
    if 'adjective' in pos_str:
        return 'adj'
    elif 'noun' in pos_str:
        return 'n'
    elif 'verb' in pos_str:
        return 'v'
    elif 'adverb' in pos_str:
        return 'adv'
    return None

def fetch_datamuse_candidates(word):
    # Check cache first
    with cache_lock:
        if word in datamuse_cache:
            return datamuse_cache[word]
            
    url = f"https://api.datamuse.com/words?ml={urllib.parse.quote(word)}&md=p"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read().decode('utf-8'))
            with cache_lock:
                datamuse_cache[word] = res
            return res
    except Exception as e:
        print(f"Error fetching Datamuse for {word}: {e}")
        return []

def get_wordnet_synonyms(word, wn_pos):
    synonyms = set()
    synsets = wn.synsets(word, pos=wn_pos)
    for syn in synsets:
        # Direct lemmas in the synset
        for lemma in syn.lemmas():
            name = lemma.name().lower().replace('_', ' ').replace('-', ' ').strip()
            if name != word:
                synonyms.add(name)
        # Lemmas in similar_to synsets
        for sim in syn.similar_tos():
            for lemma in sim.lemmas():
                name = lemma.name().lower().replace('_', ' ').replace('-', ' ').strip()
                if name != word:
                    synonyms.add(name)
    return synonyms

def process_entry(entry, vocab_words):
    word = entry["word"].lower().strip()
    pos = entry["pos"]
    
    wn_pos = get_wordnet_pos(pos)
    dm_pos = get_datamuse_pos_tag(pos)
    
    if not wn_pos or not dm_pos:
        return entry["id"], []
        
    # Get WordNet synonyms
    wn_syns = get_wordnet_synonyms(word, wn_pos)
    
    # Get Datamuse candidates
    dm_candidates = fetch_datamuse_candidates(word)
    
    # Filter Datamuse candidates by POS and quality
    dm_syns = []
    for cand in dm_candidates:
        cand_word = cand.get('word', '').lower().strip()
        tags = cand.get('tags', [])
        
        # Must match the part of speech tag
        if dm_pos not in tags:
            continue
            
        # Ignore same word or derivatives (e.g. accept -> acceptable)
        if cand_word == word or cand_word.startswith(word) or word.startswith(cand_word):
            continue
            
        dm_syns.append(cand_word)
        
    # Find intersection of WordNet and Datamuse synonyms
    intersection = [s for s in dm_syns if s in wn_syns]
    
    # Sort candidates by prioritizing those in the vocabulary
    final_syns = []
    
    # Priority 1: Synonyms in both WordNet and Datamuse that are in the vocabulary
    in_vocab_intersection = [s for s in intersection if s in vocab_words]
    final_syns.extend(in_vocab_intersection)
    
    # Priority 2: Synonyms in Datamuse (matching POS) that are in the vocabulary
    in_vocab_dm = [s for s in dm_syns if s in vocab_words and s not in final_syns]
    final_syns.extend(in_vocab_dm)
    
    # Priority 3: Synonyms in both WordNet and Datamuse (general, even if not in vocabulary)
    general_intersection = [s for s in intersection if s not in final_syns]
    final_syns.extend(general_intersection[:3]) # Limit to top 3
    
    # Priority 4: Top Datamuse synonyms (general, even if not in vocabulary)
    general_dm = [s for s in dm_syns if s not in final_syns]
    final_syns.extend(general_dm[:2]) # Limit to top 2
    
    # Remove duplicates while maintaining order
    seen = set()
    unique_syns = []
    for s in final_syns:
        if s not in seen and s != word:
            seen.add(s)
            unique_syns.append(s)
            
    # Filter out multi-word synonyms if they are too long (keep it simple for quizing, e.g. <= 2 words)
    unique_syns = [s for s in unique_syns if len(s.split()) <= 2]
            
    return entry["id"], unique_syns

def main():
    if not os.path.exists(VOCAB_PATH):
        print("Vocabulary file not found!")
        return
        
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
        
    entries = vocab.get("data", [])
    vocab_words = set(e["word"].lower().strip() for e in entries)
    
    print(f"Total entries: {len(entries)}")
    print(f"Total unique words: {len(vocab_words)}")
    
    synonym_map = {}
    
    # We will process entries in parallel to make it fast
    # Limit workers to 25 to avoid heavy rate limiting
    start_time = time.time()
    
    # Filter entries that have a valid POS
    valid_entries = [e for e in entries if get_wordnet_pos(e["pos"]) is not None]
    print(f"Processing {len(valid_entries)} valid POS entries...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        # Create a mapping of future to entry ID
        future_to_entry = {executor.submit(process_entry, entry, vocab_words): entry for entry in valid_entries}
        
        for idx, future in enumerate(concurrent.futures.as_completed(future_to_entry)):
            entry = future_to_entry[future]
            try:
                entry_id, syns = future.result()
                if syns:
                    synonym_map[entry_id] = syns
            except Exception as exc:
                print(f"Entry {entry['id']} generated an exception: {exc}")
                
            if (idx + 1) % 500 == 0:
                print(f"Processed {idx + 1}/{len(valid_entries)} entries...")
                
    duration = time.time() - start_time
    print(f"Finished processing in {duration:.2f} seconds.")
    print(f"Entries with synonyms: {len(synonym_map)}")
    
    # Save synonyms
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        json.dump(synonym_map, f_out, ensure_ascii=False, indent=2)
    print(f"Saved standard synonyms to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
