const API_URL = 'http://localhost:8000/api';

let carrito = [];
let productos = [];

// Mostrar alerta
function mostrarAlerta(mensaje, tipo = 'success') {
    const alertContainer = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo} alert-dismissible fade show`;
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

// Cargar productos desde la API
async function cargarProductos() {
    try {
        const response = await fetch(`${API_URL}/productos/`);
        if (!response.ok) throw new Error('Error al cargar productos');
        
        productos = await response.json();
        mostrarProductos();
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('Error al cargar productos', 'danger');
    }
}

// Mostrar productos en la interfaz
function mostrarProductos() {
    const lista = document.getElementById('lista-productos');
    const buscador = document.getElementById('buscador').value.toLowerCase();

    const productosFiltrados = productos.filter(producto => 
        producto.nombre.toLowerCase().includes(buscador) ||
        producto.codigo.toLowerCase().includes(buscador)
    );

    if (productosFiltrados.length === 0) {
        lista.innerHTML = '<div class="col-12 text-center"><p>No se encontraron productos</p></div>';
        return;
    }

    lista.innerHTML = productosFiltrados.map(producto => `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-3">
            <div class="card producto-card ${producto.stock === 0 ? 'border-danger' : ''}" 
                 onclick="agregarAlCarrito(${producto.id})">
                <div class="card-body">
                    <h6 class="card-title">${producto.nombre}</h6>
                    <p class="card-text fs-5 fw-bold">$${producto.precio.toLocaleString()}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="${producto.stock < 3 ? 'stock-bajo' : 'text-muted'}">
                            Stock: ${producto.stock}
                        </small>
                        <span class="badge bg-primary">${producto.codigo}</span>
                    </div>
                    ${producto.stock === 0 ? 
                        '<div class="mt-2"><span class="badge bg-danger">Sin stock</span></div>' : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// Funciones del carrito
function agregarAlCarrito(productoId) {
    const producto = productos.find(p => p.id === productoId);
    
    if (!producto) return;
    
    if (producto.stock === 0) {
        mostrarAlerta('❌ Este producto no tiene stock disponible', 'warning');
        return;
    }

    const existe = carrito.find(item => item.id === productoId);
    
    if (existe) {
        if (existe.cantidad >= producto.stock) {
            mostrarAlerta('❌ No hay suficiente stock disponible', 'warning');
            return;
        }
        existe.cantidad++;
    } else {
        carrito.push({
            id: producto.id,
            nombre: producto.nombre,
            precio: producto.precio,
            cantidad: 1
        });
    }
    
    actualizarCarrito();
    mostrarAlerta(`✅ ${producto.nombre} agregado al carrito`, 'success');
}

function removerDelCarrito(productoId) {
    carrito = carrito.filter(item => item.id !== productoId);
    actualizarCarrito();
    mostrarAlerta('Producto removido del carrito', 'info');
}

function actualizarCarrito() {
    const carritoHTML = document.getElementById('carrito-items');
    const totalHTML = document.getElementById('total-carrito');
    
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    
    if (carrito.length === 0) {
        carritoHTML.innerHTML = '<p class="text-muted text-center">No hay productos en el carrito</p>';
    } else {
        carritoHTML.innerHTML = carrito.map(item => `
            <div class="carrito-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <small><strong>${item.nombre}</strong></small><br>
                        <small class="text-muted">${item.cantidad} x $${item.precio.toLocaleString()}</small>
                    </div>
                    <div class="text-end">
                        <strong>$${(item.precio * item.cantidad).toLocaleString()}</strong>
                        <div class="mt-1">
                            <button class="btn btn-sm btn-outline-secondary" onclick="modificarCantidad(${item.id}, -1)">-</button>
                            <span class="mx-2">${item.cantidad}</span>
                            <button class="btn btn-sm btn-outline-secondary" onclick="modificarCantidad(${item.id}, 1)">+</button>
                            <button class="btn btn-sm btn-outline-danger ms-2" onclick="removerDelCarrito(${item.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    totalHTML.textContent = total.toLocaleString();
}

function modificarCantidad(productoId, cambio) {
    const item = carrito.find(item => item.id === productoId);
    const producto = productos.find(p => p.id === productoId);
    
    if (item && producto) {
        const nuevaCantidad = item.cantidad + cambio;
        
        if (nuevaCantidad <= 0) {
            removerDelCarrito(productoId);
            return;
        }
        
        if (nuevaCantidad > producto.stock) {
            mostrarAlerta('❌ No hay suficiente stock disponible', 'warning');
            return;
        }
        
        item.cantidad = nuevaCantidad;
        actualizarCarrito();
    }
}

function limpiarCarrito() {
    if (carrito.length === 0) return;
    
    if (confirm('¿Estás seguro de que quieres limpiar el carrito?')) {
        carrito = [];
        actualizarCarrito();
        mostrarAlerta('Carrito limpiado', 'info');
    }
}

// Procesar venta
async function procesarVenta() {
    if (carrito.length === 0) {
        mostrarAlerta('⚠️ Agrega productos al carrito primero', 'warning');
        return;
    }
    
    try {
        const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
        const ventaData = {
            total: total,
            items: carrito.map(item => ({
                producto_id: item.id,
                cantidad: item.cantidad,
                precio: item.precio
            }))
        };
        
        const response = await fetch(`${API_URL}/ventas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(ventaData)
        });
        
        if (response.ok) {
            const resultado = await response.json();
            
            // Mostrar modal de éxito
            document.getElementById('venta-mensaje').textContent = 
                `Venta #${resultado.id} procesada correctamente. Total: $${total.toLocaleString()}`;
            
            // Mostrar detalles
            document.getElementById('venta-detalles').innerHTML = `
                <div class="mt-3">
                    <strong>Productos vendidos:</strong>
                    <ul class="mt-2">
                        ${carrito.map(item => `
                            <li>${item.cantidad} x ${item.nombre} - $${(item.precio * item.cantidad).toLocaleString()}</li>
                        `).join('')}
                    </ul>
                </div>
            `;
            
            // Mostrar modal
            new bootstrap.Modal(document.getElementById('ventaModal')).show();
            
            carrito = [];
            actualizarCarrito();
            await cargarProductos();
            
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Error al procesar la venta');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta(`❌ Error: ${error.message}`, 'danger');
    }
}

function imprimirTicket() {
    window.print();
}

// Buscador en tiempo real
document.getElementById('buscador').addEventListener('input', mostrarProductos);

// Actualizar hora
function actualizarHora() {
    const ahora = new Date();
    document.getElementById('hora-actual').textContent = ahora.toLocaleTimeString();
}
setInterval(actualizarHora, 1000);

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    cargarProductos();
    actualizarHora();
});