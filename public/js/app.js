function displayItem(item) {
    const popup = document.getElementById("itemInfo")
    
    axios({
        method: "GET",
        url: `/order/menu-item/${item}`
    })
    .then(response => {
        popup.innerHTML = response.data;
        
        const modal = new bootstrap.Modal(popup);
        modal.show()
    })
    .catch(error => {
        console.log(error)
    })
}

function displayOrderItems() {
    const popup = document.getElementById("cartWindow")

    axios({
        method: "GET",
        url: "/order/orders"
    })
    .then(response => {
        popup.innerHTML = response.data;

        const modal = new bootstrap.Modal(popup);
        modal.show()
    })
    .catch(error => (
        console.log(error)
    ))
}

function addItem() {
    const formData = new FormData(document.getElementById("itemForm"))

    axios({
        method: "POST",
        url: "/order/add",
        data: formData
    })
    .then(response => {
        const popup = bootstrap.Modal.getInstance(document.getElementById("itemInfo"));

        if (popup) {
            popup.hide();
        }

        const notify = new bootstrap.Modal(document.getElementById("notify"));
        notify.show();
    })
    .catch(error => {
        console.log(error)
    })
}

function deleteOrderItem(orderItemId) {    
    axios({
        method: "DELETE",
        url: `/order/delete/item?id=${orderItemId}`
    })
    .then(response => {
        if (document.querySelector(".orders")) {
            getOrders()
        } else {
            refreshCart()  
        }
    })
    .catch(error => {
        console.log(error)
    })
}

function refreshCart() {
    const popup = document.getElementById("cartWindow");

    axios({
        method: "GET",
        url: "/order/orders"
    })
    .then(response => {
        // Close the existing modal
        const existingModal = bootstrap.Modal.getInstance(popup);

        if (existingModal) {
            existingModal.hide();
        }

        popup.innerHTML = response.data;

        // Open the updated cart modal
        const newModal = new bootstrap.Modal(popup);
        newModal.show();
    })
    .catch(error => {
        console.log(error);
    });
}

function finishOrder() {
    axios({
        method: "PUT",
        url: "/order/finish"
    })
    .then(response => {
        window.location = "/order/"
    })
    .catch(error => {
        console.log(error)
    })
}

function setTime() {
    const clock = document.getElementById("dashboardClock");
    const date = new Date();

    let mins = date.getMinutes();
    let hours = date.getHours();

    if (mins < 10) {
        mins = `0${mins}`;
    }

    if (hours < 10) {
        hours = `0${hours}`;
    }

    clock.innerHTML = `${hours}:${mins}`
}

function getOrders() {
    const orders = document.querySelector(".orders");

    axios({
        method: "GET",
        url: "/order/all"
    })
    .then(response => {
        orders.innerHTML = response.data
    })
    .catch(error => {
        console.log(error)
    })
}

function deleteOrder(token) {
    axios({
        method: "DELETE",
        url: `/order/delete?token=${token}`
    })
    .then(response => {
        getOrders()
    })
    .catch(error => {
        console.log(error)
    })
}

function displayMenuItems() {
    const items = document.querySelector(".items")

    axios({
        method: "GET",
        url: "/menu"
    })
    .then(response => {
        items.innerHTML = response.data;
    })
    .catch(error => {
        console.log(error)
    })
}

function deleteMenuItem(item) {
    axios({
        method: "DELETE",
        url: `/menu/delete?item=${item}`
    })
    .then(response => {
        displayMenuItems()
    })
    .catch(error => {
        console.log(error)
    })
}

function addMenuItem() {
    const formData = new FormData(document.getElementById("addItemForm"))

    axios({
        method: "POST",
        url: "/menu/add",
        data: formData
    })
    .then(response => {
        console.log(response)
        window.location = "/user/home"
    })
    .catch(error => {
        console.log(error)
    })
}

function displayModifyMenu(item) {
    const modifyPopUp = document.querySelector("#modifyItem")

    axios({
        method: "GET",
        url: `/menu/popup?item=${item}`
    })
    .then(response => {
        modifyPopUp.innerHTML = response.data;

        console.log(modifyPopUp)

        const modal = new bootstrap.Modal(modifyPopUp);
        modal.show()
    })
    .catch(error => {
        console.log(error)
    })
}

function submitModified() {
    const formData = new FormData(document.getElementById("modifyItemForm"))

    axios({
        method: "PUT",
        url: "/menu/update",
        data: formData
    })
    .then(response => {
        console.log(response)
        window.location = "/user/home"
    })
    .catch(error => {
        console.log(error)
    })
}

function setStats() {
    const counter = document.querySelector("#orderCount")

    axios({
        method: "GET",
        url: "/order/total"
    })
    .then(response => {
        counter.innerHTML = response.data
    })
    .catch(error => {
        console.log(error)
    })
}

function markOrderComplete(token) {
    axios({
        method: "PUT",
        url: `/order/complete?token=${token}`
    })
    .then(response => {
        getOrders();
    })
    .catch(error => {
        console.log(error)
    })
}

function resetOrders() {
    axios({
        method: "DELETE",
        url: "/order/delete/all"
    })
    .then(response => {
        getOrders();
    })
    .catch(error => {
        console.log(error)
    })
}

$(document).ready(() => {
    'use strict';

    if (document.querySelector(".splide")) {
        new Splide( '.splide', {
            type: "loop",
            autoplay: true,
            focus: "center",
            gap: '8px',
            perPage: 2
        }).mount();
    }

    if (document.querySelector("#dashboardClock")) {
        setInterval(setTime, 1000)
    }

    if (document.querySelector("#side-nav")) {
        $(document).on("click", ".side-nav-close", (event) => {
            document.querySelector("#side-nav").setAttribute("data-collapsed", "true")
        })

        $(document).on("click", ".side-nav-open", (event) => {
            document.querySelector("#side-nav").setAttribute("data-collapsed", "false")
        })
    }

    if (document.querySelector(".orders")) {
        getOrders()
        displayMenuItems()
        setStats()

        setInterval(getOrders, 7000)
        setInterval(displayMenuItems, 7000)
        setInterval(setStats, 7000)
    }

    $(document).on("click", ".item-card", (event) => {
        displayItem(event.target.getAttribute("data-item"))
    })

    $(document).on("click", "#cartToggle", (event) => {
        displayOrderItems()
    })

    $(document).on("submit", "#itemForm", (event) => {
        addItem(); 
        return false;
    });

    $(document).on("submit", "#addItemForm", (event) => {
        addMenuItem();
        displayMenuItems();
        return false;
    })

    $(document).on("submit", "#modifyItemForm", (event) => {
        submitModified();
        displayMenuItems();
        return false;
    })

    $(document).on("click", ".delOrderItem", (event) => {
        deleteOrderItem(event.target.getAttribute("data-item"))
    })

    $(document).on("click", ".deleteOrder", (event) => {
        deleteOrder(event.target.getAttribute("data-token"))
    })

    $(document).on("click", ".orderComplete", (event) => {
        finishOrder();
    })

    $(document).on("click", ".markOrder", (event) => {
        markOrderComplete(event.target.getAttribute("data-token"))
    })

    $(document).on("click", ".delItem", (event) => {
        deleteMenuItem(event.target.getAttribute("data-item"))
    })

    $(document).on("click", ".modifyItem", (event) => {
        displayModifyMenu(event.target.getAttribute("data-item"))
    })

    $(document).on("click", ".resetOrders", (event) => {
        resetOrders();
    })
})