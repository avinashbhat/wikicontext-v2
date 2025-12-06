/**
 * TextRank Algorithm for Text Summarization
 * JavaScript implementation of the TextRank algorithm
 */

class TextRank {
    constructor() {
        this.dampingFactor = 0.85;
        this.minDiff = 0.001;
        this.steps = 100;
    }

    /**
     * Calculate sentence similarity based on word overlap
     */
    sentenceSimilarity(sent1, sent2) {
        // Split into words and remove stopwords
        const words1 = Utils.removeStopwords(Utils.splitIntoWords(sent1));
        const words2 = Utils.removeStopwords(Utils.splitIntoWords(sent2));

        if (words1.length === 0 || words2.length === 0) {
            return 0;
        }

        // Calculate Jaccard similarity
        const set1 = new Set(words1);
        const set2 = new Set(words2);

        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);

        return intersection.size / union.size;
    }

    /**
     * Build similarity matrix for sentences
     */
    buildSimilarityMatrix(sentences) {
        const n = sentences.length;
        const matrix = Array(n).fill(0).map(() => Array(n).fill(0));

        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                if (i !== j) {
                    matrix[i][j] = this.sentenceSimilarity(sentences[i], sentences[j]);
                }
            }
        }

        return matrix;
    }

    /**
     * Normalize matrix rows to create transition probability matrix
     */
    normalizeMatrix(matrix) {
        const n = matrix.length;
        const normalized = Array(n).fill(0).map(() => Array(n).fill(0));

        for (let i = 0; i < n; i++) {
            const rowSum = matrix[i].reduce((sum, val) => sum + val, 0);

            for (let j = 0; j < n; j++) {
                if (rowSum > 0) {
                    normalized[i][j] = matrix[i][j] / rowSum;
                } else {
                    normalized[i][j] = 0;
                }
            }
        }

        return normalized;
    }

    /**
     * PageRank algorithm to score sentences
     */
    pageRank(matrix) {
        const n = matrix.length;
        let scores = Array(n).fill(1.0 / n);
        const normalized = this.normalizeMatrix(matrix);

        for (let step = 0; step < this.steps; step++) {
            const newScores = Array(n).fill(0);
            let diff = 0;

            for (let i = 0; i < n; i++) {
                let score = (1 - this.dampingFactor) / n;

                for (let j = 0; j < n; j++) {
                    score += this.dampingFactor * normalized[j][i] * scores[j];
                }

                newScores[i] = score;
                diff += Math.abs(newScores[i] - scores[i]);
            }

            scores = newScores;

            // Converged
            if (diff < this.minDiff) {
                break;
            }
        }

        return scores;
    }

    /**
     * Extract top N sentences based on TextRank scores
     */
    extractTopSentences(sentences, scores, topN) {
        // Create array of {sentence, score, index} objects
        const sentenceData = sentences.map((sentence, index) => ({
            sentence,
            score: scores[index],
            index
        }));

        // Sort by score (descending)
        sentenceData.sort((a, b) => b.score - a.score);

        // Take top N and sort by original index to maintain order
        const topSentences = sentenceData
            .slice(0, topN)
            .sort((a, b) => a.index - b.index);

        return topSentences.map(item => item.sentence);
    }

    /**
     * Generate summary from text
     * @param {string} text - Input text to summarize
     * @param {number} ratio - Ratio of sentences to keep (0-1)
     * @param {number} sentenceCount - Fixed number of sentences (overrides ratio)
     */
    summarize(text, ratio = 0.2, sentenceCount = null) {
        if (!text || text.trim().length === 0) {
            return '';
        }

        // Clean and split text into sentences
        const cleanText = Utils.cleanWikiText(text);
        const sentences = Utils.splitIntoSentences(cleanText);

        if (sentences.length === 0) {
            return '';
        }

        // If only one sentence, return it
        if (sentences.length === 1) {
            return sentences[0];
        }

        // Calculate number of sentences to extract
        let numSentences;
        if (sentenceCount !== null) {
            numSentences = Math.min(sentenceCount, sentences.length);
        } else {
            numSentences = Math.max(1, Math.ceil(sentences.length * ratio));
        }

        // If we want all or more sentences than available, return original
        if (numSentences >= sentences.length) {
            return sentences.join(' ');
        }

        // Build similarity matrix
        const similarityMatrix = this.buildSimilarityMatrix(sentences);

        // Calculate sentence scores using PageRank
        const scores = this.pageRank(similarityMatrix);

        // Extract top sentences
        const topSentences = this.extractTopSentences(sentences, scores, numSentences);

        return topSentences.join(' ');
    }

    /**
     * Get summary with fixed sentence count (mimics Python version)
     */
    getSummary(text, sentenceCount = 5) {
        return this.summarize(text, null, sentenceCount);
    }

    /**
     * Get summary with ratio
     */
    getSummaryByRatio(text, ratio = 0.2) {
        return this.summarize(text, ratio, null);
    }
}
