var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
        base: {
            color: '#2c3e50',
            fontFamily: '"Roboto", sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#95a5a6'
            }
        },
        invalid: {
            color: '#e74c3c',
            iconColor: '#e74c3c'
        }
};

var card = elements.create('card', {style: style});
card.mount('#card-element');