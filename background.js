let vocabulary = null;
let sentences = null;

const DEFAULT_SETTINGS = {
  intervalMinutes: 30,
  questionsPerSession: 10,
  difficulty: "all",
  quizMode: "random",
  enabled: true,
  soundEnabled: true,
  theme: "dark"
};

// Initialize extension
chrome.runtime.onInstalled.addListener(async () => {
  console.log("Extension installed/updated");
  
  // Initialize settings if not exist
  const result = await chrome.storage.local.get(['settings', 'stats']);
  if (!result.settings) {
    await chrome.storage.local.set({ settings: DEFAULT_SETTINGS });
  }
  if (!result.stats) {
    await chrome.storage.local.set({
      stats: {
        totalAnswered: 0,
        totalCorrect: 0,
        currentStreak: 0,
        bestStreak: 0,
        lastQuizDate: null
      }
    });
  }

  // Set up the alarm based on current settings
  setupAlarm();
});

async function setupAlarm() {
  const { settings } = await chrome.storage.local.get('settings');
  const currentSettings = settings || DEFAULT_SETTINGS;
  
  // Clear existing alarms
  await chrome.alarms.clearAll();
  
  if (currentSettings.enabled) {
    console.log(`Setting alarm for every ${currentSettings.intervalMinutes} minutes`);
    chrome.alarms.create("quiz-alarm", {
      periodInMinutes: parseInt(currentSettings.intervalMinutes, 10)
    });
  }
}

// Listen for alarm
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === "quiz-alarm") {
    console.log("Alarm triggered! Time for a quiz.");
    const { settings } = await chrome.storage.local.get('settings');
    if (settings && settings.enabled) {
      triggerQuizSession();
    }
  }
});

// Load vocabulary data
async function loadVocabulary() {
  if (vocabulary) return vocabulary;
  
  try {
    const url = chrome.runtime.getURL('data/vocabulary.json');
    const response = await fetch(url);
    const json = await response.json();
    vocabulary = json.data;
    console.log(`Loaded ${vocabulary.length} words`);
    return vocabulary;
  } catch (error) {
    console.error("Failed to load vocabulary:", error);
    return [];
  }
}

// Load sentences data
async function loadSentences() {
  if (sentences) return sentences;
  
  try {
    const url = chrome.runtime.getURL('data/sentences.json');
    const response = await fetch(url);
    const json = await response.json();
    sentences = json;
    console.log(`Loaded ${sentences.length} sentences`);
    return sentences;
  } catch (error) {
    console.error("Failed to load sentences:", error);
    return [];
  }
}

// Trigger a quiz session on the active tab
async function triggerQuizSession() {
  const { settings } = await chrome.storage.local.get('settings');
  const numQuestions = settings ? settings.questionsPerSession : 10;
  
  const quizData = await generateQuizData(numQuestions);
  if (!quizData || quizData.length === 0) return { success: false, error: "no_data" };

  // Save the current quiz data so the standalone popup can fetch it if needed
  await chrome.storage.local.set({ currentQuizData: quizData });

  function openQuizWindow() {
    chrome.windows.create({
      url: chrome.runtime.getURL("quiz-page.html"),
      type: "popup",
      width: 450,
      height: 620,
      focused: true
    });
    return { success: true };
  }

  // Get active tab from the last focused window
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const activeTab = tabs.length > 0 ? tabs[0] : null;
  
  // Check if Chrome is currently focused
  const currentWindow = await chrome.windows.getCurrent();
  const isChromeFocused = currentWindow && currentWindow.focused;
  
  // If no active tab, or Chrome is not focused (running in background), or it's a restricted page
  const isRestricted = !activeTab || !isChromeFocused || !activeTab.url ||
      activeTab.url.startsWith('chrome://') || 
      activeTab.url.startsWith('chrome-extension://') || 
      activeTab.url.startsWith('edge://') ||
      activeTab.url.startsWith('about:') ||
      activeTab.url.startsWith('https://chrome.google.com/webstore') ||
      activeTab.url.startsWith('https://chromewebstore.google.com/');

  if (isRestricted) {
    console.log("Restricted page or Chrome not focused, opening popup window instead.");
    return openQuizWindow();
  }

  // Try to inject script dynamically (in case the tab was opened before extension was installed)
  try {
    await chrome.scripting.executeScript({
      target: { tabId: activeTab.id },
      files: ['content.js']
    });
    await chrome.scripting.insertCSS({
      target: { tabId: activeTab.id },
      files: ['quiz.css']
    });
  } catch (e) {
    console.log("Dynamic injection skipped or failed (might already be injected):", e);
  }

  // Send message to content script
  try {
    await chrome.tabs.sendMessage(activeTab.id, {
      type: "START_QUIZ",
      payload: {
        questions: quizData,
        settings: settings || DEFAULT_SETTINGS
      }
    });
    return { success: true };
  } catch (error) {
    console.log("Content script not ready in tab, falling back to popup window:", error);
    return openQuizWindow();
  }
}

