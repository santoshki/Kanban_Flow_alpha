document.addEventListener('DOMContentLoaded', () => { const navButtons = document.querySelectorAll('.nav-button');
 const containers = document.querySelectorAll('.container');

 // Show only the container with the given id
 function showContainer(id) {
 containers.forEach(c => {
 c.classList.toggle('visible', c.id === id);
 });
 }

 // Navigation button click handler
 navButtons.forEach(btn => {
 btn.addEventListener('click', () => {
 navButtons.forEach(b => b.classList.remove('active'));
 btn.classList.add('active');

 const target = btn.getAttribute('data-target');
 if (target) {
 showContainer(target);
 }
 });
 });

 // Initially activate Home container and button
 const homeBtn = document.querySelector('.nav-button[data-target="home-container"]');
 if (homeBtn) {
 homeBtn.classList.add('active');
 }
 showContainer('home-container');

 const projectsBtn = document.querySelector('.nav-button[data-target="projects-container"]');
 const newProjectBtn = document.getElementById('new-project-button');
 const newProjectContainer = document.getElementById('new-project-container');
 const cancelNewProjectBtn = document.getElementById('cancel-new-project');
 const newProjectForm = document.getElementById('new-project-form');

 // When New Project button clicked: show new project container & deactivate nav buttons
 newProjectBtn.addEventListener('click', () => {
 showContainer('new-project-container');
 navButtons.forEach(btn => btn.classList.remove('active'));
 });

 // Cancel new project, return to projects container with nav active
 cancelNewProjectBtn.addEventListener('click', () => {
 showContainer('projects-container');
 if (projectsBtn) {
 navButtons.forEach(btn => btn.classList.remove('active'));
 projectsBtn.classList.add('active');
 }
 });

 // On submit, show projects container and reset form
 newProjectForm.addEventListener('submit', e => {
 e.preventDefault();
 alert(`Project "${newProjectForm['project-name'].value}" created!`);
 newProjectForm.reset();
 showContainer('projects-container');
 if (projectsBtn) {
 navButtons.forEach(btn => btn.classList.remove('active'));
 projectsBtn.classList.add('active');
 }
 });

 // Drag and Drop handlers
 window.allowDrop = ev => ev.preventDefault();

 window.drag = ev => {
 ev.dataTransfer.setData('text', ev.target.id);
 ev.target.classList.add('dragging');
 };

 window.drop = ev => {
 ev.preventDefault();
 const data = ev.dataTransfer.getData('text');
 const task = document.getElementById(data);
 const column = ev.target.closest('.column');
 if (column && task) {
 column.appendChild(task);
 task.classList.remove('dragging');
 }
 };

 // Bind drag and drop events dynamically on tasks and columns
 function bindDragDrop() {
 document.querySelectorAll('.task').forEach(task => {
 task.setAttribute('draggable', 'true');
 task.removeEventListener('dragstart', window.drag);
 task.addEventListener('dragstart', window.drag);
 });

 document.querySelectorAll('.column').forEach(col => {
 col.removeEventListener('dragover', window.allowDrop);
 col.removeEventListener('drop', window.drop);
 col.addEventListener('dragover', window.allowDrop);
 col.addEventListener('drop', window.drop);
 });
 }

 // Bind drag/drop handlers initially
 bindDragDrop();
});

