// C:\Users\unkno\soundproof\soundproofing-calculator\static\js\utils\debounce.js

/**
 * Returns a function, that, as long as it continues to be invoked, will not
 * be triggered. The function will be called after it stops being called for
 * N milliseconds. If `immediate` is passed, trigger the function on the
 * leading edge, instead of the trailing.
 * @param {function} func - The function to debounce.
 * @param {number} wait - The number of milliseconds to wait.
 * @param {boolean} [immediate=false] - If true, trigger the function on the leading edge.
 * @returns {function} - The debounced function.
 */
export function debounce(func, wait, immediate = false) {
    let timeout;
    let result;

    return function() {
        const context = this;
        const args = arguments;

        const later = function() {
            timeout = null;
            if (!immediate) {
                result = func.apply(context, args);
            }
        };

        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) {
            result = func.apply(context, args);
        }

        return result;
    };
}
