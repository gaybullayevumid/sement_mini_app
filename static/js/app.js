// Global Variables
let currentRole = null;
let products = [];
let cart = [];
let orders = [];

// Sample Data
const sampleProducts = [
    {
        id: 1,
        name: "Portland Sement M400",
        brand: "O'zSement",
        type: "Portland",
        quality: "Yuqori",
        weight: 50,
        image: "",
        description: "Yuqori sifatli qurilish sementi",
        origin: "O'zbekiston",
        cement_class: "M400",
        price: 120000
    }
];

// Initialize Application
function init() {
    loadDataFromStorage();
    updateCartBadge();
    setupEventListeners();

    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }
}

// Load data from localStorage
function loadDataFromStorage() {
    try {
        products = JSON.parse(localStorage.getItem('products')) || sampleProducts;
        cart = JSON.parse(localStorage.getItem('cart')) || [];
        orders = JSON.parse(localStorage.getItem('orders')) || [];
    } catch (error) {
        products = sampleProducts;
        cart = [];
        orders = [];
    }
}

// Save data to localStorage
function saveDataToStorage() {
    try {
        localStorage.setItem('products', JSON.stringify(products));
        localStorage.setItem('cart', JSON.stringify(cart));
        localStorage.setItem('orders', JSON.stringify(orders));
    } catch (error) {}
}

// Setup Event Listeners
function setupEventListeners() {
    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', handleAddProduct);
    }
    const cartModal = document.getElementById('cartModal');
    if (cartModal) {
        cartModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeCart();
            }
        });
    }
}

// Role Selection
function selectRole(role) {
    currentRole = role;
    document.getElementById('roleSelector').style.display = 'none';
    document.getElementById('backBtn').classList.add('show');
    if (role === 'client') {
        document.getElementById('clientInterface').classList.add('active');
        loadProducts();
        document.getElementById('floatingCart').classList.add('show');
    } else if (role === 'seller') {
        document.getElementById('sellerInterface').classList.add('active');
        loadOrders();
    }
}

// Go Back to Role Selection
function goBack() {
    document.getElementById('roleSelector').style.display = 'block';
    document.getElementById('clientInterface').classList.remove('active');
    document.getElementById('sellerInterface').classList.remove('active');
    document.getElementById('backBtn').classList.remove('show');
    document.getElementById('floatingCart').classList.remove('show');
    currentRole = null;
    closeCart();
}

// Load Products for Client
function loadProducts() {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';

    if (products.length === 0) {
        productList.innerHTML = '<p class="loading">Mahsulotlar yuklanmoqda</p>';
        return;
    }
    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product-item';
        productDiv.innerHTML = `
            ${product.image ? `<img src="${product.image}" alt="Rasm" style="width:100%;max-width:180px;border-radius:8px;margin-bottom:10px;" />` : ''}
            <h4>${product.name}</h4>
            <p><b>Brend:</b> ${product.brand || ''}</p>
            <p><b>Turi:</b> ${product.type || ''}</p>
            <p><b>Sifat:</b> ${product.quality || ''}</p>
            <p><b>Og'irligi:</b> ${product.weight || ''} t</p>
            <p><b>Klass:</b> ${product.cement_class || ''}</p>
            <p><b>Kelib chiqishi:</b> ${product.origin || ''}</p>
            <p>${product.description}</p>
            <div class="product-price">${product.price ? product.price.toLocaleString() : 0} so'm/tonna</div>
            <button class="btn" onclick="addToCart(${product.id})" ${product.weight === 0 ? 'disabled' : ''}>
                ${product.weight === 0 ? 'Tugagan' : 'Savatga qo\'shish'}
            </button>
        `;
        productList.appendChild(productDiv);
    });
}

// Add Product to Cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    if (product.weight === 0) return;
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        if (existingItem.quantity < product.weight) {
            existingItem.quantity += 1;
        } else {
            showNotification('Mavjud miqdordan ko\'p buyurtma bera olmaysiz!', 'error');
            return;
        }
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1,
            maxQuantity: product.weight
        });
    }
    saveDataToStorage();
    updateCartBadge();
    showNotification('Mahsulot savatga qo\'shildi!', 'success');
}

// Update Cart Badge
function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = totalItems;
    }
}

// Show Cart Modal
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
                <button class="btn-danger" onclick="removeFromCart(${item.id})" 
                        style="margin-left: 10px; padding: 5px 10px; font-size: 12px; width: auto;">
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

