document.addEventListener("DOMContentLoaded", () => {

    checkAuthentication();

    // LOGIN PAGE
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            await loginUser(email, password);
        });
    }

    const reviewForm = document.getElementById("review-form");

    if (reviewForm) {
        const token = getCookie("token");

        if (!token) {
            window.location.href = "index.html";
            return;
        }

        reviewForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const placeId = getPlaceIdFromURL();

            const reviewText =
                document.getElementById("review-text").value;

            const rating =
                document.getElementById("rating").value;

            await submitReview(
                token,
                placeId,
                reviewText,
                rating
            );
        });
    }

    // INDEX PAGE PRICE FILTER
    const priceFilter = document.getElementById("price-filter");

    if (priceFilter) {
        priceFilter.addEventListener("change", () => {
            filterPlaces();
        });
    }

    // PLACE DETAILS PAGE
    const placeDetails = document.getElementById("place-details");

    if (placeDetails) {

        const placeId = getPlaceIdFromURL();
        const token = getCookie("token");

        const addReviewSection =
            document.getElementById("add-review");

        if (addReviewSection) {

            if (token) {

                addReviewSection.style.display = "block";

                const reviewLink =
                    document.getElementById("review-link");

                if (reviewLink) {
                    reviewLink.href =
                        `add_review.html?id=${placeId}`;
                }

            } else {
                addReviewSection.style.display = "none";
            }
        }

        fetchPlaceDetails(token, placeId);
    }
});


/* ==========================
   COOKIES
========================== */

function getCookie(name) {

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }

    return null;
}


/* ==========================
   AUTHENTICATION
========================== */

function checkAuthentication() {

    const token = getCookie("token");

    const loginLink =
        document.getElementById("login-link");

    if (loginLink) {

        if (token) {
            loginLink.style.display = "none";
        } else {
            loginLink.style.display = "block";
        }
    }

    if (document.getElementById("places-list")) {
        fetchPlaces(token);
    }
}


async function loginUser(email, password) {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/v1/auth/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            document.cookie =
                `token=${data.access_token}; path=/`;

            window.location.href = "index.html";

        } else {

            alert(
                data.error || "Login failed"
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to API"
        );
    }
}


/* ==========================
   PLACES LIST
========================== */

let allPlaces = [];


async function fetchPlaces(token) {

    try {

        const headers = {
            "Content-Type": "application/json"
        };

        if (token) {
            headers["Authorization"] =
                `Bearer ${token}`;
        }

        const response = await fetch(
            "http://127.0.0.1:5000/api/v1/places/",
            {
                method: "GET",
                headers
            }
        );

        if (!response.ok) {
            throw new Error(
                "Failed to fetch places"
            );
        }

        allPlaces = await response.json();

        displayPlaces(allPlaces);

    } catch (error) {

        console.error(error);
    }
}


function displayPlaces(places) {

    const placesList =
        document.getElementById("places-list");

    if (!placesList) return;

    placesList.innerHTML = "";

    places.forEach(place => {

        const card =
            document.createElement("div");

        card.className = "place-card";

        card.setAttribute(
            "data-price",
            place.price || 0
        );

        card.innerHTML = `
            <h3>${place.title}</h3>

            <p>
                Price per night:
                $${place.price}
            </p>

            <a
                href="place.html?id=${place.id}"
                class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(card);
    });
}


/* ==========================
   PRICE FILTER
========================== */

function filterPlaces() {

    const filter =
        document.getElementById("price-filter");

    if (!filter) return;

    const maxPrice = filter.value;

    const cards =
        document.querySelectorAll(
            ".place-card"
        );

    cards.forEach(card => {

        const price =
            parseFloat(card.dataset.price);

        if (
            maxPrice === "All" ||
            price <= parseFloat(maxPrice)
        ) {

            card.style.display = "block";

        } else {

            card.style.display = "none";
        }
    });
}

/* ==========================
   ADD REVIEW
========================== */

async function submitReview(
    token,
    placeId,
    reviewText,
    rating
) {
    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/v1/reviews/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: Number(rating),
                    place_id: placeId
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            alert("Review submitted successfully!");

            document
                .getElementById("review-form")
                .reset();

            window.location.href =
                `place.html?id=${placeId}`;

        } else {

            alert(
                data.error ||
                "Failed to submit review"
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to API"
        );
    }
}


/* ==========================
   PLACE DETAILS
========================== */

function getPlaceIdFromURL() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    return params.get("id");
}


async function fetchPlaceDetails(
    token,
    placeId
) {

    try {

        const headers = {
            "Content-Type": "application/json"
        };

        if (token) {
            headers["Authorization"] =
                `Bearer ${token}`;
        }

        const response = await fetch(
            `http://127.0.0.1:5000/api/v1/places/${placeId}`,
            {
                method: "GET",
                headers
            }
        );

        if (!response.ok) {
            throw new Error(
                "Failed to fetch place details"
            );
        }

        const place =
            await response.json();

        displayPlaceDetails(place);

    } catch (error) {

        console.error(error);
    }
}


function displayPlaceDetails(place) {

    const section =
        document.getElementById(
            "place-details"
        );

    if (!section) return;

    const amenities =
        place.amenities || [];

    const reviews =
        place.reviews || [];

    section.innerHTML = `
        <div class="place-details">

            <h2>${place.title}</h2>

            <div class="place-info">

                <p>
                    <strong>Description:</strong>
                    ${place.description || ""}
                </p>

                <p>
                    <strong>Price:</strong>
                    $${place.price}
                </p>

                <p>
                    <strong>Owner:</strong>
                    ${place.owner || ""}
                </p>

            </div>

            <h3>Amenities</h3>

            <ul>
                ${amenities.map(a =>
                    `<li>${a.name || a}</li>`
                ).join("")}
            </ul>

            <h3>Reviews</h3>

            <div>

                ${
                    reviews.length > 0
                    ?
                    reviews.map(review => `
                        <div class="review-card">
                            <p>${review.text}</p>
                            <p>
                                Rating:
                                ${review.rating}
                            </p>
                        </div>
                    `).join("")
                    :
                    "<p>No reviews yet.</p>"
                }

            </div>

        </div>
    `;
}
