/**
 * COPY ARTICLE BUTTON - Standalone Script
 *
 * Installation:
 * 1. Copy to: content/themes/dein-theme/assets/js/copy-article.js
 * 2. In default.hbs vor </body>:
 *    <script src="{{asset "js/copy-article.js"}}" defer></script>
 *
 * Features:
 * - Extrahiert Artikel als Markdown
 * - Preserviert Formatierung (Headings, Listen, Code, etc.)
 * - Ghost-spezifische Cards werden unterstützt
 * - Dark Mode Support
 * - Anthropic-inspiriertes Design
 */

(function() {
  'use strict';

  // Konfiguration
  const CONFIG = {
    // CSS-Selektoren für verschiedene Ghost Themes
    contentSelectors: [
      '.gh-content',
      '.post-content',
      'article.post',
      '.article-content',
      'main article'
    ],
    titleSelectors: [
      '.gh-article-title',
      '.post-title',
      'h1.article-title',
      'article h1',
      'h1'
    ],
    authorSelectors: [
      '.author-name',
      '.gh-article-author-name',
      '.post-author-name'
    ],
    dateSelectors: [
      '.post-date',
      '.gh-article-date',
      'time.published',
      'time'
    ],
    // Button-Text
    buttonText: {
      default: 'Artikel kopieren',
      copied: '✓ Kopiert!',
      error: '❌ Fehler'
    },
    // Visuelle Feedback-Dauer (ms)
    feedbackDuration: 2000
  };

  // Nur auf Post-Seiten ausführen
  const articleContent = findElement(CONFIG.contentSelectors);
  if (!articleContent) {
    console.log('[Copy Button] Kein Artikel-Content gefunden');
    return;
  }

  // Button initialisieren
  initCopyButton();

  /**
   * Findet erstes Element das mit Selektor-Liste übereinstimmt
   */
  function findElement(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) return element;
    }
    return null;
  }

  /**
   * Initialisiert Copy-Button
   */
  function initCopyButton() {
    // Button-Container erstellen
    const container = createButtonContainer();

    // Nach Artikel-Content einfügen
    articleContent.appendChild(container);

    // Click-Handler
    const btn = container.querySelector('.copy-article-btn');
    const btnText = container.querySelector('.btn-text');

    btn.addEventListener('click', async function() {
      await handleCopyClick(btn, btnText);
    });
  }

  /**
   * Erstellt Button-Container HTML
   */
  function createButtonContainer() {
    const container = document.createElement('div');
    container.className = 'copy-article-container';
    container.innerHTML = `
      <button class="copy-article-btn" type="button" aria-label="Artikel kopieren">
        <svg class="copy-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span class="btn-text">${CONFIG.buttonText.default}</span>
      </button>
    `;
    return container;
  }

  /**
   * Handhabt Button-Click
   */
  async function handleCopyClick(btn, btnText) {
    try {
      // Artikel-Content extrahieren
      const markdown = extractArticleAsMarkdown();

      // In Zwischenablage kopieren
      await navigator.clipboard.writeText(markdown);

      // Success-Feedback
      showFeedback(btn, btnText, 'success');

    } catch (err) {
      console.error('[Copy Button] Copy failed:', err);
      showFeedback(btn, btnText, 'error');
    }
  }

  /**
   * Zeigt visuelles Feedback
   */
  function showFeedback(btn, btnText, type) {
    const originalText = CONFIG.buttonText.default;
    const feedbackText = type === 'success'
      ? CONFIG.buttonText.copied
      : CONFIG.buttonText.error;

    btnText.textContent = feedbackText;
    btn.classList.add(type === 'success' ? 'copied' : 'error');

    setTimeout(() => {
      btnText.textContent = originalText;
      btn.classList.remove('copied', 'error');
    }, CONFIG.feedbackDuration);
  }

  /**
   * Extrahiert Artikel als Markdown
   */
  function extractArticleAsMarkdown() {
    let markdown = '';

    // Titel
    const title = findElement(CONFIG.titleSelectors);
    if (title) {
      markdown += '# ' + title.textContent.trim() + '\n\n';
    }

    // Autor & Datum
    const meta = extractMetadata();
    if (meta) {
      markdown += meta + '\n\n---\n\n';
    }

    // Hauptcontent
    markdown += processContentToMarkdown(articleContent);

    return markdown.trim();
  }

  /**
   * Extrahiert Metadaten (Autor, Datum)
   */
  function extractMetadata() {
    const author = findElement(CONFIG.authorSelectors);
    const date = findElement(CONFIG.dateSelectors);

    if (!author && !date) return null;

    let meta = '_';
    if (author) meta += 'Von ' + author.textContent.trim();
    if (author && date) meta += ' | ';
    if (date) meta += date.textContent.trim();
    meta += '_';

    return meta;
  }

  /**
   * Konvertiert HTML-Content zu Markdown
   */
  function processContentToMarkdown(element) {
    let md = '';

    function processNode(node) {
      // Text-Knoten
      if (node.nodeType === Node.TEXT_NODE) {
        const text = node.textContent.trim();
        if (text && !isWithinSpecialElement(node)) {
          md += text + ' ';
        }
        return;
      }

      // Element-Knoten
      if (node.nodeType !== Node.ELEMENT_NODE) return;

      // Skip unwanted elements
      if (shouldSkipElement(node)) return;

      const tagName = node.tagName;

      // Headings
      if (tagName.match(/^H[1-6]$/)) {
        const level = parseInt(tagName[1]);
        md += '\n\n' + '#'.repeat(level) + ' ' + node.textContent.trim() + '\n\n';
        return;
      }

      // Paragraphs
      if (tagName === 'P') {
        md += '\n' + node.textContent.trim() + '\n';
        return;
      }

      // Lists
      if (tagName === 'UL' || tagName === 'OL') {
        md += '\n';
        Array.from(node.children).forEach((li, index) => {
          const prefix = tagName === 'UL' ? '- ' : `${index + 1}. `;
          md += prefix + li.textContent.trim() + '\n';
        });
        md += '\n';
        return;
      }

      // Code blocks
      if (tagName === 'PRE') {
        const code = node.querySelector('code');
        if (code) {
          const language = extractCodeLanguage(code);
          md += '\n```' + language + '\n' + code.textContent + '\n```\n\n';
        }
        return;
      }

      // Inline code
      if (tagName === 'CODE' && !node.closest('pre')) {
        md += '`' + node.textContent + '`';
        return;
      }

      // Bold
      if (tagName === 'STRONG' || tagName === 'B') {
        md += '**' + node.textContent + '**';
        return;
      }

      // Italic
      if (tagName === 'EM' || tagName === 'I') {
        md += '_' + node.textContent + '_';
        return;
      }

      // Links
      if (tagName === 'A') {
        md += '[' + node.textContent + '](' + node.href + ')';
        return;
      }

      // Blockquotes
      if (tagName === 'BLOCKQUOTE') {
        const lines = node.textContent.trim().split('\n');
        lines.forEach(line => {
          md += '\n> ' + line.trim();
        });
        md += '\n\n';
        return;
      }

      // Line breaks
      if (tagName === 'BR') {
        md += '\n';
        return;
      }

      // Horizontal rules
      if (tagName === 'HR') {
        md += '\n---\n\n';
        return;
      }

      // Images
      if (tagName === 'IMG') {
        md += processImage(node);
        return;
      }

      // Ghost-spezifische Cards
      if (node.classList.contains('kg-card')) {
        md += processGhostCard(node);
        return;
      }

      // Rekursiv Kinder verarbeiten
      for (const child of node.childNodes) {
        processNode(child);
      }
    }

    processNode(element);

    // Cleanup: Multiple line breaks
    return md.replace(/\n{3,}/g, '\n\n');
  }

  /**
   * Prüft ob Element übersprungen werden soll
   */
  function shouldSkipElement(node) {
    const skipClasses = [
      'copy-article-container',
      'kg-bookmark-card',
      'gh-subscription-form'
    ];

    const skipTags = ['SCRIPT', 'STYLE', 'NOSCRIPT'];

    return skipTags.includes(node.tagName) ||
           skipClasses.some(cls => node.classList.contains(cls));
  }

  /**
   * Prüft ob Node innerhalb eines speziellen Elements ist
   */
  function isWithinSpecialElement(node) {
    let parent = node.parentNode;
    while (parent) {
      if (parent.tagName && ['CODE', 'PRE', 'A'].includes(parent.tagName)) {
        return true;
      }
      parent = parent.parentNode;
    }
    return false;
  }

  /**
   * Extrahiert Programmiersprache aus Code-Block
   */
  function extractCodeLanguage(codeElement) {
    // Versuche className zu parsen (z.B. "language-javascript")
    const match = codeElement.className.match(/language-(\w+)/);
    if (match) return match[1];

    // Ghost-spezifische Data-Attribute
    const lang = codeElement.getAttribute('data-language');
    if (lang) return lang;

    return ''; // Keine Sprache gefunden
  }

  /**
   * Verarbeitet Image-Element
   */
  function processImage(img) {
    const alt = img.alt || 'Image';
    const src = img.src || '';

    // Caption suchen (Ghost-spezifisch)
    const caption = img.closest('figure')?.querySelector('figcaption');

    let md = '\n![' + alt + '](' + src + ')';
    if (caption) {
      md += '\n*' + caption.textContent.trim() + '*';
    }
    md += '\n';

    return md;
  }

  /**
   * Verarbeitet Ghost-spezifische Cards
   */
  function processGhostCard(card) {
    // Image Card
    if (card.classList.contains('kg-image-card')) {
      const img = card.querySelector('img');
      if (img) return processImage(img);
    }

    // Gallery Card
    if (card.classList.contains('kg-gallery-card')) {
      const images = card.querySelectorAll('img');
      let md = '\n**Galerie:**\n\n';
      images.forEach(img => {
        md += processImage(img);
      });
      return md;
    }

    // Embed Card (YouTube, Twitter, etc.)
    if (card.classList.contains('kg-embed-card')) {
      const iframe = card.querySelector('iframe');
      if (iframe) {
        return '\n[Embedded Content: ' + iframe.src + ']\n\n';
      }
    }

    // Bookmark Card
    if (card.classList.contains('kg-bookmark-card')) {
      const link = card.querySelector('a');
      const title = card.querySelector('.kg-bookmark-title');
      if (link) {
        const text = title ? title.textContent : link.href;
        return '\n**Lesezeichen:** [' + text + '](' + link.href + ')\n\n';
      }
    }

    // Button Card
    if (card.classList.contains('kg-button-card')) {
      const button = card.querySelector('a');
      if (button) {
        return '\n**→ [' + button.textContent.trim() + '](' + button.href + ')**\n\n';
      }
    }

    // Callout Card
    if (card.classList.contains('kg-callout-card')) {
      const text = card.textContent.trim();
      return '\n> 💡 ' + text + '\n\n';
    }

    // Fallback: Text extrahieren
    return '\n' + card.textContent.trim() + '\n\n';
  }

})();
