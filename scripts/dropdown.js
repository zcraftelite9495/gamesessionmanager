// scripts/dropdown.js
// Script Purpose: Add arrow to dropdown menus
// Description: Uses a query selector to search for dropdown menus and add an arrow to the end of them to signify that they are a dropdown.
document.addEventListener("click", function(e) {
    const dropdown = document.querySelector(".nav-dropdown");
    if (!dropdown.contains(e.target)) {
        const dropdownContent = document.querySelector(".nav-dropdown-content");
        dropdownContent.classList.remove("show");
        document.querySelector(".nav-dropbtn").classList.remove("up-arrow");
    }
});

document.querySelector(".nav-dropbtn").addEventListener("click", function() {
    const dropdownContent = document.querySelector(".nav-dropdown-content");
    dropdownContent.classList.toggle("show");
    document.querySelector(".nav-dropbtn").classList.toggle("up-arrow");
});
