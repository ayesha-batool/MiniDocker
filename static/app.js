// Socket.IO connection
const socket = io();

let selectedContainers = new Set();
let containers = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadContainers();
    setupSocketListeners();
    setInterval(loadContainers, 2000); // Refresh every 2 seconds
});

// Socket listeners
function setupSocketListeners() {
    socket.on('container_created', (data) => {
        loadContainers();
        switchTab('manage');
        showNotification('Container created successfully!', 'success');
    });

    socket.on('container_updated', (data) => {
        loadContainers();
    });

    socket.on('container_deleted', (data) => {
        loadContainers();
        selectedContainers.clear();
        updateButtonStates();
    });

    socket.on('container_started', (data) => {
        loadContainers();
        if (data.status === 'success') {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
        updateButtonStates();
    });

    socket.on('status_update', (data) => {
        updateContainerStatus(data.name, data.status);
    });

    socket.on('log_update', (data) => {
        // Update log in table if visible
        const row = document.querySelector(`tr[data-name="${data.name}"]`);
        if (row) {
            const logCell = row.querySelector('.latest-log');
            if (logCell) {
                const logText = data.message.length > 50 ? data.message.substring(0, 47) + '...' : data.message;
                logCell.textContent = logText;
            }
        }
    });
}

// Tab switching
function switchTab(tab) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(`${tab}-tab`).classList.add('active');
    document.querySelectorAll('.tab-btn')[tab === 'create' ? 0 : 1].classList.add('active');
    
    if (tab === 'manage') {
        loadContainers();
    }
}

// Load containers
async function loadContainers() {
    try {
        const response = await fetch('/api/containers');
        containers = await response.json();
        renderContainers();
    } catch (error) {
        console.error('Error loading containers:', error);
    }
}

// Render containers table
function renderContainers() {
    const tbody = document.getElementById('containers-tbody');
    
    if (containers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="11" class="empty-state">No containers found. Create one to get started!</td></tr>';
        return;
    }
    
    tbody.innerHTML = containers.map(container => `
        <tr data-name="${container.name}" class="${container.status.toLowerCase()}">
            <td><input type="checkbox" class="container-checkbox" value="${container.name}" onchange="toggleContainer('${container.name}')"></td>
            <td><strong>${container.name}</strong><br><small style="color: #64748b;">${container.id}</small></td>
            <td>${escapeHtml(container.command)}</td>
            <td><span class="status-badge-table status-${container.status.toLowerCase()}">${container.status}</span></td>
            <td>${container.pid}</td>
            <td>${container.uptime}</td>
            <td>${container.resources}</td>
            <td class="latest-log">${escapeHtml(container.latest_log)}</td>
            <td>${container.last_started}</td>
            <td>${container.cpu}</td>
            <td class="action-buttons">
                <button class="action-btn delete" onclick="deleteContainer('${container.name}')" title="Delete">🗑️</button>
                <button class="action-btn" onclick="showContainerMenu(event, '${container.name}')" title="Menu">⋮</button>
            </td>
        </tr>
    `).join('');
    
    updateButtonStates();
}

// Create container
async function createContainer(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('container-name').value,
        command: document.getElementById('container-command').value,
        mem_limit: parseInt(document.getElementById('mem-limit').value),
        cpu_limit: parseInt(document.getElementById('cpu-limit').value),
        volumes: getVolumes(),
        env_vars: getEnvVars()
    };
    
    try {
        const response = await fetch('/api/containers', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        if (response.ok) {
            document.getElementById('container-form').reset();
            document.getElementById('advanced-options').style.display = 'none';
            showNotification('Container created successfully!', 'success');
        } else {
            showNotification(data.error || 'Failed to create container', 'error');
        }
    } catch (error) {
        showNotification('Error creating container: ' + error.message, 'error');
    }
}

// Container actions
async function containerAction(name, action) {
    try {
        const response = await fetch(`/api/containers/${name}/${action}`, {method: 'POST'});
        const data = await response.json();
        if (response.ok) {
            loadContainers();
            // For start action, wait for delayed notification from server
            if (action !== 'start') {
                showNotification(`Container ${action}ed successfully`, 'success');
            }
        } else {
            showNotification(data.error || `Failed to ${action} container`, 'error');
        }
    } catch (error) {
        showNotification(`Error ${action}ing container: ${error.message}`, 'error');
    }
}

