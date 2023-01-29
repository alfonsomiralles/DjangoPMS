document.querySelector('.plus-button').addEventListener('click', function() {
    // logic to show a modal and collect the input values
    var customCity = document.querySelector('#custom_city').value;
    var customCountry = document.querySelector('#custom_country').value;

    // assign the values to the hidden inputs
    document.querySelector('#id_custom_city').value = customCity;
    document.querySelector('#id_custom_country').value = customCountry;
});