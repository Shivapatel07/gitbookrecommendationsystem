
// Wait until the webpage is completely loaded
document.addEventListener("DOMContentLoaded", function () {

    // Get elements from the HTML page
    const searchForm = document.querySelector(".search-form");
    const searchInput = document.querySelector(
        'input[name="book_name"]'
    );

    const searchButton = document.querySelector(
        ".search-form button"
    );


    


    if (searchForm) {

        searchForm.addEventListener("submit", function (event) {

            const bookName = searchInput.value.trim();

            // Check whether the user entered a book name
            if (bookName === "") {

                event.preventDefault();

                alert("Please enter a book name.");

                searchInput.focus();

                return;
            }

            // Show loading message
            if (searchButton) {
                searchButton.textContent = "Searching...";
                searchButton.disabled = true;
            }
        });
    }



    const clearButton = document.querySelector("#clear-search");

    if (clearButton) {

        clearButton.addEventListener("click", function () {

            searchInput.value = "";

            searchInput.focus();
        });
    }



    const bookCards = document.querySelectorAll(".book-card");

    bookCards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            card.classList.add("active");
        });

        card.addEventListener("mouseleave", function () {
            card.classList.remove("active");
        });

    });

    const detailButtons =
        document.querySelectorAll(".book-details");

    detailButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const title = button.dataset.title;
            const author = button.dataset.author;

            alert(
                "Book: " + title +
                "\nAuthor: " + author
            );

        });

    });



    const loginForm = document.querySelector("#login-form");

    if (loginForm) {

        loginForm.addEventListener("submit", function (event) {

            const username =
                document.querySelector("#username");

            const password =
                document.querySelector("#password");


            if (username.value.trim() === "") {

                event.preventDefault();

                alert("Please enter your username.");

                username.focus();

                return;
            }


            if (password.value.trim() === "") {

                event.preventDefault();

                alert("Please enter your password.");

                password.focus();

                return;
            }

        });

    }

    const signupForm =
        document.querySelector("#signup-form");

    if (signupForm) {

        signupForm.addEventListener("submit", function (event) {

            const username =
                document.querySelector("#username");
            const password =
                document.querySelector("#password");

            const confirmPassword =
                document.querySelector("#confirm-password");


            if (username.value.trim() === "") {

                event.preventDefault();

                alert("Please enter a username.");

                username.focus();

                return;
            }


            if (password.value.length < 6) {

                event.preventDefault();

                alert(
                    "Password must contain at least 6 characters."
                );

                password.focus();

                return;
            }


            if (password.value !== confirmPassword.value) {

                event.preventDefault();

                alert("Passwords do not match.");

                confirmPassword.focus();

                return;
            }

        });

    }




    if (searchInput) {

        searchInput.addEventListener("keypress", function (event) {

            if (event.key === "Enter") {
                searchForm.submit();

            }

        });

    }

    const recommendationSection =
        document.querySelector(".recommendations");

    if (recommendationSection) {

        setTimeout(function () {

            recommendationSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 300);

    }

    const yearElement =
        document.querySelector("#current-year");
    if (yearElement) {

        yearElement.textContent =
            new Date().getFullYear();
    }
});
