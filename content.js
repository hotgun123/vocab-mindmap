// State
var quizData = null;
var currentQuestionIndex = 0;
var score = 0;
var settings = null;
var container = null;
var questionResults = [];

// Clean up old listener if injected multiple times
if (window.quizMessageListener) {
  try {
    chrome.runtime.onMessage.removeListener(window.quizMessageListener);
  } catch (e) {
    console.log("Error removing old listener", e);
  }
}

window.quizMessageListener = (message, sender, sendResponse) => {
  if (message.type === "START_QUIZ") {
    console.log("Received START_QUIZ message", message.payload);
    startQuiz(message.payload);
    sendResponse({ success: true });
  }
  return true;
};

chrome.runtime.onMessage.addListener(window.quizMessageListener);

function playSound(type) {
  if (!settings || !settings.soundEnabled) return;
  
  const audio = new Audio(chrome.runtime.getURL(`sounds/${type}.mp3`));
  audio.volume = 0.5;
  audio.play().catch(e => console.log("Audio play prevented:", e));
}

function startQuiz(payload) {
  quizData = payload.questions;
  settings = payload.settings;
  currentQuestionIndex = 0;
  score = 0;
  questionResults = [];
  
  createOverlay();
  renderQuestion();
}

function speakWord(word) {
  if (!settings || !settings.soundEnabled) return;
  if ('speechSynthesis' in window) {
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  }
}

function createOverlay() {
  // Remove existing if any
  if (container) {
    document.body.removeChild(container);
  }
  
  container = document.createElement('div');
  container.id = 'eq-overlay-container';
  
  // HTML Template
  container.innerHTML = `
    <div class="eq-backdrop"></div>
    <div class="eq-quiz-card ${settings.theme === 'light' ? 'eq-light-mode' : ''}">
      <div class="eq-header">
        <h2 class="eq-title">📖 English Quiz</h2>
        <button class="eq-close-btn">&times;</button>
      </div>
      
      <div class="eq-progress-container">
        <div class="eq-progress-bar" style="width: 0%"></div>
      </div>
      
      <div id="eq-content-area">
        <!-- Content gets injected here -->
      </div>
      
      <div class="eq-footer">
        <div class="eq-stats">
          <span id="eq-score-display">Đúng: 0/0</span>
        </div>
        <div id="eq-question-counter">Câu: 1/10</div>
      </div>
    </div>
  `;
  
  document.body.appendChild(container);
  
  // Add event listeners
  container.querySelector('.eq-close-btn').addEventListener('click', closeOverlay);
  container.querySelector('.eq-backdrop').addEventListener('click', closeOverlay);
  
  // Trigger animation
  setTimeout(() => {
    container.classList.add('eq-show');
  }, 10);
}

function closeOverlay() {
  if (container) {
    container.classList.remove('eq-show');
    setTimeout(() => {
      if (container && document.body.contains(container)) {
        document.body.removeChild(container);
        container = null;
      }
      if (window.location.protocol === 'chrome-extension:' && window.location.pathname.endsWith('/quiz-page.html')) {
        window.close();
      }
    }, 300); // Wait for transition
  } else {
    // Fallback if container is null
    if (window.location.protocol === 'chrome-extension:' && window.location.pathname.endsWith('/quiz-page.html')) {
      window.close();
    }
  }
}

