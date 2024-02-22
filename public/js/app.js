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
        console.log(response)
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
        refreshCart()  
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
        popup.innerHTML = response.data;

        // Close the existing modal
        const existingModal = bootstrap.Modal.getInstance(popup);
        if (existingModal) {
            existingModal.hide();
            existingModal.dispose();
        }

        // Open the updated cart modal
        const newModal = new bootstrap.Modal(popup);
        newModal.show();
    })
    .catch(error => (
        console.log(error)
    ));
}

function finishOrder() {
    axios({
        method: "GET",
        url: "/order/complete"
    })
    .then(response => {
        window.location = "/order/complete"
    })
    .catch(error => {
        console.log(error)
    })
}

function setTime () {
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
            console.log("hey")
            document.querySelector("#side-nav").setAttribute("data-collapsed", "true")
        })

        $(document).on("click", ".side-nav-open", (event) => {
            console.log("hey")
            document.querySelector("#side-nav").setAttribute("data-collapsed", "false")
        })
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

    $(document).on("click", ".delOrderItem", (event) => {
        deleteOrderItem(event.target.getAttribute("data-item"))
    })

    $(document).on("click", ".orderComplete", (event) => {
        finishOrder();
    })
})