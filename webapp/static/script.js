const dropZone  = document.getElementById('dropZone');
const fileInput  = document.getElementById('fileInput');
const previewCard = document.getElementById('previewCard');
const previewImg  = document.getElementById('previewImg');
const resultSection = document.getElementById('resultSection');
const spinner    = document.getElementById('spinner');

let selectedFile = null;

// ── Drag & Drop ──
dropZone.addEventListener('dragover', e => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) loadPreview(file);
});
dropZone.addEventListener('click', e => {
  if (e.target.closest('button') || e.target === fileInput) return;
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) loadPreview(fileInput.files[0]);
});

function loadPreview(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    previewCard.style.display = 'flex';
    resultSection.style.display = 'none';
  };
  reader.readAsDataURL(file);
}

function clearAll() {
  selectedFile = null;
  fileInput.value = '';
  previewCard.style.display = 'none';
  resultSection.style.display = 'none';
  previewImg.src = '';
}

// ── Run Detection ──
async function runDetection() {
  if (!selectedFile) return;

  const detectBtn = document.getElementById('detectBtn');
  detectBtn.disabled = true;
  spinner.style.display = 'flex';
  resultSection.style.display = 'none';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('/predict', { method: 'POST', body: formData });
    const data = await response.json();

    if (data.error) {
      alert('Prediction error: ' + data.error);
      return;
    }

    showResult(data);

  } catch (err) {
    alert('Cannot reach server. Make sure app.py is running on port 5000.');
  } finally {
    spinner.style.display = 'none';
    detectBtn.disabled = false;
  }
}

// ── Display Result ──
function showResult(data) {
  const resultHeader     = document.getElementById('resultHeader');
  const resultIcon       = document.getElementById('resultIcon');
  const resultLabel      = document.getElementById('resultLabel');
  const resultConfidence = document.getElementById('resultConfidence');
  const scoresBars       = document.getElementById('scoresBars');

  const isTumor = data.is_tumor;

  // Header styling
  resultHeader.className = 'result-header ' + (isTumor ? 'tumor' : 'no-tumor');
  resultIcon.textContent = isTumor ? '⚠️' : '✅';

  resultLabel.textContent = isTumor
    ? `Tumor Detected: ${data.predicted_class}`
    : 'No Tumor Detected';
  resultLabel.className = isTumor ? 'tumor-color' : 'no-tumor-color';

  resultConfidence.textContent = `Model confidence: ${data.confidence.toFixed(1)}%`;

  // Confidence bars
  scoresBars.innerHTML = '';
  const topClass = data.predicted_class;

  Object.entries(data.all_scores)
    .sort((a, b) => b[1] - a[1])
    .forEach(([label, score]) => {
      const isTop      = label === topClass;
      const isNoTumor  = label === 'No Tumor';
      const barClass   = isTop
        ? (isNoTumor ? 'score-bar no-tumor' : 'score-bar top')
        : 'score-bar';

      const row = document.createElement('div');
      row.className = 'score-row';
      row.innerHTML = `
        <span class="score-label">${label}</span>
        <div class="score-bar-wrap">
          <div class="${barClass}" style="width:0%" data-score="${score}"></div>
        </div>
        <span class="score-value">${score.toFixed(1)}%</span>
      `;
      scoresBars.appendChild(row);
    });

  // Show section, then animate bars
  resultSection.style.display = 'block';
  resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.querySelectorAll('.score-bar').forEach(bar => {
        bar.style.width = Math.min(parseFloat(bar.dataset.score), 100) + '%';
      });
    });
  });
}
