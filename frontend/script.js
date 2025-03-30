async function fetchShips() {
    const response = await fetch("http://127.0.0.1:5000/ships");
    const data = await response.json();
    
    let shipList = document.getElementById("shipList");
    shipList.innerHTML = "";

    data.forEach(ship => {
        let item = document.createElement("li");
        item.textContent = `${ship.ship_name} - Captain: ${ship.captain} - Capacity: ${ship.capacity}`;
        shipList.appendChild(item);
    });
}

async function fetchOperations() {
    const response = await fetch("http://127.0.0.1:5000/operations");
    const data = await response.json();
    
    let operationList = document.getElementById("operationList");
    operationList.innerHTML = "";

    data.forEach(operation => {
        let item = document.createElement("li");
        item.textContent = `${operation.operation_type} - Details: ${operation.details} - Time: ${operation.timestamp}`;
        operationList.appendChild(item);
    });
}
