const els = {
  playerName: document.querySelector("#playerName"),
  characterSelect: document.querySelector("#characterSelect"),
  modeButtons: [...document.querySelectorAll(".segment")],
  affectionValue: document.querySelector("#affectionValue"),
  affectionBar: document.querySelector("#affectionBar"),
  stageLabel: document.querySelector("#stageLabel"),
  goalText: document.querySelector("#goalText"),
  portrait: document.querySelector("#portrait"),
  modeEyebrow: document.querySelector("#modeEyebrow"),
  characterName: document.querySelector("#characterName"),
  characterBrief: document.querySelector("#characterBrief"),
  profileTags: document.querySelector("#profileTags"),
  storyPanel: document.querySelector("#storyPanel"),
  freePanel: document.querySelector("#freePanel"),
  archivePanel: document.querySelector("#archivePanel"),
  chapterTitle: document.querySelector("#chapterTitle"),
  chapterProgress: document.querySelector("#chapterProgress"),
  sceneLocation: document.querySelector("#sceneLocation"),
  sceneTitle: document.querySelector("#sceneTitle"),
  sceneText: document.querySelector("#sceneText"),
  storyLog: document.querySelector("#storyLog"),
  choices: document.querySelector("#choices"),
  freeTitle: document.querySelector("#freeTitle"),
  modernText: document.querySelector("#modernText"),
  personaText: document.querySelector("#personaText"),
  chatLog: document.querySelector("#chatLog"),
  chatForm: document.querySelector("#chatForm"),
  chatInput: document.querySelector("#chatInput"),
  suggestButton: document.querySelector("#suggestButton"),
  saveButton: document.querySelector("#saveButton"),
  resetButton: document.querySelector("#resetButton"),
  toast: document.querySelector("#toast"),
};

const defaultState = () => ({
  mode: "story",
  selected: "abigail",
  playerName: "",
  affection: Object.fromEntries(Object.keys(characters).map((key) => [key, 0])),
  story: Object.fromEntries(
    storyCharacters.map((key) => [
      key,
      { chapter: 0, completed: false, ending: "", log: [] },
    ]),
  ),
  chat: Object.fromEntries(Object.keys(characters).map((key) => [key, []])),
  memory: Object.fromEntries(Object.keys(characters).map((key) => [key, []])),
});

let state = loadState();

function loadState() {
  try {
    const stored = JSON.parse(localStorage.getItem("dokidoki-salem-state") || "null");
    return stored ? mergeState(defaultState(), stored) : defaultState();
  } catch {
    return defaultState();
  }
}

function mergeState(base, incoming) {
  return {
    ...base,
    ...incoming,
    affection: { ...base.affection, ...(incoming.affection || {}) },
    story: { ...base.story, ...(incoming.story || {}) },
    chat: { ...base.chat, ...(incoming.chat || {}) },
    memory: { ...base.memory, ...(incoming.memory || {}) },
  };
}

function saveState(show = false) {
  localStorage.setItem("dokidoki-salem-state", JSON.stringify(state));
  if (show) showToast("저장 완료");
}

function showToast(text) {
  els.toast.textContent = text;
  els.toast.classList.add("is-visible");
  window.setTimeout(() => els.toast.classList.remove("is-visible"), 1300);
}

function getStage(value) {
  return STAGES.reduce((current, item) => (value >= item.min ? item : current), STAGES[0]);
}

function clamp(value) {
  return Math.max(0, Math.min(100, value));
}

function playerLabel() {
  return state.playerName.trim() || "나";
}

function init() {
  els.characterSelect.innerHTML = Object.entries(characters)
    .map(([key, char]) => `<option value="${key}">${char.name}</option>`)
    .join("");
  els.playerName.value = state.playerName;
  els.characterSelect.value = state.selected;
  bindEvents();
  render();
}

function bindEvents() {
  els.modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      if (state.mode === "story" && !storyCharacters.includes(state.selected)) {
        state.selected = "abigail";
      }
      saveState();
      render();
    });
  });

  els.characterSelect.addEventListener("change", (event) => {
    state.selected = event.target.value;
    if (state.mode === "story" && !storyCharacters.includes(state.selected)) {
      state.mode = "free";
    }
    saveState();
    render();
  });

  els.playerName.addEventListener("input", (event) => {
    state.playerName = event.target.value.trim();
    saveState();
  });

  els.chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = els.chatInput.value.trim();
    if (!text) return;
    sendChat(text);
    els.chatInput.value = "";
  });

  els.suggestButton.addEventListener("click", () => {
    const q = starterQuestions[Math.floor(Math.random() * starterQuestions.length)];
    els.chatInput.value = q;
    els.chatInput.focus();
  });

  els.saveButton.addEventListener("click", () => saveState(true));
  els.resetButton.addEventListener("click", () => {
    if (!confirm("진행도와 대화 기록을 초기화할까요?")) return;
    state = defaultState();
    saveState();
    render();
    showToast("초기화 완료");
  });
}

