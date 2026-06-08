#!/usr/bin/env python3
"""
Generate index.html from content.md
Medium-style publication-quality article: Storage and Databases in System Design
"""

import re, sys, subprocess

subprocess.run(
    [sys.executable, '-m', 'pip', 'install', 'markdown', '--break-system-packages', '-q'],
    capture_output=True
)
import markdown

# ─── 1. Load & pre-process markdown ───────────────────────────────────────────

with open('content.md', 'r') as f:
    md_src = f.read()

IMAGES = [
    ("wal-write-path.png",             "WAL-Based Write Path: client write to fsync durability guarantee"),
    ("acid-properties-pillars.png",    "The Four ACID Storage Properties: Durability, Availability, Consistency, Atomicity"),
    ("nosql-four-types.png",           "Four NoSQL Database Architectures: Document, Key-Value, Wide-Column, Graph"),
    ("cap-theorem-triangle.png",       "CAP Theorem Triangle: CP vs AP Systems in Distributed Storage"),
    ("leader-follower-replication.png","Leader-Follower Replication: Write/Read Paths and Failover Mechanism"),
    ("sharding-strategies.png",        "Sharding Strategies: Range-Based, Hash-Based, and Consistent Hashing Compared"),
    ("hdfs-architecture.png",          "HDFS Architecture: NameNode Metadata Management and DataNode Block Replication"),
    ("big-data-5vs.png",               "The 5 V's of Big Data: Volume, Velocity, Variety, Veracity, Value"),
    ("batch-vs-stream-processing.png", "Batch vs. Stream Processing Architectures with Lambda Architecture"),
    ("delta-lake-architecture.png",    "Delta Lake on Cloud Object Storage: ACID, Time Travel, Schema Enforcement"),
]

counter = [0]
def replace_img(m):
    i = counter[0]; counter[0] += 1
    fn, alt = IMAGES[i] if i < len(IMAGES) else ("diagram.png", "Architecture Diagram")
    return (
        '\n\n<figure class="diagram">\n'
        '  <img src="images/{}" alt="{}" loading="lazy">\n'
        '  <figcaption>{}</figcaption>\n'
        '</figure>\n\n'
    ).format(fn, alt, alt)

md_processed = re.sub(
    r'\[ILLUSTRATION_PROMPT_START\].*?\[ILLUSTRATION_PROMPT_END\]',
    replace_img, md_src, flags=re.DOTALL
)

# ─── 2. Convert markdown → HTML ───────────────────────────────────────────────

md_conv = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])
article_body = md_conv.convert(md_processed)

# ─── 3. CSS ───────────────────────────────────────────────────────────────────

