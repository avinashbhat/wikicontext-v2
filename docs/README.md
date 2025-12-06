# WikiContext - Client-Side Version

This is a pure JavaScript implementation of WikiContext that runs entirely in the browser and can be hosted on GitHub Pages.

## 🚀 Live Demo

Visit the live app at: `https://yourusername.github.io/wikicontext-v2/`

## 📁 Files

- **index.html** - Main HTML structure and UI
- **styles.css** - Styling and responsive design
- **app.js** - Main application logic and UI handlers
- **wikicontext.js** - WikiContext class (orchestrator)
- **wikipedia-api.js** - Wikipedia API client
- **textrank.js** - TextRank summarization algorithm
- **rake.js** - RAKE keyword extraction algorithm
- **utils.js** - Utility functions for text processing
- **.nojekyll** - Tells GitHub Pages not to use Jekyll

## 🔧 How It Works

1. **User Input**: Enter a Wikipedia topic
2. **Wikipedia API**: Fetches article content via Wikipedia's public API
3. **RAKE**: Extracts important keywords from the article
4. **Keyword Matching**: Matches keywords with Wikipedia links to find prerequisites
5. **TextRank**: Summarizes main article and prerequisites using graph-based ranking
6. **Display**: Shows results in a clean, responsive UI

## 🌟 Features

- ✅ No server required - runs entirely in the browser
- ✅ Free hosting on GitHub Pages
- ✅ TextRank algorithm for extractive summarization
- ✅ RAKE algorithm for keyword extraction
- ✅ Automatic prerequisite identification
- ✅ Disambiguation handling
- ✅ Responsive design
- ✅ URL sharing support

## 📊 Algorithm Implementations

### TextRank Summarization
- Builds sentence similarity matrix using word overlap
- Applies PageRank algorithm to score sentences
- Extracts top-ranked sentences while preserving order

### RAKE Keyword Extraction
- Splits text into candidate phrases at stopwords
- Calculates word scores based on co-occurrence
- Ranks phrases by combined word scores

## 🎨 Customization

You can customize the app by modifying:
- **styles.css** - Change colors, fonts, layout
- **index.html** - Modify UI structure
- **app.js** - Adjust default settings (max prereqs, summary ratio)

## 🔬 Limitations

Compared to the Python version:
- **No Transformer Models**: Browser can't run BART, T5, or Pegasus
- **Simpler NLP**: JavaScript NLP libraries are less sophisticated
- **Performance**: May be slower on very large articles
- **Summary Quality**: TextRank is extractive only (no abstractive summaries)

## 🛠️ Development

To test locally:

```bash
# Simple HTTP server with Python
cd docs
python -m http.server 8000

# Or with Node.js
npx http-server
```

Then open `http://localhost:8000` in your browser.

## 📝 Deployment to GitHub Pages

1. Push the `docs/` folder to your GitHub repository
2. Go to repository Settings → Pages
3. Set Source to "Deploy from a branch"
4. Select branch: `main` and folder: `/docs`
5. Click Save
6. Wait a few minutes for deployment
7. Your app will be live at `https://yourusername.github.io/wikicontext-v2/`

## 🐛 Troubleshooting

**CORS errors**: Should not occur as Wikipedia API supports CORS, but if you see them, make sure you're accessing via HTTP/HTTPS (not `file://`)

**Page not found**: Check that the Wikipedia article name is spelled correctly. The app will suggest alternatives if available.

**Slow performance**: Large articles with many links may take time to process. Consider reducing max prerequisites.

**Empty summaries**: Some Wikipedia articles are stubs or have limited content. The app will show a message if content is insufficient.

## 📄 License

Same as parent project - see LICENSE file in root directory.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the client-side implementation!
