/**
 * WikiContext - Main class for Wikipedia article summarization
 * Orchestrates Wikipedia API, RAKE, and TextRank to generate summaries
 */

class WikiContext {
    constructor(topic, maxPrereqs = 5, summaryRatio = 0.2) {
        this.topic = topic;
        this.maxPrereqs = maxPrereqs;
        this.summaryRatio = summaryRatio;

        // Initialize components
        this.wikiAPI = new WikipediaAPI();
        this.rake = new RAKE();
        this.textRank = new TextRank();

        // Cache
        this.mainContent = null;
        this.mainSummary = null;
        this.prerequisites = [];
        this.pageInfo = null;
    }

    /**
     * Fetch main article content
     */
    async getMainContent() {
        if (this.mainContent) {
            return this.mainContent;
        }

        try {
            const page = await this.wikiAPI.getPage(this.topic);
            this.pageInfo = page;
            this.mainContent = page.content;
            return this.mainContent;
        } catch (error) {
            throw new Error(`Failed to fetch article "${this.topic}": ${error.message}`);
        }
    }

    /**
     * Generate summary for main article
     */
    async getMainSummary() {
        if (this.mainSummary) {
            return this.mainSummary;
        }

        const content = await this.getMainContent();

        if (!Utils.isValidText(content)) {
            throw new Error('Article content is too short or empty');
        }

        // Generate summary using TextRank
        this.mainSummary = this.textRank.getSummaryByRatio(content, this.summaryRatio);

        return this.mainSummary;
    }

    /**
     * Extract prerequisites from article
     */
    async getPrerequisites() {
        if (this.prerequisites.length > 0) {
            return this.prerequisites;
        }

        const content = await this.getMainContent();

        // Extract keywords using RAKE
        const keywords = this.rake.extractKeywordStrings(content, 50);

        // Get links from Wikipedia page
        const links = await this.wikiAPI.getLinks(this.topic, 500);

        // Match keywords with links (case-insensitive)
        const matchedPrereqs = this.matchKeywordsWithLinks(keywords, links);

        // Limit to maxPrereqs
        this.prerequisites = matchedPrereqs.slice(0, this.maxPrereqs);

        return this.prerequisites;
    }

    /**
     * Match keywords with Wikipedia links
     */
    matchKeywordsWithLinks(keywords, links) {
        const matched = [];
        const linksLower = links.map(link => ({
            original: link,
            lower: link.toLowerCase()
        }));

        for (const keyword of keywords) {
            const keywordLower = keyword.toLowerCase();

            // Check for exact match or contains
            for (const linkObj of linksLower) {
                if (linkObj.lower === keywordLower ||
                    linkObj.lower.includes(keywordLower) ||
                    keywordLower.includes(linkObj.lower)) {

                    // Avoid duplicates
                    if (!matched.includes(linkObj.original)) {
                        matched.push(linkObj.original);
                        break;
                    }
                }
            }

            // Stop if we have enough
            if (matched.length >= this.maxPrereqs * 2) {
                break;
            }
        }

        return matched;
    }

    /**
     * Get summaries for all prerequisites
     */
    async getPrerequisiteSummaries() {
        const prereqs = await this.getPrerequisites();
        const summaries = [];

        for (const prereq of prereqs) {
            try {
                // Fetch prerequisite page
                const page = await this.wikiAPI.getPage(prereq);

                // Generate summary
                let summary = '';
                if (Utils.isValidText(page.content, 100)) {
                    summary = this.textRank.getSummary(page.content, 3);
                } else {
                    // Fallback to excerpt if content is too short
                    summary = Utils.getExcerpt(page.content, 50);
                }

                summaries.push({
                    title: page.title,
                    summary: summary || 'No summary available.',
                    url: page.url
                });
            } catch (error) {
                console.warn(`Failed to fetch prerequisite "${prereq}":`, error);
                // Skip failed prerequisites
            }
        }

        return summaries;
    }

    /**
     * Get complete analysis (main summary + prerequisites)
     */
    async getCompleteAnalysis() {
        const mainSummary = await this.getMainSummary();
        const prereqSummaries = await this.getPrerequisiteSummaries();

        return {
            topic: this.pageInfo?.title || this.topic,
            url: this.pageInfo?.url || '',
            mainSummary,
            prerequisites: prereqSummaries
        };
    }

    /**
     * Search for Wikipedia articles
     */
    static async search(query, limit = 10) {
        const api = new WikipediaAPI();
        return await api.search(query, limit);
    }

    /**
     * Check if a page exists
     */
    static async pageExists(title) {
        const api = new WikipediaAPI();
        return await api.pageExists(title);
    }

    /**
     * Check if page is disambiguation
     */
    static async isDisambiguation(title) {
        const api = new WikipediaAPI();
        return await api.checkDisambiguation(title);
    }
}
