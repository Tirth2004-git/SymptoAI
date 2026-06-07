// App State
let allSymptoms = [];
let selectedSymptoms = new Set();
let activeCategory = 'all';

// DOM Elements
const searchInput = document.getElementById('symptom-search');
const clearSearchBtn = document.getElementById('clear-search-btn');
const suggestionsDropdown = document.getElementById('suggestions-dropdown');
const categoryPillsContainer = document.getElementById('category-pills');
const selectedTagsContainer = document.getElementById('selected-symptoms-tags');
const selectedCountLabel = document.getElementById('selected-count');
const clearAllBtn = document.getElementById('clear-all-btn');
const toggleListBtn = document.getElementById('toggle-list-btn');
const symptomsGridContainer = document.getElementById('symptoms-grid-container');
const symptomsGrid = document.getElementById('symptoms-grid');
const predictBtn = document.getElementById('predict-btn');

// Results elements
const resultsCard = document.getElementById('results-card');
const resultsPlaceholder = document.getElementById('results-placeholder');
const resultsLoader = document.getElementById('results-loader');
const resultsContent = document.getElementById('results-content');
const predictedDiseaseLabel = document.getElementById('predicted-disease');
const resModelLabel = document.getElementById('res-model-used');
const resConfidenceLabel = document.getElementById('res-confidence');
const resSymptomsCountLabel = document.getElementById('res-symptoms-count');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    fetchSymptoms();
    setupEventListeners();
});

// Fetch Symptoms from API
async function fetchSymptoms() {
    try {
        const response = await fetch('/api/symptoms');
        const data = await response.json();
        
        allSymptoms = data.symptoms;
        
        // Render system category pills
        renderCategoryPills(data.categories);
        // Render browse checklist grid
        renderChecklistGrid();
    } catch (error) {
        console.error('Error fetching symptoms:', error);
        selectedTagsContainer.innerHTML = '<div class="empty-state" style="color: #ef4444;">Failed to load symptoms from server. Make sure app.py is running.</div>';
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Search Autocomplete
    searchInput.addEventListener('input', (e) => {
        const value = e.target.value.trim().toLowerCase();
        if (value.length > 0) {
            clearSearchBtn.style.display = 'block';
            filterSuggestions(value);
        } else {
            clearSearchBtn.style.display = 'none';
            suggestionsDropdown.style.display = 'none';
        }
    });

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        suggestionsDropdown.style.display = 'none';
        searchInput.focus();
    });

    // Close suggestions if clicked outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !suggestionsDropdown.contains(e.target)) {
            suggestionsDropdown.style.display = 'none';
        }
    });

    // Clear All Selections
    clearAllBtn.addEventListener('click', () => {
        selectedSymptoms.clear();
        updateSelectedTags();
    });

    // Toggle Browse List Accordion
    toggleListBtn.addEventListener('click', () => {
        const isVisible = symptomsGridContainer.style.display !== 'none';
        if (isVisible) {
            symptomsGridContainer.style.display = 'none';
            toggleListBtn.classList.remove('active');
        } else {
            symptomsGridContainer.style.display = 'block';
            toggleListBtn.classList.add('active');
            renderChecklistGrid();
        }
    });

    // Handle Prediction trigger
    predictBtn.addEventListener('click', runPrediction);
}

// Render dynamic Category Pills
function renderCategoryPills(categories) {
    // Sort categories alphabetically
    categories.sort();
    
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'category-pill';
        btn.textContent = cat;
        btn.dataset.category = cat;
        
        btn.addEventListener('click', () => {
            document.querySelectorAll('.category-pill').forEach(pill => pill.classList.remove('active'));
            btn.classList.add('active');
            activeCategory = cat;
            renderChecklistGrid();
        });
        
        categoryPillsContainer.appendChild(btn);
    });
    
    // Add event for "All" pill
    const allPill = categoryPillsContainer.querySelector('[data-category="all"]');
    allPill.addEventListener('click', () => {
        document.querySelectorAll('.category-pill').forEach(pill => pill.classList.remove('active'));
        allPill.classList.add('active');
        activeCategory = 'all';
        renderChecklistGrid();
    });
}

