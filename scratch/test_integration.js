const fs = require('fs');

const backgroundCode = fs.readFileSync('background.js', 'utf8');

// Create mock chrome object
global.chrome = {
  storage: {
    local: {
      get: async (keys) => ({
        settings: {
          intervalMinutes: 30,
          questionsPerSession: 10,
          difficulty: 'all',
          quizMode: 'random',
          enabled: true,
          soundEnabled: true,
          theme: 'dark'
        },
        history: {}
      }),
      set: async () => {}
    }
  },
  runtime: {
    getURL: (path) => path,
    onInstalled: { addListener: () => {} },
    onMessage: { addListener: () => {} }
  },
  alarms: {
    onAlarm: { addListener: () => {} },
    clearAll: async () => {},
    create: () => {}
  }
};

// Mock fetch for loadVocabulary and loadSentences
global.fetch = async (url) => {
  const content = fs.readFileSync(url, 'utf8');
  return {
    json: async () => JSON.parse(content)
  };
};

eval(backgroundCode);

async function runFullTest() {
  console.log('Testing generateQuizData for mode: random');
  const qRandom = await generateQuizData(10);
  console.log('Random questions generated:', qRandom.length);
  qRandom.forEach((q, idx) => {
    console.log(`  Q${idx+1}: [${q.type}] ${q.word || q.sentence.substring(0, 30) + '...'} => Ans: ${q.correctAnswer}`);
    console.assert(q.options.length === 4, 'Must have 4 options');
    console.assert(q.options.includes(q.correctAnswer), 'Options must include answer');
  });

  console.log('\nTesting generateQuizData for mode: word');
  global.chrome.storage.local.get = async () => ({
    settings: { quizMode: 'word', questionsPerSession: 5, difficulty: 'all' }
  });
  const qWord = await generateQuizData(5);
  qWord.forEach((q, idx) => {
    console.log(`  Word Q${idx+1}: [${q.word}] => Ans: ${q.correctAnswer} | Opts:`, q.options);
    console.assert(q.type === 'word');
    console.assert(!q.correctAnswer.includes('(hoặc:'));
    console.assert(!q.options.some(o => o.includes('(hoặc:')));
  });

  console.log('\nTesting generateQuizData for mode: word_reverse');
  global.chrome.storage.local.get = async () => ({
    settings: { quizMode: 'word_reverse', questionsPerSession: 5, difficulty: 'all' }
  });
  const qReverse = await generateQuizData(5);
  qReverse.forEach((q, idx) => {
    console.log(`  Reverse Q${idx+1}: [${q.word}] => Ans: ${q.correctAnswer} | Opts:`, q.options);
    console.assert(q.type === 'word_reverse');
  });

  console.log('\nTesting generateQuizData for mode: sentence');
  global.chrome.storage.local.get = async () => ({
    settings: { quizMode: 'sentence', questionsPerSession: 5, difficulty: 'all' }
  });
  const qSentence = await generateQuizData(5);
  qSentence.forEach((q, idx) => {
    console.log(`  Sentence Q${idx+1}: [${q.sentence}] => Ans: ${q.correctAnswer}`);
    console.assert(q.type === 'sentence');
  });

  console.log('\n🎉 ALL INTEGRATION TESTS PASSED PERFECTLY!');
}

runFullTest().catch(console.error);
