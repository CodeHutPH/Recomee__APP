function validate_input_courses() {
    var selectElement = document.getElementById('courses');
    var selectedValue = selectElement.value;
    var alertBox = document.getElementById('course_alert');

    if (selectedValue === "") {
        alertBox.style.display = 'block';
        return false;
    }

    // If validation passes, proceed to next section or action
    // For example, you can navigate to the next section using anchor link
    window.location.href = "#section-two";
}

function validate_input_skills() {
    var selectElement = document.getElementById('skills');
    var selectedValue = selectElement.value;
    var alertBox = document.getElementById('skill_alert');

    if (selectedValue === "") {
        alertBox.style.display = 'block';
        return false;
    }

    // If validation passes, proceed to next section or action
    // For example, you can navigate to the next section using anchor link
    window.location.href = "#section-three";
}

function validate_input_interests() {
    var selectElement = document.getElementById('interests');
    var selectedValue = selectElement.value;
    var alertBox = document.getElementById('interest_alert');

    if (selectedValue === "") {
        alertBox.style.display = 'block';
        return false;
    }

    // If validation passes, proceed to next section or action
    // For example, you can navigate to the next section using anchor link
    window.location.href = "#section-four";
}

window.onload = function() {
    window.scrollTo(0, 0);
  };

  // Smooth scroll to the top when clicking "Back to top" link
document.getElementById('back_to_top_link').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior

    // Scroll to the top of the page smoothly
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

