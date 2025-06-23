let currentRole = null;
let cart = [];
const clientName = "Mijoz"; // Real loyihada foydalanuvchi nomini olish lozim
const userId = "default_user"; // Real loyihada Telegram user ID

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
    // Serverdan savat ma'lumotlarini olish
    fetch(`/cart/view/?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('cartBadge');
            if (badge && data.success) {
                badge.textContent = data.count || 0;
            }
        })
        .catch(error => console.error('Cart badge update error:', error));
}

function selectRole(role) {
    currentRole = role;
    document.getElementById('roleSelector').style.display = 'none';
    document.getElementById('backBtn').classList.add('show');
    if (role === 'client') {
        document.getElementById('clientInterface').classList.add('active');
        document.getElementById('floatingCart').classList.add('show');
        updateCartBadge(); // Mijoz interfeysini ochganda cartni yangilash
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

// YANGI: Savatga qo'shish funksiyasi - serverga yuboradi
function addToCart(productId) {
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product_id: productId,
            user_id: userId,
            quantity: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Mahsulot savatga qo\'shildi!', 'success');
            updateCartBadge();
        } else {
            showNotification(data.error || 'Xatolik yuz berdi', 'error');
        }
    })
    .catch(error => {
        console.error('Add to cart error:', error);
        showNotification('Xatolik yuz berdi', 'error');
    });
}

// YANGI: Savatni ko'rsatish - serverdan ma'lumot oladi
function showCart() {
    const modal = document.getElementById('cartModal');
    const cartItems = document.getElementById('cartItems');
    cartItems.innerHTML = '<p style="text-align: center;">Yuklanmoqda...</p>';
    modal.classList.add('show');

    // Serverdan cart ma'lumotlarini olish
    fetch(`/cart/view/?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            cartItems.innerHTML = '';
            
            if (!data.success || data.cart_items.length === 0) {
                cartItems.innerHTML = '<p style="text-align: center; color: #7f8c8d;">Savat bo\'sh</p>';
                document.getElementById('totalPrice').textContent = '0';
                return;
            }

            let total = 0;
            data.cart_items.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'cart-item';
                itemDiv.innerHTML = `
                    <div>
                        <h4>${item.product_name}</h4>
                        <p>${item.price.toLocaleString()} so'm/tonna</p>
                    </div>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span style="margin: 0 10px; font-weight: bold;">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, ${item.quantity + 1})">+</button>
                        <button class="btn-danger" onclick="removeFromCart(${item.id})" style="margin-left: 10px; padding: 5px 10px; font-size: 12px; width: auto;">
                            O'chirish
                        </button>
                    </div>
                `;
                cartItems.appendChild(itemDiv);
                total += item.total_price;
            });

            document.getElementById('totalPrice').textContent = total.toLocaleString();
        })
        .catch(error => {
            console.error('Show cart error:', error);
            cartItems.innerHTML = '<p style="text-align: center; color: #e74c3c;">Xatolik yuz berdi</p>';
        });

    // Pending orderlarni ham ko'rsatish (eski kod)
    fetch(`/order/my_pending/?client=${encodeURIComponent(clientName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.orders && data.orders.length > 0) {
                data.orders.forEach(order => {
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
                });
            }
        })
        .catch(error => console.error('Pending orders error:', error));
}

function closeCart() {
    const modal = document.getElementById('cartModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// YANGI: Cart quantity ni o'zgartirish
function updateCartQuantity(cartItemId, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(cartItemId);
        return;
    }

    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            cart_item_id: cartItemId,
            quantity: newQuantity,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showCart(); // Cart ni qayta yuklash
            updateCartBadge();
        } else {
            showNotification(data.error || 'Xatolik yuz berdi', 'error');
        }
    })
    .catch(error => {
        console.error('Update quantity error:', error);
        showNotification('Xatolik yuz berdi', 'error');
    });
}

// YANGI: Savatdan o'chirish
function removeFromCart(cartItemId) {
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            cart_item_id: cartItemId,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Mahsulot savatdan o\'chirildi', 'info');
            showCart(); // Cart ni qayta yuklash
            updateCartBadge();
        } else {
            showNotification(data.error || 'Xatolik yuz berdi', 'error');
        }
    })
    .catch(error => {
        console.error('Remove from cart error:', error);
        showNotification('Xatolik yuz berdi', 'error');
    });
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

// YANGI: Checkout funksiyasi - serverga yuboradi
function checkout() {
    fetch('/cart/checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            user_id: userId,
            client: clientName,
            seller: "Sotuvchi"
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Buyurtma muvaffaqiyatli berildi!', 'success');
            updateCartBadge();
            closeCart();
            if (currentRole === 'seller') {
                window.location.reload();
            }
        } else {
            showNotification(data.error || 'Xatolik yuz berdi!', 'error');
        }
    })
    .catch(error => {
        console.error('Checkout error:', error);
        showNotification('Xatolik yuz berdi!', 'error');
    });
}

function showNotification(msg, type) {
    alert(msg); // Custom notification logic uchun o'zgartiring
}

// Sahifa yuklanganda cartni yangilash
window.onload = function() {
    updateCartBadge();
};

// Eski funksiyalar - backward compatibility uchun
function updateQuantity(productId, change) {
    // Bu funksiya endi ishlatilmaydi, lekin xatolik chiqmasligi uchun qoldirildi
    console.warn('updateQuantity is deprecated, use updateCartQuantity instead');
}