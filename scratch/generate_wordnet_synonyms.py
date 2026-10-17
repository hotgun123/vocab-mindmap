import json
import os
from nltk.corpus import wordnet as wn

VOCAB_PATH = "d:/extension English/BOT-idicator/extension English/data/vocabulary.json"

def get_wordnet_pos(pos_str):
    pos_str = pos_str.lower()
    if 'adjective' in pos_str:
        return wn.ADJ
    elif 'noun' in pos_str:
        return wn.NOUN
    elif 'verb' in pos_str:
        return wn.VERB
    elif 'adverb' in pos_str:
        return wn.ADV
    return None

def main():
    if not os.path.exists(VOCAB_PATH):
        print("Vocabulary file not found!")
        return
        
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
        
    entries = vocab.get("data", [])
    
    # Map words to their parts of speech in the vocab
    vocab_words = set(e["word"].lower().strip() for e in entries)
    
    synonym_map = {} # Maps entry_id -> list of synonyms in vocabulary
    
    for entry in entries:
        word = entry["word"].lower().strip()
        pos = entry["pos"]
        wn_pos = get_wordnet_pos(pos)
        
        if not wn_pos:
            continue
            
        # Get synonyms from WordNet
        synsets = wn.synsets(word, pos=wn_pos)
        lemmas = set()
        for syn in synsets:
            for lemma in syn.lemmas():
                lemma_name = lemma.name().lower().replace('_', ' ').replace('-', ' ').strip()
                if lemma_name != word:
                    lemmas.add(lemma_name)
                    
        # Filter lemmas to those present in our vocabulary
        in_vocab_syns = sorted(list(set(l for l in lemmas if l in vocab_words)))
        if in_vocab_syns:
            synonym_map[entry["id"]] = in_vocab_syns
            
    print(f"Total vocabulary entries: {len(entries)}")
    print(f"Entries with WordNet synonyms in vocabulary: {len(synonym_map)}")
    
    # Save the mapping
    output_path = "d:/extension English/BOT-idicator/extension English/data/synonyms.json"
    with open(output_path, "w", encoding="utf-8") as f_out:
        json.dump(synonym_map, f_out, ensure_ascii=False, indent=2)
    print(f"Saved synonyms to {output_path}")

if __name__ == "__main__":
    main()
