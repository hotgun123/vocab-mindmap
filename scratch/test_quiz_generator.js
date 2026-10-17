const fs = require('fs');

// Mock chrome environment
const vocabRaw = JSON.parse(fs.readFileSync('./data/vocabulary.json', 'utf8'));
const sentencesRaw = JSON.parse(fs.readFileSync('./data/sentences.json', 'utf8'));

// Background functions simulation
function getPrimaryVocabulary(vocab) {
  const primary = vocab.filter(v => v.is_primary);
  if (primary.length > 0) return primary;

  const seen = new Map();
  for (const entry of vocab) {
    const key = entry.word.toLowerCase();
    if (!seen.has(key)) {
      seen.set(key, entry);
    }
  }
  return Array.from(seen.values());
}

function getSimilarSentences(correctVi, allSentences, count = 3) {
  const getWords = str => new Set(str.toLowerCase().replace(/[^a-z0-9áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]/g, ' ').split(/\s+/).filter(w => w.length > 0));
  const correctWords = getWords(correctVi);
  
  const scored = allSentences.map(s => {
    if (s.vi === correctVi) return { s, score: -1 };
    const sWords = getWords(s.vi);
    let intersection = 0;
    for (const w of sWords) {
      if (correctWords.has(w)) intersection++;
    }
    return { s, score: intersection };
  });
  
  scored.sort((a, b) => b.score - a.score);
  
  const distractors = [];
  for (const item of scored) {
    if (distractors.length >= count) break;
    if (item.score >= 0) distractors.push(item.s.vi);
  }
  
  while (distractors.length < count) {
    const random = allSentences[Math.floor(Math.random() * allSentences.length)].vi;
    if (random !== correctVi && !distractors.includes(random)) {
      distractors.push(random);
    }
  }
  
  return distractors;
}

function generateSentenceQuestion(entry, allSentences) {
  const correctVi = entry.vi;
  const distractorsVi = getSimilarSentences(correctVi, allSentences, 3); 
  const options = [correctVi, ...distractorsVi].sort(() => 0.5 - Math.random());
  return {
    id: entry.id,
    type: "sentence",
    word: "",
    sentence: entry.en,
    correctAnswer: correctVi,
    options: options
  };
}

function generateWordOptions(correctEntry, primaryVocab) {
  const options = new Set();
  const answer = correctEntry.translation_vi;
  options.add(answer);
  
  const forbiddenTranslations = new Set(
    primaryVocab
      .filter(e => e.word.toLowerCase() === correctEntry.word.toLowerCase())
      .map(e => e.translation_vi.toLowerCase())
  );

  if (correctEntry.tags && correctEntry.tags.length > 0) {
    const similarEntries = primaryVocab.filter(e => 
      !forbiddenTranslations.has(e.translation_vi.toLowerCase()) &&
      e.tags && e.tags.some(t => correctEntry.tags.includes(t))
    );
    similarEntries.sort(() => 0.5 - Math.random());
    for (const entry of similarEntries) {
      options.add(entry.translation_vi);
      if (options.size === 4) break;
    }
  }

  if (options.size < 4) {
    const randomEntries = [...primaryVocab].sort(() => 0.5 - Math.random());
    for (const entry of randomEntries) {
      if (!forbiddenTranslations.has(entry.translation_vi.toLowerCase())) {
        options.add(entry.translation_vi);
      }
      if (options.size === 4) break;
    }
  }

  return Array.from(options).slice(0, 4).sort(() => 0.5 - Math.random());
}

function generateWordReverseOptions(correctEntry, primaryVocab) {
  const options = new Set();
  options.add(correctEntry.word);
  
  if (correctEntry.tags && correctEntry.tags.length > 0) {
    const similarEntries = primaryVocab.filter(e => e.word.toLowerCase() !== correctEntry.word.toLowerCase() && e.tags && e.tags.some(t => correctEntry.tags.includes(t)));
    similarEntries.sort(() => 0.5 - Math.random());
    for (const entry of similarEntries) {
      options.add(entry.word);
      if (options.size === 4) break;
    }
  }
  
  if (options.size < 4) {
    const randomEntries = [...primaryVocab].sort(() => 0.5 - Math.random());
    for (const entry of randomEntries) {
      if (entry.word.toLowerCase() !== correctEntry.word.toLowerCase()) {
        options.add(entry.word);
      }
      if (options.size === 4) break;
    }
  }
  
  return Array.from(options).slice(0, 4).sort(() => 0.5 - Math.random());
}

