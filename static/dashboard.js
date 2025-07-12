// This function runs when the entire HTML page is loaded
document.addEventListener('DOMContentLoaded', function () {

    // Fetch data from our Flask API
    fetch('/api/laptops')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                console.error("API returned no data.");
                return;
            }

            console.log("Data received from API:", data);

            // Process the data for our charts
            const brandData = processBrandData(data);
            const ratingData = processRatingData(data);

            // Create the charts
            createBrandChart(brandData.brands, brandData.counts);
            createPriceChart(brandData.brands, brandData.avgPrices);
            createRatingChart(Object.keys(ratingData), Object.values(ratingData));
        })
        .catch(error => console.error('Error fetching or processing data:', error));

});

/**
 * Processes raw laptop data to calculate count and average price per brand.
 * @param {Array} data - The array of laptop objects from the API.
 * @returns {Object} - An object containing lists of brands, counts, and average prices.
 */
function processBrandData(data) {
    const brandStats = {};

    data.forEach(laptop => {
        // Extract brand name from the full name (e.g., "HP", "Dell", "Lenovo")
        const brand = laptop.Name.split(' ')[0].toUpperCase();

        if (!brandStats[brand]) {
            brandStats[brand] = { count: 0, total_price: 0, prices: [] };
        }

        brandStats[brand].count += 1;
        brandStats[brand].prices.push(laptop.Price);
    });

    // Calculate average price for each brand
    for (const brand in brandStats) {
        const sum = brandStats[brand].prices.reduce((a, b) => a + b, 0);
        brandStats[brand].avg_price = Math.round(sum / brandStats[brand].count);
    }

    const sortedBrands = Object.keys(brandStats).sort((a, b) => brandStats[b].count - brandStats[a].count);

    const brands = sortedBrands;
    const counts = sortedBrands.map(brand => brandStats[brand].count);
    const avgPrices = sortedBrands.map(brand => brandStats[brand].avg_price);

    return { brands, counts, avgPrices };
}

/**
 * Processes raw laptop data to group laptops by their rating.
 * @param {Array} data - The array of laptop objects from the API.
 * @returns {Object} - An object where keys are rating ranges and values are counts.
 */
function processRatingData(data) {
    const ratingGroups = {
        "4.5+ (Excellent)": 0,
        "4.0 - 4.4 (Very Good)": 0,
        "3.5 - 3.9 (Good)": 0,
        "< 3.5 (Average)": 0,
        "Not Rated": 0
    };

    data.forEach(laptop => {
        const rating = laptop.Rating;
        if (rating === null || rating === 'N/A') {
            ratingGroups["Not Rated"]++;
        } else if (rating >= 4.5) {
            ratingGroups["4.5+ (Excellent)"]++;
        } else if (rating >= 4.0) {
            ratingGroups["4.0 - 4.4 (Very Good)"]++;
        } else if (rating >= 3.5) {
            ratingGroups["3.5 - 3.9 (Good)"]++;
        } else {
            ratingGroups["< 3.5 (Average)"]++;
        }
    });
    return ratingGroups;
}

// --- Chart Creation Functions ---

function createBrandChart(labels, data) {
    const ctx = document.getElementById('brandChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut', // Type of chart
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Laptops',
                data: data,
                backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6610f2'],
            }]
        }
    });
}

function createPriceChart(labels, data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar', // Type of chart
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Price (in ₹)',
                data: data,
                backgroundColor: '#17a2b8',
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function createRatingChart(labels, data) {
    const ctx = document.getElementById('ratingChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar', // Type of chart
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Laptops',
                data: data,
                backgroundColor: ['#28a745', '#ffc107', '#fd7e14', '#dc3545', '#6c757d'],
            }]
        },
        options: {
            indexAxis: 'y', // Makes the bar chart horizontal
        }
    });
}