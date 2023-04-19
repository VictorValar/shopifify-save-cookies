console.log("send_cookies_aws.js loaded");


// Use this if you want to serve this file to multiple sites.
domain = window.location.href
if (domain.indexOf("your-site1.com") > -1) {
    post_url = "YOUR_LAMBDA_URL";
    console.log("Website name");
} else if (domain.indexOf("your-site2.com") > -1) {
    post_url = "YOUR_LAMBDA_URL"
    console.log("Website name");
}
var counter = 0;

function sendCookiesToLambdaAPI() {
    counter++;
    console.log("sendCookiesToLambdaAPI() called");
    // Get the _fbp, _fbc, gclid, _ttp and ttclid cookies
    var fbpCookie, fbcCookie, gclidCookie, ttpCookie, ttclidCookie;
    try {
        fbpCookie = getCookie("_fbp");
        fbcCookie = getCookie("_fbc");
        gclidCookie = getCookie("gclid");
        ttpCookie = getCookie("_ttp");
        ttclidCookie = getCookie("ttclid");
    } catch (e) {
        console.error("Error getting cookies" + e);
    }

    // Get the User-Agent request header
    var userAgent = navigator.userAgent;

    // Loop though the DataLayer and looks for a  transaction_id from the eventModel on purchase events
    // console.log(dataLayer[32][2]['transaction_id'])
    var transaction_id;
    for (var i = 0; i < dataLayer.length; i++) {
        console.log("looking for purchase event");
        if (dataLayer[i][1] == "purchase") {
            transaction_id = dataLayer[i][2]['transaction_id'];
            console.log("purchase event found");
            break;
        }
    }

    console.log("transaction id: " + transaction_id)


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

            // Prits the payload to the console as a table
            console.table(payload);

            var request = new XMLHttpRequest();
            request.open("POST", post_url, true);
            request.setRequestHeader("Content-Type", "application/json");
            request.onreadystatechange = function() {
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        console.log("Data sent successfully to Lambda HTTP API");
                        console.log(request.responseText);
                        return true
                    } else {
                        console.error("Error sending data to Lambda HTTP API. Status: " + request.status);
                        console.error(request.responseText);
                        if (counter <= 5) {
                            setTimeout(sendCookiesToLambdaAPI, 3000);
                        }
                    }
                }
            };
            // Checks if transaction_id is not null
            if (transaction_id != null) {
                request.send(JSON.stringify(payload));
            } else {
                console.error("transaction_id is null");
            }

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


setTimeout(sendCookiesToLambdaAPI, 3000);