async function initializeFormHandlers() {
    console.log('Initializing form handlers');
    
    try {
        await bindAllEvents();
        console.log('Form handlers initialized successfully');
    } catch (error) {
        console.error('Failed to initialize form handlers:', error);
        throw error;
    }
}

// Bind all events
async function bindAllEvents() {
    try {
        await Promise.all([
            bindInputEvents(),
            bindNoiseInputEvents(),
            bindSurfaceEvents(),
            bindSoundproofingEvents()
        ]);
        console.log('All events bound successfully');
    } catch (error) {
        console.error('Failed to bind events:', error);
        throw error;
    }
}

// Input events
function bindInputEvents() {
    const dimensionInputs = document.querySelectorAll('input[type="number"]');
    
    dimensionInputs.forEach(input => {
        input.addEventListener('input', debounce((e) => {
            const value = parseFloat(e.target.value);
            window.FormState.dimensions[e.target.id] = value || 0;
            window.roomManager?.updateDimensions({ [e.target.id]: value || 0 });
            updateSummary();
        }, 300));
    });

    console.log('Input events bound');
}

// Surface events
function bindSurfaceEvents() {
    // Surface type selection
    const surfaceTypeButtons = document.querySelectorAll('.surface-type-btn');
    surfaceTypeButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!window.surfaceManager?.initialized) {
                console.warn('SurfaceManager not initialized');
                return;
            }

            const surfaceType = button.dataset.surface;
            window.surfaceManager.selectSurfaceType(surfaceType);
            updateSummary();
        });
    });

    // Feature selection
    const featureCheckboxes = document.querySelectorAll('.feature-checkbox');
    featureCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            if (!window.surfaceManager?.initialized) {
                console.warn('SurfaceManager not initialized');
                return;
            }

            const feature = e.target.value;
            const surfaceType = e.target.dataset.surface;
            window.surfaceManager.updateFeature(surfaceType, feature, e.target.checked);
            updateSummary();
        });
    });

    console.log('Surface events bound');
}

// Soundproofing events
function bindSoundproofingEvents() {
    const solutionButtons = document.querySelectorAll('.solution-btn');
    solutionButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!window.soundproofingManager?.initialized) {
                console.warn('SoundproofingManager not initialized');
                return;
            }

            const solution = button.dataset.solution;
            const category = button.dataset.category;
            window.soundproofingManager.selectSolution(category, solution);
            updateSummary();
        });
    });

    // Add listener for noise reduction goal changes
    const noiseReductionSelect = document.getElementById('noise-reduction-goal');
    if (noiseReductionSelect) {
        noiseReductionSelect.addEventListener('change', () => {
            updateSummary();
        });
    }

    console.log('Soundproofing events bound');
}

// Noise events
function bindNoiseEvents() {
    // Handle noise type selection
    const noiseTypeSelect = document.getElementById('noise-type');
    if (noiseTypeSelect) {
        noiseTypeSelect.addEventListener('change', (e) => {
            window.FormState.noiseData = window.FormState.noiseData || {};
            window.FormState.noiseData.type = e.target.value;
            updateSummary();
        });
    }

    // Handle noise intensity
    const intensitySlider = document.getElementById('noise-intensity');
    if (intensitySlider) {
        intensitySlider.addEventListener('input', (e) => {
            window.FormState.noiseData = window.FormState.noiseData || {};
            window.FormState.noiseData.intensity = parseInt(e.target.value);
            updateSummary();
        });
    }

    // Handle time checkboxes
    const timeCheckboxes = document.querySelectorAll('input[name="noise-time"]');
    timeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            window.FormState.noiseData = window.FormState.noiseData || {};
            window.FormState.noiseData.time = Array.from(timeCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            updateSummary();
        });
    });

    // Handle direction checkboxes
    const directionCheckboxes = document.querySelectorAll('input[name="noise-direction"]');
    directionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            window.FormState.noiseData = window.FormState.noiseData || {};
            window.FormState.noiseData.direction = Array.from(directionCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            updateSummary();
        });
    });
}

// Helper functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    }
}

// Error handling wrapper
function handleError(context, error) {
    console.error(`${context}:`, error);
    if (window.errorUtils?.initialized) {
        window.errorUtils.displayError(`${context}: ${error.message}`);
    }
    throw error;
}

// Export if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeFormHandlers,
        bindAllEvents,
        bindNavigationEvents,
        bindInputEvents,
        bindSurfaceEvents,
        bindSoundproofingEvents,
        bindWorkflowEvents
    };
}

// Make form handlers available globally
window.initializeFormHandlers = initializeFormHandlers;

