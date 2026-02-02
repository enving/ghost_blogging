# Copy-Paste Button für Ghost Blog

## 🎯 Ziel

Nutzer können mit einem Klick den gesamten Text-Content eines Blog-Posts kopieren - wie bei Anthropic's Claude.ai Conversations.

## 📋 Inspiration: Anthropic's Implementierung

**Was Anthropic macht**:
1. "Copy" Button neben jedem Code-Block
2. "Copy conversation" Button für gesamten Chat
3. Kopiert nur Text-Content, kein HTML/Styling
4. Visuelles Feedback: Button zeigt "✓ Copied!" kurz an

## 🔧 Implementierung für Ghost

### Option 1: Einfacher Copy-Button (Vanilla JS)

**In Ghost Theme** (`post.hbs` oder `default.hbs`):

```html
<!-- Am Ende des Post-Contents -->
<article class="post-content">
  {{content}}

  <!-- Copy Button -->
  <div class="copy-post-container">
    <button id="copy-post-btn" class="copy-button">
      <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
        <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2"/>
      </svg>
      <span class="copy-text">Copy full article</span>
      <span class="copied-text" style="display:none;">✓ Copied!</span>
    </button>
  </div>
</article>

<script>
document.getElementById('copy-post-btn').addEventListener('click', function() {
  // Get only the text content, not HTML
  const postContent = document.querySelector('.post-content');

  // Extract text while preserving structure
  let textContent = '';

  // Get title
  const title = document.querySelector('.post-title, h1.article-title');
  if (title) {
    textContent += title.innerText + '\n\n';
  }

  // Get main content - extract text with basic formatting
  const walker = document.createTreeWalker(
    postContent,
    NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
    null
  );

  let node;
  while (node = walker.nextNode()) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent.trim();
      if (text) textContent += text + ' ';
    } else if (node.nodeName === 'BR' || node.nodeName === 'P') {
      textContent += '\n';
    } else if (node.nodeName.match(/^H[1-6]$/)) {
      textContent += '\n\n' + '#'.repeat(parseInt(node.nodeName[1])) + ' ';
    } else if (node.nodeName === 'CODE') {
      textContent += '`';
    } else if (node.nodeName === 'PRE') {
      textContent += '\n```\n';
    }
  }

  // Copy to clipboard
  navigator.clipboard.writeText(textContent.trim()).then(() => {
    // Visual feedback
    const btn = this;
    const copyText = btn.querySelector('.copy-text');
    const copiedText = btn.querySelector('.copied-text');

    copyText.style.display = 'none';
    copiedText.style.display = 'inline';

    setTimeout(() => {
      copyText.style.display = 'inline';
      copiedText.style.display = 'none';
    }, 2000);
  }).catch(err => {
    console.error('Failed to copy:', err);
    alert('Copy failed. Please select and copy manually.');
  });
});
</script>

<style>
.copy-post-container {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e5e5;
  text-align: center;
}

.copy-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: all 0.2s;
}

.copy-button:hover {
  background: #eee;
  border-color: #ccc;
}

.copy-button:active {
  transform: scale(0.98);
}

.copy-icon {
  color: #666;
}

.copied-text {
  color: #10b981;
  font-weight: 500;
}
</style>
```

### Option 2: Bessere Markdown-Extraktion

**Für sauberes Markdown statt Plain Text**:

```javascript
function extractMarkdown(element) {
  let markdown = '';

  const processNode = (node, level = 0) => {
    // Headings
    if (node.nodeName.match(/^H[1-6]$/)) {
      const hLevel = parseInt(node.nodeName[1]);
      markdown += '\n\n' + '#'.repeat(hLevel) + ' ' + node.textContent.trim() + '\n';
      return;
    }

    // Paragraphs
    if (node.nodeName === 'P') {
      markdown += '\n' + node.textContent.trim() + '\n';
      return;
    }

    // Lists
    if (node.nodeName === 'UL' || node.nodeName === 'OL') {
      Array.from(node.children).forEach((li, index) => {
        const prefix = node.nodeName === 'UL' ? '- ' : `${index + 1}. `;
        markdown += prefix + li.textContent.trim() + '\n';
      });
      markdown += '\n';
      return;
    }

    // Code blocks
    if (node.nodeName === 'PRE') {
      const code = node.querySelector('code');
      if (code) {
        markdown += '\n```\n' + code.textContent + '\n```\n';
      }
      return;
    }

    // Inline code
    if (node.nodeName === 'CODE' && node.parentNode.nodeName !== 'PRE') {
      markdown += '`' + node.textContent + '`';
      return;
    }

    // Bold
    if (node.nodeName === 'STRONG' || node.nodeName === 'B') {
      markdown += '**' + node.textContent + '**';
      return;
    }

    // Italic
    if (node.nodeName === 'EM' || node.nodeName === 'I') {
      markdown += '_' + node.textContent + '_';
      return;
    }

    // Links
    if (node.nodeName === 'A') {
      markdown += '[' + node.textContent + '](' + node.href + ')';
      return;
    }

    // Blockquotes
    if (node.nodeName === 'BLOCKQUOTE') {
      markdown += '\n> ' + node.textContent.trim() + '\n';
      return;
    }

    // Recursively process child nodes
    if (node.childNodes.length > 0 && !['CODE', 'PRE', 'A'].includes(node.nodeName)) {
      for (const child of node.childNodes) {
        if (child.nodeType === Node.TEXT_NODE) {
          markdown += child.textContent;
        } else if (child.nodeType === Node.ELEMENT_NODE) {
          processNode(child, level + 1);
        }
      }
    }
  };

  processNode(element);
  return markdown.trim();
}

