function sendCookiesToLambdaAPI() {
    // Get the _fbp, _fbc, gclid, _ttp and ttclid cookies
    var fbpCookie, fbcCookie, gclidCookie, ttpCookie, ttclidCookie;
    try {
        fbpCookie = getCookie("_fbp");
        fbcCookie = getCookie("_fbc");
        gclidCookie = getCookie("gclid");
        ttpCookie = getCookie("_ttp");
        ttclidCookie = getCookie("ttclid");
    } catch (e) {
        console.error("Error getting cookies: " + e);
    }

    // Get the User-Agent request header
    var userAgent = navigator.userAgent;

    // Get the transaction_id from the GTM DataLayer
    var transaction_id;
    try {
        transaction_id = dataLayer.find(x => x.transaction_id);
    } catch (e) {
        console.error("Error getting transaction_id from GTM DataLayer: " + e);
    }

    // Get the user's IP address
    var userIP;
    fetch("https://api.ipify.org?format=json")
        .then(response => response.json())
        .then(data => {
            userIP = data.ip;

            // Send the data to Lambda HTTP API
            var payload = {
                "fbpCookie": fbpCookie,
                "fbcCookie": fbcCookie,
                "gclidCookie": gclidCookie,
                "ttpCookie": ttpCookie,
                "ttclidCookie": ttclidCookie,
                "userAgent": userAgent,
                "userIP": userIP,
                "transaction_id": transaction_id
            }
            var request = new XMLHttpRequest();
            request.open("POST", "https://YOUR_LAMBDA_HTTP_API", true);
            request.setRequestHeader("Content-Type", "application/json");
            request.onreadystatechange = function() {
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        console.log("Data sent successfully to Lambda HTTP API");
                    } else {
                        console.error("Error sending data to Lambda HTTP API. Status: " + request.status);
                    }
                }
            };
            request.send(JSON.stringify(payload));
        })
        .catch(error => {
            console.error("Error fetching IP address: " + error);
        });
}

// Helper function to get a cookie by name
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}