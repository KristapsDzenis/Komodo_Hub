// Section navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
    
    // Update active state in sidebar
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.classList.remove('active');
    });
    
    // If it's a main section, highlight the sidebar link
    if (sectionId === 'users-section' || sectionId === 'organizations-section' || sectionId === 'placeholder-section' || sectionId === 'placeholder2-section') {
        const sidebarLink = document.getElementById(sectionId.replace('-section', '-link'));
        if (sidebarLink) {
            sidebarLink.classList.add('active');
        }
    }

    // Update URL with the new section
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('section', sectionId);
    window.history.pushState({}, '', currentUrl.toString());
}

// Table column management
function toggleColumn(tableType, columnIndex) {
    const table = tableType === 'users' ? 
        document.querySelector('#users-section table') : 
        document.querySelector('#organizations-section table');
        
    const cells = table.getElementsByClassName(`column-${columnIndex}`);
    for (let cell of cells) {
        cell.classList.toggle('hidden-column');
    }
}

function resetColumns(tableType) {
    const table = tableType === 'users' ? 
        document.querySelector('#users-section table') : 
        document.querySelector('#organizations-section table');
        
    const hiddenCells = table.getElementsByClassName('hidden-column');
    // Convert to array since we'll be modifying the live HTMLCollection
    Array.from(hiddenCells).forEach(cell => {
        cell.classList.remove('hidden-column');
    });
}

// Modal handling
function openModal(modalId, data) {
    const modal = document.getElementById(modalId);
    modal.style.display = "block";
    
    // Fill form with existing data
    if (modalId === 'editUserModal') {
        document.getElementById('edit-fname').value = data.fname;
        document.getElementById('edit-sname').value = data.sname;
        document.getElementById('edit-email').value = data.email;
        document.getElementById('edit-organization').value = data.organization;
        document.getElementById('edit-account-type').value = data.account_type;
        document.getElementById('edit-id').value = data.id;
        
        // Store username for submission
        document.getElementById('editUserForm').dataset.username = data.username;
    } else if (modalId === 'editOrgModal') {
        document.getElementById('edit-org-name').value = data.org_school_name;
        document.getElementById('edit-org-email').value = data.email;
        document.getElementById('edit-org-account-type').value = data.account_type;
        
        // Store username for submission
        document.getElementById('editOrgForm').dataset.username = data.username;
    }
}

// Modal event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Close modal when clicking the X or outside the modal
    document.querySelectorAll('.modal .close, .modal').forEach(element => {
        element.onclick = function(event) {
            if (event.target === element) {
                element.closest('.modal').style.display = "none";
            }
        };
    });

    // Prevent modal content clicks from closing the modal
    document.querySelectorAll('.modal-content').forEach(element => {
        element.onclick = function(event) {
            event.stopPropagation();
        };
    });

    // Handle form submissions
    document.getElementById('editUserForm').onsubmit = function(e) {
        e.preventDefault();
        const username = this.dataset.username;
        const formData = {
            fname: document.getElementById('edit-fname').value,
            sname: document.getElementById('edit-sname').value,
            email: document.getElementById('edit-email').value,
            organization: document.getElementById('edit-organization').value,
            account_type: document.getElementById('edit-account-type').value,
            id: document.getElementById('edit-id').value
        };

        submitForm(`/admin/edit_user/${username}`, formData, 'User');
    };

    document.getElementById('editOrgForm').onsubmit = function(e) {
        e.preventDefault();
        const username = this.dataset.username;
        const formData = {
            org_school_name: document.getElementById('edit-org-name').value,
            email: document.getElementById('edit-org-email').value,
            account_type: document.getElementById('edit-org-account-type').value
        };

        submitForm(`/admin/edit_organization/${username}`, formData, 'Organization');
    };
});

// Helper function for form submissions
function submitForm(url, formData, entityType) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${entityType} updated successfully`);
            location.reload();
        } else {
            alert(`Error updating ${entityType.toLowerCase()}: ${data.message}`);
        }
    })
    .catch(error => {
        alert(`Error updating ${entityType.toLowerCase()}: ${error}`);
    });
} 