// Helper to get primary vocabulary (one entry per unique word)
function getPrimaryVocabulary(vocab) {
  const primary = vocab.filter(v => v.is_primary);
  if (primary.length > 0) return primary;

  // Fallback: Pick first entry of each unique word
  const seen = new Map();
  for (const entry of vocab) {
    const key = entry.word.toLowerCase();
    if (!seen.has(key)) {
      seen.set(key, entry);
    }
  }
  return Array.from(seen.values());
}

// Algorithm to generate quiz questions and distractors
async function generateQuizData(numQuestions) {
  const vocab = await loadVocabulary();
  const sentencesDataRaw = await loadSentences();
  if (!vocab || vocab.length === 0) return [];
  
  const primaryVocab = getPrimaryVocabulary(vocab);
  const sentencesData = sentencesDataRaw.map((s, i) => ({ ...s, id: `sentence_${i}` }));

  const data = await chrome.storage.local.get(['settings', 'history']);
  const settings = data.settings || DEFAULT_SETTINGS;
  const wordHistory = data.history || {};
  const diff = settings.difficulty;
  let mode = settings.quizMode || "random";
  if (mode === "synonym") mode = "random";
  
  let pool = [];
  
  if (mode === "word") {
    pool = primaryVocab.map(entry => ({ item: entry, type: mode }));
  } else if (mode === "word_reverse") {
    pool = primaryVocab.map(entry => ({ item: entry, type: mode }));
  } else if (mode === "sentence") {
    pool = sentencesData.map(entry => ({ item: entry, type: "sentence" }));
  } else if (mode === "sentence_reverse") {
    pool = sentencesData.map(entry => ({ item: entry, type: "sentence_reverse" }));
  } else { // random
    const mixed = [];
    primaryVocab.forEach(v => {
      const rand = Math.random();
      let type = "word";
      if (rand < 0.5) type = "word_reverse";
      mixed.push({ item: v, type });
    });
    sentencesData.forEach(s => mixed.push({ item: s, type: Math.random() < 0.5 ? "sentence" : "sentence_reverse" }));
    pool = mixed;
  }

  if (diff !== "all") {
    pool = pool.filter(p => p.type === "sentence" || p.type === "sentence_reverse" || p.item.difficulty === parseInt(diff, 10));
    if (mode !== "sentence" && mode !== "sentence_reverse" && pool.filter(p => p.type !== "sentence" && p.type !== "sentence_reverse").length === 0) {
      primaryVocab.forEach(v => {
        let type = "word";
        if (mode === "word_reverse") type = "word_reverse";
        else if (mode === "random") {
           const rand = Math.random();
           if (rand < 0.5) type = "word_reverse";
        }
        pool.push({ item: v, type: type });
      });
    }
  }

  const now = new Date().getTime();

  // Assign a weight to each entry.
  const scoredPool = pool.map(p => {
    const h = wordHistory[p.item.id];
    let weight = 0;
    
    if (!h || h.timesShown === 0) {
      weight = 100 + Math.random() * 50; 
    } else {
      const isLastAnswerWrong = h.timesShown > h.timesCorrect && (!h.lastCorrect || new Date(h.lastShown).getTime() > new Date(h.lastCorrect).getTime());
      if (isLastAnswerWrong) {
        weight = 80 + Math.random() * 20;
      } else {
        const lastSeen = new Date(h.lastShown).getTime();
        const daysElapsed = (now - lastSeen) / (1000 * 60 * 60 * 24);
        let baseWeight = daysElapsed * 10;
        if (h.timesShown > h.timesCorrect) {
          baseWeight = Math.max(baseWeight, 40);
        }
        weight = Math.min(70, baseWeight) + Math.random() * 10;
      }
    }
    
    return { ...p, weight };
  });

  scoredPool.sort((a, b) => b.weight - a.weight);

  const selectedEntries = scoredPool.slice(0, Math.min(numQuestions, scoredPool.length));
  selectedEntries.sort(() => 0.5 - Math.random());

  const questions = [];
  for (const selected of selectedEntries) {
    const { item, type } = selected;
    let question = null;

    if (type === "sentence") {
      question = generateSentenceQuestion(item, sentencesData);
    } else if (type === "sentence_reverse") {
      question = generateSentenceReverseQuestion(item, sentencesData);
    } else if (type === "word") {
      question = {
        id: item.id,
        type: "word",
        word: item.word,
        pos: item.pos,
        ipa: item.ipa || item.phonetic || "",
        sentence: item.example_en,
        definition: item.definition_en,
        correctAnswer: item.translation_vi,
        options: generateWordOptions(item, primaryVocab)
      };
    } else if (type === "word_reverse") {
      question = {
        id: item.id,
        type: "word_reverse",
        word: item.translation_vi,
        pos: item.pos || "",
        ipa: "",
        sentence: "",
        definition: "",
        correctAnswer: item.word,
        options: generateWordReverseOptions(item, primaryVocab)
      };
    }

    if (question) questions.push(question);
  }

  return questions;
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
    word: "", // Used to skip word highlighting if necessary
    sentence: entry.en,
    correctAnswer: correctVi,
    options: options
  };
}

