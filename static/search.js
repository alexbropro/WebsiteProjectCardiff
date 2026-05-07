document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('search-input');
  const dropdown = document.getElementById('search-dropdown');

  if (!input || !dropdown) return;

  let debounceTimer;

  input.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    const query = input.value.trim();

    if (!query) {
      dropdown.classList.remove('active');
      dropdown.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(function() {
      fetch('/api/search?q=' + encodeURIComponent(query))
        .then(res => res.json())
        .then(results => {
          dropdown.innerHTML = '';

          if (results.length === 0) {
            dropdown.innerHTML = '<div class="search-no-results">No results found</div>';
            dropdown.classList.add('active');
            return;
          }

          dropdown.innerHTML = '<div class="search-category">Manga</div>';

          results.forEach(function(item) {
            const link = document.createElement('a');
            link.href = '/product/' + item.id;
            link.className = 'search-result-item';
            link.innerHTML = `
              <img src="/static/${item.image}" alt="${item.name}">
              <div class="search-result-info">
                <span class="search-result-name">${item.name}</span>
                <span class="search-result-sub">By ${item.author} · £${item.price.toFixed(2)}</span>
              </div>
            `;
            dropdown.appendChild(link);
          });

          dropdown.classList.add('active');
        });
    }, 250);
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.search-form')) {
      dropdown.classList.remove('active');
    }
  });
});