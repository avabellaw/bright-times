// Code from Stripe has been taken and modified in this file
// [https://docs.stripe.com/payments/quickstart]

// This is your test publishable API key.
const pub_key = document.getElementById("stripe_pub_key").value;
const stripe = Stripe(pub_key);
let csrf = $("input[name='csrfmiddlewaretoken']").val();
const event_id = document.getElementById("event_id").value;
const form = document.getElementById("payment-form");
const return_url = `${window.location.protocol}//${window.location.host}${document.getElementById("return-url").value}`;

// The items the customer wants to buy
const items = [{ id: event_id }];

let elements;

initialize();
checkStatus();

form.addEventListener("submit", handleSubmit);

// Fetches a payment intent and captures the client secret
async function initialize() {
    setLoading(true);
    const response = await fetch("/tickets/create-payment-intent/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
        },
        body: JSON.stringify({ items })
    });
    const { clientSecret } = await response.json();

    const appearance = {
        theme: "stripe"
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElementOptions = {
        layout: "tabs"
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.on("ready", function() {
            setLoading(false);
      });
    paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: return_url
        }
    });

    // User will only get to this point if payment not successful
    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }

    setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        "payment_intent_client_secret"
    );

    if (!clientSecret) {
        return;
    }

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
        case "succeeded":
            showMessage("Payment succeeded!");
            break;
        case "processing":
            showMessage("Your payment is processing.");
            break;
        case "requires_payment_method":
            showMessage("Your payment was not successful, please try again.");
            break;
        default:
            showMessage("Something went wrong.");
    }
}

// ------- UI helpers -------

function showMessage(messageText) {
    const messageContainer = document.querySelector("#payment-message");

    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;

    setTimeout(function () {
        messageContainer.classList.add("hidden");
        messageContainer.textContent = "";
    }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("#submit").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#submit").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}