const products = {
  db1: {
    name: "Dragon Ball: Volume 1",
    description: "Classic adventure manga with Goku, friends, and epic battles.",
    price: "£7.99",
    image: "DB_1.png",
    releaseDate: "6 July 2026",
    author: "Akira Toriyama"
  },
  db3: {
    name: "Dragon Ball: Volume 3",
    description: "A bold continuation of the adventure with stronger enemies and higher stakes.",
    price: "£7.99",
    image: "DB_3.jpg",
    releaseDate: "12 October 2026",
    author: "Akira Toriyama"
  },
  jjk1: {
    name: "Jujutsu Kaisen: Volume 1",
    description: "Dark fantasy action manga following sorcerers against cursed spirits.",
    price: "£8.99",
    image: "JJK_!.PNG",
    releaseDate: "6 October 2025",
    author: "Gege Akutami"
  },
  hxh1: {
    name: "Hunter X Hunter: Volume 1",
    description: "Young adventurers face the Hunter Exam and strange creatures.",
    price: "£8.99",
    image: "HXH_1.PNG",
    releaseDate: "26 July 2024",
    author: "Yoshihiro Togashi"
  }
};

function renderProductGrid() {
  const grid = document.querySelector(".product-grid");
  if (!grid) return;

  grid.innerHTML = Object.entries(products)
    .map(([id, product]) => `
      <article class="product-card">
        <a class="product-link" href="Product.html?id=${id}">
          <div class="product-image-wrap">
            <img src="${product.image}" alt="${product.name}">
            <span class="product-badge">Pre-Order</span>
            <span class="product-label">Manga</span>
          </div>
        </a>
        <div class="product-info">
          <h3>${product.name}</h3>
          <div class="price-row">
            <span class="price">${product.price}</span>
            <span class="price-old">${product.price}</span>
          </div>
          <ul class="product-meta">
            <li><strong>Due for release:</strong> ${product.releaseDate}</li>
            <li><strong>By:</strong> ${product.author}</li>
          </ul>
          <button class="product-button">Add to Basket</button>
        </div>
      </article>
    `)
    .join("");
}

function renderProductDetail() {
  const params = new URLSearchParams(window.location.search);
  const productId = params.get("id");
  if (!productId) return;

  const product = products[productId];
  const detailRoot = document.querySelector(".product");
  if (!detailRoot) return;

  if (!product) {
    detailRoot.innerHTML = "<h1>Product not found</h1>";
    return;
  }

  detailRoot.innerHTML = `
    <div class="product-detail-card">
      <img id="productImage" src="${product.image}" alt="${product.name}" />
      <div class="product-detail-info">
        <h1 id="productName">${product.name}</h1>
        <p id="productDescription">${product.description}</p>
        <p><strong>Price:</strong> <span id="productPrice">${product.price}</span></p>
        <p><strong>Release Date:</strong> ${product.releaseDate}</p>
        <p><strong>By:</strong> ${product.author}</p>
        <button class="product-button">Add to Basket</button>
      </div>
    </div>
  `;
}

window.addEventListener("DOMContentLoaded", () => {
  renderProductGrid();
  renderProductDetail();
});