// Filter and Display suggestions
function filterSuggestions(query) {
    const matches = allSymptoms.filter(sym => {
        const isNotSelected = !selectedSymptoms.has(sym.id);
        const nameMatches = sym.name.toLowerCase().includes(query);
        const catMatches = sym.category.toLowerCase().includes(query);
        return isNotSelected && (nameMatches || catMatches);
    });

    if (matches.length > 0) {
        suggestionsDropdown.innerHTML = '';
        matches.slice(0, 10).forEach(sym => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                <span>${sym.name}</span>
                <span class="item-cat">${sym.category}</span>
            `;
            item.addEventListener('click', () => {
                addSymptom(sym.id);
                searchInput.value = '';
                clearSearchBtn.style.display = 'none';
                suggestionsDropdown.style.display = 'none';
            });
            suggestionsDropdown.appendChild(item);
        });
        suggestionsDropdown.style.display = 'block';
    } else {
        suggestionsDropdown.innerHTML = '<div style="padding: 0.8rem 1.1rem; color: #4b5563; font-style: italic; font-size: 0.88rem;">No matching symptoms found</div>';
        suggestionsDropdown.style.display = 'block';
    }
}

// Add Symptom helper
function addSymptom(id) {
    selectedSymptoms.add(id);
    updateSelectedTags();
}

// Remove Symptom helper
function removeSymptom(id) {
    selectedSymptoms.delete(id);
    updateSelectedTags();
}

// Update selections area & Predict button active states
function updateSelectedTags() {
    selectedTagsContainer.innerHTML = '';
    
    if (selectedSymptoms.size === 0) {
        selectedTagsContainer.innerHTML = '<div class="empty-state">No symptoms selected. Start typing above or choose from the list.</div>';
        selectedCountLabel.textContent = '0';
        clearAllBtn.style.display = 'none';
        predictBtn.disabled = true;
    } else {
        selectedCountLabel.textContent = selectedSymptoms.size;
        clearAllBtn.style.display = 'block';
        predictBtn.disabled = false;
        
        selectedSymptoms.forEach(id => {
            const sym = allSymptoms.find(s => s.id === id);
            if (sym) {
                const tag = document.createElement('span');
                tag.className = 'symptom-tag';
                tag.innerHTML = `
                    ${sym.name}
                    <button class="tag-remove" title="Remove ${sym.name}"><i class="fa-solid fa-xmark"></i></button>
                `;
                tag.querySelector('button').addEventListener('click', () => removeSymptom(id));
                selectedTagsContainer.appendChild(tag);
            }
        });
    }

    // Keep checklist checkboxes synced in browser grid
    document.querySelectorAll('.symptoms-grid input[type="checkbox"]').forEach(chk => {
        chk.checked = selectedSymptoms.has(chk.value);
        const label = chk.closest('label');
        if (chk.checked) {
            label.classList.add('selected-active');
        } else {
            label.classList.remove('selected-active');
        }
    });
}

// Render checklists based on filters
function renderChecklistGrid() {
    symptomsGrid.innerHTML = '';
    
    const filtered = allSymptoms.filter(sym => {
        return activeCategory === 'all' || sym.category === activeCategory;
    });
    
    if (filtered.length === 0) {
        symptomsGrid.innerHTML = '<div class="empty-state" style="grid-column: 1/-1;">No symptoms found in this system category.</div>';
        return;
    }
    
    // Sort alphabetically by friendly name
    filtered.sort((a, b) => a.name.localeCompare(b.name));

    filtered.forEach(sym => {
        const label = document.createElement('label');
        label.className = 'checkbox-label';
        if (selectedSymptoms.has(sym.id)) {
            label.classList.add('selected-active');
        }
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = sym.id;
        checkbox.checked = selectedSymptoms.has(sym.id);
        
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                selectedSymptoms.add(sym.id);
            } else {
                selectedSymptoms.delete(sym.id);
            }
            updateSelectedTags();
        });
        
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(sym.name));
        symptomsGrid.appendChild(label);
    });
}

// Run prediction trigger
async function runPrediction() {
    if (selectedSymptoms.size === 0) return;
    
    // UI state: loading
    resultsCard.classList.remove('empty-results');
    resultsPlaceholder.style.display = 'none';
    resultsContent.style.display = 'none';
    resultsLoader.style.display = 'flex';
    
    const selectedModel = document.querySelector('input[name="ml-model"]:checked').value;
    const symptomPayload = Array.from(selectedSymptoms);
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symptoms: symptomPayload,
                model: selectedModel
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Wait slightly for animation feel
            setTimeout(() => {
                displayResults(data);
            }, 600);
        } else {
            showErrorState(data.error || 'Server error occurred during prediction.');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showErrorState('Failed to communicate with prediction server.');
    }
}

// Display results details
function displayResults(data) {
    resultsLoader.style.display = 'none';
    resultsContent.style.display = 'flex';
    
    predictedDiseaseLabel.textContent = data.disease;
    
    // Format model name display
    let modelNameDisp = 'Random Forest';
    if (data.model_used === 'decision_tree') modelNameDisp = 'Decision Tree';
    else if (data.model_used === 'mnb') modelNameDisp = 'Naive Bayes';
    else if (data.model_used === 'gradient_boost') modelNameDisp = 'Gradient Boosting';
    
    resModelLabel.textContent = modelNameDisp;
    resSymptomsCountLabel.textContent = data.symptoms_count;
    
    if (data.probability !== null && data.probability !== undefined) {
        resConfidenceLabel.textContent = `${data.probability}%`;
    } else {
        resConfidenceLabel.textContent = 'N/A';
    }
}

// Error state display helper
function showErrorState(message) {
    resultsLoader.style.display = 'none';
    resultsContent.style.display = 'none';
    resultsPlaceholder.style.display = 'flex';
    resultsCard.classList.add('empty-results');
    
    alert(`Error: ${message}`);
}
