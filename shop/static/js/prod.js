const products = [
      { id: 1, name: "Casual T-Shirts", price: 850, img: "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=500" },
      { id: 2, name: "Blue Denim Jeans", price: 1200, img: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500" },
      { id: 3, name: "Cotton Hoodie", price: 999, img: "https://offnorth.com/cdn/shop/files/Offnorth-Mockingbird_4.jpg?v=1757822709&width=493" },
      { id: 4, name: "White T-Shirt", price: 650, img: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500" },
      { id: 5, name: "Men’s Kurta", price: 1150, img: "https://kisah.in/cdn/shop/files/KA-1109-01.jpg?v=1757057466&width=5000" },
      { id: 6, name: "Stylish Jacket", price: 1450, img: "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQrTbzdup2jNbuVJNIrSInSfgs7K7MAtZPL0eu_661TvtRR4Ynn56AAo_fR1qm8bEMZqqSyWjF2dwCedbz1Sr5ymLPHFapwplfH4BSi2Ti1" },
    ];

    const productList = document.getElementById("productList");
    const cartIcon = document.getElementById("cartIcon");
    const cartModal = document.getElementById("cartModal");
    const cartItems = document.getElementById("cartItems");
    const totalPrice = document.getElementById("totalPrice");
    const cartCount = document.getElementById("cartCount");
    const buyBtn = document.getElementById("buyBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    let cart = [];

    // Load products
    products.forEach(p => {
      const card = document.createElement("div");
      card.classList.add("card");
      card.innerHTML = `
        <img src="${p.img}" alt="${p.name}">
        <h3>${p.name}</h3>
        <p>₹${p.price}</p>
        <button onclick="addToCart(${p.id})">Add</button>
      `;
      productList.appendChild(card);
    });

    // Add item to cart
    function addToCart(id) {
      const item = products.find(p => p.id === id);
      const exists = cart.find(p => p.id === id);
      if (exists) {
        alert("Item already added to cart!");
        return;
      }
      cart.push({ ...item, quantity: 1 });
      updateCart();
    }

    // Update cart UI
    function updateCart() {
      cartItems.innerHTML = "";
      let total = 0;

      cart.forEach(item => {
        total += item.price * item.quantity;
        const div = document.createElement("div");
        div.classList.add("cart-item");
        div.innerHTML = `
          <img src="${item.img}" alt="${item.name}">
          <div class="item-info">
            <h4>${item.name}</h4>
            <p>₹${item.price}</p>
          </div>
          <div class="quantity-controls">
            <button onclick="changeQty(${item.id}, -1)">−</button>
            <span>${item.quantity}</span>
            <button onclick="changeQty(${item.id}, 1)">+</button>
          </div>
        `;
        cartItems.appendChild(div);
      });

      totalPrice.textContent = `Total: ₹${total}`;
      cartCount.textContent = cart.length;
    }

    // Change item quantity
    function changeQty(id, delta) {
      const item = cart.find(p => p.id === id);
      if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) {
          cart = cart.filter(p => p.id !== id);
        }
        updateCart();
      }
    }

    // Open cart
    cartIcon.addEventListener("click", () => {
      cartModal.style.display = "flex";
    });

    // Close cart when clicking outside
    cartModal.addEventListener("click", (e) => {
      if (e.target === cartModal) cartModal.style.display = "none";
    });

    // Buy items
    buyBtn.addEventListener("click", () => {
      if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
      }
      alert("🛍️ Thank you for ordering from ALOO!");
      cart = [];
      updateCart();
      cartModal.style.display = "none";
    });

    // Logout
    logoutBtn.addEventListener("click", () => {
      window.location.href = "login.html";
    });
  