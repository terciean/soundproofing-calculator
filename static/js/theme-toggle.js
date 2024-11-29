document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-dark-mode');
    if (!toggleButton) {
        console.warn('Dark mode toggle button not found');
        return;
    }

    // Check for saved user preference in localStorage with a fallback
    const currentTheme = (typeof localStorage !== 'undefined' && localStorage.getItem('theme')) || 'light'; // Safeguard for localStorage
    document.body.classList.toggle('dark-mode', currentTheme === 'dark');

    // Event listener for the toggle button
    toggleButton.addEventListener('click', () => {
        const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light'; // Update currentTheme here
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.classList.toggle('dark-mode', newTheme === 'dark');
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem('theme', newTheme); // Safeguard for localStorage
        }
    });
});