CSS = """
/* ========================================================
   DESIGN TOKENS
   ======================================================== */
:root {
  --bg:            #FDFCF7;
  --bg-alt:        #F4F1E8;
  --bg-alt2:       #EDEADF;
  --text:          #1C1A22;
  --text-muted:    #58566A;
  --text-light:    #8E8B9E;
  --accent:        #B5341A;
  --accent-dark:   #8C2813;
  --accent-bg:     #FDF2EF;
  --code-bg:       #0E1117;
  --code-surface:  #161B27;
  --code-border:   #1E2337;
  --code-text:     #CDD6F4;
  --border:        #E2DECE;
  --border-light:  #EDE9DE;
  --shadow-sm:     0 1px 4px rgba(0,0,0,.06);
  --shadow-md:     0 4px 20px rgba(0,0,0,.08);
  --shadow-lg:     0 12px 48px rgba(0,0,0,.12);
  --radius:        8px;
  --f-display:     'Playfair Display', Georgia, 'Times New Roman', serif;
  --f-body:        'Lora', Georgia, 'Times New Roman', serif;
  --f-sans:        'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --f-code:        'JetBrains Mono', 'Fira Code', Consolas, monospace;
  --col-article:   740px;
}

/* ========================================================
   RESET & BASE
   ======================================================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--f-body);
  font-size: 1.1rem;
  line-height: 1.85;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
img { max-width: 100%; height: auto; display: block; }
a { color: inherit; }

/* ========================================================
   READING PROGRESS BAR
   ======================================================== */
#progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg, var(--accent) 0%, #E86A2B 100%);
  z-index: 9999;
  transition: width .08s linear;
  will-change: width;
}

/* ========================================================
   STICKY SITE NAV
   ======================================================== */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 900;
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .65rem 2rem;
  background: rgba(253,252,247,.93);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-light);
}
.nav-crumb {
  display: flex;
  align-items: center;
  gap: .45rem;
  font-family: var(--f-sans);
  font-size: .75rem;
  color: var(--text-light);
}
.nav-crumb .sep { color: var(--border); }
.nav-crumb .active { color: var(--text-muted); font-weight: 500; }
.nav-logo {
  font-family: var(--f-sans);
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .04em;
  color: var(--accent);
  text-transform: uppercase;
  margin-right: auto;
}
.nav-tag {
  font-family: var(--f-sans);
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: rgba(255,255,255,.5);
  background: var(--accent);
  padding: .15rem .55rem;
  border-radius: 2px;
}

/* ========================================================
   ARTICLE HERO
   ======================================================== */
.article-hero {
  background: linear-gradient(150deg, #0D0F1A 0%, #161829 55%, #1F1525 100%);
  padding: 5.5rem 2rem 4.5rem;
  position: relative;
  overflow: hidden;
}
.article-hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 15% 85%, rgba(181,52,26,.14) 0%, transparent 55%),
    radial-gradient(ellipse at 85% 15%, rgba(40,60,140,.15) 0%, transparent 55%);
  pointer-events: none;
}
.article-hero::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(181,52,26,.4), transparent);
}
.hero-inner {
  max-width: var(--col-article);
  margin: 0 auto;
  position: relative; z-index: 1;
}
.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: .4rem;
  margin-bottom: 1.6rem;
}
.hero-tag {
  font-family: var(--f-sans);
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: rgba(255,255,255,.5);
  background: rgba(255,255,255,.07);
  border: 1px solid rgba(255,255,255,.1);
  padding: .2rem .6rem;
  border-radius: 2px;
}
.hero-title {
  font-family: var(--f-display);
  font-size: clamp(2rem, 5.5vw, 3.25rem);
  font-weight: 900;
  line-height: 1.12;
  color: #FFFFFF;
  margin-bottom: 1.25rem;
  letter-spacing: -.025em;
}
.hero-subtitle {
  font-family: var(--f-body);
  font-size: 1.05rem;
  line-height: 1.7;
  color: rgba(255,255,255,.6);
  margin-bottom: 2rem;
  max-width: 620px;
  font-style: italic;
}
.hero-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .9rem;
  font-family: var(--f-sans);
  font-size: .78rem;
  color: rgba(255,255,255,.35);
}
.hero-meta .dot { color: rgba(255,255,255,.15); font-size: 1rem; }

/* ========================================================
   TABLE OF CONTENTS
   ======================================================== */
.toc-outer {
  max-width: var(--col-article);
  margin: 3rem auto 0;
  padding: 0 2rem;
}
.toc-box {
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 1.75rem 2rem;
}
.toc-heading {
  font-family: var(--f-sans);
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 1.1rem;
}
#toc-list {
  list-style: none;
  counter-reset: toc;
}
#toc-list li.toc-h2 {
  counter-increment: toc;
  margin-bottom: .4rem;
}
#toc-list li.toc-h2 > a {
  display: flex;
  align-items: flex-start;
  gap: .6rem;
  font-family: var(--f-sans);
  font-size: .86rem;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  line-height: 1.4;
  transition: color .15s;
}
#toc-list li.toc-h2 > a::before {
  content: counter(toc, decimal-leading-zero);
  font-family: var(--f-code);
  font-size: .68rem;
  color: var(--accent);
  min-width: 1.6rem;
  padding-top: .15rem;
  flex-shrink: 0;
}
#toc-list li.toc-h2 > a:hover { color: var(--accent); }
#toc-list li.toc-h3 {
  margin: .15rem 0 .15rem 2.2rem;
}
#toc-list li.toc-h3 > a {
  font-family: var(--f-sans);
  font-size: .79rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color .15s;
  line-height: 1.4;
  display: block;
}
#toc-list li.toc-h3 > a:hover { color: var(--accent); }
#toc-list a.active { color: var(--accent) !important; font-weight: 600; }

/* ========================================================
   ARTICLE BODY — CONTAINER
   ======================================================== */
.article-body {
  max-width: var(--col-article);
  margin: 0 auto;
  padding: 4rem 2rem 6rem;
}

/* ── HEADINGS ─────────────────────────────────────────── */
.article-body h1 { display: none; } /* shown in hero */

.article-body h2 {
  font-family: var(--f-display);
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text);
  margin-top: 4.5rem;
  margin-bottom: 1.4rem;
  letter-spacing: -.02em;
  padding-top: 2rem;
  border-top: 2px solid var(--border);
  scroll-margin-top: 5rem;
}
.article-body h2:first-of-type {
  margin-top: 0;
  border-top: none;
  padding-top: 0;
}

.article-body h3 {
  font-family: var(--f-display);
  font-size: 1.28rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text);
  margin-top: 3rem;
  margin-bottom: 1rem;
  letter-spacing: -.01em;
  scroll-margin-top: 5rem;
}
.article-body h3::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 1em;
  background: var(--accent);
  margin-right: .55rem;
  vertical-align: middle;
  border-radius: 2px;
  position: relative;
  top: -.1em;
}

.article-body h4 {
  font-family: var(--f-sans);
  font-size: .88rem;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--text);
  margin-top: 2.25rem;
  margin-bottom: .75rem;
  scroll-margin-top: 5rem;
}

/* ── PARAGRAPHS ───────────────────────────────────────── */
.article-body p {
  margin-bottom: 1.45rem;
  color: var(--text);
}

/* ── BLOCKQUOTE ───────────────────────────────────────── */
.article-body blockquote {
  margin: 2rem 0;
  padding: 1.25rem 1.6rem;
  background: var(--accent-bg);
  border-left: 4px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
}
.article-body blockquote p {
  margin: 0;
  font-style: italic;
  font-size: 1.05rem;
  color: var(--text-muted);
  line-height: 1.7;
}

/* ── HORIZONTAL RULE ──────────────────────────────────── */
.article-body hr {
  border: none;
  border-top: 2px solid var(--border);
  margin: 3.5rem 0;
}

/* ── LINKS ────────────────────────────────────────────── */
.article-body a {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-color: rgba(181,52,26,.3);
  text-underline-offset: 3px;
  transition: color .15s, text-decoration-color .15s;
}
.article-body a:hover {
  color: var(--accent-dark);
  text-decoration-color: var(--accent-dark);
}

/* ── BOLD / EM ────────────────────────────────────────── */
.article-body strong { font-weight: 700; }
.article-body em { font-style: italic; }

/* ── LISTS ────────────────────────────────────────────── */
.article-body ul,
.article-body ol {
  margin: 0 0 1.5rem 1.6rem;
  padding: 0;
}
.article-body li {
  margin-bottom: .45rem;
  line-height: 1.7;
  color: var(--text);
}
.article-body li > ul,
.article-body li > ol { margin-top: .4rem; margin-bottom: 0; }

/* ── INLINE CODE ──────────────────────────────────────── */
.article-body :not(pre) > code {
  font-family: var(--f-code);
  font-size: .82em;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: .12em .38em;
  color: var(--accent);
  word-break: break-word;
}

/* ── CODE BLOCKS ──────────────────────────────────────── */
.article-body pre {
  margin: 2rem -0.5rem;
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--code-bg);
  border: 1px solid var(--code-border);
  box-shadow: var(--shadow-md);
  position: relative;
}
.article-body pre code {
  display: block;
  padding: 1.4rem 1.6rem;
  font-family: var(--f-code);
  font-size: .78rem;
  line-height: 1.75;
  overflow-x: auto;
  color: var(--code-text);
  tab-size: 2;
}
/* Prevent hljs from overriding our background */
.article-body pre .hljs { background: transparent !important; padding: 0 !important; }
/* Language label */
.article-body pre[class*="language-"]::before,
.article-body pre code[class*="language-"]::before {
  content: attr(data-lang);
}
.code-label {
  position: absolute;
  top: 0; right: 0;
  background: var(--code-surface);
  border-bottom: 1px solid var(--code-border);
  border-left: 1px solid var(--code-border);
  border-radius: 0 var(--radius) 0 var(--radius);
  font-family: var(--f-code);
  font-size: .65rem;
  font-weight: 500;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: rgba(205,214,244,.45);
  padding: .2rem .55rem;
}

/* ── TABLES ───────────────────────────────────────────── */
.article-body .table-wrap {
  overflow-x: auto;
  margin: 2rem 0;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
.article-body table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--f-sans);
  font-size: .85rem;
  min-width: 480px;
}
.article-body thead th {
  background: var(--bg-alt);
  border-bottom: 2px solid var(--border);
  padding: .7rem 1rem;
  text-align: left;
  font-weight: 700;
  font-size: .75rem;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}
.article-body tbody td {
  border-bottom: 1px solid var(--border-light);
  padding: .6rem 1rem;
  color: var(--text-muted);
  vertical-align: top;
  line-height: 1.55;
}
.article-body tbody tr:last-child td { border-bottom: none; }
.article-body tbody tr:nth-child(even) td { background: var(--bg-alt); }

/* ── FIGURES / DIAGRAMS ───────────────────────────────── */
figure.diagram {
  margin: 2.5rem -0.5rem;
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-md);
}
figure.diagram img {
  width: 100%;
  height: auto;
  display: block;
  background: var(--bg-alt2);
  min-height: 200px;
  object-fit: contain;
}
figure.diagram figcaption {
  padding: .7rem 1.25rem;
  font-family: var(--f-sans);
  font-size: .77rem;
  color: var(--text-light);
  border-top: 1px solid var(--border);
  font-style: italic;
  line-height: 1.5;
}

/* ── ARTICLE FOOTER ───────────────────────────────────── */
.article-footer {
  max-width: var(--col-article);
  margin: 0 auto;
  padding: 2.5rem 2rem 5rem;
  border-top: 2px solid var(--border);
}
.footer-note {
  font-family: var(--f-sans);
  font-size: .82rem;
  color: var(--text-light);
  line-height: 1.7;
}
.footer-note strong { color: var(--text-muted); }
.footer-tags {
  display: flex;
  flex-wrap: wrap;
  gap: .4rem;
  margin-top: 1.25rem;
}
.footer-tag {
  font-family: var(--f-sans);
  font-size: .72rem;
  font-weight: 500;
  color: var(--text-muted);
  background: var(--bg-alt);
  border: 1px solid var(--border);
  padding: .2rem .6rem;
  border-radius: 3px;
}

/* ── RESPONSIVE ───────────────────────────────────────── */
@media (min-width: 860px) {
  .article-body pre { margin-left: -2rem; margin-right: -2rem; }
  figure.diagram     { margin-left: -2rem; margin-right: -2rem; }
}
@media (max-width: 640px) {
  body { font-size: 1rem; }
  .article-hero { padding: 4rem 1.25rem 3.5rem; }
  .hero-title { font-size: 1.85rem; }
  .article-body { padding: 2.5rem 1.25rem 4rem; }
  .toc-outer { padding: 0 1.25rem; }
  .toc-box { padding: 1.25rem 1.25rem; }
  .article-footer { padding: 2rem 1.25rem 4rem; }
  .article-body h2 { font-size: 1.55rem; }
  .article-body h3 { font-size: 1.15rem; }
  .site-nav { padding: .6rem 1.25rem; }
  .article-body pre { margin-left: 0; margin-right: 0; }
  figure.diagram { margin-left: 0; margin-right: 0; }
}
"""

