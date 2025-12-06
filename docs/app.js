/**
 * Main application logic
 * Handles UI interactions and orchestrates WikiContext
 */

// Global state
let currentWikiContext = null;
let searchCache = new Map();

/**
 * Update max prerequisites value display
 */
function updatePrereqValue(value) {
    document.getElementById('prereqValue').textContent = value;
}

/**
 * Update summary ratio value display
 */
function updateRatioValue(value) {
    document.getElementById('ratioValue').textContent = value + '%';
}

/**
 * Show loading indicator
 */
function showLoading(show = true) {
    const loading = document.getElementById('loading');
    loading.style.display = show ? 'block' : 'none';
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    // Hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    const errorDiv = document.getElementById('error');
    errorDiv.style.display = 'none';
}

/**
 * Show results section
 */
function showResults(show = true) {
    const results = document.getElementById('results');
    results.style.display = show ? 'block' : 'none';
}

/**
 * Show disambiguation section
 */
function showDisambiguation(options) {
    const section = document.getElementById('disambiguationSection');
    const optionsDiv = document.getElementById('disambiguationOptions');

    optionsDiv.innerHTML = '';

    options.forEach(option => {
        const div = document.createElement('div');
        div.className = 'disambiguation-option';
        div.innerHTML = `
            <strong>${option.title}</strong>
            ${option.description ? `<p>${option.description}</p>` : ''}
        `;
        div.onclick = () => selectDisambiguation(option.title);
        optionsDiv.appendChild(div);
    });

    section.style.display = 'block';
}

/**
 * Hide disambiguation section
 */
function hideDisambiguation() {
    const section = document.getElementById('disambiguationSection');
    section.style.display = 'none';
}

/**
 * Handle disambiguation selection
 */
function selectDisambiguation(title) {
    hideDisambiguation();
    document.getElementById('topicInput').value = title;
    handleSearch();
}

/**
 * Display results
 */
function displayResults(data) {
    // Main summary
    document.getElementById('articleTitle').textContent = data.topic;
    document.getElementById('mainSummary').textContent = data.mainSummary || 'No summary available.';
    document.getElementById('wikiLink').href = data.url;

    // Prerequisites
    const prereqList = document.getElementById('prereqList');
    prereqList.innerHTML = '';

    if (data.prerequisites.length === 0) {
        prereqList.innerHTML = '<p>No prerequisites identified.</p>';
    } else {
        data.prerequisites.forEach(prereq => {
            const card = document.createElement('div');
            card.className = 'prereq-card';
            card.innerHTML = `
                <h3>${prereq.title}</h3>
                <p>${prereq.summary}</p>
                <a href="${prereq.url}" target="_blank">Learn more →</a>
            `;
            prereqList.appendChild(card);
        });
    }

    showResults(true);
}

/**
 * Main search handler
 */
async function handleSearch() {
    const topicInput = document.getElementById('topicInput');
    const topic = topicInput.value.trim();

    if (!topic) {
        showError('Please enter a Wikipedia topic');
        return;
    }

    // Disable search button
    const searchBtn = document.getElementById('searchBtn');
    searchBtn.disabled = true;
    searchBtn.textContent = 'Processing...';

    // Hide previous results and errors
    showResults(false);
    hideError();
    hideDisambiguation();
    showLoading(true);

    try {
        // Get settings
        const maxPrereqs = parseInt(document.getElementById('maxPrereqs').value);
        const summaryRatio = parseInt(document.getElementById('summaryRatio').value) / 100;

        // Check if page exists
        const exists = await WikiContext.pageExists(topic);

        if (!exists) {
            // Try searching for similar pages
            const searchResults = await WikiContext.search(topic, 5);

            if (searchResults.length === 0) {
                throw new Error(`No Wikipedia article found for "${topic}"`);
            }

            // Show disambiguation options
            showLoading(false);
            showDisambiguation(searchResults);
            return;
        }

        // Check if disambiguation page
        const isDisambig = await WikiContext.isDisambiguation(topic);

        if (isDisambig) {
            const searchResults = await WikiContext.search(topic, 10);
            showLoading(false);
            showDisambiguation(searchResults);
            return;
        }

        // Create WikiContext instance
        currentWikiContext = new WikiContext(topic, maxPrereqs, summaryRatio);

        // Get complete analysis
        const results = await currentWikiContext.getCompleteAnalysis();

        // Display results
        displayResults(results);
        showLoading(false);

    } catch (error) {
        console.error('Search error:', error);
        showError(error.message || 'An error occurred while processing the article');
        showLoading(false);
    } finally {
        // Re-enable search button
        searchBtn.disabled = false;
        searchBtn.textContent = 'Search';
    }
}

/**
 * Handle Enter key in input
 */
document.getElementById('topicInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        handleSearch();
    }
});

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('WikiContext loaded successfully!');

    // Focus on input
    document.getElementById('topicInput').focus();

    // Check for URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const topic = urlParams.get('topic');

    if (topic) {
        document.getElementById('topicInput').value = decodeURIComponent(topic);
        handleSearch();
    }
});

/**
 * Share results via URL
 */
function shareResults() {
    if (currentWikiContext && currentWikiContext.pageInfo) {
        const url = new URL(window.location.href);
        url.searchParams.set('topic', currentWikiContext.pageInfo.title);
        navigator.clipboard.writeText(url.toString());
        alert('Link copied to clipboard!');
    }
}
