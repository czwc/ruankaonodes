(() => {
  'use strict';

  const STORE_KEY = 'ruankao_course_progress_v2';
  const LEGACY_KEYS = ['ruankao_daily_courses_done_v1', 'ruankao_65day_plan_2026_v1'];
  const body = document.body;
  const date = body.dataset.lessonDate;
  if (!date) return;

  const type = body.dataset.courseType || 'knowledge';
  const threshold = Number(body.dataset.passScore || 75);
  const finishButton = document.getElementById('finishLesson');
  const advanceLink = document.getElementById('advanceLink');
  const checklistInputs = [...document.querySelectorAll('.checklist input[type="checkbox"]')];
  const caseSections = [...document.querySelectorAll('.case-study, .full-paper')].filter(section => section.classList.contains('full-paper') || section.querySelector('.case-questions'));

  function readStore() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
      return parsed && parsed.lessons ? parsed : { version: 2, lessons: {} };
    } catch (_) {
      return { version: 2, lessons: {} };
    }
  }

  function writeStore(store) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (_) {}
  }

  function readLegacy(key) {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (_) { return []; }
  }

  const store = readStore();
  LEGACY_KEYS.forEach(key => {
    readLegacy(key).forEach(doneDate => {
      store.lessons[doneDate] ||= { migrated: true };
    });
  });
  store.lessons[date] ||= {};
  const state = store.lessons[date];
  state.type = type;
  state.threshold = threshold;
  writeStore(store);

  function save() {
    store.lessons[date] = state;
    writeStore(store);
  }

  function mirrorCompletion() {
    LEGACY_KEYS.forEach(key => {
      const values = new Set(readLegacy(key));
      values.add(date);
      try { localStorage.setItem(key, JSON.stringify([...values])); } catch (_) {}
    });
  }

  function buildCaseSelfAssessment(section, index) {
    const total = section.classList.contains('full-paper') ? 75 : 15;
    const box = document.createElement('div');
    box.className = 'case-self-assessment';
    box.innerHTML = `
      <h3>案例作答与采分点自评</h3>
      <label class="case-answer-label">我的答案
        <textarea rows="6" placeholder="先独立写答案，再展开采分点核对。图题请写清起点、数据流名称和终点；算法题写状态、初始化、转移和复杂度。"></textarea>
      </label>
      <div class="case-score-row">
        <label><input class="case-independent" type="checkbox"> 我是在查看答案前独立完成的</label>
        <label>自评得分 <input class="case-score" type="number" min="0" max="${total}" step="1"> / ${total}</label>
        <button class="case-save" type="button">保存案例自评</button>
      </div>
      <p class="case-score-hint">专项案例达到60%，正式模拟建议达到50分以上。</p>`;
    section.appendChild(box);

    const saved = state.cases?.[index] || {};
    const textarea = box.querySelector('textarea');
    const independent = box.querySelector('.case-independent');
    const score = box.querySelector('.case-score');
    textarea.value = saved.answer || '';
    independent.checked = Boolean(saved.independent);
    score.value = saved.score ?? '';

    box.querySelector('.case-save').addEventListener('click', () => {
      const value = Math.max(0, Math.min(total, Number(score.value || 0)));
      state.cases ||= {};
      state.cases[index] = {
        answer: textarea.value.trim(),
        independent: independent.checked,
        score: value,
        total,
        percent: Math.round((value / total) * 100),
        savedAt: new Date().toISOString()
      };
      save();
      updateGate();
      box.classList.add('saved');
      box.querySelector('.case-score-hint').textContent = `已保存：${value}/${total}（${state.cases[index].percent}%）`;
    });
  }

  caseSections.forEach(buildCaseSelfAssessment);

  checklistInputs.forEach((input, index) => {
    input.checked = Boolean(state.checklist?.[index]);
    input.addEventListener('change', () => {
      state.checklist ||= {};
      state.checklist[index] = input.checked;
      save();
      updateGate();
    });
  });

  window.addEventListener('course:quiz-graded', event => {
    const detail = event.detail;
    state.attempts = (state.attempts || 0) + 1;
    state.latestScore = detail.correct;
    state.latestTotal = detail.total;
    state.latestPercent = detail.percent;
    state.bestPercent = Math.max(state.bestPercent || 0, detail.percent);
    state.bestScore = Math.max(state.bestScore || 0, detail.correct);
    state.wrongIndexes = detail.wrongIndexes;
    if (detail.mode === 'first' && state.firstPercent == null) {
      state.firstPercent = detail.percent;
      state.firstScore = detail.correct;
      state.firstTotal = detail.total;
    }
    if (detail.mode === 'first' && detail.passed) state.quizPassed = true;
    if (detail.mode === 'retry' && detail.allMastered) state.quizPassed = true;
    save();
    updateGate();
  });

  function casePassed() {
    if (!caseSections.length) return true;
    const cases = state.cases || {};
    return caseSections.every((_, index) => {
      const current = cases[index];
      if (!current?.independent || !current.answer) return false;
      const required = type.includes('mock') ? Math.min(50, current.total) : Math.ceil(current.total * 0.6);
      return current.score >= required;
    });
  }

  function checklistPassed() {
    return checklistInputs.every((_, index) => state.checklist?.[index]);
  }

  function missingRequirements() {
    const missing = [];
    if (!state.quizPassed) missing.push(`选择题达到 ${threshold}% 或错题全部重做正确`);
    if (!casePassed()) missing.push('完成案例作答并达到采分点要求');
    if (!checklistPassed()) missing.push('勾选全部课后验收项');
    return missing;
  }

  const gate = document.createElement('div');
  gate.className = 'course-completion-gate';
  finishButton?.insertAdjacentElement('beforebegin', gate);

  function updateGate() {
    const missing = missingRequirements();
    const ready = missing.length === 0 || Boolean(state.completedAt);
    if (finishButton) {
      finishButton.disabled = !ready;
      finishButton.textContent = state.completedAt ? '今日课程已通关' : (ready ? '完成今天课程' : `还差 ${missing.length} 项`);
    }
    if (advanceLink) {
      advanceLink.classList.toggle('is-locked', !ready);
      advanceLink.setAttribute('aria-disabled', String(!ready));
    }
    gate.innerHTML = ready
      ? '<b>已满足通关条件</b><span>可以完成课程并继续下一课。</span>'
      : `<b>完成课程前还需要：</b><span>${missing.join('；')}</span>`;
    gate.classList.toggle('ready', ready);
  }

  finishButton?.addEventListener('click', () => {
    const missing = missingRequirements();
    if (missing.length && !state.completedAt) {
      alert(`暂时不能完成课程：\n- ${missing.join('\n- ')}`);
      return;
    }
    state.completedAt ||= new Date().toISOString();
    save();
    mirrorCompletion();
    updateGate();
    advanceLink?.focus();
  });

  advanceLink?.addEventListener('click', event => {
    if (missingRequirements().length && !state.completedAt) {
      event.preventDefault();
      alert(`请先完成本课通关条件：\n- ${missingRequirements().join('\n- ')}`);
    }
  });

  updateGate();
})();
