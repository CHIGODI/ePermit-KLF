
let headers = new Headers();
headers.append("Content-Type", "application/json");
headers.append("Authorization", "Bearer AmYqGXO8AjHJkwRfmGKuhx8GxPYf");

fetch("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", {
    method: 'POST',
    headers,
    body: JSON.stringify({
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwNDMwMTQwNjMz",
        "Timestamp": "20240430140633",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708051357,
        "PartyB": 174379,
        "PhoneNumber": 254708051357,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    })
})
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log(error));