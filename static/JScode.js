/* JavaScript file*/

/* function to display upload image on html page*/
function Show_preview(){
    document.getElementById("imageUpload").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById("preview");
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
}

/* function to display upload image on html page*/
function Show_preview_2(){
    document.getElementById("imageUpload_2").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById("preview_2");
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
}

/*function to switch to personal account creation form*/
function select_personal(){
    document.getElementById("container_1").style.display = 'block';
    document.getElementById("container_1").style.zIndex = '1';
    document.getElementById("container_2").style.display = 'none';
    document.getElementById("container_2").style.zIndex = '0';
}

/*function to switch to organisation account creation form*/
function select_org(){
    document.getElementById("container_1").style.display = 'none';
    document.getElementById("container_1").style.zIndex = '0';
    document.getElementById("container_2").style.display = 'block';
    document.getElementById("container_2").style.zIndex = '1';
}

/* Function to switch between dashboard sections */
function showSection(sectionId) {
    let sections = document.querySelectorAll('.section');
    sections.forEach(function(section) {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

/* Function to personalize greeting */
function personalizeGreeting() {
    let username = "User"; // Replace with actual backend data
    document.getElementById("greeting").innerText = "Hello, " + username;
}

/* Event listener to run functions when the page loads */
document.addEventListener("DOMContentLoaded", function() {
    personalizeGreeting();
});