// Bulk actions
function bulkAction(action) {
    const selected = Array.from(selectedContainers);
    if (selected.length === 0) {
        showNotification('Please select at least one container', 'warning');
        return;
    }
    
    if (action === 'delete') {
        showConfirmModal(
            'Delete Containers',
            `Are you sure you want to delete ${selected.length} container(s)? This action cannot be undone.`,
            () => {
                selected.forEach(name => deleteContainer(name));
            }
        );
        return;
    }
    
    selected.forEach(name => {
        if (action === 'delete') {
            deleteContainer(name);
        } else {
            containerAction(name, action);
        }
    });
}

// Delete container
async function deleteContainer(name) {
    showConfirmModal(
        'Delete Container',
        `Are you sure you want to delete container '${name}'? This action cannot be undone.`,
        async () => {
            try {
                const response = await fetch(`/api/containers/${name}`, {method: 'DELETE'});
                const data = await response.json();
                if (response.ok) {
                    loadContainers();
                    showNotification('Container deleted successfully', 'success');
                } else {
                    showNotification(data.error || 'Failed to delete container', 'error');
                }
            } catch (error) {
                showNotification('Error deleting container: ' + error.message, 'error');
            }
        }
    );
}

// View logs
async function viewLogs(containerName = null) {
    // If containerName is provided, use it directly; otherwise get from selection
    let name = containerName;
    if (!name) {
        const selected = Array.from(selectedContainers);
        if (selected.length === 0) {
            showNotification('Please select a container', 'warning');
            return;
        }
        name = selected[0];
    }
    
    // Verify container exists in current containers list
    const container = containers.find(c => c.name === name);
    if (!container) {
        showNotification(`Container '${name}' not found`, 'error');
        return;
    }
    
    try {
        // Use encodeURIComponent to handle special characters in container name
        const response = await fetch(`/api/containers/${encodeURIComponent(name)}/logs`);
        const data = await response.json();
        if (response.ok) {
            document.getElementById('logs-title').textContent = `📄 Logs: ${name} (${container.id})`;
            document.getElementById('logs-content').textContent = data.logs || 'No logs available';
            document.getElementById('logs-modal').style.display = 'block';
        } else {
            showNotification(data.error || 'Failed to load logs', 'error');
        }
    } catch (error) {
        showNotification('Error loading logs: ' + error.message, 'error');
    }
}

function closeLogsModal() {
    document.getElementById('logs-modal').style.display = 'none';
}

// Container selection
function toggleContainer(name) {
    const checkbox = document.querySelector(`input[value="${name}"]`);
    if (checkbox.checked) {
        selectedContainers.add(name);
    } else {
        selectedContainers.delete(name);
    }
    updateButtonStates();
}

function toggleSelectAll() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.container-checkbox');
    checkboxes.forEach(cb => {
        cb.checked = selectAll.checked;
        if (selectAll.checked) {
            selectedContainers.add(cb.value);
        } else {
            selectedContainers.delete(cb.value);
        }
    });
    updateButtonStates();
}

// Update button states
function updateButtonStates() {
    const selected = Array.from(selectedContainers);
    const selectedContainersData = containers.filter(c => selected.includes(c.name));
    
    // Enable/disable buttons based on selection and status
    document.getElementById('btn-start').disabled = selected.length === 0 || 
        !selectedContainersData.some(c => ['Created', 'Stopped', 'Paused', 'Error'].includes(c.status));
    document.getElementById('btn-stop').disabled = selected.length === 0 || 
        !selectedContainersData.some(c => ['Running', 'Starting'].includes(c.status));
    document.getElementById('btn-pause').disabled = selected.length === 0 || 
        !selectedContainersData.some(c => c.status === 'Running');
    document.getElementById('btn-resume').disabled = selected.length === 0 || 
        !selectedContainersData.some(c => c.status === 'Paused');
    document.getElementById('btn-restart').disabled = selected.length === 0;
    document.getElementById('btn-logs').disabled = selected.length === 0;
    document.getElementById('btn-rootfs').disabled = selected.length === 0;
    document.getElementById('btn-delete').disabled = selected.length === 0;
}

// Container menu
function showContainerMenu(event, name) {
    event.stopPropagation();
    const menu = document.createElement('div');
    menu.className = 'context-menu';
    menu.style.position = 'fixed';
    menu.style.left = event.clientX + 'px';
    menu.style.top = event.clientY + 'px';
    menu.innerHTML = `
        <div class="menu-item" onclick="containerAction('${name}', 'start'); this.closest('.context-menu').remove();">▶️ Start</div>
        <div class="menu-item" onclick="containerAction('${name}', 'stop'); this.closest('.context-menu').remove();">⏹️ Stop</div>
        <div class="menu-item" onclick="containerAction('${name}', 'pause'); this.closest('.context-menu').remove();">⏸️ Pause</div>
        <div class="menu-item" onclick="containerAction('${name}', 'resume'); this.closest('.context-menu').remove();">▶️ Resume</div>
        <div class="menu-item" onclick="containerAction('${name}', 'restart'); this.closest('.context-menu').remove();">🔄 Restart</div>
        <div class="menu-divider"></div>
        <div class="menu-item" onclick="
            viewLogs('${name}');
            this.closest('.context-menu').remove();
        ">📄 View Logs</div>
        <div class="menu-item" onclick="deleteContainer('${name}'); this.closest('.context-menu').remove();">🗑️ Delete</div>
    `;
    
    document.body.appendChild(menu);
    
    // Close menu on outside click
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        }, { once: true });
    }, 10);
}

