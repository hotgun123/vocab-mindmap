const fs = require('fs');
const path = require('path');

const VOCAB_FILE = path.join(__dirname, '../data/vocabulary.json');
const DELAY_MS = 300; // 300ms between requests to avoid rate limits

async function fetchIPA(word) {
  try {
    const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`);
    if (!response.ok) {
      if (response.status === 404) return null; // Word not found
      if (response.status === 429) {
        console.warn(`\nRate limited! Waiting 5 seconds before retrying ${word}...`);
        await new Promise(r => setTimeout(r, 5000));
        return fetchIPA(word);
      }
      return null;
    }
    const data = await response.json();
    
    // Extract IPA from phonetics array
    if (data && data.length > 0 && data[0].phonetics) {
      for (const phonetic of data[0].phonetics) {
        if (phonetic.text && phonetic.text.length > 0) {
          return phonetic.text;
        }
      }
    }
    return null;
  } catch (error) {
    console.error(`Error fetching IPA for ${word}:`, error.message);
    return null;
  }
}

async function main() {
  console.log('Reading vocabulary data...');
  const rawData = fs.readFileSync(VOCAB_FILE, 'utf8');
  const vocabJSON = JSON.parse(rawData);
  const data = vocabJSON.data;
  
  console.log(`Total entries to process: ${data.length}`);
  let updatedCount = 0;
  let notFoundCount = 0;
  
  // Create a cache to avoid looking up the same word multiple times (since multiple ids can have the same word)
  const ipaCache = {};

  for (let i = 0; i < data.length; i++) {
    const entry = data[i];
    
    // Skip if already has ipa (if user runs script again to resume)
    if (entry.ipa) continue;

    let ipa = ipaCache[entry.word];
    
    if (!ipa) {
      ipa = await fetchIPA(entry.word);
      if (ipa) {
        ipaCache[entry.word] = ipa;
      } else {
        // Fallback to phonetic if API fails/not found
        ipa = entry.phonetic || "";
        ipaCache[entry.word] = ipa;
        notFoundCount++;
      }
      // Delay to respect rate limit
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    
    entry.ipa = ipa;
    updatedCount++;
    
    // Progress logging
    if (i % 100 === 0 && i > 0) {
      process.stdout.write(`\rProcessed ${i}/${data.length} (${Math.round((i/data.length)*100)}%). Updated: ${updatedCount}`);
      
      // Save intermediate progress every 500 words to avoid data loss
      if (i % 500 === 0) {
        fs.writeFileSync(VOCAB_FILE, JSON.stringify(vocabJSON, null, 2));
      }
    }
  }
  
  console.log(`\n\nFinished processing!`);
  console.log(`Successfully fetched or updated: ${updatedCount} entries.`);
  console.log(`Using fallback phonetic for: ${notFoundCount} entries.`);
  
  // Final save
  console.log('Saving final vocabulary.json...');
  fs.writeFileSync(VOCAB_FILE, JSON.stringify(vocabJSON, null, 2));
  console.log('Done!');
}

main().catch(console.error);
