function openModal() {
    console.log('Open Modal')
    const modal = document.getElementById("modal");
    modal.classList.add("show");
    modal.classList.remove("hidden");
}

function openDropdownMenu() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const dropdownButton = document.getElementById('filter-button');
    const isHidden = dropdownMenu.classList.toggle('hidden');

    if (!isHidden) {
        document.addEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.add('bg-gray-300');
    } else {
        document.removeEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.remove('bg-gray-300');
    }
}

function closeDropdownMenu() {
    const dropdownMenu = document.getElementById("dropdownMenu");
    dropdownMenu.classList.add('hidden');
}

function closeDropdownMenuOnClickOutside(event) {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const dropdownButton = document.getElementById('filter-button');
    
    if (!dropdownMenu.contains(event.target) && !dropdownButton.contains(event.target)) {
        dropdownMenu.classList.add('hidden');
        document.removeEventListener('click', closeDropdownMenuOnClickOutside);
        dropdownButton.classList.remove('bg-gray-300');
    }
}

function closeModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
    modal.classList.remove("show");
}

function closeModalOnOutsideClick(event) {
    const modalContent = document.getElementById('modal-content');

    if (!modalContent.contains(event.target) && !event.target.closest('.modal-content')) {
        closeModal();
    } 
}

function closeModalIfNotEmpty(inputId) {
    const inputField = document.getElementById(inputId);

    if (inputField.value != "") {
        closeModal(); 
    }
}