// Advanced options
function showAdvanced() {
    const options = document.getElementById('advanced-options');
    options.style.display = options.style.display === 'none' ? 'block' : 'none';
}

function addVolume() {
    showDualInputModal(
        'Add Volume Mount',
        'Host Path:',
        'C:/MyData',
        'Container Path:',
        '/app/data',
        (hostPath, containerPath) => {
            if (hostPath && containerPath) {
                const list = document.getElementById('volumes-list');
                const div = document.createElement('div');
                div.className = 'volume-item';
                div.innerHTML = `<span>${escapeHtml(hostPath)}:${escapeHtml(containerPath)}</span> <button type="button" class="btn-small" onclick="this.parentElement.remove()">Remove</button>`;
                list.appendChild(div);
            }
        }
    );
}

function addEnvVar() {
    showDualInputModal(
        'Add Environment Variable',
        'Variable Name:',
        'MODE',
        'Variable Value:',
        'production',
        (varName, varValue) => {
            if (varName && varValue !== null) {
                const list = document.getElementById('env-list');
                const div = document.createElement('div');
                div.className = 'env-item';
                div.innerHTML = `<span>${escapeHtml(varName)}=${escapeHtml(varValue)}</span> <button type="button" class="btn-small" onclick="this.parentElement.remove()">Remove</button>`;
                list.appendChild(div);
            }
        }
    );
}

function getVolumes() {
    // Extract volumes from DOM
    const volumes = [];
    const volumeList = document.getElementById('volumes-list');
    if (volumeList) {
        const volumeItems = volumeList.querySelectorAll('.volume-item span');
        volumeItems.forEach(item => {
            const text = item.textContent.trim();
            if (text) {
                volumes.push(text);
            }
        });
    }
    return volumes;
}

function getEnvVars() {
    // Extract env vars from DOM
    const envVars = {};
    const envList = document.getElementById('env-list');
    if (envList) {
        const envItems = envList.querySelectorAll('.env-item span');
        envItems.forEach(item => {
            const text = item.textContent.trim();
            const equalIndex = text.indexOf('=');
            if (equalIndex > 0) {
                const key = text.substring(0, equalIndex).trim();
                const value = text.substring(equalIndex + 1).trim();
                envVars[key] = value;
            }
        });
    }
    return envVars;
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Toast notification system
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span class="toast-icon">${getToastIcon(type)}</span>
            <span class="toast-message">${escapeHtml(message)}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    return icons[type] || icons.info;
}

// Modal confirmation system
function showConfirmModal(title, message, onConfirm, onCancel = null) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-header">
                <h3>${escapeHtml(title)}</h3>
            </div>
            <div class="modal-body">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
                <button class="btn btn-danger" onclick="
                    this.closest('.modal-overlay').remove();
                    if (typeof ${onConfirm.name || 'onConfirm'} === 'function') {
                        ${onConfirm.name || 'onConfirm'}();
                    }
                ">Confirm</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Handle cancel
    if (onCancel) {
        modal.querySelector('.btn-secondary').onclick = () => {
            modal.remove();
            if (typeof onCancel === 'function') onCancel();
        };
    }
    
    // Handle confirm
    modal.querySelector('.btn-danger').onclick = () => {
        modal.remove();
        if (typeof onConfirm === 'function') onConfirm();
    };
    
    // Close on overlay click
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.remove();
            if (onCancel && typeof onCancel === 'function') onCancel();
        }
    };
}