// Add this function to handle summary updates
function updateSummary() {
    const summaryContainer = document.querySelector('#review-section .review-container');
    if (!summaryContainer) return;

    const formatDimensions = () => {
        const dims = window.FormState.dimensions;
        return `Length: ${dims.length || 'N/A'}m, Width: ${dims.width || 'N/A'}m, Height: ${dims.height || 'N/A'}m`;
    };

    const formatSurfaces = () => {
        let surfaceText = '';
        window.FormState.surfaces.forEach((features, type) => {
            surfaceText += `${type}: ${Array.from(features).join(', ') || 'None'}<br>`;
        });
        return surfaceText || 'No surfaces selected';
    };

    const formatSoundproofing = () => {
        let soundText = '';
        window.FormState.soundproofing.forEach((value, key) => {
            soundText += `${key}: ${value}<br>`;
        });
        return soundText || 'No soundproofing selected';
    };

    summaryContainer.innerHTML = `
        <div class="summary-section">
            <h3>Room Dimensions</h3>
            <p>${formatDimensions()}</p>
        </div>
        <div class="summary-section">
            <h3>Surface Features</h3>
            <p>${formatSurfaces()}</p>
        </div>
        <div class="summary-section">
            <h3>Soundproofing Solutions</h3>
            <p>${formatSoundproofing()}</p>
        </div>
    `;
}

// Add validation for room dimensions
function verifyRoomDimensions() {
    const dimensions = {
        length: parseFloat(document.getElementById('length').value),
        width: parseFloat(document.getElementById('width').value),
        height: parseFloat(document.getElementById('height').value),
        roomType: document.getElementById('room-type').value
    };

    console.log('Room dimensions collected:', {
        dimensions,
        isValid: {
            length: !isNaN(dimensions.length) && dimensions.length > 0,
            width: !isNaN(dimensions.width) && dimensions.width > 0,
            height: !isNaN(dimensions.height) && dimensions.height > 0,
            roomType: Boolean(dimensions.roomType)
        }
    });

    return dimensions;
}

// Add validation for surface data
function verifySurfaceData() {
    const blockages = window.FormState?.blockages || {};
    
    console.log('Surface data collected:', {
        blockages,
        blockageCounts: {
            wall: blockages.wall?.length || 0,
            floor: blockages.floor?.length || 0,
            ceiling: blockages.ceiling?.length || 0
        },
        totalAreas: window.FormState?.blockageAreas || {}
    });

    return blockages;
}

// Enhance the quote generation process
async function generateQuote() {
    console.log('Starting quote generation...');
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (!csrfToken) {
        console.error('CSRF token not found');
        window.errorUtils?.displayError('Security token missing');
        return;
    }

    // Verify all required data
    const dimensions = verifyRoomDimensions();
    const noiseData = verifyNoiseData();
    const surfaceData = verifySurfaceData();

    // Check if we have all required data
    const isValid = {
        dimensions: dimensions.length > 0 && dimensions.width > 0 && dimensions.height > 0,
        noise: noiseData.type && noiseData.direction.length > 0,
        surfaces: true // Always valid as blockages are optional
    };

    console.log('Quote validation:', isValid);

    if (!Object.values(isValid).every(Boolean)) {
        console.error('Missing required data for quote generation');
        window.errorUtils?.displayError('Please fill in all required fields');
        return;
    }

    try {
        const response = await fetch('/api/generate-quote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                dimensions,
                noiseData,
                blockages: surfaceData,
                roomType: dimensions.roomType
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }

        const quoteData = await response.json();
        console.log('Quote generated successfully:', quoteData);
        
        displayQuote(quoteData);
    } catch (error) {
        console.error('Error generating quote:', error);
        window.errorUtils?.displayError('Failed to generate quote: ' + error.message);
    }
}

// Enhance the workflow navigation
function handleWorkflowNavigation(direction) {
    const currentSection = document.querySelector('.section.active');
    const sections = Array.from(document.querySelectorAll('.section'));
    const currentIndex = sections.indexOf(currentSection);
    
    console.log('Workflow navigation:', {
        direction,
        currentSection: currentSection.id,
        currentIndex,
        totalSections: sections.length
    });

    let nextIndex;
    if (direction === 'next') {
        // Validate current section before proceeding
        const isValid = validateCurrentSection(currentSection);
        if (!isValid) {
            console.warn('Current section validation failed');
            return;
        }

        nextIndex = currentIndex + 1;
        if (nextIndex === sections.length - 1) {
            console.log('Entering final review section');
            generateQuote().catch(error => {
                console.error('Failed to generate quote:', error);
                window.errorUtils?.displayError('Failed to generate quote. Please try again.');
            });
        }
    } else {
        nextIndex = currentIndex - 1;
    }

    // Update section visibility
    if (nextIndex >= 0 && nextIndex < sections.length) {
        updateSectionVisibility(currentSection, sections[nextIndex]);
        updateNavigationState(nextIndex, sections.length);
    }
}

