const baseUrl = 'http://127.0.0.1:5000';

// Add Tenant
document.getElementById('tenant-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('tenant-name').value;
    const contact = document.getElementById('tenant-contact').value;
    const address = document.getElementById('tenant-address').value;

    const response = await fetch(`${baseUrl}/inquilinos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: name, contato: contact, enderecoImovel: address }),
    });

    const data = await response.json();
    alert(data.message);
});

// Refresh Tenant List
document.getElementById('refresh-tenants').addEventListener('click', async () => {
    const response = await fetch(`${baseUrl}/inquilinos`);
    const tenants = await response.json();

    const tenantList = document.getElementById('tenant-list');
    tenantList.innerHTML = '';
    tenants.forEach((tenant) => {
        const li = document.createElement('li');
        li.textContent = `${tenant.id}: ${tenant.nome} - ${tenant.contato} (${tenant.enderecoImovel})`;
        tenantList.appendChild(li);
    });
});

// Add Rental
document.getElementById('rental-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const tenantId = document.getElementById('rental-tenant-id').value;
    const value = document.getElementById('rental-value').value;
    const dueDate = document.getElementById('rental-due-date').value;
    const status = document.getElementById('rental-status').value;

    const response = await fetch(`${baseUrl}/aluguels`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            inquilino_id: tenantId,
            valor: value,
            dataVencimento: dueDate,
            status: status,
        }),
    });

    const data = await response.json();
    alert(data.message);
});

// Refresh Rental List
document.getElementById('refresh-rentals').addEventListener('click', async () => {
    const response = await fetch(`${baseUrl}/aluguels`);
    const rentals = await response.json();

    const rentalList = document.getElementById('rental-list');
    rentalList.innerHTML = '';
    rentals.forEach((rental) => {
        const li = document.createElement('li');
        li.textContent = `${rental.id}: Tenant ${rental.inquilino_id} - $${rental.valor} due on ${rental.dataVencimento} (${rental.status})`;
        rentalList.appendChild(li);
    });
});
