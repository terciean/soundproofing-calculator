// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\utils\theme-toggle.js

/**
 * Manages theme toggling (e.g., light/dark mode).
 */
class ThemeToggle {
    constructor() {
        this.toggleButton = document.getElementById('theme-toggle'); // Assuming a button with this ID
        this.htmlElement = document.documentElement; // The <html> element
        this.themeKey = 'appTheme';

        this._initTheme();
    }

    _initTheme() {
        const savedTheme = localStorage.getItem(this.themeKey);
        if (savedTheme) {
            this.htmlElement.setAttribute('data-theme', savedTheme);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            // Default to dark if OS preference is dark and no theme saved
            this.htmlElement.setAttribute('data-theme', 'dark');
        } else {
            this.htmlElement.setAttribute('data-theme', 'light');
        }

        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', this.toggleTheme.bind(this));
        }
    }

    /**
     * Toggles the theme between 'light' and 'dark'.
     */
    toggleTheme() {
        const currentTheme = this.htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem(this.themeKey, newTheme);
        console.log(`Theme toggled to: ${newTheme}`);
    }

    /**
     * Sets the theme explicitly.
     * @param {string} theme - The theme to set ('light' or 'dark').
     */
    setTheme(theme) {
        if (theme === 'light' || theme === 'dark') {
            this.htmlElement.setAttribute('data-theme', theme);
            localStorage.setItem(this.themeKey, theme);
            console.log(`Theme set to: ${theme}`);
        } else {
            console.warn(`Invalid theme: ${theme}. Must be 'light' or 'dark'.`);
        }
    }
}

export default ThemeToggle;
