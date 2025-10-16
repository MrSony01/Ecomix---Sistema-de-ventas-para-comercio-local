// Require authentication
requireAuth();

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    logout();
});

// Cart state
let cart = [];
let products = [];
let customers = [];

// Load initial data
async function loadInitialData() {
    try {
        // Load products
        const productsResponse = await apiRequest('/inventory/products/?is_active=true');
        products = productsResponse.results || productsResponse;
        displayProducts(products);
        
        // Load customers
        const customersResponse = await apiRequest('/loyalty/customers/?is_active=true');
        customers = customersResponse.results || customersResponse;
        loadCustomers();
        
    } catch (error) {
        console.error('Error loading data:', error);
        showAlert('Error al cargar datos', 'danger');
    }
}

function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '';
    
    if (!products || products.length === 0) {
        grid.innerHTML = '<div class="col-12"><p class="text-center text-muted">No hay productos disponibles</p></div>';
        return;
    }
    
    products.forEach(product => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-3';
        col.innerHTML = `
            <div class="card product-card border" onclick="addToCart(${product.id})">
                <div class="card-body">
                    <h6 class="card-title">${product.name}</h6>
                    <p class="card-text mb-1">
                        <small class="text-muted">SKU: ${product.sku}</small>
                    </p>
                    <p class="card-text mb-1">
                        <strong class="text-success">${formatCurrency(product.price)}</strong>
                    </p>
                    <p class="card-text mb-0">
                        <small class="${product.stock <= product.min_stock ? 'text-danger' : 'text-muted'}">
                            Stock: ${product.stock}
                        </small>
                    </p>
                </div>
            </div>
        `;
        grid.appendChild(col);
    });
}

function loadCustomers() {
    const select = document.getElementById('customerSelect');
    customers.forEach(customer => {
        const option = document.createElement('option');
        option.value = customer.id;
        option.textContent = `${customer.name} - ${customer.phone}`;
        select.appendChild(option);
    });
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    if (product.stock <= 0) {
        showAlert('Producto sin stock disponible', 'warning');
        return;
    }
    
    const existingItem = cart.find(item => item.product.id === productId);
    
    if (existingItem) {
        if (existingItem.quantity >= product.stock) {
            showAlert('No hay suficiente stock disponible', 'warning');
            return;
        }
        existingItem.quantity++;
    } else {
        cart.push({
            product: product,
            quantity: 1,
            unit_price: parseFloat(product.price),
            discount: 0
        });
    }
    
    updateCart();
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.product.id !== productId);
    updateCart();
}

function updateQuantity(productId, quantity) {
    const item = cart.find(item => item.product.id === productId);
    if (!item) return;
    
    const product = products.find(p => p.id === productId);
    
    if (quantity > product.stock) {
        showAlert('No hay suficiente stock disponible', 'warning');
        return;
    }
    
    if (quantity <= 0) {
        removeFromCart(productId);
    } else {
        item.quantity = quantity;
        updateCart();
    }
}

function updateCart() {
    const cartItemsDiv = document.getElementById('cartItems');
    
    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<p class="text-center text-muted">Carrito vacío</p>';
        updateTotals();
        return;
    }
    
    cartItemsDiv.innerHTML = '';
    
    cart.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <div class="flex-grow-1">
                    <strong>${item.product.name}</strong><br>
                    <small class="text-muted">${formatCurrency(item.unit_price)} c/u</small>
                </div>
                <button class="btn btn-sm btn-danger" onclick="removeFromCart(${item.product.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div class="d-flex justify-content-between align-items-center">
                <div class="input-group input-group-sm" style="width: 120px;">
                    <button class="btn btn-outline-secondary" onclick="updateQuantity(${item.product.id}, ${item.quantity - 1})">-</button>
                    <input type="number" class="form-control text-center" value="${item.quantity}" 
                           onchange="updateQuantity(${item.product.id}, parseInt(this.value))" min="1" max="${item.product.stock}">
                    <button class="btn btn-outline-secondary" onclick="updateQuantity(${item.product.id}, ${item.quantity + 1})">+</button>
                </div>
                <strong>${formatCurrency(item.quantity * item.unit_price)}</strong>
            </div>
        `;
        cartItemsDiv.appendChild(itemDiv);
    });
    
    updateTotals();
}

function updateTotals() {
    const subtotal = cart.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0);
    const discount = cart.reduce((sum, item) => sum + item.discount, 0);
    const total = subtotal - discount;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    document.getElementById('discount').textContent = formatCurrency(discount);
    document.getElementById('total').textContent = formatCurrency(total);
}

// Search products
document.getElementById('searchProduct').addEventListener('input', (e) => {
    const search = e.target.value.toLowerCase();
    const filtered = products.filter(p => 
        p.name.toLowerCase().includes(search) || 
        p.sku.toLowerCase().includes(search) ||
        (p.barcode && p.barcode.toLowerCase().includes(search))
    );
    displayProducts(filtered);
});

// Clear cart
document.getElementById('clearCart').addEventListener('click', () => {
    if (confirm('¿Estás seguro de limpiar el carrito?')) {
        cart = [];
        updateCart();
    }
});

// Complete sale
document.getElementById('completeSale').addEventListener('click', async () => {
    if (cart.length === 0) {
        showAlert('El carrito está vacío', 'warning');
        return;
    }
    
    const customerId = document.getElementById('customerSelect').value;
    const paymentMethod = document.getElementById('paymentMethod').value;
    
    const saleData = {
        customer: customerId || null,
        payment_method: paymentMethod,
        items: cart.map(item => ({
            product: item.product.id,
            quantity: item.quantity,
            unit_price: item.unit_price.toFixed(2),
            discount: item.discount.toFixed(2)
        }))
    };
    
    try {
        const sale = await apiRequest('/sales/sales/', {
            method: 'POST',
            body: JSON.stringify(saleData)
        });
        
        // Show success modal
        document.getElementById('saleNumber').textContent = sale.sale_number;
        document.getElementById('saleTotal').textContent = formatCurrency(sale.total);
        
        const modal = new bootstrap.Modal(document.getElementById('saleCompletedModal'));
        modal.show();
        
        // Clear cart and reload products
        cart = [];
        updateCart();
        loadInitialData();
        
        showAlert('Venta completada exitosamente', 'success');
        
    } catch (error) {
        console.error('Error completing sale:', error);
        showAlert(error.message || 'Error al completar la venta', 'danger');
    }
});

// Initialize
loadInitialData();