function getSimilarSentencesReverse(correctEn, allSentences, count = 3) {
  const getWords = str => new Set(str.toLowerCase().replace(/[^a-z0-9]/g, ' ').split(/\s+/).filter(w => w.length > 0));
  const correctWords = getWords(correctEn);
  
  const scored = allSentences.map(s => {
    if (s.en === correctEn) return { s, score: -1 };
    const sWords = getWords(s.en);
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
    if (item.score >= 0) distractors.push(item.s.en);
  }
  
  while (distractors.length < count) {
    const random = allSentences[Math.floor(Math.random() * allSentences.length)].en;
    if (random !== correctEn && !distractors.includes(random)) {
      distractors.push(random);
    }
  }
  
  return distractors;
}

function generateSentenceReverseQuestion(entry, allSentences) {
  const correctEn = entry.en;
  const distractorsEn = getSimilarSentencesReverse(correctEn, allSentences, 3); 
  
  const options = [correctEn, ...distractorsEn].sort(() => 0.5 - Math.random());
  
  return {
    id: entry.id,
    type: "sentence_reverse",
    word: "", 
    sentence: entry.vi,
    correctAnswer: correctEn,
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

  // 1. Priority 1: Same tag/category if available
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

  // 2. Priority 2: Random from primary pool
  if (options.size < 4) {
    const randomEntries = [...primaryVocab].sort(() => 0.5 - Math.random());
    for (const entry of randomEntries) {
      if (!forbiddenTranslations.has(entry.translation_vi.toLowerCase())) {
        options.add(entry.translation_vi);
      }
      if (options.size === 4) break;
    }
  }

  const finalOptions = Array.from(options).slice(0, 4);
  return finalOptions.sort(() => 0.5 - Math.random());
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

// Listen for messages from popup or content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "UPDATE_SETTINGS") {
    setupAlarm();
    sendResponse({ success: true });
  } else if (message.type === "TRIGGER_NOW") {
    triggerQuizSession().then(result => sendResponse(result || { success: false }));
    return true; // Keep channel open for async response
  } else if (message.type === "SAVE_RESULT") {
    saveQuizResult(message.payload);
    sendResponse({ success: true });
  }
  return true;
});

async function saveQuizResult(results) {
  const data = await chrome.storage.local.get(['stats', 'history']);
  let stats = data.stats || { totalAnswered: 0, totalCorrect: 0, currentStreak: 0, bestStreak: 0, lastQuizDate: null };
  let history = data.history || {};
  
  stats.totalAnswered += results.total;
  stats.totalCorrect += results.correct;
  
  if (results.correct === results.total && results.total > 0) {
    stats.currentStreak += 1;
    if (stats.currentStreak > stats.bestStreak) {
      stats.bestStreak = stats.currentStreak;
    }
  } else {
    stats.currentStreak = 0;
  }
  
  stats.lastQuizDate = new Date().toISOString();
  
  if (results.details) {
    for (const detail of results.details) {
      if (!history[detail.id]) {
        history[detail.id] = { timesShown: 0, timesCorrect: 0, lastShown: null, lastCorrect: null };
      }
      history[detail.id].timesShown += 1;
      history[detail.id].lastShown = new Date().toISOString();
      if (detail.correct) {
        history[detail.id].timesCorrect += 1;
        history[detail.id].lastCorrect = new Date().toISOString();
      }
    }
  }
  
  await chrome.storage.local.set({ stats, history });
}
