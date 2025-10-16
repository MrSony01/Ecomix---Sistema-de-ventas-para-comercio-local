// Require authentication
requireAuth();

// Logout handler
document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    logout();
});

// Load dashboard data
async function loadDashboardData() {
    try {
        // Load today's sales
        const todaySales = await apiRequest('/sales/sales/today_sales/');
        document.getElementById('todaySales').textContent = formatCurrency(todaySales.total_sales);
        document.getElementById('transactionCount').textContent = todaySales.transaction_count;
        
        // Load low stock products
        const lowStockProducts = await apiRequest('/inventory/products/low_stock/');
        document.getElementById('lowStock').textContent = lowStockProducts.length;
        
        // Load customer count
        const customers = await apiRequest('/loyalty/customers/');
        document.getElementById('customerCount').textContent = customers.count || customers.length;
        
        // Load recent sales
        const recentSales = await apiRequest('/sales/sales/?page_size=10');
        loadRecentSales(recentSales.results || recentSales);
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Error al cargar datos del dashboard', 'danger');
    }
}

function loadRecentSales(sales) {
    const tbody = document.querySelector('#recentSalesTable tbody');
    tbody.innerHTML = '';
    
    if (!sales || sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay ventas recientes</td></tr>';
        return;
    }
    
    sales.forEach(sale => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${sale.sale_number}</td>
            <td>${sale.customer_name || 'N/A'}</td>
            <td>${formatCurrency(sale.total)}</td>
            <td><span class="badge bg-info">${sale.payment_method}</span></td>
            <td>${formatDate(sale.created_at)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Initialize dashboard
loadDashboardData();

// Auto-refresh every 30 seconds
setInterval(loadDashboardData, 30000);
