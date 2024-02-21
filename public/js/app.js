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
    .then(response => (
        console.log(response)
    ))
    .catch(error => (
        console.log(error)
    ))
}

$(document).ready(()=> {
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

    $(document).on("click", ".item-card", (event) => {
        displayItem(event.target.getAttribute("data-item"))
    })
})