function render() {
  const char = characters[state.selected];
  const value = state.affection[state.selected] || 0;
  const stage = getStage(value);

  els.characterSelect.value = state.selected;
  els.playerName.value = state.playerName;
  els.affectionValue.textContent = value;
  els.affectionBar.style.width = `${value}%`;
  els.stageLabel.textContent = `${stage.label} 단계`;
  els.goalText.textContent = char.goal;
  els.portrait.src = svgPortrait(state.selected, stage.key);
  els.characterName.textContent = char.name;
  els.characterBrief.textContent = char.role;
  els.profileTags.innerHTML = char.tags.map((tag) => `<span>${tag}</span>`).join("");

  els.modeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === state.mode);
  });

  const storyModeAvailable = storyCharacters.includes(state.selected);
  if (state.mode === "story" && !storyModeAvailable) state.mode = "free";

  els.modeEyebrow.textContent =
    state.mode === "story" ? "스토리 모드" : state.mode === "free" ? "자유대화 모드" : "자료실";
  els.storyPanel.classList.toggle("is-hidden", state.mode !== "story");
  els.freePanel.classList.toggle("is-hidden", state.mode !== "free");
  els.archivePanel.classList.toggle("is-hidden", state.mode !== "archive");

  if (state.mode === "story") renderStory();
  if (state.mode === "free") renderFree();
}

function renderStory() {
  const id = state.selected;
  const route = stories[id];
  const progress = state.story[id];
  const chapter = route.chapters[Math.min(progress.chapter, route.chapters.length - 1)];
  const value = state.affection[id] || 0;

  els.chapterTitle.textContent = route.title;
  els.chapterProgress.innerHTML = route.chapters
    .map((item, index) => {
      const cls = index < progress.chapter || progress.completed ? "is-done" : index === progress.chapter ? "is-current" : "";
      return `<span class="${cls}">${index + 1}</span>`;
    })
    .join("");

  els.sceneLocation.textContent = chapter.location;
  els.sceneTitle.textContent = chapter.title;
  els.sceneText.textContent = chapter.text;

  if (!progress.log.length) {
    progress.log.push({ type: "system", speaker: "장면", text: chapter.text });
    progress.log.push({ type: "npc", speaker: characters[id].name, text: chapter.line });
  }

  els.storyLog.innerHTML = progress.log.map(renderLogEntry).join("");
  els.storyLog.scrollTop = els.storyLog.scrollHeight;

  if (progress.completed) {
    els.choices.innerHTML = `
      <button type="button" data-action="restart">이 루트 다시 시작하기</button>
      <button type="button" data-action="free">이 인물과 자유대화하기</button>
    `;
    els.choices.querySelector('[data-action="restart"]').addEventListener("click", () => restartStory(id));
    els.choices.querySelector('[data-action="free"]').addEventListener("click", () => {
      state.mode = "free";
      saveState();
      render();
    });
    return;
  }

  els.choices.innerHTML = chapter.choices
    .map((choice, index) => `<button type="button" data-choice="${index}">${choice.text}<br><small>호감도 ${choice.delta > 0 ? "+" : ""}${choice.delta}</small></button>`)
    .join("");
  els.choices.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => applyChoice(id, Number(button.dataset.choice)));
  });

  if (value < chapter.threshold && progress.chapter > 0) {
    progress.log.push({
      type: "system",
      speaker: "위험",
      text: `현재 호감도 ${value}. 이 챕터의 권장 신뢰도는 ${chapter.threshold} 이상입니다.`,
    });
  }
}

function applyChoice(id, index) {
  const route = stories[id];
  const progress = state.story[id];
  const chapter = route.chapters[progress.chapter];
  const choice = chapter.choices[index];
  state.affection[id] = clamp((state.affection[id] || 0) + choice.delta);

  progress.log.push({ type: "player", speaker: playerLabel(), text: choice.text });
  progress.log.push({ type: "npc", speaker: characters[id].name, text: choice.reply });

  if (state.affection[id] < chapter.threshold) {
    progress.completed = true;
    progress.ending = route.endings.bad;
    progress.log.push({ type: "system", speaker: "엔딩", text: progress.ending });
  } else if (progress.chapter >= route.chapters.length - 1) {
    progress.completed = true;
    const endingKey = state.affection[id] >= 84 ? "good" : "normal";
    progress.ending = route.endings[endingKey];
    progress.log.push({ type: "system", speaker: "엔딩", text: progress.ending });
  } else {
    progress.chapter += 1;
    const next = route.chapters[progress.chapter];
    progress.log.push({ type: "system", speaker: "다음 장면", text: next.text });
    progress.log.push({ type: "npc", speaker: characters[id].name, text: next.line });
  }

  saveState();
  render();
}