// Close Cart Modal
function closeCart() {
    const modal = document.getElementById('cartModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// Update Item Quantity in Cart
function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    const product = products.find(p => p.id === productId);
    if (!item || !product) return;
    const newQuantity = item.quantity + change;
    if (newQuantity <= 0) {
        removeFromCart(productId);
        return;
    }
    if (newQuantity > product.weight) {
        showNotification('Mavjud miqdordan ko\'p buyurtma bera olmaysiz!', 'error');
        return;
    }
    item.quantity = newQuantity;
    saveDataToStorage();
    updateCartBadge();
    showCart();
}

// Remove Item from Cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveDataToStorage();
    updateCartBadge();
    showCart();
    showNotification('Mahsulot savatdan o\'chirildi', 'info');
}

// Checkout Process
function checkout() {
    if (cart.length === 0) {
        showNotification('Savat bo\'sh!', 'error');
        return;
    }
    const order = {
        id: Date.now(),
        items: [...cart],
        total: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0),
        status: 'pending',
        date: new Date().toLocaleString('uz-UZ'),
        customer: getCurrentCustomer()
    };
    orders.push(order);
    cart.forEach(cartItem => {
        const product = products.find(p => p.id === cartItem.id);
        if (product) {
            product.weight -= cartItem.quantity;
        }
    });
    cart = [];
    saveDataToStorage();
    updateCartBadge();
    closeCart();
    if (currentRole === 'client') {
        loadProducts();
    }
    showNotification('Buyurtma muvaffaqiyatli berildi!', 'success');
    if (window.Telegram && window.Telegram.WebApp) {
        const message = `Yangi buyurtma: #${order.id}\nJami: ${order.total.toLocaleString()} so'm`;
        window.Telegram.WebApp.sendData(JSON.stringify(order));
    }
}

// Get Current Customer Info
function getCurrentCustomer() {
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe.user) {
        const user = window.Telegram.WebApp.initDataUnsafe.user;
        return `${user.first_name} ${user.last_name || ''}`.trim();
    }
    return 'Mijoz #' + Math.floor(Math.random() * 1000);
}

// Handle Add Product Form
function handleAddProduct(e) {
    e.preventDefault();
    const imageInput = document.getElementById('productImage');
    let imgUrl = '';
    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(event) {
            imgUrl = event.target.result;
            saveProductWithImage(imgUrl);
        };
        reader.readAsDataURL(imageInput.files[0]);
    } else {
        saveProductWithImage('');
    }
    function saveProductWithImage(imageSrc) {
        const newProduct = {
            id: Date.now(),
            name: document.getElementById('productName').value.trim(),
            brand: document.getElementById('productBrand').value.trim(),
            type: document.getElementById('productType').value.trim(),
            quality: document.getElementById('productQuality').value.trim(),
            weight: parseFloat(document.getElementById('productWeight').value),
            image: imageSrc,
            description: document.getElementById('productDescription').value.trim(),
            origin: document.getElementById('productOrigin').value.trim(),
            cement_class: document.getElementById('productCementClass').value.trim(),
            price: parseInt(document.getElementById('productPrice').value),
        };
        if (
            !newProduct.name || !newProduct.brand || !newProduct.type ||
            !newProduct.quality || !newProduct.weight || !newProduct.image ||
            !newProduct.origin || !newProduct.cement_class ||
            !newProduct.price || newProduct.price <= 0 || newProduct.weight <= 0
        ) {
            showNotification('Iltimos, barcha maydonlarni to\'g\'ri to\'ldiring!', 'error');
            return;
        }
        products.push(newProduct);
        saveDataToStorage();
        e.target.reset();
        showNotification('Mahsulot muvaffaqiyatli qo\'shildi!', 'success');
        if (currentRole === 'client') {
            loadProducts();
        }
    }
}

// Load Orders for Seller
function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    ordersList.innerHTML = '';
    if (orders.length === 0) {
        ordersList.innerHTML = '<p style="text-align: center; color: #7f8c8d;">Buyurtmalar yo‘q</p>';
        return;
    }
    orders.forEach(order => {
        const orderDiv = document.createElement('div');
        orderDiv.className = 'order-item';
        orderDiv.innerHTML = `
            <h4>Buyurtma #${order.id}</h4>
            <p><b>Vaqti:</b> ${order.date}</p>
            <p><b>Buyurtmachi:</b> ${order.customer}</p>
            <p><b>Jami:</b> ${order.total.toLocaleString()} so'm</p>
            <p><b>Status:</b>
                <span class="order-status status-${order.status}">${order.status}</span>
            </p>
            <div>
                <b>Mahsulotlar:</b>
                <ul>
                    ${order.items.map(item => `<li>${item.name} x ${item.quantity} t</li>`).join('')}
                </ul>
            </div>
        `;
        ordersList.appendChild(orderDiv);
    });
}

// Simple notification
function showNotification(msg, type) {
    alert(msg); // You can replace with custom notification logic
}

window.onload = init;