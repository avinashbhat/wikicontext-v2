/**
 * Utility functions for text processing
 */

const Utils = {
    /**
     * Split text into sentences
     */
    splitIntoSentences(text) {
        if (!text) return [];

        // Split on period, exclamation, question mark followed by space or end
        const sentences = text
            .replace(/([.?!])\s+(?=[A-Z])/g, '$1|')
            .split('|')
            .map(s => s.trim())
            .filter(s => s.length > 0);

        return sentences;
    },

    /**
     * Split text into words
     */
    splitIntoWords(text) {
        if (!text) return [];

        return text
            .toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 0);
    },

    /**
     * Remove stopwords from word array
     */
    removeStopwords(words) {
        const stopwords = new Set([
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
            'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
            'between', 'both', 'but', 'by', 'could', 'did', 'do', 'does', 'doing', 'down',
            'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have',
            'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his',
            'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me',
            'might', 'more', 'most', 'must', 'my', 'myself', 'no', 'nor', 'not', 'now',
            'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves',
            'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some', 'such', 'than',
            'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
            'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until',
            'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while',
            'who', 'whom', 'why', 'will', 'with', 'would', 'you', 'your', 'yours',
            'yourself', 'yourselves'
        ]);

        return words.filter(word => !stopwords.has(word.toLowerCase()));
    },

    /**
     * Normalize text
     */
    normalizeText(text) {
        if (!text) return '';

        return text
            .replace(/\s+/g, ' ')
            .replace(/\n+/g, ' ')
            .trim();
    },

    /**
     * Calculate cosine similarity between two word arrays
     */
    cosineSimilarity(words1, words2) {
        const set1 = new Set(words1);
        const set2 = new Set(words2);

        const intersection = new Set([...set1].filter(x => set2.has(x)));

        if (set1.size === 0 || set2.size === 0) {
            return 0;
        }

        return intersection.size / Math.sqrt(set1.size * set2.size);
    },

    /**
     * Truncate text to specified length
     */
    truncate(text, maxLength = 500) {
        if (!text || text.length <= maxLength) {
            return text;
        }

        return text.substring(0, maxLength).trim() + '...';
    },

    /**
     * Clean Wikipedia text (remove references, etc.)
     */
    cleanWikiText(text) {
        if (!text) return '';

        return text
            // Remove reference markers like [1], [2], etc.
            .replace(/\[\d+\]/g, '')
            // Remove LaTeX display style blocks - more aggressive pattern
            .replace(/\{\\displaystyle[\s\S]*?\}/g, ' ')
            // Remove specific LaTeX environments
            .replace(/\\begin\{[^}]+\}[\s\S]*?\\end\{[^}]+\}/g, ' ')
            // Remove LaTeX commands with arguments
            .replace(/\\[a-zA-Z]+\{[^}]*\}/g, ' ')
            // Remove standalone LaTeX commands
            .replace(/\\[a-zA-Z]+/g, ' ')
            // Remove backslashes followed by special chars
            .replace(/\\[&\\\|]/g, ' ')
            // Remove remaining curly braces
            .replace(/[{}]/g, '')
            // Remove angle bracket notation (quantum states)
            .replace(/\s*[⟨⟩]\s*/g, ' ')
            // Clean up mathematical notation
            .replace(/\s*:=\s*/g, ' = ')
            .replace(/\^\d+=/g, '')
            // Remove caret symbols (exponents) when isolated
            .replace(/\s*\^\s*/g, '')
            // Remove parentheses with only numbers/spaces (matrix notation)
            .replace(/\(\s*[\d\s]+\s*\)/g, ' ')
            // Clean up semicolons used in math notation
            .replace(/\s*;\s*/g, '. ')
            // Remove multiple spaces
            .replace(/\s+/g, ' ')
            // Remove leading/trailing whitespace
            .trim();
    },

    /**
     * Extract first N sentences
     */
    extractFirstSentences(text, count = 5) {
        const sentences = this.splitIntoSentences(text);
        return sentences.slice(0, count).join(' ');
    },

    /**
     * Check if text is valid (not empty, not too short)
     */
    isValidText(text, minLength = 50) {
        return text && text.trim().length >= minLength;
    },

    /**
     * Count words in text
     */
    wordCount(text) {
        if (!text) return 0;
        return this.splitIntoWords(text).length;
    },

    /**
     * Get text excerpt
     */
    getExcerpt(text, maxWords = 100) {
        const words = this.splitIntoWords(text);
        if (words.length <= maxWords) {
            return text;
        }

        const sentences = this.splitIntoSentences(text);
        let excerpt = '';
        let wordsSoFar = 0;

        for (const sentence of sentences) {
            const sentenceWords = this.splitIntoWords(sentence);
            if (wordsSoFar + sentenceWords.length > maxWords) {
                break;
            }
            excerpt += sentence + ' ';
            wordsSoFar += sentenceWords.length;
        }

        return excerpt.trim() || this.truncate(text, 500);
    }
};
