/**
 * VOCABULARY MASTER - Thematic Vocabulary Learning Platform
 * Core Application Engine
 */

(function () {
  'use strict';

  // State Management
  const state = {
    allWords: [],
    topicGroups: [],
    filteredWords: [],
    selectedTopic: 'all', // 'all' or subtopic id
    selectedGroup: 'all', // 'all' or topic group id
    selectedLevel: 'all', // 'all', 'A1', 'A2', 'B1', 'B2', 'C1'
    selectedPos: 'all',   // 'all', 'noun', 'verb', 'adjective', 'adverb'
    searchQuery: '',
    sortOption: 'az',     // 'az', 'za', 'level-asc', 'level-desc'
    currentView: 'browse',// 'browse', 'flashcards', 'quiz', 'starred'
    vocabMode: localStorage.getItem('vm_vocab_mode') || 'all', // 'all', 'words', 'phrases'
    starredWordIds: new Set(JSON.parse(localStorage.getItem('vm_starred_words') || '[]')),
    
    // Audio & Speech Settings
    speechVoice: localStorage.getItem('vm_speech_voice') || 'en-US',
    speechRate: parseFloat(localStorage.getItem('vm_speech_rate') || '1.0'),
    soundEnabled: localStorage.getItem('vm_sound_enabled') !== 'false',
    theme: localStorage.getItem('vm_theme') || 'dark',

    // Drawer state
    activeDrawerWordIndex: -1,

    // Flashcard state
    flashcardIndex: 0,
    flashcardList: [],

    // Quiz state
    quizIndex: 0,
    quizQuestions: [],
    quizScore: 0
  };

  // Sound Effects Engine (Web Audio API + Audio fallback)
  let audioCtx = null;
  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    return audioCtx;
  }

  const soundEngine = {
    play(type) {
      if (!state.soundEnabled) return;
      try {
        const ctx = getAudioContext();
        if (ctx) {
          const now = ctx.currentTime;
          if (type === 'correct') {
            // Ascending major chime (C5 to E5)
            const osc1 = ctx.createOscillator();
            const osc2 = ctx.createOscillator();
            const gain = ctx.createGain();
            osc1.type = 'sine';
            osc2.type = 'triangle';
            osc1.frequency.setValueAtTime(523.25, now);
            osc1.frequency.exponentialRampToValueAtTime(659.25, now + 0.12);
            osc2.frequency.setValueAtTime(659.25, now + 0.1);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
            osc1.connect(gain);
            osc2.connect(gain);
            gain.connect(ctx.destination);
            osc1.start(now);
            osc2.start(now + 0.08);
            osc1.stop(now + 0.35);
            osc2.stop(now + 0.35);
            return;
          } else if (type === 'wrong') {
            // Gentle low buzz
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.linearRampToValueAtTime(160, now + 0.25);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.3);
            return;
          } else if (type === 'complete') {
            // Fanfare
            const notes = [523.25, 659.25, 783.99, 1046.50];
            notes.forEach((freq, idx) => {
              const osc = ctx.createOscillator();
              const gain = ctx.createGain();
              osc.type = 'sine';
              osc.frequency.setValueAtTime(freq, now + idx * 0.1);
              gain.gain.setValueAtTime(0.2, now + idx * 0.1);
              gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.1 + 0.35);
              osc.connect(gain);
              gain.connect(ctx.destination);
              osc.start(now + idx * 0.1);
              osc.stop(now + idx * 0.1 + 0.35);
            });
            return;
          } else if (type === 'click') {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(900, now);
            gain.gain.setValueAtTime(0.05, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.04);
            return;
          }
        }
      } catch (e) {
        // Fallback to audio files
        const soundFile = type === 'correct' ? 'sounds/correct.wav' :
                          type === 'wrong' ? 'sounds/wrong.wav' :
                          type === 'complete' ? 'sounds/complete.wav' : null;
        if (soundFile) {
          const audio = new Audio(soundFile);
          audio.volume = 0.4;
          audio.play().catch(() => {});
        }
      }
    }
  };

  // Text To Speech (SpeechSynthesis Engine)
  const speechEngine = {
    voices: [],
    currentUtterance: null,

    init() {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => {
          this.voices = window.speechSynthesis.getVoices();
        };
        this.voices = window.speechSynthesis.getVoices();
      }
    },

    speak(text, activeElem = null, onEndCallback = null) {
      if (!('speechSynthesis' in window)) {
        alert('Trình duyệt của bạn không hỗ trợ tính năng SpeechSynthesis.');
        return;
      }
      window.speechSynthesis.cancel();

      // Clean speech text
      const cleanText = text.replace(/[\/\\\(\)\[\]]/g, '').trim();
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = state.speechRate;
      utterance.lang = state.speechVoice;

      // Find best matching voice
      if (this.voices.length > 0) {
        const langPrefix = state.speechVoice.toLowerCase();
        const matchedVoice = this.voices.find(v => v.lang.toLowerCase() === langPrefix) ||
                             this.voices.find(v => v.lang.toLowerCase().startsWith(langPrefix.split('-')[0])) ||
                             this.voices.find(v => v.lang.toLowerCase().includes('en'));
        if (matchedVoice) {
          utterance.voice = matchedVoice;
        }
      }

      if (activeElem) {
        activeElem.classList.add('playing');
      }

      utterance.onend = () => {
        if (activeElem) activeElem.classList.remove('playing');
        if (onEndCallback) onEndCallback();
      };

      utterance.onerror = () => {
        if (activeElem) activeElem.classList.remove('playing');
      };

      this.currentUtterance = utterance;
      window.speechSynthesis.speak(utterance);
    },

    stop() {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    }
  };

  // DOM Elements Selection
  const elements = {
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    soundToggleBtn: document.getElementById('soundToggleBtn'),
    voiceSelect: document.getElementById('voiceSelect'),
    speedSelect: document.getElementById('speedSelect'),
    searchInput: document.getElementById('searchInput'),
    btnClearSearch: document.getElementById('btnClearSearch'),
    sortSelect: document.getElementById('sortSelect'),
    sidebar: document.getElementById('sidebar'),
    btnToggleSidebar: document.getElementById('btnToggleSidebar'),
    allTopicsBtn: document.getElementById('allTopicsBtn'),
    topicAccordionContainer: document.getElementById('topicAccordionContainer'),
    bannerEyebrow: document.getElementById('bannerEyebrow'),
    bannerTitle: document.getElementById('bannerTitle'),
    bannerDesc: document.getElementById('bannerDesc'),
    resultCountBadge: document.getElementById('resultCountBadge'),
    vocabGrid: document.getElementById('vocabGrid'),
    emptyState: document.getElementById('emptyState'),
    levelPills: document.querySelectorAll('.filter-pill[data-level]'),
    posPills: document.querySelectorAll('.filter-pill[data-pos]'),
    vocabModePills: document.querySelectorAll('.mode-pill[data-mode]'),
    modeCountAll: document.getElementById('modeCountAll'),
    modeCountWords: document.getElementById('modeCountWords'),
    modeCountPhrases: document.getElementById('modeCountPhrases'),
    allTopicsCount: document.getElementById('allTopicsCount'),
    tabBrowseAll: document.getElementById('tabBrowseAll'),
    tabOnlyWords: document.getElementById('tabOnlyWords'),
    tabOnlyPhrases: document.getElementById('tabOnlyPhrases'),
    viewTabs: document.querySelectorAll('.view-tab-btn'),
    browseViewPanel: document.getElementById('browseViewPanel'),
    flashcardsViewPanel: document.getElementById('flashcardsViewPanel'),
    quizViewPanel: document.getElementById('quizViewPanel'),

    // Drawer Elements
    drawerOverlay: document.getElementById('drawerOverlay'),
    wordDrawer: document.getElementById('wordDrawer'),
    btnCloseDrawer: document.getElementById('btnCloseDrawer'),
    btnPrevWord: document.getElementById('btnPrevWord'),
    btnNextWord: document.getElementById('btnNextWord'),
    drawerWord: document.getElementById('drawerWord'),
    drawerIpa: document.getElementById('drawerIpa'),
    drawerLevelBadge: document.getElementById('drawerLevelBadge'),
    drawerPosBadge: document.getElementById('drawerPosBadge'),
    drawerTopicTag: document.getElementById('drawerTopicTag'),
    drawerMeaningVi: document.getElementById('drawerMeaningVi'),
    drawerDefEn: document.getElementById('drawerDefEn'),
    btnHeroAudio: document.getElementById('btnHeroAudio'),
    btnDrawerStar: document.getElementById('btnDrawerStar'),
    synonymsContainer: document.getElementById('synonymsContainer'),
    synonymsList: document.getElementById('synonymsList'),
    examplesContainer: document.getElementById('examplesContainer'),

    // Flashcard Elements
    flashcardWord: document.getElementById('flashcardWord'),
    flashcardIpa: document.getElementById('flashcardIpa'),
    flashcardLevel: document.getElementById('flashcardLevel'),
    flashcardPos: document.getElementById('flashcardPos'),
    flashcardMeaning: document.getElementById('flashcardMeaning'),
    flashcardDef: document.getElementById('flashcardDef'),
    flashcardExamples: document.getElementById('flashcardExamples'),
    flashcardProgressText: document.getElementById('flashcardProgressText'),
    flashcardElem: document.getElementById('flashcardElem'),
    btnFlipCard: document.getElementById('btnFlipCard'),
    btnPrevFlashcard: document.getElementById('btnPrevFlashcard'),
    btnNextFlashcard: document.getElementById('btnNextFlashcard'),
    btnFlashcardAudio: document.getElementById('btnFlashcardAudio'),

    // Quiz Elements
    quizProgressText: document.getElementById('quizProgressText'),
    quizQuestionWord: document.getElementById('quizQuestionWord'),
    quizQuestionIpa: document.getElementById('quizQuestionIpa'),
    quizQuestionPos: document.getElementById('quizQuestionPos'),
    quizOptionsContainer: document.getElementById('quizOptionsContainer'),
    btnNextQuiz: document.getElementById('btnNextQuiz'),
    quizScoreText: document.getElementById('quizScoreText')
  };

  // Helper functions
  function getLevelClass(level) {
    return 'level-' + (level || 'b1').toLowerCase();
  }

  function highlightWordInSentence(sentence, targetWord) {
    if (!sentence || !targetWord) return sentence;
    const escaped = targetWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`\\b(${escaped}(?:s|es|ed|ing|d)?)\\b`, 'gi');
    return sentence.replace(regex, '<span class="highlight-word">$1</span>');
  }

  // Load Initial Data
  async function loadData() {
    // 1. Try to load from window.VOCAB_WORDS & window.VOCAB_TOPICS_METADATA (bundled JS)
    if (window.VOCAB_WORDS && window.VOCAB_TOPICS_METADATA) {
      state.allWords = window.VOCAB_WORDS;
      state.topicGroups = window.VOCAB_TOPICS_METADATA.topicGroups || [];
      initApp();
      return;
    }

    // 2. Fallback to fetch JSON
    try {
      const res = await fetch('data/topics_vocabulary.json');
      if (res.ok) {
        const data = await res.json();
        state.allWords = data.words || [];
        state.topicGroups = data.topicGroups || [];
        initApp();
        return;
      }
    } catch (e) {
      console.warn('Could not fetch data/topics_vocabulary.json:', e);
    }

    // 3. Last fallback: try original vocabulary.json
    try {
      const res = await fetch('data/vocabulary.json');
      if (res.ok) {
        const data = await res.json();
        const rawList = data.data || [];
        // Map raw entries to app format
        const seen = new Map();
        for (const item of rawList) {
          const w = (item.word || '').trim().toLowerCase();
          if (w && !seen.has(w)) {
            seen.set(w, {
              id: item.id || w,
              word: w,
              ipa: item.ipa || item.phonetic || '',
              pos: item.pos || 'noun',
              level: item.difficulty === 2 ? 'B2' : 'B1',
              topic_id: 'qualities_states',
              topic_vi: 'Trạng thái & Đặc tính',
              topic_en: 'Qualities & States',
              topic_group_id: 'general_concepts',
              topic_group_vi: 'Khái niệm chung & Đo lường',
              topic_icon: '🧩',
              meaning_vi: item.translation_vi || '',
              definition_en: item.definition_en || '',
              synonyms: [],
              examples: item.example_en ? [{ en: item.example_en, vi: '' }] : []
            });
          }
        }
        state.allWords = Array.from(seen.values());
        initApp();
      }
    } catch (err) {
      console.error('All data loading failed:', err);
      elements.emptyState.style.display = 'flex';
      elements.emptyState.querySelector('.empty-title').textContent = 'Không tìm thấy dữ liệu từ vựng';
      elements.emptyState.querySelector('.empty-desc').textContent = 'Vui lòng kiểm tra file data/topics_vocabulary.json hoặc data/topics_vocab_data.js.';
    }
  }

  // Initialize Application
  function initApp() {
    speechEngine.init();
    applyTheme();
    applySoundSettings();
    populateVoiceSelect();
    updateModeCounts();
    applyModePillActive();
    renderTopicSidebar();
    applyFiltersAndRender();
    setupEventListeners();
  }

  // Populate Voice Selection
  function populateVoiceSelect() {
    elements.voiceSelect.value = state.speechVoice;
    elements.speedSelect.value = state.speechRate.toString();
  }

  // Apply Theme
  function applyTheme() {
    if (state.theme === 'light') {
      document.body.classList.add('light-theme');
      elements.themeToggleBtn.textContent = '☀️';
      elements.themeToggleBtn.title = 'Chuyển sang giao diện tối';
    } else {
      document.body.classList.remove('light-theme');
      elements.themeToggleBtn.textContent = '🌙';
      elements.themeToggleBtn.title = 'Chuyển sang giao diện sáng';
    }
  }

  function applySoundSettings() {
    elements.soundToggleBtn.textContent = state.soundEnabled ? '🔊' : '🔇';
    elements.soundToggleBtn.title = state.soundEnabled ? 'Âm thanh: Bật' : 'Âm thanh: Tắt';
  }

  // Mode Switcher Management
  function setVocabMode(mode) {
    state.vocabMode = mode;
    localStorage.setItem('vm_vocab_mode', mode);
    applyModePillActive();
    renderTopicSidebar();
    updateBanner();
    applyFiltersAndRender();
  }

  function applyModePillActive() {
    if (elements.vocabModePills) {
      elements.vocabModePills.forEach(p => {
        p.classList.toggle('active', p.getAttribute('data-mode') === state.vocabMode);
      });
    }

    if (elements.tabBrowseAll && elements.tabOnlyWords && elements.tabOnlyPhrases) {
      if (state.currentView === 'browse') {
        elements.tabBrowseAll.classList.toggle('active', state.vocabMode === 'all');
        elements.tabOnlyWords.classList.toggle('active', state.vocabMode === 'words');
        elements.tabOnlyPhrases.classList.toggle('active', state.vocabMode === 'phrases');
      }
    }
  }

  function updateModeCounts() {
    const totalAll = state.allWords.length;
    const totalWords = state.allWords.filter(w => !w.is_phrase).length;
    const totalPhrases = state.allWords.filter(w => w.is_phrase).length;

    if (elements.modeCountAll) elements.modeCountAll.textContent = totalAll.toLocaleString();
    if (elements.modeCountWords) elements.modeCountWords.textContent = totalWords.toLocaleString();
    if (elements.modeCountPhrases) elements.modeCountPhrases.textContent = totalPhrases.toLocaleString();
    if (elements.allTopicsCount) {
      const activeCount = state.vocabMode === 'words' ? totalWords :
                          state.vocabMode === 'phrases' ? totalPhrases :
                          totalAll;
      elements.allTopicsCount.textContent = activeCount.toLocaleString();
    }
  }

  // Render Topic Sidebar Accordion
  function renderTopicSidebar() {
    elements.topicAccordionContainer.innerHTML = '';
    
    // Total items count for active mode
    updateModeCounts();

    state.topicGroups.forEach(group => {
      const groupItem = document.createElement('div');
      groupItem.className = 'topic-group-item';
      if (state.selectedGroup === group.id) {
        groupItem.classList.add('open');
      }

      // Group Header
      const header = document.createElement('div');
      header.className = 'topic-group-header';
      
      const groupBadgeCount = state.vocabMode === 'words' ? (group.singleWordsCount !== undefined ? group.singleWordsCount : group.count || 0) :
                             state.vocabMode === 'phrases' ? (group.phrasesCount !== undefined ? group.phrasesCount : 0) :
                             (group.wordCount || group.count || 0);

      header.innerHTML = `
        <div class="group-title-wrap">
          <span class="group-icon">${group.icon}</span>
          <span class="group-name">${group.name_vi}</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="count-badge">${groupBadgeCount}</span>
          <span class="group-arrow">▶</span>
        </div>
      `;

      header.addEventListener('click', () => {
        soundEngine.play('click');
        groupItem.classList.toggle('open');
      });

      // Subtopics List
      const subList = document.createElement('div');
      subList.className = 'topic-sub-list';

      (group.topics || []).forEach(sub => {
        const subBtn = document.createElement('button');
        subBtn.className = 'subtopic-btn';
        if (state.selectedTopic === sub.id) {
          subBtn.classList.add('active');
        }
        
        const subBadgeCount = state.vocabMode === 'words' ? (sub.singleWordsCount !== undefined ? sub.singleWordsCount : sub.count || 0) :
                             state.vocabMode === 'phrases' ? (sub.phrasesCount !== undefined ? sub.phrasesCount : 0) :
                             (sub.wordCount || sub.count || 0);

        subBtn.innerHTML = `
          <span>${sub.icon} ${sub.name_vi}</span>
          <span class="count-badge">${subBadgeCount}</span>
        `;

        subBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          soundEngine.play('click');
          selectTopic(sub.id, group.id);
        });

        subList.appendChild(subBtn);
      });

      groupItem.appendChild(header);
      groupItem.appendChild(subList);
      elements.topicAccordionContainer.appendChild(groupItem);
    });
  }

  // Select Topic
  function selectTopic(topicId, groupId = 'all') {
    state.selectedTopic = topicId;
    state.selectedGroup = groupId;

    // Update active class on all buttons
    elements.allTopicsBtn.classList.toggle('active', topicId === 'all');
    document.querySelectorAll('.subtopic-btn').forEach(btn => {
      btn.classList.remove('active');
    });

    if (topicId !== 'all') {
      const activeBtn = document.querySelector(`.subtopic-btn[data-topic="${topicId}"]`);
      if (activeBtn) activeBtn.classList.add('active');
    }

    // Close sidebar on mobile
    if (window.innerWidth <= 992) {
      elements.sidebar.classList.remove('open');
    }

    updateBanner();
    applyFiltersAndRender();
  }

  // Update Topic Banner
  function updateBanner() {
    if (state.currentView === 'starred') {
      elements.bannerEyebrow.innerHTML = `⭐ BỘ SƯU TẬP CỦA TÔI`;
      elements.bannerTitle.innerHTML = `Từ & Cụm Từ Đã Lưu`;
      elements.bannerDesc.textContent = `Danh sách những từ vựng và cụm từ bạn đã đánh dấu sao để ôn tập và ghi nhớ lâu hơn.`;
      return;
    }

    if (state.selectedTopic === 'all') {
      if (state.vocabMode === 'phrases') {
        elements.bannerEyebrow.innerHTML = `💬 CHẾ ĐỘ CỤM TỪ, COLLOCATIONS & IDIOMS`;
        elements.bannerTitle.innerHTML = `350+ Cụm Từ & Collocations Theo Chủ Đề (A1 - C1)`;
        elements.bannerDesc.textContent = `Tuyển tập hơn 350 cụm từ tiếng Anh, collocations tự nhiên và thành ngữ thông dụng nhất trong giao tiếp và công sở, kèm phát âm và câu ví dụ song ngữ.`;
      } else if (state.vocabMode === 'words') {
        elements.bannerEyebrow.innerHTML = `🔤 CHẾ ĐỘ TỪ ĐƠN CỐT LÕI`;
        elements.bannerTitle.innerHTML = `3,100+ Từ Vựng Tiếng Anh Theo Chủ Đề (A1 - C1)`;
        elements.bannerDesc.textContent = `Tuyển tập hơn 3,100 từ vựng cốt lõi tiếng Anh Oxford & Cambridge, phân loại theo 12 nhóm chủ đề với phiên âm chuẩn IPA và ví dụ thực tế.`;
      } else {
        elements.bannerEyebrow.innerHTML = `🌐 TOÀN BỘ KHO TỪ VỰNG & CỤM TỪ`;
        elements.bannerTitle.innerHTML = `3,500+ Từ Vựng & Cụm Từ Theo Chủ Đề (A1 - C1)`;
        elements.bannerDesc.textContent = `Tuyển tập toàn diện hơn 3,500 từ vựng cốt lõi và cụm từ thực tế (collocations, idioms, phrasal verbs) Oxford & Cambridge, phân loại theo chủ đề.`;
      }
      return;
    }

    // Find topic info
    let foundTopic = null;
    let foundGroup = null;
    for (const g of state.topicGroups) {
      for (const t of g.topics || []) {
        if (t.id === state.selectedTopic) {
          foundTopic = t;
          foundGroup = g;
          break;
        }
      }
      if (foundTopic) break;
    }

    if (foundTopic && foundGroup) {
      elements.bannerEyebrow.innerHTML = `${foundGroup.icon} ${foundGroup.name_vi.toUpperCase()} &bull; ${foundGroup.name_en}`;
      elements.bannerTitle.innerHTML = `${foundTopic.icon} ${foundTopic.name_vi}`;
      elements.bannerDesc.textContent = `Các từ vựng thiết yếu về chủ đề ${foundTopic.name_vi} (${foundTopic.name_en}). Bao gồm giải nghĩa tiếng Việt, phiên âm và câu ví dụ thường dùng trong ngữ cảnh.`;
    }
  }

  // Filter and Sort Logic
  function applyFiltersAndRender() {
    let list = state.allWords;

    // Vocab Mode Filter (All vs Single Words vs Phrases)
    if (state.vocabMode === 'words') {
      list = list.filter(w => !w.is_phrase);
    } else if (state.vocabMode === 'phrases') {
      list = list.filter(w => w.is_phrase);
    }

    // View filter: Starred
    if (state.currentView === 'starred') {
      list = list.filter(w => state.starredWordIds.has(w.id));
    } else {
      // Topic filter
      if (state.selectedTopic !== 'all') {
        list = list.filter(w => w.topic_id === state.selectedTopic);
      } else if (state.selectedGroup !== 'all') {
        list = list.filter(w => w.topic_group_id === state.selectedGroup);
      }
    }

    // Level filter
    if (state.selectedLevel !== 'all') {
      list = list.filter(w => (w.level || '').toUpperCase() === state.selectedLevel);
    }

    // Part of speech filter
    if (state.selectedPos !== 'all') {
      list = list.filter(w => (w.pos || '').toLowerCase().includes(state.selectedPos.toLowerCase()));
    }

    // Search query filter
    if (state.searchQuery.trim()) {
      const q = state.searchQuery.trim().toLowerCase();
      list = list.filter(w => 
        w.word.toLowerCase().includes(q) ||
        (w.meaning_vi && w.meaning_vi.toLowerCase().includes(q)) ||
        (w.definition_en && w.definition_en.toLowerCase().includes(q)) ||
        (w.topic_vi && w.topic_vi.toLowerCase().includes(q))
      );
    }

    // Sort list
    const sorted = [...list];
    if (state.sortOption === 'az') {
      sorted.sort((a, b) => a.word.localeCompare(b.word));
    } else if (state.sortOption === 'za') {
      sorted.sort((a, b) => b.word.localeCompare(a.word));
    } else if (state.sortOption === 'level-asc') {
      const order = { 'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5 };
      sorted.sort((a, b) => (order[a.level] || 3) - (order[b.level] || 3));
    } else if (state.sortOption === 'level-desc') {
      const order = { 'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5 };
      sorted.sort((a, b) => (order[b.level] || 3) - (order[a.level] || 3));
    }

    state.filteredWords = sorted;
    elements.resultCountBadge.textContent = `${sorted.length} từ`;

    if (state.currentView === 'browse' || state.currentView === 'starred') {
      renderWordGrid(sorted);
    } else if (state.currentView === 'flashcards') {
      initFlashcards();
    } else if (state.currentView === 'quiz') {
      initQuiz();
    }
  }

  // Render Word Cards Grid
  function renderWordGrid(words) {
    elements.vocabGrid.innerHTML = '';

    if (words.length === 0) {
      elements.emptyState.style.display = 'flex';
      return;
    }
    elements.emptyState.style.display = 'none';

    const fragment = document.createDocumentFragment();

    words.forEach((item, index) => {
      const card = document.createElement('div');
      card.className = 'vocab-card';
      if (item.is_phrase) {
        card.classList.add('is-phrase-card');
      }
      const isStarred = state.starredWordIds.has(item.id);
      const levelClass = getLevelClass(item.level);

      // Determine phrase badge
      let phraseBadgeHtml = '';
      if (item.is_phrase) {
        const posLower = (item.pos || '').toLowerCase();
        if (posLower.includes('idiom')) {
          phraseBadgeHtml = '<span class="badge-type-phrase" style="background:rgba(236,72,153,0.15); color:#f472b6; border-color:rgba(236,72,153,0.35);">✨ Thành ngữ</span>';
        } else if (posLower.includes('collocation')) {
          phraseBadgeHtml = '<span class="badge-type-phrase" style="background:rgba(59,130,246,0.15); color:#60a5fa; border-color:rgba(59,130,246,0.35);">🔗 Collocation</span>';
        } else if (posLower.includes('phrasal')) {
          phraseBadgeHtml = '<span class="badge-type-phrase" style="background:rgba(245,158,11,0.15); color:#fbbf24; border-color:rgba(245,158,11,0.35);">⚡ Phrasal verb</span>';
        } else {
          phraseBadgeHtml = '<span class="badge-type-phrase">💬 Cụm từ</span>';
        }
      }

      card.innerHTML = `
        <div class="card-top">
          <div class="card-header-info">
            <h3 class="word-title">${item.word}</h3>
            <span class="word-phonetic">${item.ipa || ''}</span>
          </div>
          <div class="card-actions">
            <button class="btn-card-audio" title="Nghe phát âm từ này" data-word="${item.word}">
              🔊
            </button>
            <button class="btn-card-star ${isStarred ? 'starred' : ''}" title="${isStarred ? 'Bỏ lưu' : 'Lưu từ này'}" data-id="${item.id}">
              ${isStarred ? '★' : '☆'}
            </button>
          </div>
        </div>
        <div class="card-meaning">${item.meaning_vi || 'Đang cập nhật nghĩa...'}</div>
        <div class="card-definition-en">${item.definition_en || ''}</div>
        <div class="card-bottom">
          <div class="badges-wrap">
            <span class="badge-level ${levelClass}">${item.level || 'B1'}</span>
            ${phraseBadgeHtml}
            <span class="badge-pos">${item.pos || 'noun'}</span>
          </div>
          <div class="examples-badge" title="${(item.examples || []).length} câu ví dụ thường dùng">
            💬 ${(item.examples || []).length} câu
          </div>
        </div>
      `;

      // Card Click -> Open Detail Drawer
      card.addEventListener('click', (e) => {
        // If clicked on audio or star button, do not open drawer
        if (e.target.closest('.btn-card-audio') || e.target.closest('.btn-card-star')) {
          return;
        }
        soundEngine.play('click');
        openWordDrawer(index);
      });

      // Audio Button Click
      const audioBtn = card.querySelector('.btn-card-audio');
      audioBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        speechEngine.speak(item.word, audioBtn);
      });

      // Star Button Click
      const starBtn = card.querySelector('.btn-card-star');
      starBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleStarWord(item.id, starBtn);
      });

      fragment.appendChild(card);
    });

    elements.vocabGrid.appendChild(fragment);
  }

  // Toggle Star / Favorite Word
  function toggleStarWord(wordId, starBtn = null) {
    if (state.starredWordIds.has(wordId)) {
      state.starredWordIds.delete(wordId);
      if (starBtn) {
        starBtn.classList.remove('starred');
        starBtn.textContent = '☆';
        starBtn.title = 'Lưu từ này';
      }
    } else {
      state.starredWordIds.add(wordId);
      soundEngine.play('correct');
      if (starBtn) {
        starBtn.classList.add('starred');
        starBtn.textContent = '★';
        starBtn.title = 'Bỏ lưu';
      }
    }

    localStorage.setItem('vm_starred_words', JSON.stringify(Array.from(state.starredWordIds)));

    // Update drawer star if open
    if (elements.drawerOverlay.classList.contains('active')) {
      const currentWord = state.filteredWords[state.activeDrawerWordIndex];
      if (currentWord && currentWord.id === wordId) {
        const isStarred = state.starredWordIds.has(wordId);
        elements.btnDrawerStar.classList.toggle('starred', isStarred);
        elements.btnDrawerStar.textContent = isStarred ? '★' : '☆';
      }
    }

    // If currently in starred view, re-filter
    if (state.currentView === 'starred') {
      applyFiltersAndRender();
    }
  }

  // Open Word Detail Drawer
  function openWordDrawer(index) {
    if (index < 0 || index >= state.filteredWords.length) return;
    state.activeDrawerWordIndex = index;
    const item = state.filteredWords[index];

    elements.drawerWord.textContent = item.word;
    elements.drawerIpa.textContent = item.ipa || '';
    
    // Level badge
    const levelClass = getLevelClass(item.level);
    elements.drawerLevelBadge.className = `badge-level ${levelClass}`;
    elements.drawerLevelBadge.textContent = item.level || 'B1';
    
    // Pos & Topic tags
    if (item.is_phrase) {
      elements.drawerPosBadge.textContent = `💬 ${item.pos || 'cụm từ'}`;
      elements.drawerPosBadge.style.background = 'rgba(168, 85, 247, 0.15)';
      elements.drawerPosBadge.style.color = '#c084fc';
      elements.drawerPosBadge.style.border = '1px solid rgba(168, 85, 247, 0.35)';
    } else {
      elements.drawerPosBadge.textContent = item.pos || 'noun';
      elements.drawerPosBadge.style.background = '';
      elements.drawerPosBadge.style.color = '';
      elements.drawerPosBadge.style.border = '';
    }
    elements.drawerTopicTag.textContent = `${item.topic_icon || '📌'} ${item.topic_vi || 'Tổng quát'}`;

    elements.drawerMeaningVi.textContent = item.meaning_vi || '';
    elements.drawerDefEn.textContent = item.definition_en || '';

    // Star state
    const isStarred = state.starredWordIds.has(item.id);
    elements.btnDrawerStar.classList.toggle('starred', isStarred);
    elements.btnDrawerStar.textContent = isStarred ? '★' : '☆';

    // Synonyms
    if (item.synonyms && item.synonyms.length > 0) {
      elements.synonymsContainer.style.display = 'flex';
      elements.synonymsList.innerHTML = '';
      item.synonyms.forEach(syn => {
        const synPill = document.createElement('span');
        synPill.className = 'synonym-pill';
        synPill.textContent = syn;
        synPill.addEventListener('click', () => {
          elements.searchInput.value = syn;
          state.searchQuery = syn;
          applyFiltersAndRender();
          closeWordDrawer();
        });
        elements.synonymsList.appendChild(synPill);
      });
    } else {
      elements.synonymsContainer.style.display = 'none';
    }

    // Example Sentences
    elements.examplesContainer.innerHTML = '';
    const examples = item.examples || [];
    if (examples.length === 0) {
      elements.examplesContainer.innerHTML = `<div style="font-size:13px; color:var(--text-muted); font-style:italic;">Đang cập nhật câu ví dụ...</div>`;
    } else {
      examples.forEach(ex => {
        const exCard = document.createElement('div');
        exCard.className = 'example-card';
        const highlightedEn = highlightWordInSentence(ex.en, item.word);

        exCard.innerHTML = `
          <div class="example-en-row">
            <div class="example-en-text">${highlightedEn}</div>
            <button class="btn-sentence-audio" title="Nghe câu này">
              🔊
            </button>
          </div>
          <div class="example-vi-text">${ex.vi || ''}</div>
        `;

        const sentenceAudioBtn = exCard.querySelector('.btn-sentence-audio');
        sentenceAudioBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          speechEngine.speak(ex.en, exCard);
        });

        elements.examplesContainer.appendChild(exCard);
      });
    }

    // Hero Word Audio
    elements.btnHeroAudio.onclick = () => {
      speechEngine.speak(item.word, elements.btnHeroAudio);
    };

    // Nav prev / next disabled states
    elements.btnPrevWord.disabled = index === 0;
    elements.btnNextWord.disabled = index === state.filteredWords.length - 1;

    // Show drawer
    elements.drawerOverlay.classList.add('active');
  }

  function closeWordDrawer() {
    elements.drawerOverlay.classList.remove('active');
    speechEngine.stop();
  }

  // Flashcards Feature
  function initFlashcards() {
    state.flashcardList = [...state.filteredWords];
    state.flashcardIndex = 0;
    renderCurrentFlashcard();
  }

  function renderCurrentFlashcard() {
    if (state.flashcardList.length === 0) {
      elements.flashcardWord.textContent = 'Không có từ nào';
      elements.flashcardIpa.textContent = '';
      elements.flashcardMeaning.textContent = 'Vui lòng chọn chủ đề hoặc điều chỉnh bộ lọc.';
      elements.flashcardDef.textContent = '';
      elements.flashcardExamples.innerHTML = '';
      elements.flashcardProgressText.textContent = '0 / 0';
      return;
    }

    elements.flashcardElem.classList.remove('is-flipped');
    const item = state.flashcardList[state.flashcardIndex];

    elements.flashcardProgressText.textContent = `Thẻ ${state.flashcardIndex + 1} / ${state.flashcardList.length}`;
    elements.flashcardWord.textContent = item.word;
    elements.flashcardIpa.textContent = item.ipa || '';
    
    const levelClass = getLevelClass(item.level);
    elements.flashcardLevel.className = `badge-level ${levelClass}`;
    elements.flashcardLevel.textContent = item.level || 'B1';
    elements.flashcardPos.textContent = item.pos || 'noun';

    elements.flashcardMeaning.textContent = item.meaning_vi || '';
    elements.flashcardDef.textContent = item.definition_en || '';

    // Flashcard Examples
    elements.flashcardExamples.innerHTML = '';
    const examples = item.examples || [];
    examples.slice(0, 2).forEach(ex => {
      const p = document.createElement('div');
      p.style.marginBottom = '6px';
      p.innerHTML = `<strong style="color:var(--primary-light);">${ex.en}</strong><br><span style="font-size:12px; color:var(--text-secondary);">${ex.vi}</span>`;
      elements.flashcardExamples.appendChild(p);
    });

    elements.btnFlashcardAudio.onclick = (e) => {
      e.stopPropagation();
      speechEngine.speak(item.word, elements.btnFlashcardAudio);
    };
  }

  // Quiz Feature
  function initQuiz() {
    state.quizIndex = 0;
    state.quizScore = 0;

    // Build 10 random questions from current filtered list
    const pool = [...state.filteredWords];
    if (pool.length < 4) {
      elements.quizQuestionWord.textContent = 'Chưa đủ từ vựng để tạo bài kiểm tra';
      elements.quizQuestionIpa.textContent = '';
      elements.quizQuestionPos.textContent = '';
      elements.quizOptionsContainer.innerHTML = `<div style="text-align:center; color:var(--text-muted);">Cần ít nhất 4 từ vựng trong danh sách để bắt đầu Quiz.</div>`;
      elements.quizProgressText.textContent = '0 / 0';
      elements.quizScoreText.textContent = 'Điểm: 0';
      elements.btnNextQuiz.style.display = 'none';
      return;
    }

    // Shuffle and pick 10 words
    pool.sort(() => Math.random() - 0.5);
    const selected = pool.slice(0, 10);

    state.quizQuestions = selected.map(correctWord => {
      // Pick 3 distractors
      const distractors = pool
        .filter(w => w.id !== correctWord.id && w.meaning_vi)
        .sort(() => Math.random() - 0.5)
        .slice(0, 3)
        .map(w => w.meaning_vi);

      const options = [correctWord.meaning_vi, ...distractors].sort(() => Math.random() - 0.5);
      return {
        word: correctWord,
        correctMeaning: correctWord.meaning_vi,
        options: options
      };
    });

    renderCurrentQuiz();
  }

  function renderCurrentQuiz() {
    if (state.quizIndex >= state.quizQuestions.length) {
      // Quiz Completed
      soundEngine.play('complete');
      elements.quizProgressText.textContent = 'Hoàn thành bài kiểm tra!';
      elements.quizQuestionWord.textContent = `🎉 Bạn đạt ${state.quizScore} / ${state.quizQuestions.length} điểm!`;
      elements.quizQuestionIpa.textContent = '';
      elements.quizQuestionPos.textContent = '';
      elements.quizOptionsContainer.innerHTML = `
        <button class="btn-ctrl btn-primary" style="margin: 20px auto; display:block;" id="btnRestartQuiz">
          🔄 Làm lại bài kiểm tra
        </button>
      `;
      elements.btnNextQuiz.style.display = 'none';
      document.getElementById('btnRestartQuiz').addEventListener('click', () => {
        initQuiz();
      });
      return;
    }

    const q = state.quizQuestions[state.quizIndex];
    elements.quizProgressText.textContent = `Câu hỏi ${state.quizIndex + 1} / ${state.quizQuestions.length}`;
    elements.quizScoreText.textContent = `Điểm: ${state.quizScore}`;
    elements.quizQuestionWord.textContent = q.word.word;
    elements.quizQuestionIpa.textContent = q.word.ipa || '';
    elements.quizQuestionPos.textContent = `(${q.word.pos || 'noun'}) - Nghĩa tiếng Việt đúng là gì?`;
    elements.btnNextQuiz.style.display = 'none';

    // Auto pronounce the question word
    speechEngine.speak(q.word.word);

    elements.quizOptionsContainer.innerHTML = '';
    q.options.forEach(opt => {
      const optBtn = document.createElement('button');
      optBtn.className = 'quiz-opt-btn';
      optBtn.textContent = opt;

      optBtn.addEventListener('click', () => {
        // Disable all option buttons
        const allBtns = elements.quizOptionsContainer.querySelectorAll('.quiz-opt-btn');
        allBtns.forEach(b => b.disabled = true);

        if (opt === q.correctMeaning) {
          soundEngine.play('correct');
          optBtn.classList.add('correct');
          state.quizScore++;
          elements.quizScoreText.textContent = `Điểm: ${state.quizScore}`;
        } else {
          soundEngine.play('wrong');
          optBtn.classList.add('wrong');
          // Highlight correct one
          allBtns.forEach(b => {
            if (b.textContent === q.correctMeaning) {
              b.classList.add('correct');
            }
          });
        }
        elements.btnNextQuiz.style.display = 'block';
      });

      elements.quizOptionsContainer.appendChild(optBtn);
    });
  }

  // Setup Event Listeners
  function setupEventListeners() {
    // Theme toggle
    elements.themeToggleBtn.addEventListener('click', () => {
      soundEngine.play('click');
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('vm_theme', state.theme);
      applyTheme();
    });

    // Sound toggle
    elements.soundToggleBtn.addEventListener('click', () => {
      state.soundEnabled = !state.soundEnabled;
      localStorage.setItem('vm_sound_enabled', state.soundEnabled.toString());
      applySoundSettings();
      if (state.soundEnabled) soundEngine.play('click');
    });

    // Voice & Speed Change
    elements.voiceSelect.addEventListener('change', (e) => {
      state.speechVoice = e.target.value;
      localStorage.setItem('vm_speech_voice', state.speechVoice);
      speechEngine.speak('Hello, this is the voice sample.');
    });

    elements.speedSelect.addEventListener('change', (e) => {
      state.speechRate = parseFloat(e.target.value);
      localStorage.setItem('vm_speech_rate', state.speechRate.toString());
      speechEngine.speak('Speed adjusted.');
    });

    // Sidebar Mobile Toggle
    elements.btnToggleSidebar.addEventListener('click', () => {
      elements.sidebar.classList.toggle('open');
    });

    // All topics button
    elements.allTopicsBtn.addEventListener('click', () => {
      soundEngine.play('click');
      selectTopic('all', 'all');
    });

    // Search Input
    elements.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      elements.btnClearSearch.style.display = state.searchQuery ? 'block' : 'none';
      applyFiltersAndRender();
    });

    elements.btnClearSearch.addEventListener('click', () => {
      elements.searchInput.value = '';
      state.searchQuery = '';
      elements.btnClearSearch.style.display = 'none';
      applyFiltersAndRender();
      elements.searchInput.focus();
    });

    // Sort Select
    elements.sortSelect.addEventListener('change', (e) => {
      state.sortOption = e.target.value;
      applyFiltersAndRender();
    });

    // CEFR Level Pills
    elements.levelPills.forEach(pill => {
      pill.addEventListener('click', () => {
        soundEngine.play('click');
        elements.levelPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.selectedLevel = pill.getAttribute('data-level');
        applyFiltersAndRender();
      });
    });

    // Part of Speech Pills
    elements.posPills.forEach(pill => {
      pill.addEventListener('click', () => {
        soundEngine.play('click');
        elements.posPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.selectedPos = pill.getAttribute('data-pos');
        applyFiltersAndRender();
      });
    });

    // Mode Segmented Pills (All / Words / Phrases)
    if (elements.vocabModePills) {
      elements.vocabModePills.forEach(pill => {
        pill.addEventListener('click', () => {
          soundEngine.play('click');
          const mode = pill.getAttribute('data-mode') || 'all';
          setVocabMode(mode);
        });
      });
    }

    // View Tabs (Browse, Starred, Flashcards, Quiz)
    elements.viewTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        soundEngine.play('click');
        const v = tab.getAttribute('data-view');
        
        if (v === 'words') {
          state.currentView = 'browse';
          setVocabMode('words');
        } else if (v === 'phrases') {
          state.currentView = 'browse';
          setVocabMode('phrases');
        } else if (v === 'browse') {
          state.currentView = 'browse';
          setVocabMode('all');
        } else {
          state.currentView = v;
          elements.viewTabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
        }

        // Toggle Panels
        elements.browseViewPanel.classList.toggle('active', state.currentView === 'browse' || state.currentView === 'starred');
        elements.flashcardsViewPanel.classList.toggle('active', state.currentView === 'flashcards');
        elements.quizViewPanel.classList.toggle('active', state.currentView === 'quiz');

        updateBanner();
        applyFiltersAndRender();
      });
    });

    // Drawer Event Listeners
    elements.btnCloseDrawer.addEventListener('click', closeWordDrawer);
    elements.drawerOverlay.addEventListener('click', (e) => {
      if (e.target === elements.drawerOverlay) closeWordDrawer();
    });

    elements.btnPrevWord.addEventListener('click', () => {
      soundEngine.play('click');
      if (state.activeDrawerWordIndex > 0) {
        openWordDrawer(state.activeDrawerWordIndex - 1);
      }
    });

    elements.btnNextWord.addEventListener('click', () => {
      soundEngine.play('click');
      if (state.activeDrawerWordIndex < state.filteredWords.length - 1) {
        openWordDrawer(state.activeDrawerWordIndex + 1);
      }
    });

    elements.btnDrawerStar.addEventListener('click', () => {
      const currentWord = state.filteredWords[state.activeDrawerWordIndex];
      if (currentWord) {
        toggleStarWord(currentWord.id);
      }
    });

    // Flashcard Flip & Nav
    elements.btnFlipCard.addEventListener('click', () => {
      elements.flashcardElem.classList.toggle('is-flipped');
    });

    elements.flashcardElem.addEventListener('click', (e) => {
      if (e.target.closest('#btnFlashcardAudio')) return;
      elements.flashcardElem.classList.toggle('is-flipped');
    });

    elements.btnPrevFlashcard.addEventListener('click', () => {
      soundEngine.play('click');
      if (state.flashcardIndex > 0) {
        state.flashcardIndex--;
        renderCurrentFlashcard();
      }
    });

    elements.btnNextFlashcard.addEventListener('click', () => {
      soundEngine.play('click');
      if (state.flashcardIndex < state.flashcardList.length - 1) {
        state.flashcardIndex++;
        renderCurrentFlashcard();
      }
    });

    // Quiz Next
    elements.btnNextQuiz.addEventListener('click', () => {
      soundEngine.play('click');
      state.quizIndex++;
      renderCurrentQuiz();
    });

    // Global Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeWordDrawer();
      } else if (elements.drawerOverlay.classList.contains('active')) {
        if (e.key === 'ArrowLeft' && state.activeDrawerWordIndex > 0) {
          openWordDrawer(state.activeDrawerWordIndex - 1);
        } else if (e.key === 'ArrowRight' && state.activeDrawerWordIndex < state.filteredWords.length - 1) {
          openWordDrawer(state.activeDrawerWordIndex + 1);
        } else if (e.key === ' ') {
          e.preventDefault();
          const currentWord = state.filteredWords[state.activeDrawerWordIndex];
          if (currentWord) speechEngine.speak(currentWord.word, elements.btnHeroAudio);
        }
      }
    });
  }

  // Start initialization on DOM loaded
  document.addEventListener('DOMContentLoaded', loadData);

})();
