function openModal() {
    const modal = document.getElementById("modal");
    modal.classList.remove("hidden");
}

function closeModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
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
