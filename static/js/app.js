let currentRole = null;
let cart = [];
const clientName = "Mijoz"; // Real loyihada foydalanuvchi nomini olish lozim

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
    const productDiv = Array.from(document.querySelectorAll('.product-item')).find(item => {
        const btn = item.querySelector('button.btn');
        return btn && btn.getAttribute('onclick') === `addToCart(${productId})`;
    });
    if (!productDiv) return;

    const name = productDiv.querySelector('h4').innerText;
    const price = parseFloat(productDiv.querySelector('.product-price').innerText.replace(/[^\d\.]/g, ''));
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

    fetch(`/order/my_pending/?client=${encodeURIComponent(clientName)}`)
    .then(response => response.json())
    .then(data => {
        // Pending product id'larini aniqlang va local cartdan olib tashlang (duplikat bo'lmasin)
        const pendingProductIds = (data.orders || []).map(o => o.product_id);
        cart = cart.filter(item => !pendingProductIds.includes(item.id));

        if (cart.length === 0 && (!data.orders || data.orders.length === 0)) {
            cartItems.innerHTML = '<p style="text-align: center; color: #7f8c8d;">Savat bo\'sh</p>';
            document.getElementById('totalPrice').textContent = '0';
            modal.classList.add('show');
            updateCartBadge();
            return;
        }
        let total = 0;

        // Local cart itemlari
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

        // Pending orderlar
        data.orders && data.orders.forEach(order => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'cart-item pending';
            itemDiv.innerHTML = `
                <div>
                    <h4>${order.name}</h4>
                    <p>${order.price.toLocaleString()} so'm</p>
                    <span style="color: #f39c12;">Status: pending</span>
                </div>
                <div>
                    <span style="margin-right: 10px;">${order.quantity} t</span>
                    <button class="btn-danger" onclick="cancelOrder(${order.id})" style="padding: 5px 15px; font-size: 13px;">Bekor qilish</button>
                </div>
            `;
            cartItems.appendChild(itemDiv);
            total += order.price;
        });

        document.getElementById('totalPrice').textContent = total.toLocaleString();
        modal.classList.add('show');
        updateCartBadge();
    });
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

function cancelOrder(orderId) {
    fetch(`/order/cancel/${orderId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Buyurtma bekor qilindi', 'success');
            showCart();
        } else {
            showNotification(data.error || 'Xatolik', 'error');
        }
    });
}

function checkout() {
    if (cart.length === 0) {
        showNotification('Savat bo\'sh!', 'error');
        return;
    }
    const client = clientName;
    const seller = "Sotuvchi";
    let promises = [];
    cart.forEach(item => {
        promises.push(
            fetch('/order/add/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `product_id=${item.id}&quantity=${item.quantity}&client=${encodeURIComponent(client)}&seller=${encodeURIComponent(seller)}`
            }).then(response => response.json())
        );
    });

    Promise.all(promises).then(results => {
        let allSuccess = results.every(r => r.success);
        if (allSuccess) {
            showNotification('Buyurtma muvaffaqiyatli berildi!', 'success');
            // cart = []; // Savatni tozalash kerak emas!
            updateCartBadge();
            closeCart();
            if (currentRole === 'seller') {
                window.location.reload();
            }
        } else {
            showNotification('Xatolik yuz berdi!', 'error');
        }
    }).catch(() => {
        showNotification('Xatolik yuz berdi!', 'error');
    });
}

function showNotification(msg, type) {
    alert(msg); // Custom notification logic uchun o'zgartiring
}

window.onload = function() {
    updateCartBadge();
};