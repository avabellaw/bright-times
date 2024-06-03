document.addEventListener("DOMContentLoaded", function() {

    let price = parseFloat(document.getElementById("ticket-price").textContent);
    document.getElementById("total-cost").innerText = price;
    const errorMessage = document.getElementById("error-message");

    document.getElementById("quantity").addEventListener("change", function() {

        let quantity = document.getElementById("quantity");
        if (quantity.value < 1) {
            document.getElementById("quantity").value = 1;
            errorMessage.innerText = "You must buy at least one ticket";
        } else if (quantity.value > 10) {
            document.getElementById("quantity").value = 10;
            errorMessage.innerText = "You can only buy up" +
                                     "to 10 tickets per user.";
        } else {
            errorMessage.innerText = "";
        }

        quantity = document.getElementById("quantity").value;

        price = parseFloat(document.getElementById("ticket-price").textContent);
        let total = quantity * price;
        document.getElementById("total-cost").innerText = total;
    });
});