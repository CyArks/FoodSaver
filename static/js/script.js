// Include this script in your HTML files like this:
// <script src="{{ url_for('static', filename='js/script.js') }}"></script>

// Define variables
let mobileMenuButton = document.querySelector("#mobile-menu-button");
let mobileMenu = document.querySelector("#mobile-menu");

// Toggle Mobile Menu
mobileMenuButton.addEventListener("click", function() {
    mobileMenu.classList.toggle("hidden");
});

// Adaptive JavaScript based on screen size
window.addEventListener("resize", function() {
    let width = window.innerWidth;

    if (width > 768) {
        // Code for larger screens
        mobileMenu.classList.add("hidden");
    } else {
        // Code for mobile screens
    }
});

// Function to dynamically update some content, just as an example
function updateContent() {
    let contentElement = document.querySelector("#dynamic-content");
    let newContent = "Updated content here";
    contentElement.textContent = newContent;
}

// Call function to update content
updateContent();
