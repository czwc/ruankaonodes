(() => {
  'use strict';

  const LETTERS = 'ABCD';
  const sections = document.querySelectorAll('.quiz-section');

  sections.forEach(section => {
    const questions = [...section.querySelectorAll('.quiz-item')];
    if (!questions.length) return;

    let retryIndexes = null;
    questions.forEach((question, index) => {
      question.dataset.questionIndex = String(index);
      question.querySelectorAll('.options label').forEach((label, optionIndex) => {
        label.dataset.letter = LETTERS[optionIndex];
      });
    });

    const panel = document.createElement('div');
    panel.className = 'quiz-submit-panel';
    panel.innerHTML = `
      <div class="quiz-submit-copy">
        <strong>完成 ${questions.length} 题后统一判分</strong>
        <span>提交后显示成绩、逐题对错和正确答案，并自动展开错题详解。</span>
      </div>
      <div class="quiz-submit-actions">
        <button class="quiz-submit-btn" type="button">提交答案并判分</button>
        <button class="quiz-retry-btn" type="button" hidden>只重做错题</button>
      </div>`;
    const result = document.createElement('div');
    result.className = 'quiz-result';
    result.hidden = true;
    result.setAttribute('role', 'status');
    result.setAttribute('aria-live', 'polite');
    section.append(panel, result);

    const submitButton = panel.querySelector('.quiz-submit-btn');
    const retryButton = panel.querySelector('.quiz-retry-btn');

    function getCorrectLetter(question) {
      const text = question.querySelector('.answer-result strong')?.textContent || '';
      return text.match(/正确答案[：:]\s*([ABCD])/)?.[1] || '';
    }

    function resetVisual(question) {
      question.classList.remove('is-correct', 'is-wrong', 'is-unanswered', 'is-retry-hidden');
      question.querySelectorAll('.options label').forEach(label => {
        label.classList.remove('option-correct', 'option-wrong', 'option-selected');
      });
      question.querySelector('.question-result-badge')?.remove();
      const details = question.querySelector('.answer');
      if (details) details.open = false;
    }

    function addBadge(question, state, text) {
      const badge = document.createElement('span');
      badge.className = `question-result-badge ${state}`;
      badge.textContent = text;
      question.querySelector('h3')?.insertAdjacentElement('afterend', badge);
    }

    function grade() {
      const active = retryIndexes
        ? questions.filter(question => retryIndexes.has(question.dataset.questionIndex))
        : questions;
      let correct = 0;
      let wrong = 0;
      let unanswered = 0;
      const remainingWrong = [];

      active.forEach(question => {
        resetVisual(question);
        const correctLetter = getCorrectLetter(question);
        const selected = question.querySelector('input[type="radio"]:checked');
        const labels = [...question.querySelectorAll('.options label')];
        labels.find(label => label.dataset.letter === correctLetter)?.classList.add('option-correct');
        const details = question.querySelector('.answer');

        if (!selected) {
          unanswered += 1;
          remainingWrong.push(question);
          question.classList.add('is-unanswered');
          addBadge(question, 'unanswered', `未作答 · 正确答案 ${correctLetter}`);
          if (details) details.open = true;
          return;
        }

        const selectedLabel = selected.closest('label');
        const selectedLetter = selectedLabel?.dataset.letter || '';
        selectedLabel?.classList.add('option-selected');
        if (selectedLetter === correctLetter) {
          correct += 1;
          question.classList.add('is-correct');
          addBadge(question, 'correct', '回答正确');
        } else {
          wrong += 1;
          remainingWrong.push(question);
          question.classList.add('is-wrong');
          selectedLabel?.classList.add('option-wrong');
          addBadge(question, 'wrong', `回答错误 · 你选 ${selectedLetter} · 正确答案 ${correctLetter}`);
          if (details) details.open = true;
        }
      });

      const total = active.length;
      const percent = total ? Math.round((correct / total) * 100) : 0;
      const isRetry = Boolean(retryIndexes);
      const allMastered = isRetry && remainingWrong.length === 0;
      const threshold = Number(document.body.dataset.passScore || 75);
      const passed = isRetry ? allMastered : percent >= threshold;

      result.hidden = false;
      result.className = `quiz-result ${passed ? 'passed' : 'not-passed'}`;
      result.innerHTML = `
        <div class="result-score"><strong>${correct}</strong><span>/ ${total}</span></div>
        <div class="result-detail">
          <b>${isRetry ? (allMastered ? '本轮错题已全部掌握' : '仍有错题需要重做') : (passed ? `达到 ${threshold}% 通关线` : `暂未达到 ${threshold}% 通关线`)}</b>
          <p>本轮正确率 ${percent}% · 错误 ${wrong} 题 · 未答 ${unanswered} 题</p>
          <small>${remainingWrong.length ? '阅读自动展开的详解后，只重做剩余错题。' : '请继续完成案例自评和课后验收。'}</small>
        </div>`;

      retryButton.hidden = remainingWrong.length === 0;
      retryButton.dataset.wrongIndexes = remainingWrong.map(q => q.dataset.questionIndex).join(',');
      submitButton.textContent = isRetry ? '重新提交本轮错题' : '重新提交并判分';

      window.dispatchEvent(new CustomEvent('course:quiz-graded', {
        detail: {
          mode: isRetry ? 'retry' : 'first',
          correct,
          total,
          percent,
          wrongIndexes: remainingWrong.map(q => Number(q.dataset.questionIndex)),
          passed,
          allMastered
        }
      }));
      result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    submitButton.addEventListener('click', grade);
    retryButton.addEventListener('click', () => {
      retryIndexes = new Set((retryButton.dataset.wrongIndexes || '').split(',').filter(Boolean));
      questions.forEach(question => {
        const isWrong = retryIndexes.has(question.dataset.questionIndex);
        resetVisual(question);
        question.classList.toggle('is-retry-hidden', !isWrong);
        if (isWrong) {
          question.querySelectorAll('input[type="radio"]').forEach(input => { input.checked = false; });
        }
      });
      result.hidden = true;
      retryButton.hidden = true;
      submitButton.textContent = '提交本轮错题';
      questions.find(q => retryIndexes.has(q.dataset.questionIndex))?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
})();