# ─── 4. JavaScript ────────────────────────────────────────────────────────────

JS = """
(function () {
  'use strict';

  /* ---- Reading progress bar ---- */
  const bar = document.getElementById('progress-bar');
  if (bar) {
    const updateBar = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const pct = scrollable > 0 ? Math.min((window.scrollY / scrollable) * 100, 100) : 0;
      bar.style.width = pct + '%';
    };
    window.addEventListener('scroll', updateBar, { passive: true });
    updateBar();
  }

  /* ---- Wrap tables for horizontal scroll ---- */
  document.querySelectorAll('.article-body table').forEach(table => {
    if (!table.parentElement.classList.contains('table-wrap')) {
      const wrap = document.createElement('div');
      wrap.className = 'table-wrap';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    }
  });

  /* ---- Add language labels to code blocks ---- */
  document.querySelectorAll('.article-body pre code[class]').forEach(code => {
    const match = code.className.match(/language-([a-z0-9+#-]+)/i);
    if (match) {
      const label = document.createElement('span');
      label.className = 'code-label';
      label.textContent = match[1].toUpperCase();
      code.closest('pre').style.position = 'relative';
      code.closest('pre').appendChild(label);
    }
  });

  /* ---- Build TOC from headings ---- */
  const articleBody = document.querySelector('.article-body');
  const tocList     = document.getElementById('toc-list');

  if (articleBody && tocList) {
    const headings  = Array.from(articleBody.querySelectorAll('h2, h3'));
    const tocItems  = [];

    headings.forEach((h) => {
      /* Generate a readable slug ID */
      const slug = h.textContent
        .toLowerCase()
        .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
        .replace(/[^a-z0-9\\s-]/g, '')
        .replace(/\\s+/g, '-')
        .replace(/-{2,}/g, '-')
        .replace(/^-|-$/g, '')
        .slice(0, 64);
      h.id = slug;

      const li = document.createElement('li');
      li.className = h.tagName === 'H2' ? 'toc-h2' : 'toc-h3';

      const a = document.createElement('a');
      a.href = '#' + slug;
      a.textContent = h.textContent;
      li.appendChild(a);
      tocList.appendChild(li);
      tocItems.push({ el: h, anchor: a });
    });

    /* Active section tracking */
    let activeAnchor = null;
    const setActive = (anchor) => {
      if (anchor === activeAnchor) return;
      if (activeAnchor) activeAnchor.classList.remove('active');
      if (anchor) anchor.classList.add('active');
      activeAnchor = anchor;
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const item = tocItems.find(t => t.el === entry.target);
            if (item) setActive(item.anchor);
          }
        });
      },
      { rootMargin: '-15% 0px -80% 0px', threshold: 0 }
    );
    headings.forEach(h => observer.observe(h));

    /* Smooth scroll on TOC click */
    tocList.addEventListener('click', e => {
      const a = e.target.closest('a');
      if (!a) return;
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  /* ---- Highlight.js ---- */
  if (typeof hljs !== 'undefined') {
    document.querySelectorAll('pre code').forEach(block => {
      hljs.highlightElement(block);
    });
  }

})();
"""

