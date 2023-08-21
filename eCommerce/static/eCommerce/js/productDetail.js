  
    const addToCartBtn = document.getElementById('addToCartBtn');
    addToCartBtn.addEventListener('click', addToCart);
    const notification = document.getElementById('alert');
    function addToCart() {
        const product_id = {{ product.id }};
        const csrf_token = '{{ csrf_token }}';

        fetch('/add_to_cart/' + product_id + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
              
              notification.style.display = 'block';
              notification.style.opacity = '1';
              setTimeout(() => {
                  hideNotification();
              }, 4000); // Hide after 6 seconds
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    function hideNotification() {
    const notification = document.getElementById('alert');
    notification.style.opacity = '0';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 300); // Fade out transition time
}
