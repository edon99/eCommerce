

function changeTab(tabIndex) {
    var tabs = document.getElementsByClassName('tab');
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove('active');
    }
    tabs[tabIndex].classList.add('active');
    
    // Store the active tab index in session storage
    sessionStorage.setItem('activeTabIndex', tabIndex);
  }

  // Retrieve the active tab index from session storage
  var activeTabIndex = sessionStorage.getItem('activeTabIndex');
  if (activeTabIndex !== null) {
    // Set the corresponding tab as active
    var tabs = document.getElementsByClassName('tab');
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove('active');
    }
    tabs[activeTabIndex].classList.add('active');
  }

  const productData = {
    labels: [
      {% for product in top_products %}
      "{{ product.title }}",
      {% endfor %}
    ],
    datasets: [
      {
        label: 'Number of Orders',
        data: [
          {% for product in top_products %}
          {{ product.order_count }},
          {% endfor %}
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }
    ]
  };

  const ctx = document.getElementById('productChart').getContext('2d');
  const productChart = new Chart(ctx, {
    type: 'bar',
    data: productData,
    options: {
      scales: {
        y: {
          beginAtZero: true,
          precision: 0
        }
      }
    }
  });

  const orderData = {
    labels: [
      {% for category in order_distribution_by_category %}
      "{{ category.product__categorie }}",
      {% endfor %}
    ],
    datasets: [
      {
        label: 'Order Count',
        data: [
          {% for category in order_distribution_by_category %}
          {{ category.order_count }},
          {% endfor %}
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }
    ]
  };

  const ctx2 = document.getElementById('orderChart').getContext('2d');
  const orderChart = new Chart(ctx2, {
    type: 'bar',
    data: orderData,
    options: {
      scales: {
        y: {
          beginAtZero: true,
          precision: 0
        }
      }
    }
  });
  const salesData = {
labels: [
  {% for month in best_selling_months %}
    "{{ month.month }}",
  {% endfor %}
],
datasets: [
  {
    label: 'Total Sales',
    data: [
      {% for month in best_selling_months %}
        {{ month.total_sales }},
      {% endfor %}
    ],
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 1
  }
]
};

const ctx3 = document.getElementById('salesChart').getContext('2d');
const salesChart = new Chart(ctx3, {
type: 'bar',
data: salesData,
options: {
  scales: {
    y: {
      beginAtZero: true,
      precision: 0
    }
  }
}
});
