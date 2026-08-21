(() => {
  'use strict';

  const LETTERS = 'ABCD';
  const sections = document.querySelectorAll('.quiz-section');

  sections.forEach((section, sectionIndex) => {
    const questions = [...section.querySelectorAll('.quiz-item')];
    if (!questions.length) return;

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
        <span>提交后会标出每题对错、未答题和正确答案，并自动展开错题详解。</span>
      </div>
      <div class="quiz-submit-actions">
        <button class="quiz-submit-btn" type="button">提交答案并判分</button>
        <button class="quiz-retry-btn" type="button" hidden>只重做错题</button>
      </div>
    `;

    const result = document.createElement('div');
    result.className = 'quiz-result';
    result.hidden = true;
    panel.insertAdjacentElement('afterend', result);
    section.appendChild(panel);

    const submitButton = panel.querySelector('.quiz-submit-btn');
    const retryButton = panel.querySelector('.quiz-retry-btn');

    function getCorrectLetter(question) {
      const text = question.querySelector('.answer-result strong')?.textContent || '';
      return text.match(/正确答案[：:]\s*([ABCD])/)?.[1] || '';
    }

    function resetQuestion(question) {
      question.classList.remove('is-correct', 'is-wrong', 'is-unanswered', 'is-retry-hidden');
      question.querySelectorAll('.options label').forEach(label => {
        label.classList.remove('option-correct', 'option-wrong', 'option-selected');
      });
      const badge = question.querySelector('.question-result-badge');
      if (badge) badge.remove();
      const details = question.querySelector('.answer');
      if (details) details.open = false;
    }

    function addBadge(question, state, text) {
      const heading = question.querySelector('h3');
      const badge = document.createElement('span');
      badge.className = `question-result-badge ${state}`;
      badge.textContent = text;
      heading.insertAdjacentElement('afterend', badge);
    }

    submitButton.addEventListener('click', () => {
      let correct = 0;
      let wrong = 0;
      let unanswered = 0;
      const wrongQuestions = [];

      questions.forEach(question => {
        resetQuestion(question);
        const correctLetter = getCorrectLetter(question);
        const selected = question.querySelector('input[type="radio"]:checked');
        const labels = [...question.querySelectorAll('.options label')];
        const correctLabel = labels.find(label => label.dataset.letter === correctLetter);
        const details = question.querySelector('.answer');

        if (correctLabel) correctLabel.classList.add('option-correct');

        if (!selected) {
          unanswered += 1;
          wrongQuestions.push(question);
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
          wrongQuestions.push(question);
          question.classList.add('is-wrong');
          selectedLabel?.classList.add('option-wrong');
          addBadge(question, 'wrong', `回答错误 · 你选 ${selectedLetter} · 正确答案 ${correctLetter}`);
          if (details) details.open = true;
        }
      });

      const total = questions.length;
      const answered = total - unanswered;
      const percent = Math.round((correct / total) * 100);
      const passed = percent >= 75;
      const status = passed ? '达到今日选择题通关线' : '暂未达到75%通关线';

      result.hidden = false;
      result.className = `quiz-result ${passed ? 'passed' : 'not-passed'}`;
      result.innerHTML = `
        <div class="result-score"><strong>${correct}</strong><span>/ ${total}</span></div>
        <div class="result-detail">
          <b>${status}</b>
          <p>正确率 ${percent}% · 已答 ${answered} 题 · 错误 ${wrong} 题 · 未答 ${unanswered} 题</p>
          <small>${passed ? '建议仍把错题讲清楚，再进入下一课。' : '先阅读已自动展开的错题详解，然后点击“只重做错题”。'}</small>
        </div>
      `;

      retryButton.hidden = wrongQuestions.length === 0;
      retryButton.dataset.wrongIndexes = wrongQuestions.map(q => q.dataset.questionIndex).join(',');
      submitButton.textContent = '重新提交并判分';
      result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    retryButton.addEventListener('click', () => {
      const wrongIndexes = new Set((retryButton.dataset.wrongIndexes || '').split(','));
      questions.forEach(question => {
        const isWrong = wrongIndexes.has(question.dataset.questionIndex);
        resetQuestion(question);
        question.classList.toggle('is-retry-hidden', !isWrong);
        if (isWrong) {
          question.querySelectorAll('input[type="radio"]').forEach(input => { input.checked = false; });
        }
      });
      result.hidden = true;
      retryButton.hidden = true;
      submitButton.textContent = '提交错题并判分';
      const firstWrong = questions.find(q => wrongIndexes.has(q.dataset.questionIndex));
      firstWrong?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
})();