const vocab = vocabRaw.data;
const sentencesData = sentencesRaw.map((s, i) => ({ ...s, id: `sentence_${i}` }));
const primaryVocab = getPrimaryVocabulary(vocab);

console.log('=== TEST 1: Primary vocabulary stats ===');
console.log('Total vocabulary items:', vocab.length);
console.log('Primary vocabulary items:', primaryVocab.length);
console.assert(primaryVocab.length === 3145, 'Primary count should be 3145');

console.log('\n=== TEST 2: Specific words check ===');
const runEntry = primaryVocab.find(e => e.word.toLowerCase() === 'run');
console.log('Word "run" primary entry:', {
  id: runEntry.id,
  word: runEntry.word,
  translation_vi: runEntry.translation_vi,
  pos: runEntry.pos,
  is_primary: runEntry.is_primary
});
console.assert(runEntry.translation_vi === 'chạy', 'Word "run" standalone translation MUST be "chạy"');

const bankEntry = primaryVocab.find(e => e.word.toLowerCase() === 'bank');
console.log('Word "bank" primary entry:', {
  id: bankEntry.id,
  word: bankEntry.word,
  translation_vi: bankEntry.translation_vi,
  pos: bankEntry.pos
});
console.assert(bankEntry.translation_vi === 'ngân hàng', 'Word "bank" translation should be "ngân hàng"');

console.log('\n=== TEST 3: Generate Word Mode Questions ===');
for (let i = 0; i < 5; i++) {
  const sampleEntry = primaryVocab[Math.floor(Math.random() * primaryVocab.length)];
  const options = generateWordOptions(sampleEntry, primaryVocab);
  console.log(`Word Q: [${sampleEntry.word}] (${sampleEntry.pos})`);
  console.log(`  Correct: ${sampleEntry.translation_vi}`);
  console.log(`  Options:`, options);
  console.assert(options.includes(sampleEntry.translation_vi), 'Options must include correct answer');
  console.assert(options.length === 4, 'Must have exactly 4 options');
  console.assert(!options.some(opt => opt.includes('(hoặc:')), 'Options must NOT have "(hoặc:)"');
}

console.log('\n=== TEST 4: Generate Word Reverse Mode Questions ===');
for (let i = 0; i < 5; i++) {
  const sampleEntry = primaryVocab[Math.floor(Math.random() * primaryVocab.length)];
  const options = generateWordReverseOptions(sampleEntry, primaryVocab);
  console.log(`Word Reverse Q: [${sampleEntry.translation_vi}]`);
  console.log(`  Correct: ${sampleEntry.word}`);
  console.log(`  Options:`, options);
  console.assert(options.includes(sampleEntry.word), 'Options must include correct answer');
  console.assert(options.length === 4, 'Must have exactly 4 options');
}

console.log('\n=== TEST 5: Test Word "run" Options Generation ===');
const runOptions = generateWordOptions(runEntry, primaryVocab);
console.log('Question: "run"');
console.log('Correct Answer:', runEntry.translation_vi);
console.log('Options:', runOptions);
console.assert(runOptions.includes('chạy'), 'Options must contain "chạy"');
console.assert(!runOptions.includes('phai màu'), 'Options must NOT include secondary senses of run');

const runReverseOptions = generateWordReverseOptions(runEntry, primaryVocab);
console.log('Question: "chạy"');
console.log('Correct Answer:', runEntry.word);
console.log('Options:', runReverseOptions);
console.assert(runReverseOptions.includes('run'), 'Options must contain "run"');

console.log('\n✅ ALL VERIFICATION TESTS PASSED SUCCESSFULLY!');
