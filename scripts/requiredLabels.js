// scripts/required-labels.js
// Script Purpose: Add a red "*" at the end of each label for a required input
// Description: Adds a red "*" at the end of each label for required inputs, and ensures that if there is a ":" at the end, that the "*" appears before it.
document.querySelectorAll('input[required]').forEach(input => {
    const label = document.querySelector(`label[for="${input.id}"]`);
    if (label) {
        // Check if the label ends with a colon
        if (label.textContent.trim().endsWith(':')) {
            // Insert the asterisk before the colon
            label.innerHTML = label.textContent.trim().slice(0, -1) + 
                '<span style="color: red;">*</span>:';
        } else {
            // Append the asterisk at the end
            label.innerHTML = label.textContent.trim() + '<span style="color: red;">*</span>';
        }
    }
});
