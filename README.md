## WikiContext

Wikipedia articles are hardly lucid. There is always some kind of jargon which floats around, which is difficult to understand in layman's term. This is an attempt to simplify the understanding of any Wikipedia article by providing a summary of some of the key concepts of the said article.
We provide the context, hence the name WikiContext.

### Beneath the hood

WikiContext makes use of extractive text summarization, using [TextRank](https://www.aclweb.org/anthology/W04-3252). First step is to define a keyword list based on the hyperlinks present in the article. Once this is done, based on [keyword ranking](http://ceur-ws.org/Vol-706/poster13.pdf), we identify the most relevent keywords in the article. Then the data is fetched and the summarization is performed.

### Usage
WikiContext has two types of searches - linear and recommended. Recommended is, as name suggests, what we recommend. This has a more stringent criteria for the keyword search and we can assure you that this will usually suffice. However, if you are not satisfied with the results, you can try the linear search which will provide you with more results. 

### Contributing
We are doing some active development on this now, because there is a provision to host the app using streamlit! 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/nihaldsouza/wikicontext-v2/streamlit)

