// Cart, role and orders logic (adapt to Django and localStorage if needed)
let currentRole = null;
let cart = [];

function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = totalItems;
    }
}

function selectRole(role) {
    currentRole = role;
    document.getElementById('roleSelector').style.display = 'none';
    document.getElementById('backBtn').classList.add('show');
    if (role === 'client') {
        document.getElementById('clientInterface').classList.add('active');
        document.getElementById('floatingCart').classList.add('show');
    } else if (role === 'seller') {
        document.getElementById('sellerInterface').classList.add('active');
    }
}

function goBack() {
    document.getElementById('roleSelector').style.display = 'block';
    document.getElementById('clientInterface').classList.remove('active');
    document.getElementById('sellerInterface').classList.remove('active');
    document.getElementById('backBtn').classList.remove('show');
    document.getElementById('floatingCart').classList.remove('show');
    currentRole = null;
    closeCart();
}

function addToCart(productId) {
    // AJAX orqali product ma'lumotlarini olish mumkin
    const productDiv = document.querySelector(`button[onclick="addToCart(${productId})"]`).closest('.product-item');
    const name = productDiv.querySelector('h4').innerText;
    const price = parseInt(productDiv.querySelector('.product-price').innerText.replace(/\D/g, ''));
    let existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id: productId, name, price, quantity: 1 });
    }
    updateCartBadge();
    showNotification('Mahsulot savatga qo\'shildi!', 'success');
}

function showCart() {
    const modal = document.getElementById('cartModal');
    const cartItems = document.getElementById('cartItems');
    cartItems.innerHTML = '';
    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="text-align: center; color: #7f8c8d;">Savat bo\'sh</p>';
        document.getElementById('totalPrice').textContent = '0';
        modal.classList.add('show');
        return;
    }
    let total = 0;
    cart.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <div>
                <h4>${item.name}</h4>
                <p>${item.price.toLocaleString()} so'm/tonna</p>
            </div>
            <div class="quantity-controls">
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">-</button>
                <span style="margin: 0 10px; font-weight: bold;">${item.quantity}</span>
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
                <button class="btn-danger" onclick="removeFromCart(${item.id})" style="margin-left: 10px; padding: 5px 10px; font-size: 12px; width: auto;">
                    O'chirish
                </button>
            </div>
        `;
        cartItems.appendChild(itemDiv);
        total += item.price * item.quantity;
    });
    document.getElementById('totalPrice').textContent = total.toLocaleString();
    modal.classList.add('show');
}

function closeCart() {
    const modal = document.getElementById('cartModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

function updateQuantity(productId, change) {
    let item = cart.find(item => item.id === productId);
    if (!item) return;
    let newQuantity = item.quantity + change;
    if (newQuantity <= 0) {
        removeFromCart(productId);
        return;
    }
    item.quantity = newQuantity;
    updateCartBadge();
    showCart();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartBadge();
    showCart();
    showNotification('Mahsulot savatdan o\'chirildi', 'info');
}

function checkout() {
    if (cart.length === 0) {
        showNotification('Savat bo\'sh!', 'error');
        return;
    }
    // Django orqali AJAX POST bilan buyurtma qilish mumkin
    showNotification('Buyurtma muvaffaqiyatli berildi!', 'success');
    cart = [];
    updateCartBadge();
    closeCart();
    // Sahifani yangilash yoki buyurtmalar ro'yxatini yangilash
}

function showNotification(msg, type) {
    alert(msg); // Custom notification logic uchun o'zgartiring
}

window.onload = function() {
    updateCartBadge();
};