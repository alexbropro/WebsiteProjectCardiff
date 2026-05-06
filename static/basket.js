document.addEventListener('DOMContentLoaded', function() {
  const toast = document.createElement('div');
  toast.classList.add('toast');
  toast.textContent = '✓ Added to basket';
  document.body.appendChild(toast);

  function showToast() {
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
  }

  document.addEventListener('click', function(e) {
    const btn = e.target.closest('.add-to-basket');
    if (!btn) return;

    const id = btn.dataset.id;

    fetch(`/add/${id}`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        if (data.success) showToast();
      });
  });
});
