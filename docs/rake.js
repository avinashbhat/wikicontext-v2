/**
 * RAKE - Rapid Automatic Keyword Extraction
 * JavaScript implementation of the RAKE algorithm for keyword extraction
 */

class RAKE {
    constructor() {
        // Stopwords and delimiters
        this.stopwords = new Set([
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
            'yourself', 'yourselves', 'also', 'may', 'can', 'one', 'two', 'three', 'etc',
            'often', 'many', 'much', 'get', 'became', 'become', 'becomes'
        ]);

        this.punctuation = new Set([
            '.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']', '{', '}', '-', '–', '—'
        ]);
    }

    /**
     * Check if word is a stopword
     */
    isStopword(word) {
        return this.stopwords.has(word.toLowerCase());
    }

    /**
     * Split text into sentences using punctuation
     */
    splitSentences(text) {
        // Split on sentence-ending punctuation
        return text
            .split(/[.!?;]+/)
            .map(s => s.trim())
            .filter(s => s.length > 0);
    }

    /**
     * Generate candidate keywords from sentences
     */
    generateCandidateKeywords(sentences) {
        const candidateKeywords = [];

        for (const sentence of sentences) {
            // Split into words
            const words = sentence
                .toLowerCase()
                .replace(/[^\w\s]/g, ' ')
                .split(/\s+/)
                .filter(w => w.length > 0);

            // Group words into phrases (stop at stopwords)
            let currentPhrase = [];

            for (const word of words) {
                if (this.isStopword(word)) {
                    if (currentPhrase.length > 0) {
                        candidateKeywords.push(currentPhrase.join(' '));
                        currentPhrase = [];
                    }
                } else {
                    currentPhrase.push(word);
                }
            }

            // Add remaining phrase
            if (currentPhrase.length > 0) {
                candidateKeywords.push(currentPhrase.join(' '));
            }
        }

        return candidateKeywords;
    }

    /**
     * Calculate word scores based on co-occurrence
     */
    calculateWordScores(phrases) {
        const wordFrequency = new Map();
        const wordDegree = new Map();

        // Calculate frequency and degree for each word
        for (const phrase of phrases) {
            const words = phrase.split(' ');
            const wordCount = words.length;

            for (const word of words) {
                // Update frequency
                wordFrequency.set(word, (wordFrequency.get(word) || 0) + 1);

                // Update degree (number of co-occurrences)
                wordDegree.set(word, (wordDegree.get(word) || 0) + wordCount);
            }
        }

        // Calculate word scores (degree / frequency)
        const wordScores = new Map();
        for (const [word, frequency] of wordFrequency) {
            const degree = wordDegree.get(word) || 0;
            wordScores.set(word, degree / frequency);
        }

        return wordScores;
    }

    /**
     * Calculate phrase scores
     */
    calculatePhraseScores(phrases, wordScores) {
        const phraseScores = new Map();

        for (const phrase of phrases) {
            const words = phrase.split(' ');
            let score = 0;

            for (const word of words) {
                score += wordScores.get(word) || 0;
            }

            phraseScores.set(phrase, score);
        }

        return phraseScores;
    }

    /**
     * Extract keywords from text
     * Returns array of {keyword, score} objects sorted by score
     */
    extractKeywords(text, topN = 20) {
        if (!text || text.trim().length === 0) {
            return [];
        }

        // Split into sentences
        const sentences = this.splitSentences(text);

        // Generate candidate keywords
        const phrases = this.generateCandidateKeywords(sentences);

        if (phrases.length === 0) {
            return [];
        }

        // Calculate word scores
        const wordScores = this.calculateWordScores(phrases);

        // Calculate phrase scores
        const phraseScores = this.calculatePhraseScores(phrases, wordScores);

        // Sort by score and return top N
        const sortedKeywords = Array.from(phraseScores.entries())
            .map(([keyword, score]) => ({ keyword, score }))
            .sort((a, b) => b.score - a.score)
            .slice(0, topN);

        return sortedKeywords;
    }

    /**
     * Extract just keyword strings (no scores)
     */
    extractKeywordStrings(text, topN = 20) {
        const keywords = this.extractKeywords(text, topN);
        return keywords.map(k => k.keyword);
    }

    /**
     * Extract ranked keywords with scores
     */
    extractRankedKeywords(text, topN = 20) {
        return this.extractKeywords(text, topN);
    }
}
