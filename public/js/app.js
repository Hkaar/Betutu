$(document).ready(()=> {
    'use strict';

    new Splide( '.splide', {
        type: "loop",
        autoplay: true,
        focus: "center",
        gap: '8px',
        perPage: 2
    }).mount();
})