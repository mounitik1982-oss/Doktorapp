const form = document.getElementById('analyzeForm');
const loading = document.getElementById('loading');
const analysisCard = document.getElementById('analysisCard');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  loading.classList.remove('d-none');
  analysisCard.innerText = 'جارٍ التحليل...';

  const formData = new FormData(form);

  try {
    const resp = await axios.post('/api/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (resp.data && resp.data.analysis) {
      analysisCard.innerText = resp.data.analysis;
    } else if (resp.data && resp.data.error) {
      analysisCard.innerText = 'خطأ: ' + resp.data.error;
    } else {
      analysisCard.innerText = 'لم تصل نتيجة. حاول لاحقًا.';
    }

  } catch (err) {
    console.error(err);
    analysisCard.innerText = 'فشل أثناء الاتصال بالخادم.';
  } finally {
    loading.classList.add('d-none');
  }
});