# ─── 5. HTML parts ────────────────────────────────────────────────────────────

HEAD = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    '  <meta charset="UTF-8">\n'
    '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '  <meta name="description" content="A comprehensive guide to storage and databases in system design — covering ACID, CAP theorem, sharding, object storage, and big data pipelines.">\n'
    '  <title>Storage &amp; Databases in System Design — The Engineer\'s Complete Guide</title>\n'
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&amp;family=Lora:ital,wght@0,400;0,600;1,400&amp;family=DM+Sans:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">\n'
    '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">\n'
    '  <style>' + CSS + '</style>\n'
    '</head>\n'
)

BODY_START = (
    '<body>\n'
    '<div id="progress-bar"></div>\n\n'

    '<!-- Site nav -->\n'
    '<nav class="site-nav">\n'
    '  <span class="nav-logo">SD Guide</span>\n'
    '  <div class="nav-crumb">\n'
    '    <span>System Design</span>\n'
    '    <span class="sep">›</span>\n'
    '    <span class="active">Storage &amp; Databases</span>\n'
    '  </div>\n'
    '  <span class="nav-tag">Deep Dive</span>\n'
    '</nav>\n\n'

    '<!-- Hero -->\n'
    '<header class="article-hero">\n'
    '  <div class="hero-inner">\n'
    '    <div class="hero-tags">\n'
    '      <span class="hero-tag">System Design</span>\n'
    '      <span class="hero-tag">Data Engineering</span>\n'
    '      <span class="hero-tag">ML Engineering</span>\n'
    '      <span class="hero-tag">Distributed Systems</span>\n'
    '    </div>\n'
    '    <h1 class="hero-title">The Engineer\'s Complete Guide to Storage and Databases in System Design</h1>\n'
    '    <p class="hero-subtitle">From durability guarantees and ACID properties to distributed sharding, object storage, and big data pipelines — everything a data scientist or ML engineer needs to design robust storage architectures.</p>\n'
    '    <div class="hero-meta">\n'
    '      <span>~40 min read</span>\n'
    '      <span class="dot">·</span>\n'
    '      <span>10,000+ words</span>\n'
    '      <span class="dot">·</span>\n'
    '      <span>Storage · CAP Theorem · Sharding · Big Data · Delta Lake</span>\n'
    '    </div>\n'
    '  </div>\n'
    '</header>\n\n'

    '<!-- Table of Contents -->\n'
    '<div class="toc-outer">\n'
    '  <nav class="toc-box" aria-label="Table of contents">\n'
    '    <p class="toc-heading">In This Guide</p>\n'
    '    <ul id="toc-list"></ul>\n'
    '  </nav>\n'
    '</div>\n\n'
)

