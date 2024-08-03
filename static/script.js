document.addEventListener('DOMContentLoaded', function () {
    const homeMenu = document.getElementById('home-menu');
    const projectsMenu = document.getElementById('projects-menu');
    const welcomeMessage = document.getElementById('welcome-message');
    const projectsContainer = document.getElementById('projects-container');
    const homepageContent = document.getElementById('homepage-content');

    homeMenu.addEventListener('click', function () {
        welcomeMessage.classList.add('visible');
        projectsContainer.classList.remove('visible');
        homepageContent.classList.remove('visible');
    });

    projectsMenu.addEventListener('click', function () {
        welcomeMessage.classList.remove('visible');
        projectsContainer.classList.add('visible');
        homepageContent.classList.remove('visible');
    });

    // Initially show the welcome message
    welcomeMessage.classList.add('visible');
    projectsContainer.classList.remove('visible');
    homepageContent.classList.remove('visible');
});
