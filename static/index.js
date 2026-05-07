document.addEventListener('DOMContentLoaded', function() {
  const overlay = document.getElementById('item-overlay');
  let hideTimeout;

  document.querySelectorAll('.image-box').forEach(function(box) {
    box.addEventListener('mouseenter', function() {
      clearTimeout(hideTimeout);
      const id = box.dataset.id;

      fetch('/api/item/' + id)
        .then(res => res.json())
        .then(data => {
          document.getElementById('overlay-img').src = '/static/' + data.image;
          document.getElementById('overlay-name').textContent = data.name;
          document.getElementById('overlay-desc').textContent = data.description;
          document.getElementById('overlay-price').textContent = data.price.toFixed(2);
          document.getElementById('overlay-author').textContent = data.author;
          document.getElementById('overlay-link').href = '/product/' + data.id;

          const rect = box.getBoundingClientRect();
          overlay.style.top = (window.scrollY + rect.top) + 'px';
          overlay.style.left = (rect.right + 12) + 'px';
          overlay.style.display = 'flex';
        });
    });

    box.addEventListener('mouseleave', function() {
      hideTimeout = setTimeout(() => { overlay.style.display = 'none'; }, 200);
    });
  });

  overlay.addEventListener('mouseenter', function() { clearTimeout(hideTimeout); });
  overlay.addEventListener('mouseleave', function() {
    hideTimeout = setTimeout(() => { overlay.style.display = 'none'; }, 200);
  });
});