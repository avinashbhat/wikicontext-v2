/**
 * Wikipedia API Client
 * Handles fetching Wikipedia content, links, and search functionality
 */

class WikipediaAPI {
    constructor() {
        this.baseURL = 'https://en.wikipedia.org/w/api.php';
        this.origin = '*'; // Required for CORS
    }

    /**
     * Build URL with query parameters
     */
    buildURL(params) {
        const url = new URL(this.baseURL);
        params.origin = this.origin;
        params.format = 'json';
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        return url.toString();
    }

    /**
     * Fetch data from Wikipedia API
     */
    async fetchAPI(params) {
        try {
            const url = this.buildURL(params);
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Wikipedia API error:', error);
            throw new Error(`Failed to fetch from Wikipedia: ${error.message}`);
        }
    }

    /**
     * Search for Wikipedia pages
     */
    async search(query, limit = 10) {
        const params = {
            action: 'opensearch',
            search: query,
            limit: limit,
            namespace: 0,
            redirects: 'resolve'
        };

        const data = await this.fetchAPI(params);
        // OpenSearch returns: [query, [titles], [descriptions], [urls]]
        if (data && data.length >= 4) {
            const titles = data[1];
            const descriptions = data[2];
            const urls = data[3];

            return titles.map((title, i) => ({
                title: title,
                description: descriptions[i] || '',
                url: urls[i] || ''
            }));
        }
        return [];
    }

    /**
     * Get page content
     */
    async getPage(title) {
        const params = {
            action: 'query',
            prop: 'extracts|info',
            titles: title,
            explaintext: true,
            exsectionformat: 'plain',
            redirects: 1,
            inprop: 'url'
        };

        const data = await this.fetchAPI(params);
        const pages = data.query.pages;
        const pageId = Object.keys(pages)[0];

        if (pageId === '-1') {
            throw new Error(`Page "${title}" not found`);
        }

        const page = pages[pageId];
        return {
            title: page.title,
            content: page.extract || '',
            url: page.fullurl || `https://en.wikipedia.org/wiki/${encodeURIComponent(title)}`
        };
    }

    /**
     * Get links from a Wikipedia page
     */
    async getLinks(title, limit = 500) {
        const params = {
            action: 'query',
            prop: 'links',
            titles: title,
            pllimit: limit,
            plnamespace: 0,
            redirects: 1
        };

        const data = await this.fetchAPI(params);
        const pages = data.query.pages;
        const pageId = Object.keys(pages)[0];

        if (pageId === '-1') {
            return [];
        }

        const page = pages[pageId];
        if (!page.links) {
            return [];
        }

        return page.links.map(link => link.title);
    }

    /**
     * Check if page exists
     */
    async pageExists(title) {
        try {
            const params = {
                action: 'query',
                titles: title,
                redirects: 1
            };

            const data = await this.fetchAPI(params);
            const pages = data.query.pages;
            const pageId = Object.keys(pages)[0];

            return pageId !== '-1';
        } catch (error) {
            return false;
        }
    }

    /**
     * Get page summary (shorter version)
     */
    async getSummary(title) {
        const params = {
            action: 'query',
            prop: 'extracts',
            titles: title,
            exintro: true,
            explaintext: true,
            redirects: 1
        };

        const data = await this.fetchAPI(params);
        const pages = data.query.pages;
        const pageId = Object.keys(pages)[0];

        if (pageId === '-1') {
            throw new Error(`Page "${title}" not found`);
        }

        const page = pages[pageId];
        return page.extract || '';
    }

    /**
     * Resolve disambiguation pages
     */
    async checkDisambiguation(title) {
        const params = {
            action: 'query',
            titles: title,
            prop: 'categories',
            cllimit: 100,
            redirects: 1
        };

        const data = await this.fetchAPI(params);
        const pages = data.query.pages;
        const pageId = Object.keys(pages)[0];

        if (pageId === '-1') {
            return false;
        }

        const page = pages[pageId];
        if (!page.categories) {
            return false;
        }

        // Check if page has disambiguation category
        return page.categories.some(cat =>
            cat.title.includes('disambiguation') ||
            cat.title.includes('Disambiguation')
        );
    }
}