FOOTER = (
    '\n<!-- Footer -->\n'
    '<footer class="article-footer">\n'
    '  <p class="footer-note">\n'
    '    <strong>Storage and Databases in System Design</strong> — This article covers foundational concepts\n'
    '    in distributed storage architecture. Each section represents an area of deep independent study:\n'
    '    PostgreSQL internals, Cassandra\'s gossip protocol, Spark\'s execution model, and Delta Lake\'s\n'
    '    transaction log are each book-length topics. Consider this your conceptual map.\n'
    '  </p>\n'
    '  <div class="footer-tags">\n'
    '    <span class="footer-tag">ACID</span>\n'
    '    <span class="footer-tag">CAP Theorem</span>\n'
    '    <span class="footer-tag">Sharding</span>\n'
    '    <span class="footer-tag">Replication</span>\n'
    '    <span class="footer-tag">Object Storage</span>\n'
    '    <span class="footer-tag">HDFS</span>\n'
    '    <span class="footer-tag">Delta Lake</span>\n'
    '    <span class="footer-tag">Apache Spark</span>\n'
    '    <span class="footer-tag">Apache Kafka</span>\n'
    '    <span class="footer-tag">PostgreSQL</span>\n'
    '    <span class="footer-tag">Cassandra</span>\n'
    '    <span class="footer-tag">Amazon S3</span>\n'
    '  </div>\n'
    '</footer>\n'
)

SCRIPTS = (
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>\n'
    '<script>' + JS + '</script>\n'
    '</body>\n</html>\n'
)

# ─── 6. Assemble and write ─────────────────────────────────────────────────────

final_html = (
    HEAD
    + BODY_START
    + '\n<main class="article-body">\n'
    + article_body
    + '\n</main>\n'
    + FOOTER
    + SCRIPTS
)

out_path = '/mnt/user-data/outputs/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

char_count = len(final_html)
line_count = final_html.count('\n')
img_count  = final_html.count('<figure class="diagram">')
code_count = final_html.count('<pre>')
print(f"Written to {out_path}")
print(f"  {char_count:,} characters | {line_count:,} lines")
print(f"  {img_count} diagram figures | {code_count} code blocks")
print("Done.")
