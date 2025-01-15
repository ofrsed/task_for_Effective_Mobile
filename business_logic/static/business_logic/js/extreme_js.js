    // Добавление нового блюда в заказ
function addDishField() {
    const orderItemsList = document.getElementById("order-items-list");

    const remainingDishes = availableDishes.filter(
        (dish) => !selectedDishes.some((selected) => selected.id === dish.id)
    );

    if (remainingDishes.length === 0) {
        alert("Все блюда уже добавлены.");
        return;
    }


    const dishRow = document.createElement("div");
    dishRow.style.display = "flex";
    dishRow.style.alignItems = "center";
    dishRow.style.marginBottom = "10px";

    const select = document.createElement("select");
    select.style.flex = "1";
    select.style.marginRight = "10px";

    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Выберите блюдо...";
    select.appendChild(emptyOption);

    remainingDishes.forEach((dish) => {
        const option = document.createElement("option");
        option.value = dish.id;
        option.textContent = `${dish.name} (${dish.price} ₽)`;
        select.appendChild(option);
    });

    const quantityInput = document.createElement("input");
    quantityInput.type = "number";
    quantityInput.value = 1; // По умолчанию количество 1
    quantityInput.style.marginRight = "10px";
    quantityInput.min = 1;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Удалить";
    deleteBtn.style.marginLeft = "10px";
    deleteBtn.onclick = () => {
        const selectedId = parseInt(select.value);
        selectedDishes = selectedDishes.filter(dish => dish.id !== selectedId);
        dishRow.remove();
    };

    select.onchange = () => {
        const selectedId = parseInt(select.value);
        if (selectedId) {
            const dish = availableDishes.find((dish) => dish.id === selectedId);
            if (dish && !selectedDishes.some((selected) => selected.id === dish.id)) {
                selectedDishes.push(dish);
            }
        }
    };

    dishRow.appendChild(select);
    dishRow.appendChild(quantityInput);
    dishRow.appendChild(deleteBtn);

    orderItemsList.appendChild(dishRow);
}

        const orders = [];
    let socket;
    let availableDishes = [];
    let selectedDishes = [];


function setupWebSocket() {
    socket = new WebSocket('ws://localhost:8000/ws/orders/');

    socket.onopen = () => {
        console.log("WebSocket соединение установлено.");
        socket.send(JSON.stringify({ action: "get-orders" }));
        socket.send(JSON.stringify({ action: "get-dishes" }));
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Получены данные:", data);

        if (data.action === "get-orders") {
            updateOrdersList(data.orders);
        } else if (data.action === "new-order") {
            orders.push(data.order);
            updateOrdersList(orders);
        } else if (data.action === "get-dishes") {
            availableDishes = data.dishes;
        }
    };

    socket.onclose = () => {
        console.log("WebSocket соединение закрыто.");
    };

    socket.onerror = (error) => {
        console.error("WebSocket ошибка:", error);
    };
}


function addDishField() {
    const orderItemsList = document.getElementById("order-items-list");

    const remainingDishes = availableDishes.filter(
        (dish) => !selectedDishes.some((selected) => selected.id === dish.id)
    );

    if (remainingDishes.length === 0) {
        alert("Все блюда уже добавлены.");
        return;
    }

    const dishRow = document.createElement("div");
    dishRow.style.display = "flex";
    dishRow.style.alignItems = "center";
    dishRow.style.marginBottom = "10px";

    const select = document.createElement("select");
    select.style.flex = "1";
    select.style.marginRight = "10px";

    // Добавляем пустое значение в select
    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Выберите блюдо...";
    select.appendChild(emptyOption);

    remainingDishes.forEach((dish) => {
        const option = document.createElement("option");
        option.value = dish.id;
        option.textContent = `${dish.name} (${dish.price} ₽)`;
        select.appendChild(option);
    });

    const quantityInput = document.createElement("input");
    quantityInput.type = "number";
    quantityInput.value = 1;
    quantityInput.style.marginRight = "10px";
    quantityInput.min = 1;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Удалить";
    deleteBtn.style.marginLeft = "10px";
    deleteBtn.onclick = () => {
        const selectedId = parseInt(select.value);
        selectedDishes = selectedDishes.filter(dish => dish.id !== selectedId);
        dishRow.remove();
    };

    select.onchange = () => {
        const selectedId = parseInt(select.value);
        const dish = availableDishes.find((dish) => dish.id === selectedId);
        if (dish && !selectedDishes.some((selected) => selected.id === dish.id)) {
            selectedDishes.push(dish);
        }
    };

    dishRow.appendChild(select);
    dishRow.appendChild(quantityInput);
    dishRow.appendChild(deleteBtn);

    orderItemsList.appendChild(dishRow);
}


        // Отправка заказа
