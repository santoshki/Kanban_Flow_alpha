document.addEventListener('DOMContentLoaded', function() {
    var projectsMenu = document.getElementById('projects-menu');
    var projectsContainer = document.getElementById('projects-container');

    projectsMenu.addEventListener('click', function() {
        if (projectsContainer.classList.contains('visible')) {
            projectsContainer.classList.remove('visible');
        } else {
            projectsContainer.classList.add('visible');
        }
    });
});