// Dual input modal for two fields at once
function showDualInputModal(title, label1, placeholder1, label2, placeholder2, onConfirm, onCancel = null) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    const modalId = 'dual-input-modal-' + Date.now();
    modal.id = modalId;
    
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-header">
                <h3>${escapeHtml(title)}</h3>
            </div>
            <div class="modal-body">
                <div style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 500; color: var(--text-dark);">${escapeHtml(label1)}</label>
                    <input type="text" id="${modalId}-input1" class="form-input" placeholder="${escapeHtml(placeholder1)}" style="width: 100%;">
                </div>
                <div>
                    <label style="display: block; margin-bottom: 8px; font-weight: 500; color: var(--text-dark);">${escapeHtml(label2)}</label>
                    <input type="text" id="${modalId}-input2" class="form-input" placeholder="${escapeHtml(placeholder2)}" style="width: 100%;">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="document.getElementById('${modalId}').remove()">Cancel</button>
                <button class="btn btn-primary" id="${modalId}-submit">Add</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Set up submit handler
    const submitBtn = document.getElementById(modalId + '-submit');
    submitBtn.addEventListener('click', () => {
        const input1 = document.getElementById(modalId + '-input1').value.trim();
        const input2 = document.getElementById(modalId + '-input2').value.trim();
        if (input1 && input2) {
            modal.remove();
            if (typeof onConfirm === 'function') {
                onConfirm(input1, input2);
            }
        } else {
            showNotification('Please fill in both fields', 'warning');
        }
    });
    
    // Focus on first input
    setTimeout(() => {
        const input1 = document.getElementById(modalId + '-input1');
        if (input1) {
            input1.focus();
            // Allow Enter key to move to next field
            input1.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    document.getElementById(modalId + '-input2').focus();
                }
            });
        }
        const input2 = document.getElementById(modalId + '-input2');
        if (input2) {
            // Allow Enter key to submit
            input2.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    submitBtn.click();
                }
            });
        }
    }, 10);
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
            if (onCancel && typeof onCancel === 'function') {
                onCancel();
            }
        }
    });
}

// Prompt modal system
function showPromptModal(title, message, placeholder = '', onConfirm, onCancel = null) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    const inputId = 'prompt-input-' + Date.now();
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-header">
                <h3>${escapeHtml(title)}</h3>
            </div>
            <div class="modal-body">
                <p>${escapeHtml(message)}</p>
                <input type="text" id="${inputId}" class="form-input" placeholder="${escapeHtml(placeholder)}" autofocus>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
                <button class="btn btn-primary" onclick="
                    const input = document.getElementById('${inputId}');
                    const value = input.value;
                    this.closest('.modal-overlay').remove();
                    if (typeof ${onConfirm.name || 'onConfirm'} === 'function') {
                        ${onConfirm.name || 'onConfirm'}(value);
                    }
                ">OK</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Focus input
    setTimeout(() => document.getElementById(inputId).focus(), 100);
    
    // Handle Enter key
    document.getElementById(inputId).onkeypress = (e) => {
        if (e.key === 'Enter') {
            const value = e.target.value;
            modal.remove();
            if (typeof onConfirm === 'function') onConfirm(value);
        }
    };
    
    // Handle cancel
    if (onCancel) {
        modal.querySelector('.btn-secondary').onclick = () => {
            modal.remove();
            if (typeof onCancel === 'function') onCancel();
        };
    }
    
    // Handle confirm
    modal.querySelector('.btn-primary').onclick = () => {
        const input = document.getElementById(inputId);
        const value = input.value;
        modal.remove();
        if (typeof onConfirm === 'function') onConfirm(value);
    };
    
    // Close on overlay click
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.remove();
            if (onCancel && typeof onCancel === 'function') onCancel();
        }
    };
}

function refreshContainers() {
    loadContainers();
    showNotification('Containers refreshed', 'success');
}

async function openRootfs() {
    const selected = Array.from(selectedContainers);
    if (selected.length === 0) {
        showNotification('Please select a container', 'warning');
        return;
    }
    
    const name = selected[0];
    try {
        const response = await fetch(`/api/containers/${name}/rootfs`, {method: 'POST'});
        const data = await response.json();
        if (response.ok) {
            showNotification('Rootfs opened in file explorer', 'success');
        } else {
            showNotification(data.error || 'Failed to open rootfs', 'error');
        }
    } catch (error) {
        showNotification('Error opening rootfs: ' + error.message, 'error');
    }
}

function updateContainerStatus(name, status) {
    const row = document.querySelector(`tr[data-name="${name}"]`);
    if (row) {
        row.className = status.status.toLowerCase();
        const statusCell = row.querySelector('.status-badge-table');
        if (statusCell) {
            statusCell.textContent = status.status;
            statusCell.className = `status-badge-table status-${status.status.toLowerCase()}`;
        }
        row.querySelector('td:nth-child(5)').textContent = status.pid;
        row.querySelector('td:nth-child(6)').textContent = status.uptime;
        row.querySelector('td:nth-child(9)').textContent = status.last_started;
        row.querySelector('td:nth-child(10)').textContent = status.cpu;
    }
}

