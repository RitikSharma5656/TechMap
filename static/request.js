const REQUEST_METHOD = {
    POST: "POST",
    GET: "GET",
    DELETE: "DELETE",
    PUT: "PUT"
};

function makeServerRequest(requestURL, requestMethod, data, callBackFunction, onErrorEvent) {
    let requestParams = {
        method: requestMethod,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: data
    };
    fetch(requestURL, requestParams)
        .then(function(response) {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                if (onErrorEvent) {
                    onErrorEvent(response)
                }
            }
        })
        .then(function(responseJSON) {
            if (responseJSON !== undefined) {
                callBackFunction(JSON.stringify(responseJSON));
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}