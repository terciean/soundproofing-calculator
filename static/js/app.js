document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 0;
    const sections = document.querySelectorAll('.sections-container .section');
    const progressSteps = document.querySelectorAll('.progress-step');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const nextButtonText = nextBtn.querySelector('.button-text');

    // Noise Details elements
    const noiseTypeSelect = document.getElementById('noise-type');
    const noiseIntensityInput = document.getElementById('noise-intensity');
    const noiseDirectionCheckboxes = document.querySelectorAll('input[name="noise-direction"]');
    const recommendationsContainer = document.getElementById('recommendations-container');

    // Room Dimensions elements (assuming these are available globally or can be fetched)
    const lengthInput = document.getElementById('length');
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');

    function showStep(stepIndex) {
        // Hide all sections and remove active class from progress steps
        sections.forEach((section, index) => {
            section.classList.remove('active');
            if (progressSteps[index]) {
                progressSteps[index].classList.remove('active');
            }
        });

        // Show the current section and add active class to current and previous progress steps
        if (sections[stepIndex]) {
            sections[stepIndex].classList.add('active');
        }
        for (let i = 0; i <= stepIndex; i++) {
            if (progressSteps[i]) {
                progressSteps[i].classList.add('active');
            }
        }

        // Update button visibility and text
        prevBtn.style.display = stepIndex === 0 ? 'none' : 'inline-block';
        if (stepIndex === sections.length - 1) {
            nextButtonText.textContent = 'Submit';
        } else {
            nextButtonText.textContent = 'Next';
        }

        // If navigating to the Noise Details section, trigger recommendations
        if (sections[stepIndex].id === 'noise-details') {
            fetchRecommendations();
        }
    }

    // Function to fetch recommendations from the backend
    async function fetchRecommendations() {
        console.log('Fetching recommendations...');
        recommendationsContainer.innerHTML = '<div class="loading-placeholder"><div class="loading-spinner"></div><p>Generating recommendations...</p></div>';

        const noiseType = noiseTypeSelect.value;
        const noiseIntensity = parseInt(noiseIntensityInput.value, 10);
        const noiseDirections = Array.from(noiseDirectionCheckboxes)
                                    .filter(checkbox => checkbox.checked)
                                    .map(checkbox => checkbox.value);

        const roomDimensions = {
            length: parseFloat(lengthInput.value) || 0,
            width: parseFloat(widthInput.value) || 0,
            height: parseFloat(heightInput.value) || 0
        };

        // Basic validation: only proceed if essential inputs are available
        if (!noiseType || noiseDirections.length === 0 || !roomDimensions.length || !roomDimensions.width || !roomDimensions.height) {
            recommendationsContainer.innerHTML = '<p>Please select noise type, direction, and enter room dimensions to get recommendations.</p>';
            return;
        }

        try {
            const response = await fetch('/api/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify({
                    noise_profile: {
                        type: noiseType,
                        intensity: noiseIntensity,
                        direction: noiseDirections
                    },
                    room_profile: {
                        dimensions: roomDimensions
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Recommendations received:', data);
            displayRecommendations(data.recommendations);

        } catch (error) {
            console.error('Error fetching recommendations:', error);
            recommendationsContainer.innerHTML = '<p style="color: red;">Error loading recommendations. Please try again.</p>';
        }
    }

    // Function to display recommendations
    function displayRecommendations(recommendations) {
        let html = '';
        if (recommendations && recommendations.primary) {
            // Wall recommendations
            if (recommendations.primary.walls && recommendations.primary.walls.length > 0) {
                html += '<div class="recommendation-section"><h5>Wall Solutions</h5><ul>';
                recommendations.primary.walls.forEach(wall => {
                    if (wall) {
                        html += `<li>${wall.name || 'Wall Treatment'} (Score: ${wall.score || 'N/A'})</li>`;
                    }
                });
                html += '</ul></div>';
            }

            // Ceiling recommendation
            if (recommendations.primary.ceiling) {
                html += '<div class="recommendation-section"><h5>Ceiling Solution</h5>';
                html += `<p>${recommendations.primary.ceiling.name || 'Ceiling Treatment'} (Score: ${recommendations.primary.ceiling.score || 'N/A'})</p></div>`;
            }

            // Floor recommendation
            if (recommendations.primary.floor) {
                html += '<div class="recommendation-section"><h5>Floor Solution</h5>';
                html += `<p>${recommendations.primary.floor.name || 'Floor Treatment'} (Score: ${recommendations.primary.floor.score || 'N/A'})</p></div>`;
            }

            // Reasoning
            if (recommendations.reasoning && recommendations.reasoning.length > 0) {
                html += '<div class="recommendation-section"><h5>Reasoning</h5><ul>';
                recommendations.reasoning.forEach(reason => {
                    html += `<li>${reason}</li>`;
                });
                html += '</ul></div>';
            }

        } else {
            html = '<p>No specific recommendations available based on your selections. Please adjust inputs.</p>';
        }
        recommendationsContainer.innerHTML = html;
    }

    // Event Listeners for navigation buttons
    nextBtn.addEventListener('click', () => {
        if (currentStep < sections.length - 1) {
            currentStep++;
            showStep(currentStep);
        } else {
            // Handle form submission on the last step
            alert('Form Submitted!'); // Placeholder for actual submission logic
            console.log('Form submission triggered.');
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    });

    // Event listeners for noise details to trigger recommendations
    noiseTypeSelect.addEventListener('change', fetchRecommendations);
    noiseIntensityInput.addEventListener('change', fetchRecommendations);
    noiseDirectionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', fetchRecommendations);
    });

    // Also listen for changes in room dimensions if they are on the first step
    // This assumes room dimensions are updated before navigating to noise details
    // If room dimensions are on a different step, you might need to call fetchRecommendations
    // when the noise details step becomes active, as done in showStep.
    lengthInput.addEventListener('change', fetchRecommendations);
    widthInput.addEventListener('change', fetchRecommendations);
    heightInput.addEventListener('change', fetchRecommendations);

    // Initialize the form to the first step
    showStep(currentStep);
});