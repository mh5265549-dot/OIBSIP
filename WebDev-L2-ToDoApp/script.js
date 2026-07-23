document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const pendingList = document.getElementById('pendingList');
    const completedList = document.getElementById('completedList');
    const pendingCount = document.getElementById('pendingCount');
    const completedCount = document.getElementById('completedCount');
    const pendingEmpty = document.getElementById('pendingEmpty');
    const completedEmpty = document.getElementById('completedEmpty');

    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    function saveAndRender() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
        renderTasks();
    }

    function addTask() {
        const text = taskInput.value.trim();
        if (text === '') return;

        const newTask = {
            id: Date.now(),
            text: text,
            completed: false,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        tasks.push(newTask);
        taskInput.value = '';
        saveAndRender();
    }

    function toggleTaskStatus(id) {
        tasks = tasks.map(task => {
            if (task.id === id) {
                return { ...task, completed: !task.completed };
            }
            return task;
        });
        saveAndRender();
    }

    function deleteTask(id) {
        tasks = tasks.filter(task => task.id !== id);
        saveAndRender();
    }

    function editTask(id, liElement) {
        const taskObj = tasks.find(t => t.id === id);
        const textRow = liElement.querySelector('.task-content-row');
        const currentText = taskObj.text;

        textRow.innerHTML = `
            <input type="text" class="edit-input" value="${currentText}" style="flex:1; padding:4px 8px; font-size:14px; border:1px solid #ccc; border-radius:4px;">
            <button class="btn-save" style="background:#0284c7; color:white; border:none; padding:4px 8px; border-radius:4px; margin-left:5px; cursor:pointer;">Save</button>
        `;

        const editInput = textRow.querySelector('.edit-input');
        editInput.focus();

        textRow.querySelector('.btn-save').addEventListener('click', () => {
            const updatedText = editInput.value.trim();
            if (updatedText !== '') {
                taskObj.text = updatedText;
                saveAndRender();
            }
        });

        editInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const updatedText = editInput.value.trim();
                if (updatedText !== '') {
                    taskObj.text = updatedText;
                    saveAndRender();
                }
            }
        });
    }

    function renderTasks() {
        pendingList.innerHTML = '';
        completedList.innerHTML = '';

        const pendingTasks = tasks.filter(t => !t.completed);
        const completedTasks = tasks.filter(t => t.completed);

        pendingCount.textContent = `${pendingTasks.length} pending`;
        completedCount.textContent = `${completedTasks.length} completed`;

        if (pendingTasks.length === 0) {
            pendingEmpty.classList.remove('hidden');
        } else {
            pendingEmpty.classList.add('hidden');
            pendingTasks.forEach(task => appendTaskDOM(task, pendingList));
        }

        if (completedTasks.length === 0) {
            completedEmpty.classList.remove('hidden');
        } else {
            completedEmpty.classList.add('hidden');
            completedTasks.forEach(task => appendTaskDOM(task, completedList));
        }
    }

    function appendTaskDOM(task, listElement) {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        li.dataset.id = task.id;

        li.innerHTML = `
            <div class="task-content-row">
                <span class="task-text">${escapeHTML(task.text)}</span>
                <div class="task-actions">
                    <button class="btn-complete">${task.completed ? 'Undo' : 'Complete'}</button>
                    ${!task.completed ? '<button class="btn-edit">Edit</button>' : ''}
                    <button class="btn-delete">Delete</button>
                </div>
            </div>
            <span class="task-timestamp">Added at: ${task.timestamp}</span>
        `;

        li.querySelector('.btn-complete').addEventListener('click', () => toggleTaskStatus(task.id));
        li.querySelector('.btn-delete').addEventListener('click', () => deleteTask(task.id));
        
        const editBtn = li.querySelector('.btn-edit');
        if (editBtn) {
            editBtn.addEventListener('click', () => editTask(task.id, li));
        }

        listElement.appendChild(li);
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
        );
    }

    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });

    renderTasks();
});