function validateCurrentSection(section) {
    console.log('Validating section:', section.id);
    
    switch (section.id) {
        case 'room-details':
            const dimensions = verifyRoomDimensions();
            return dimensions.length > 0 && dimensions.width > 0 && dimensions.height > 0;
            
        case 'noise-details':
            const noiseData = verifyNoiseData();
            return noiseData.type && noiseData.direction.length > 0;
            
        case 'surface-details':
            verifySurfaceData(); // Always valid as blockages are optional
            return true;
            
        default:
            return true;
    }
}

function updateSectionVisibility(currentSection, nextSection) {
    console.log('Updating section visibility:', {
        from: currentSection.id,
        to: nextSection.id
    });
    
    currentSection.classList.remove('active');
    nextSection.classList.add('active');
}

function updateNavigationState(currentIndex, totalSections) {
    console.log('Updating navigation state:', {
        currentIndex,
        totalSections
    });
    
    updateNavigationButtons(currentIndex, totalSections);
    updateProgressBar(currentIndex);
}

function updateNavigationButtons(currentIndex, totalSections) {
    const prevButton = document.querySelector('.prev-btn');
    const nextButton = document.querySelector('.next-btn');
    
    prevButton.disabled = currentIndex === 0;
    nextButton.disabled = currentIndex === totalSections - 1;
    
    // Update next button text based on section
    if (currentIndex === totalSections - 2) {
        nextButton.textContent = 'Generate Quote';
    } else {
        nextButton.textContent = 'Next';
    }
}

function saveQuote() {
    // TODO: Implement quote saving functionality
    alert('Quote saved successfully!');
}

function printQuote() {
    window.print();
}

// Update summary whenever form state changes
function updateSummary() {
    if (document.getElementById('review').classList.contains('active')) {
        window.workflowManager?.populateSummary();
    }
}

// Add this to your form handlers
function verifyNoiseData() {
    const noiseData = {
        type: document.getElementById('noise-type').value,
        intensity: parseInt(document.getElementById('noise-intensity').value),
        time: Array.from(document.querySelectorAll('input[name="noise-time"]:checked'))
            .map(cb => cb.value),
        direction: Array.from(document.querySelectorAll('input[name="noise-direction"]:checked'))
            .map(cb => cb.value)
    };

    console.log('Collected noise data:', {
        type: noiseData.type,
        intensity: noiseData.intensity,
        time: noiseData.time,
        direction: noiseData.direction,
        isValid: {
            type: Boolean(noiseData.type),
            intensity: !isNaN(noiseData.intensity) && noiseData.intensity >= 1 && noiseData.intensity <= 5,
            time: Array.isArray(noiseData.time) && noiseData.time.length > 0,
            direction: Array.isArray(noiseData.direction) && noiseData.direction.length > 0
        }
    });

    return noiseData;
}

// Replace the form submission handler with individual input handlers
function bindNoiseInputEvents() {
    console.log('Binding noise input events...');

    // Noise type select
    const noiseTypeSelect = document.getElementById('noise-type');
    if (noiseTypeSelect) {
        noiseTypeSelect.addEventListener('change', () => {
            updateNoiseData();
        });
    }

    // Noise intensity slider
    const intensitySlider = document.getElementById('noise-intensity');
    if (intensitySlider) {
        intensitySlider.addEventListener('input', () => {
            updateNoiseData();
        });
    }

    // Time checkboxes
    document.querySelectorAll('input[name="noise-time"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateNoiseData();
        });
    });

    // Direction checkboxes
    document.querySelectorAll('input[name="noise-direction"]').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            updateNoiseData();
        });
    });
}

function updateNoiseData() {
    const noiseData = verifyNoiseData();
    if (window.FormState) {
        window.FormState.noiseData = noiseData;
        console.log('Updated FormState:', window.FormState);
        
        // Trigger form state update event
        window.dispatchEvent(new CustomEvent('formStateUpdated', {
            detail: { noiseData }
        }));
    }
}

// Initialize the noise input handlers when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeFormHandlers().catch(error => {
        console.error('Failed to initialize form handlers:', error);
        window.errorUtils?.displayError('Failed to initialize form handlers');
    });
});

async function updateRoom() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (!csrfToken) {
        console.error('CSRF token not found');
        window.errorUtils?.displayError('Security token missing');
        return;
    }

    try {
        const response = await fetch('/update_room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                dimensions: window.FormState.dimensions,
                surfaces: window.FormState.surfaces,
                blockages: window.FormState.blockages
            })
        });

        // ... rest of the function ...
    } catch (error) {
        console.error('Room update error:', error);
        window.errorUtils?.displayError('Failed to update room');
    }
}