function renderQuestion() {
  if (currentQuestionIndex >= quizData.length) {
    renderCompletion();
    return;
  }
  
  const q = quizData[currentQuestionIndex];
  const contentArea = document.getElementById('eq-content-area');
  
  // Update progress
  const progressPercent = (currentQuestionIndex / quizData.length) * 100;
  document.querySelector('.eq-progress-bar').style.width = `${progressPercent}%`;
  
  document.getElementById('eq-question-counter').textContent = `Câu: ${currentQuestionIndex + 1}/${quizData.length}`;
  document.getElementById('eq-score-display').textContent = `Đúng: ${score}/${currentQuestionIndex}`;
  
  // Highlight the target word in the sentence if possible
  let highlightedSentence = q.sentence;
  if (q.word) {
    try {
      const regex = new RegExp(`\\b(${q.word}\\w*)\\b`, 'gi');
      highlightedSentence = q.sentence.replace(regex, '<u>$1</u>');
    } catch (e) {
      // ignore
    }
  }

  let contentHtml = '';
  
  if (q.type === 'sentence' || q.type === 'sentence_reverse') {
    let instruction = q.type === 'sentence' ? 'Chọn bản dịch đúng cho câu trên:' : 'Chọn câu tiếng Anh có nghĩa tương đương:';
    contentHtml = `
      <div class="eq-sentence-container">
        <div class="eq-sentence">"${highlightedSentence}"</div>
      </div>
      <div class="eq-instruction">${instruction}</div>
    `;
  } else {
    // word or word_reverse
    let instruction = 'Chọn NGHĨA đúng của từ trên:';
    let hasAudio = true;
    if (q.type === 'word_reverse') {
      instruction = 'Chọn TỪ TIẾNG ANH có nghĩa như trên:';
      hasAudio = false;
    }
    contentHtml = `
      <div class="eq-word-mode-container">
        <div class="eq-main-word">
          ${q.word}
          ${hasAudio ? '<button class="eq-audio-btn" id="eq-speak-btn" title="Nghe phát âm">🔊</button>' : ''}
        </div>
        <div class="eq-ipa">${q.ipa ? q.ipa : ''}</div>
      </div>
      <div class="eq-instruction">${instruction}</div>
    `;
  }

  contentArea.innerHTML = `
    ${contentHtml}
    <div class="eq-options-grid ${q.type === 'sentence' || q.type === 'sentence_reverse' ? 'eq-options-col' : ''}">
      ${q.options.map((opt, i) => `
        <button class="eq-option-btn" data-answer="${opt.replace(/"/g, '&quot;')}">
          <span class="eq-option-text">${String.fromCharCode(65 + i)}. ${opt}</span>
          <span class="eq-option-icon"></span>
        </button>
      `).join('')}
    </div>
  `;
  
  // Add event listeners to options
  const buttons = contentArea.querySelectorAll('.eq-option-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', handleAnswer);
  });
  
  // Add audio listener if word mode
  if (q.type === 'word') {
    const speakBtn = document.getElementById('eq-speak-btn');
    if (speakBtn) {
      speakBtn.addEventListener('click', () => speakWord(q.word));
    }
    // Auto-play sound if enabled
    if (settings && settings.soundEnabled) {
      speakWord(q.word);
    }
  }
}

function handleAnswer(e) {
  const selectedBtn = e.currentTarget;
  const selectedAnswer = selectedBtn.getAttribute('data-answer');
  const q = quizData[currentQuestionIndex];
  const isCorrect = selectedAnswer === q.correctAnswer;
  
  questionResults.push({
    id: q.id,
    correct: isCorrect
  });
  
  // Disable all buttons
  const buttons = document.querySelectorAll('.eq-option-btn');
  buttons.forEach(btn => btn.disabled = true);
  
  if (isCorrect) {
    score++;
    selectedBtn.classList.add('eq-correct');
    selectedBtn.querySelector('.eq-option-icon').textContent = '✅';
    playSound('correct');
  } else {
    selectedBtn.classList.add('eq-wrong');
    selectedBtn.querySelector('.eq-option-icon').textContent = '❌';
    playSound('wrong');
    
    // Highlight correct answer
    buttons.forEach(btn => {
      if (btn.getAttribute('data-answer') === q.correctAnswer) {
        btn.classList.add('eq-correct');
        btn.querySelector('.eq-option-icon').textContent = '✅';
      }
    });
  }
  
  // Move to next question after delay
  setTimeout(() => {
    currentQuestionIndex++;
    renderQuestion();
  }, 1500);
}

function renderCompletion() {
  // Update progress to 100%
  document.querySelector('.eq-progress-bar').style.width = `100%`;
  document.getElementById('eq-score-display').textContent = `Đúng: ${score}/${quizData.length}`;
  
  playSound('complete');
  
  // Send results to background script to update stats
  chrome.runtime.sendMessage({
    type: "SAVE_RESULT",
    payload: {
      correct: score,
      total: quizData.length,
      details: questionResults
    }
  });
  
  const contentArea = document.getElementById('eq-content-area');
  
  const percent = Math.round((score / quizData.length) * 100);
  let emoji = "🎉";
  if (percent < 50) emoji = "💪";
  else if (percent < 80) emoji = "👍";
  else if (percent === 100) emoji = "🔥";
  
  contentArea.innerHTML = `
    <div class="eq-completion">
      <div class="eq-completion-icon">${emoji}</div>
      <h3 class="eq-completion-title">Hoàn thành Quiz!</h3>
      <div class="eq-completion-stats">
        Bạn đã trả lời đúng <strong>${score}/${quizData.length}</strong> câu (${percent}%)
      </div>
      <button class="eq-btn-primary" id="eq-finish-btn">Đóng</button>
    </div>
  `;
  
  document.getElementById('eq-finish-btn').addEventListener('click', closeOverlay);
}

// Auto-start if running in standalone quiz-page.html
if (window.location.protocol === 'chrome-extension:' && window.location.pathname.endsWith('/quiz-page.html')) {
  chrome.storage.local.get(['currentQuizData', 'settings'], (data) => {
    if (data.currentQuizData) {
      // Small delay to ensure styles are loaded
      setTimeout(() => {
        startQuiz({ questions: data.currentQuizData, settings: data.settings || { soundEnabled: true, theme: 'dark' } });
      }, 100);
    }
  });
}