function submitOrder() {
    const tableNumber = document.getElementById("table-number").value;
    if (!tableNumber || selectedDishes.length === 0) {
        alert("Пожалуйста, заполните номер стола и добавьте хотя бы одно блюдо.");
        return;
    }

    const order = {
        table_number: parseInt(tableNumber),
        items: selectedDishes.map((dish) => {
            return {
                dish: dish.name,
                quantity: 1 // TODO
            };
        }),
    };

    socket.send(JSON.stringify({ action: "add-order", order: order }));
    selectedDishes = [];
    document.getElementById("order-items-list").innerHTML = "";
        }

 // Обновление заказов
function updateOrdersList(orders) {
    const orderListElement = document.getElementById("order-items");
    orderListElement.innerHTML = "";

    orders.forEach((order) => {
        const orderCard = document.createElement("div");
        orderCard.classList.add("order-card");

        let orderDetails = `
            <h3>Заказ ${order.id}</h3>
            <p>Стол: ${order.table_number}</p>
            <p>Статус: ${order.status}</p>
            <p style="margin-bottom: 20px; border-bottom: 1px solid gray;">Общая сумма: ${order.total_price}</p>
        `;

        orderDetails += "<ul>";
        order.items.forEach((item) => {
            orderDetails += `
                <li class="item">
                    <p><strong>Блюдо:</strong> ${item.dish} : ${item.quantity} шт.</p>

                </li>
            `;
        });
        orderDetails += "</ul>";

        orderDetails += `
        <div class="actions">
            <button class="delete-btn" onclick="deleteOrder(${order.id})">Удалить</button>
            <button class="status-btn" onclick="changeOrderStatus(${order.id}, this)">Изменить статус</button>
            <div id="status-dropdown-${order.id}" class="status-dropdown" style="display: none;">
                <select id="status-select-${order.id}">
                    <option value="pending">В ожидании</option>
                    <option value="ready">Готово</option>
                    <option value="paid">Оплачено</option>
                </select>
                <button onclick="submitStatusChange(${order.id})">Отправить</button>
            </div>
        </div>
        `;

        orderCard.innerHTML = orderDetails;
        orderListElement.appendChild(orderCard);
    });
}




// Список статаусов
function changeOrderStatus(orderId, buttonElement) {
    const dropdown = document.getElementById(`status-dropdown-${orderId}`);
    const rect = buttonElement.getBoundingClientRect();
    dropdown.style.left = `${rect.left}px`;
    dropdown.style.top = `${rect.bottom + window.scrollY}px`;
    dropdown.style.display = 'block';
}


function submitStatusChange(orderId) {
    const selectedStatus = document.getElementById(`status-select-${orderId}`).value;

    socket.send(JSON.stringify({
        action: "change-status",
        order_id: orderId,
        status: selectedStatus
    }));

    document.getElementById(`status-dropdown-${orderId}`).style.display = "none";
}

function deleteOrder(orderId) {
    socket.send(JSON.stringify({
        action: "delete-order",
        order_id: orderId
    }));
    console.log(`Запрос на удаление заказа с ID ${orderId} отправлен на сервер.`);
}


// Запуск WebSocket
setupWebSocket();