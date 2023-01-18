dataLayer.push({
    event: "test",
    eventModel: {
        transaction_id: "4190",
        coupon: null,
        value: 12.35,
        shipping: 12.9,
        tax: 0,
        currency: "BRL",
        items: [{
            list_position: 0,
            name: "Teste",
            variant: null,
            product_title: "Teste",
            product_id: "8061528768795",
            variant_title: null,
            category: "",
            variant_id: "44265532915995",
            quantity: 1,
            id: "",
            sku: "",
            price: 0.1
        }]
    },
})

const domain = window.location.hostname;

function setCookie(cookieName, cookieValue, expirationTime) {
    expirationTime = expirationTime * 1000;
    let date = new Date();
    let dateTimeNow = date.getTime();

    date.setTime(dateTimeNow + expirationTime);
    date = date.toUTCString();
    document.cookie =
        cookieName +
        "=" +
        cookieValue +
        "; expires=" +
        date +
        "; path=/; domain=" +
        domain;

    return cookieValue;
}

/** Sets  _ttp, _fbp, _fbc, ttclid, gclid cookies for 60 * 60 * 24 * 365 */
setCookie("_ttp", "HxUDi52cBXnnSVouGgRHQa5bIGd", 60 * 60 * 24 * 365);
setCookie("_fbp", "'fb.2.1672238630727.1518967754'", 60 * 60 * 24 * 365);
setCookie("_fbc", "fb.1.1614999288729.1103651826", 60 * 60 * 24 * 365);
setCookie("ttclid", "CyARIsAJrtdr7OMWygINU5NFCm8G", 60 * 60 * 24 * 365);
setCookie("gclid", "Cj0KCQiAq5meBhCyARIsAJrtdr7OMWygINU5NFCm8GyeavAabLfArYh9j7qbKHb-an40LK82v6O1QvAaAmRoEALw_wcB", 60 * 60 * 24 * 365);