// Usage
document.getElementById('copy-post-btn').addEventListener('click', function() {
  const postContent = document.querySelector('.post-content');
  const title = document.querySelector('.post-title, h1.article-title');

  let markdown = '';
  if (title) {
    markdown = '# ' + title.innerText + '\n\n';
  }

  markdown += extractMarkdown(postContent);

  navigator.clipboard.writeText(markdown).then(/* ... */);
});
```

### Option 3: Ghost Content API (Server-Side)

**Hole Original-Markdown vom Server**:

```javascript
async function copyOriginalMarkdown() {
  const postSlug = window.location.pathname.split('/').filter(Boolean).pop();
  const apiKey = 'YOUR_CONTENT_API_KEY'; // Public key, OK to expose

  try {
    const response = await fetch(
      `https://digitalalchemisten.de/ghost/api/content/posts/slug/${postSlug}/?key=${apiKey}&formats=html,plaintext`
    );
    const data = await response.json();

    if (data.posts && data.posts.length > 0) {
      const post = data.posts[0];

      // Kopiere plaintext (Ghost's interne Markdown-Representation)
      await navigator.clipboard.writeText(post.plaintext);

      // Visual feedback
      showCopiedFeedback();
    }
  } catch (err) {
    console.error('Failed to fetch post:', err);
  }
}
```

## 🎨 Styling wie bei Anthropic

**Minimalistischer Button**:

```css
.copy-button {
  /* Anthropic Style */
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;

  background: transparent;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;

  font-size: 13px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.65);

  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}

.copy-button:hover {
  background: rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.15);
  color: rgba(0, 0, 0, 0.85);
}

.copy-button:active {
  transform: scale(0.97);
}

/* Checkmark animation */
.copied-text {
  color: #10b981;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-2px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## 📦 Ghost Theme Integration

### Schritt 1: Theme-Datei bearbeiten

**In `content/themes/dein-theme/post.hbs`**:

```handlebars
<article class="article-content">
  {{content}}

  {{! Copy Button }}
  <div class="article-actions">
    <button class="copy-article-btn" data-post-slug="{{slug}}">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="9" y="9" width="13" height="13" rx="2"/>
        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
      </svg>
      <span class="btn-text">Copy article</span>
    </button>
  </div>
</article>
```

### Schritt 2: JavaScript in `assets/js/`

**`assets/js/copy-article.js`**:

```javascript
(function() {
  'use strict';

  document.querySelectorAll('.copy-article-btn').forEach(button => {
    button.addEventListener('click', async function() {
      const article = this.closest('.article-content');
      const markdown = extractMarkdown(article);

      try {
        await navigator.clipboard.writeText(markdown);

        // Feedback
        const btnText = this.querySelector('.btn-text');
        const originalText = btnText.textContent;
        btnText.textContent = '✓ Copied!';
        btnText.style.color = '#10b981';

        setTimeout(() => {
          btnText.textContent = originalText;
          btnText.style.color = '';
        }, 2000);
      } catch (err) {
        console.error('Copy failed:', err);
      }
    });
  });

  function extractMarkdown(element) {
    // Implementation from Option 2 above
    // ...
  }
})();
```

### Schritt 3: CSS in `assets/css/`

**`assets/css/copy-button.css`**:

```css
.article-actions {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border, #e5e5e5);
  display: flex;
  justify-content: center;
}

.copy-article-btn {
  /* Styles from above */
}
```

### Schritt 4: Theme Assets einbinden

**In `default.hbs` (im `<head>` oder vor `</body>`)**:

```handlebars
<link rel="stylesheet" href="{{asset "css/copy-button.css"}}">
<script src="{{asset "js/copy-article.js"}}" defer></script>
```

## 🚀 Quick Implementation (Ohne Theme-Edit)

**Ghost Code Injection** (Settings → Code Injection):

**Header**:
```html
<style>
/* Copy Button Styles */
.copy-post-container {
  margin: 2rem 0;
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: #eee;
}
</style>
```

**Footer**:
```html
<script>
if (document.querySelector('.post-content')) {
  // Create button
  const btn = document.createElement('div');
  btn.className = 'copy-post-container';
  btn.innerHTML = '<button class="copy-btn"><span>📋 Copy full article</span></button>';

  // Insert after content
  const content = document.querySelector('.post-content');
  content.appendChild(btn);

  // Add click handler
  btn.querySelector('.copy-btn').addEventListener('click', async function() {
    const text = content.innerText;
    await navigator.clipboard.writeText(text);
    this.innerHTML = '✓ Copied!';
    setTimeout(() => this.innerHTML = '<span>📋 Copy full article</span>', 2000);
  });
}
</script>
```

## 📋 Testing Checklist

- [ ] Button erscheint am Ende jedes Blog-Posts
- [ ] Click kopiert gesamten Text-Content
- [ ] Visual Feedback: "✓ Copied!" für 2 Sekunden
- [ ] Funktioniert auf Desktop (Chrome, Firefox, Safari)
- [ ] Funktioniert auf Mobile (iOS Safari, Chrome Android)
- [ ] Kopierter Text ist gut formatiert (Absätze, Headlines)
- [ ] Code-Blocks werden korrekt kopiert
- [ ] Links bleiben als Markdown erhalten

## 🎯 Nächste Schritte

1. **Jetzt**: Quick Implementation via Code Injection testen
2. **Später**: Proper Theme-Integration für bessere Kontrolle
3. **Optional**: Markdown-Extraktion verfeinern für perfekte Formatting

---

**Inspiration**: https://claude.ai (jeder Chat hat "Copy conversation" Button)
**Ghost Docs**: https://ghost.org/docs/themes/
