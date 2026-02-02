/**
 * ENHANCED COPY ARTICLE BUTTON + GLOSSARY + KNOWLEDGE LINKS
 *
 * Features:
 * - Copy-to-Clipboard Button (wie Anthropic)
 * - Inline-Glossar für Fachbegriffe
 * - Wikilink-Support ([[Begriff]]) → automatische Links
 * - Backlinks-Anzeige (welche Posts verlinken hierher)
 * - Related Posts basierend auf Tags + Links
 * - Knowledge Graph Integration (optional)
 *
 * Installation:
 * 1. Copy to: content/themes/dein-theme/assets/js/enhanced-copy.js
 * 2. In default.hbs:
 *    <script src="{{asset "js/enhanced-copy.js"}}" defer></script>
 */

(function() {
  'use strict';

  // ==================== KONFIGURATION ====================

  const CONFIG = {
    // Ghost Content API (für Related Posts & Backlinks)
    ghostApiUrl: window.location.origin + '/ghost/api/content',
    ghostApiKey: 'YOUR_CONTENT_API_KEY', // TODO: Setze deinen Public Content API Key

    // Glossar-Begriffe (später aus Ghost-Seite laden)
    glossary: {
      'Ghost': {
        definition: 'Open-Source Blogging-Plattform, fokussiert auf Publishing.',
        url: '/glossar/ghost'
      },
      'MCP': {
        definition: 'Model Context Protocol - Schnittstelle zwischen KI und Tools.',
        url: '/glossar/mcp'
      },
      'VPS': {
        definition: 'Virtual Private Server - Virtueller dedizierter Server.',
        url: '/glossar/vps'
      },
      'DSGVO': {
        definition: 'Datenschutz-Grundverordnung der EU.',
        url: '/glossar/dsgvo'
      },
      'Docker': {
        definition: 'Container-Technologie für isolierte Anwendungen.',
        url: '/glossar/docker'
      },
      'Self-Hosting': {
        definition: 'Eigenbetrieb von Software auf eigener Infrastruktur.',
        url: '/glossar/self-hosting'
      }
    },

    // Feature Toggles
    features: {
      copyButton: true,
      glossaryTooltips: true,
      wikilinks: true,
      relatedPosts: true,
      backlinks: true,
      knowledgeGraph: false // Später aktivieren
    },

    // Selektoren
    selectors: {
      content: ['.gh-content', '.post-content', 'article.post'],
      title: ['.gh-article-title', '.post-title', 'h1'],
      author: ['.author-name', '.gh-article-author-name'],
      date: ['.post-date', '.gh-article-date', 'time']
    },

    // UI-Texte
    text: {
      copyButton: 'Artikel kopieren',
      copied: '✓ Kopiert!',
      error: '❌ Fehler',
      relatedPosts: 'Verwandte Artikel',
      backlinks: 'Erwähnt in',
      glossary: 'Glossar'
    }
  };

  // ==================== INITIALISIERUNG ====================

  const articleContent = findElement(CONFIG.selectors.content);
  if (!articleContent) return;

  // Features initialisieren
  if (CONFIG.features.copyButton) initCopyButton();
  if (CONFIG.features.glossaryTooltips) initGlossary();
  if (CONFIG.features.wikilinks) convertWikilinks();
  if (CONFIG.features.relatedPosts) loadRelatedPosts();
  if (CONFIG.features.backlinks) loadBacklinks();

  // ==================== COPY BUTTON ====================

  function initCopyButton() {
    const container = document.createElement('div');
    container.className = 'copy-article-container';
    container.innerHTML = `
      <button class="copy-article-btn" type="button">
        <svg class="copy-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span class="btn-text">${CONFIG.text.copyButton}</span>
      </button>
    `;

    articleContent.appendChild(container);

    const btn = container.querySelector('.copy-article-btn');
    const btnText = container.querySelector('.btn-text');

    btn.addEventListener('click', async () => {
      try {
        const markdown = extractArticleAsMarkdown();
        await navigator.clipboard.writeText(markdown);

        btnText.textContent = CONFIG.text.copied;
        btn.classList.add('copied');

        setTimeout(() => {
          btnText.textContent = CONFIG.text.copyButton;
          btn.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Copy failed:', err);
        btnText.textContent = CONFIG.text.error;
        setTimeout(() => {
          btnText.textContent = CONFIG.text.copyButton;
        }, 2000);
      }
    });
  }

  // ==================== GLOSSAR ====================

  function initGlossary() {
    // Lade Glossar dynamisch von Ghost-Seite (falls vorhanden)
    loadGlossaryFromGhost().then(externalGlossary => {
      if (externalGlossary) {
        Object.assign(CONFIG.glossary, externalGlossary);
      }

      // Füge Tooltips hinzu
      addGlossaryTooltips();
    });
  }

  async function loadGlossaryFromGhost() {
    try {
      // Versuche Glossar-Seite zu laden
      const response = await fetch(
        `${CONFIG.ghostApiUrl}/pages/slug/glossar/?key=${CONFIG.ghostApiKey}&formats=html`
      );

      if (!response.ok) return null;

      const data = await response.json();
      if (!data.pages || !data.pages[0]) return null;

      // Parse Glossar aus HTML (z.B. <dl> Liste)
      const parser = new DOMParser();
      const doc = parser.parseFromString(data.pages[0].html, 'text/html');

      const glossary = {};
      const terms = doc.querySelectorAll('dt');
      const definitions = doc.querySelectorAll('dd');

      terms.forEach((term, index) => {
        const key = term.textContent.trim();
        const definition = definitions[index]?.textContent.trim();
        if (definition) {
          glossary[key] = {
            definition,
            url: `/glossar#${key.toLowerCase().replace(/\s+/g, '-')}`
          };
        }
      });

      return glossary;
    } catch (err) {
      console.warn('Glossar konnte nicht geladen werden:', err);
      return null;
    }
  }

  function addGlossaryTooltips() {
    // Finde alle Textstellen im Artikel
    const walker = document.createTreeWalker(
      articleContent,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          // Skip Code, Links, bereits verarbeitete
          if (node.parentElement.closest('code, pre, a, .glossary-term')) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
      textNodes.push(node);
    }

    // Ersetze Glossar-Begriffe
    textNodes.forEach(textNode => {
      let html = textNode.textContent;
      let hasReplacement = false;

      Object.keys(CONFIG.glossary).forEach(term => {
        const { definition, url } = CONFIG.glossary[term];

        // Regex: Finde ganzes Wort (case-insensitive)
        const regex = new RegExp(`\\b(${term})\\b`, 'gi');

        if (regex.test(html)) {
          html = html.replace(regex, (match) => {
            return `<abbr class="glossary-term" title="${definition}" data-url="${url}">${match}</abbr>`;
          });
          hasReplacement = true;
        }
      });

      if (hasReplacement) {
        const span = document.createElement('span');
        span.innerHTML = html;
        textNode.parentNode.replaceChild(span, textNode);
      }
    });

    // Tooltip-Interaktionen
    document.querySelectorAll('.glossary-term').forEach(term => {
      term.addEventListener('click', (e) => {
        e.preventDefault();
        const url = term.getAttribute('data-url');
        if (url) window.location.href = url;
      });
    });
  }

  // ==================== WIKILINKS ====================

  function convertWikilinks() {
    // Finde alle [[Begriff]] im Content
    const walker = document.createTreeWalker(
      articleContent,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: (node) => {
          if (node.parentElement.closest('code, pre, a')) {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
      if (/\[\[.*?\]\]/.test(node.textContent)) {
        textNodes.push(node);
      }
    }

    textNodes.forEach(textNode => {
      let html = textNode.textContent;

      // [[Begriff]] → Link
      html = html.replace(/\[\[(.*?)\]\]/g, (match, linkText) => {
        const slug = slugify(linkText);
        return `<a href="/${slug}" class="wikilink">${linkText}</a>`;
      });

      const span = document.createElement('span');
      span.innerHTML = html;
      textNode.parentNode.replaceChild(span, textNode);
    });
  }

  // ==================== RELATED POSTS ====================

  async function loadRelatedPosts() {
    try {
      // Hole aktuellen Post-Slug
      const currentSlug = getCurrentPostSlug();
      if (!currentSlug) return;

      // Hole aktuellen Post mit Tags
      const response = await fetch(
        `${CONFIG.ghostApiUrl}/posts/slug/${currentSlug}/?key=${CONFIG.ghostApiKey}&include=tags`
      );

      if (!response.ok) return;

      const data = await response.json();
      const currentPost = data.posts[0];

      if (!currentPost || !currentPost.tags || currentPost.tags.length === 0) return;

      // Finde Posts mit gleichen Tags
      const tagSlugs = currentPost.tags.map(tag => tag.slug);
      const tagFilter = tagSlugs.map(slug => `tag:${slug}`).join(',');

      const relatedResponse = await fetch(
        `${CONFIG.ghostApiUrl}/posts/?key=${CONFIG.ghostApiKey}&filter=${tagFilter}&limit=5`
      );

      if (!relatedResponse.ok) return;

      const relatedData = await relatedResponse.json();
      const relatedPosts = relatedData.posts.filter(post => post.slug !== currentSlug);

      if (relatedPosts.length === 0) return;

      // Rendere Related Posts
      renderRelatedPosts(relatedPosts);

    } catch (err) {
      console.warn('Related Posts konnten nicht geladen werden:', err);
    }
  }

  function renderRelatedPosts(posts) {
    const container = document.createElement('aside');
    container.className = 'related-posts-section';
    container.innerHTML = `
      <h3>${CONFIG.text.relatedPosts}</h3>
      <ul class="related-posts-list">
        ${posts.map(post => `
          <li>
            <a href="${post.url}">
              <span class="related-post-title">${post.title}</span>
              ${post.custom_excerpt ? `<span class="related-post-excerpt">${post.custom_excerpt}</span>` : ''}
            </a>
          </li>
        `).join('')}
      </ul>
    `;

    // Füge vor Copy-Button ein
    const copyContainer = articleContent.querySelector('.copy-article-container');
    if (copyContainer) {
      articleContent.insertBefore(container, copyContainer);
    } else {
      articleContent.appendChild(container);
    }
  }

  // ==================== BACKLINKS ====================

  async function loadBacklinks() {
    try {
      const currentSlug = getCurrentPostSlug();
      if (!currentSlug) return;

      // Hole alle Posts
      const response = await fetch(
        `${CONFIG.ghostApiUrl}/posts/?key=${CONFIG.ghostApiKey}&limit=all&formats=html`
      );

      if (!response.ok) return;

      const data = await response.json();

      // Finde Posts die auf aktuellen Post verlinken
      const backlinks = data.posts.filter(post => {
        if (post.slug === currentSlug) return false;

        // Check ob HTML einen Link zum aktuellen Post enthält
        return post.html && post.html.includes(`href="/${currentSlug}"`);
      });

      if (backlinks.length === 0) return;

      renderBacklinks(backlinks);

    } catch (err) {
      console.warn('Backlinks konnten nicht geladen werden:', err);
    }
  }

  function renderBacklinks(posts) {
    const container = document.createElement('aside');
    container.className = 'backlinks-section';
    container.innerHTML = `
      <h4>${CONFIG.text.backlinks}</h4>
      <ul class="backlinks-list">
        ${posts.map(post => `
          <li><a href="${post.url}">${post.title}</a></li>
        `).join('')}
      </ul>
    `;

    // Füge vor Related Posts ein
    const relatedSection = articleContent.querySelector('.related-posts-section');
    if (relatedSection) {
      articleContent.insertBefore(container, relatedSection);
    } else {
      const copyContainer = articleContent.querySelector('.copy-article-container');
      if (copyContainer) {
        articleContent.insertBefore(container, copyContainer);
      } else {
        articleContent.appendChild(container);
      }
    }
  }

  // ==================== MARKDOWN EXTRACTION ====================

  function extractArticleAsMarkdown() {
    let md = '';

    // Titel
    const title = findElement(CONFIG.selectors.title);
    if (title) {
      md += '# ' + title.textContent.trim() + '\n\n';
    }

    // Metadata
    const author = findElement(CONFIG.selectors.author);
    const date = findElement(CONFIG.selectors.date);
    if (author || date) {
      md += '_';
      if (author) md += 'Von ' + author.textContent.trim();
      if (author && date) md += ' | ';
      if (date) md += date.textContent.trim();
      md += '_\n\n---\n\n';
    }

    // Content
    md += processContentToMarkdown(articleContent);

    return md.trim();
  }

  function processContentToMarkdown(element) {
    let md = '';

    function processNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent.trim();
        if (text) md += text + ' ';
        return;
      }

      if (node.nodeType !== Node.ELEMENT_NODE) return;

      // Skip unwanted
      if (shouldSkipElement(node)) return;

      const tag = node.tagName;

      // Headings
      if (tag.match(/^H[1-6]$/)) {
        const level = parseInt(tag[1]);
        md += '\n\n' + '#'.repeat(level) + ' ' + node.textContent.trim() + '\n\n';
        return;
      }

      // Paragraphs
      if (tag === 'P') {
        md += '\n' + node.textContent.trim() + '\n';
        return;
      }

      // Lists
      if (tag === 'UL' || tag === 'OL') {
        md += '\n';
        Array.from(node.children).forEach((li, i) => {
          const prefix = tag === 'UL' ? '- ' : `${i + 1}. `;
          md += prefix + li.textContent.trim() + '\n';
        });
        md += '\n';
        return;
      }

      // Code
      if (tag === 'PRE') {
        const code = node.querySelector('code');
        if (code) {
          const lang = code.className.match(/language-(\w+)/)?.[1] || '';
          md += '\n```' + lang + '\n' + code.textContent + '\n```\n\n';
        }
        return;
      }

      if (tag === 'CODE' && !node.closest('pre')) {
        md += '`' + node.textContent + '`';
        return;
      }

      // Formatting
      if (tag === 'STRONG' || tag === 'B') {
        md += '**' + node.textContent + '**';
        return;
      }

      if (tag === 'EM' || tag === 'I') {
        md += '_' + node.textContent + '_';
        return;
      }

      // Links
      if (tag === 'A') {
        md += '[' + node.textContent + '](' + node.href + ')';
        return;
      }

      // Blockquotes
      if (tag === 'BLOCKQUOTE') {
        node.textContent.trim().split('\n').forEach(line => {
          md += '\n> ' + line.trim();
        });
        md += '\n\n';
        return;
      }

      // Misc
      if (tag === 'BR') md += '\n';
      if (tag === 'HR') md += '\n---\n\n';

      // Images
      if (tag === 'IMG') {
        md += '\n![' + (node.alt || 'Image') + '](' + node.src + ')\n';
        return;
      }

      // Recurse
      for (const child of node.childNodes) {
        processNode(child);
      }
    }

    processNode(element);
    return md.replace(/\n{3,}/g, '\n\n');
  }

  function shouldSkipElement(node) {
    const skipClasses = [
      'copy-article-container',
      'related-posts-section',
      'backlinks-section',
      'kg-bookmark-card'
    ];

    const skipTags = ['SCRIPT', 'STYLE', 'NOSCRIPT'];

    return skipTags.includes(node.tagName) ||
           skipClasses.some(cls => node.classList.contains(cls));
  }

  // ==================== HELPER FUNCTIONS ====================

  function findElement(selectors) {
    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el) return el;
    }
    return null;
  }

  function getCurrentPostSlug() {
    const path = window.location.pathname;
    const match = path.match(/\/([^\/]+)\/?$/);
    return match ? match[1] : null;
  }

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/ä/g, 'ae')
      .replace(/ö/g, 'oe')
      .replace(/ü/g, 'ue')
      .replace(/ß/g, 'ss')
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  }

})();