function restartStory(id) {
  state.story[id] = { chapter: 0, completed: false, ending: "", log: [] };
  state.affection[id] = 0;
  saveState();
  render();
}

function renderFree() {
  const char = characters[state.selected];
  els.freeTitle.textContent = `${char.name}와 대화`;
  els.modernText.textContent = `${char.modern} ${char.mbti}`;
  els.personaText.textContent = `${char.persona} 숨은 감정: ${char.hidden}`;

  const log = state.chat[state.selected];
  if (!log.length) {
    const opener = makeOpener(state.selected);
    log.push({ type: "npc", speaker: char.name, text: opener });
  }
  els.chatLog.innerHTML = log.map(renderLogEntry).join("");
  els.chatLog.scrollTop = els.chatLog.scrollHeight;
}

function sendChat(text) {
  const id = state.selected;
  const char = characters[id];
  const log = state.chat[id];
  log.push({ type: "player", speaker: playerLabel(), text });

  const delta = scoreFreeMessage(char, text);
  state.affection[id] = clamp((state.affection[id] || 0) + delta);
  remember(id, text);

  log.push({ type: "npc", speaker: char.name, text: generateReply(id, text, delta) });
  saveState();
  render();
}

function remember(id, text) {
  const memory = state.memory[id];
  const useful = text.replace(/[!?.,]/g, "").trim();
  if (useful.length >= 8) {
    memory.push(useful.slice(0, 46));
    if (memory.length > 5) memory.shift();
  }
}

function scoreFreeMessage(char, text) {
  const lowered = text.toLowerCase();
  let score = 0;
  char.likes.forEach((word) => {
    if (text.includes(word)) score += 3;
  });
  char.dislikes.forEach((word) => {
    if (text.includes(word)) score -= 3;
  });
  if (/(고마워|믿어|괜찮|이해|들어줄|함께|도와)/.test(text)) score += 4;
  if (/(거짓말|멍청|틀렸|비겁|미쳤|싫어)/.test(text)) score -= 4;
  if (lowered.includes("mbti") || text.includes("직업") || text.includes("숨기")) score += 2;
  return Math.max(-8, Math.min(9, score || 1));
}

function generateReply(id, text, delta) {
  const char = characters[id];
  const value = state.affection[id] || 0;
  const stage = getStage(value).key;
  const memory = state.memory[id].length ? ` 네가 전에 말한 "${state.memory[id][state.memory[id].length - 1]}"도 기억하고 있어.` : "";

  if (text.toLowerCase().includes("mbti")) {
    return `${char.mbti} 그래서 나는 같은 말도 누가 하느냐에 따라 전혀 다르게 받아들여.${memory}`;
  }
  if (text.includes("직업") || text.includes("현대")) {
    return `${char.modern} 세일럼이 아니라 지금의 도시였다면, 내 욕망도 조금 덜 위험한 모양을 했을까.${memory}`;
  }
  if (text.includes("숨기") || text.includes("두려")) {
    return `${char.hidden} 그걸 들키면 사람들이 나를 이해하는 대신 더 쉽게 판결할 것 같아.${memory}`;
  }

  const warmReplies = {
    cold: [
      "그 말이 정말 네 생각인지, 아니면 나를 시험하려는 말인지 아직 모르겠어.",
      "세일럼에서는 다정한 말도 증거처럼 쓰여. 그래서 나는 쉽게 믿지 않아.",
    ],
    neutral: [
      "네 말에는 적어도 나를 단정하지 않으려는 태도가 있어. 그건 드문 일이야.",
      "조금 더 말해봐. 나는 네가 어느 편인지보다, 왜 그렇게 생각하는지가 궁금해.",
    ],
    warm: [
      "이상하지. 네가 말하면 내 안의 날카로운 부분이 잠깐 멈춰.",
      "네가 내 편이라는 뜻이 아니라도 좋아. 적어도 나를 한 문장으로 끝내지는 않으니까.",
    ],
    bond: [
      "이 정도로 오래 곁에 남은 사람은 많지 않아. 그래서 네 말은 더 아프고, 더 필요해.",
      "내가 틀렸을 때도 떠나지 않고 말해주는 사람. 어쩌면 그게 내가 가장 원한 사람이었나 봐.",
    ],
  };

  const base = warmReplies[stage][Math.floor(Math.random() * warmReplies[stage].length)];
  const reaction = delta > 3 ? " 방금 말은 마음에 남았어." : delta < 0 ? " 하지만 그 표현은 조금 아팠어." : "";
  return `${base}${reaction}${memory}`;
}

function makeOpener(id) {
  const char = characters[id];
  return `...${playerLabel()}? 좋아. 오늘은 ${char.role}으로서가 아니라, 내 목소리로 대답해볼게. 무엇이 궁금해?`;
}

function renderLogEntry(entry) {
  return `<div class="log-entry ${entry.type}"><strong>${entry.speaker}</strong>${escapeHtml(entry.text)}</div>`;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

init();
