document.addEventListener('DOMContentLoaded', async () => {
  // Elements
  const themeToggle = document.getElementById('themeToggle');
  const enableToggle = document.getElementById('enableToggle');
  const soundToggle = document.getElementById('soundToggle');
  const intervalSelect = document.getElementById('intervalSelect');
  const questionsSelect = document.getElementById('questionsSelect');
  const difficultySelect = document.getElementById('difficultySelect');
  const quizModeSelect = document.getElementById('quizModeSelect');
  
  const saveBtn = document.getElementById('saveBtn');
  const triggerBtn = document.getElementById('triggerBtn');
  const saveStatus = document.getElementById('saveStatus');
  
  const statTotal = document.getElementById('stat-total');
  const statPercent = document.getElementById('stat-percent');
  const statStreak = document.getElementById('stat-streak');

  // Load current data
  const data = await chrome.storage.local.get(['settings', 'stats']);
  
  // Apply Stats
  if (data.stats) {
    statTotal.textContent = data.stats.totalAnswered;
    statStreak.textContent = data.stats.bestStreak;
    if (data.stats.totalAnswered > 0) {
      const percent = Math.round((data.stats.totalCorrect / data.stats.totalAnswered) * 100);
      statPercent.textContent = `${percent}%`;
    }
  }

  // Apply Settings
  const settings = data.settings || {
    intervalMinutes: 30,
    questionsPerSession: 10,
    difficulty: "all",
    quizMode: "random",
    enabled: true,
    soundEnabled: true,
    theme: "dark"
  };

  if (settings.quizMode === "synonym") {
    settings.quizMode = "random";
  }

  enableToggle.checked = settings.enabled;
  soundToggle.checked = settings.soundEnabled;
  intervalSelect.value = settings.intervalMinutes;
  questionsSelect.value = settings.questionsPerSession;
  difficultySelect.value = settings.difficulty;
  quizModeSelect.value = settings.quizMode || "random";
  
  if (settings.theme === 'light') {
    document.body.classList.replace('dark-theme', 'light-theme');
    themeToggle.checked = true;
  }

  // Theme Toggle Handler
  themeToggle.addEventListener('change', () => {
    if (themeToggle.checked) {
      document.body.classList.replace('dark-theme', 'light-theme');
    } else {
      document.body.classList.replace('light-theme', 'dark-theme');
    }
  });

  // Save Settings Handler
  saveBtn.addEventListener('click', async () => {
    const newSettings = {
      intervalMinutes: intervalSelect.value,
      questionsPerSession: parseInt(questionsSelect.value, 10),
      difficulty: difficultySelect.value,
      quizMode: quizModeSelect.value,
      enabled: enableToggle.checked,
      soundEnabled: soundToggle.checked,
      theme: themeToggle.checked ? 'light' : 'dark'
    };

    await chrome.storage.local.set({ settings: newSettings });
    
    // Notify background script to update alarm
    chrome.runtime.sendMessage({ type: "UPDATE_SETTINGS" });

    // Show status
    saveStatus.textContent = "Đã lưu cài đặt thành công!";
    saveStatus.classList.add('show');
    
    setTimeout(() => {
      saveStatus.classList.remove('show');
    }, 2000);
  });

  // Trigger Now Handler
  triggerBtn.addEventListener('click', async () => {
    const newSettings = {
      intervalMinutes: intervalSelect.value,
      questionsPerSession: parseInt(questionsSelect.value, 10),
      difficulty: difficultySelect.value,
      quizMode: quizModeSelect.value,
      enabled: enableToggle.checked,
      soundEnabled: soundToggle.checked,
      theme: themeToggle.checked ? 'light' : 'dark'
    };
    await chrome.storage.local.set({ settings: newSettings });
    chrome.runtime.sendMessage({ type: "UPDATE_SETTINGS" });

    chrome.runtime.sendMessage({ type: "TRIGGER_NOW" }, (response) => {
      if (response && response.success) {
        window.close(); // Close popup
      } else {
        if (response && response.error === "invalid_page") {
          saveStatus.textContent = "Không thể hiện quiz trên trang cài đặt Chrome!";
        } else if (response && response.error === "no_data") {
          saveStatus.textContent = "Chưa có dữ liệu từ vựng! Hãy kiểm tra data/vocabulary.json";
        } else {
          saveStatus.textContent = "Hãy thử tải lại (F5) trang web bạn đang xem!";
        }
        saveStatus.style.color = "#ef4444";
        saveStatus.classList.add('show');
        setTimeout(() => {
          saveStatus.classList.remove('show');
          saveStatus.style.color = "#10b981"; // reset to green
        }, 3000);
      }
    });
  });
});
