# Documentation Setup Guide

This guide explains how to view and deploy the Custom Evals documentation.

## 📚 Documentation Options

### Option 1: GitHub.com (Automatic - No Setup Needed!)

**The easiest way!** Your `.md` files work automatically on GitHub:

1. Push your code to GitHub
2. Users navigate to `docs/` folder
3. Click any `.md` file → GitHub renders it as beautiful HTML
4. All links work automatically!

**Example URLs:**
- Main docs: `https://github.com/your-username/cust-evals/blob/main/docs/README.md`
- Getting Started: `https://github.com/your-username/cust-evals/blob/main/docs/getting-started.md`

**✅ Already done! No setup required.**

---

### Option 2: Local Viewing in Editor

**Quick and simple** - View in any text editor:

**VSCode** (Recommended):
```bash
# Open file
code docs/README.md

# Preview Markdown (built-in)
# Press: Cmd+Shift+V (Mac) or Ctrl+Shift+V (Windows/Linux)
```

**Other Editors:**
- **Sublime Text**: Install "MarkdownPreview" package
- **Atom**: Built-in Markdown preview (Ctrl+Shift+M)
- **PyCharm**: Built-in Markdown preview

**✅ No additional packages needed!**

---

### Option 3: MkDocs Documentation Site (Professional)

**Beautiful, searchable documentation site** with Material theme.

#### Why Use MkDocs?

- 🎨 **Beautiful Design** - Material Design theme
- 🔍 **Search** - Full-text search built-in
- 📱 **Responsive** - Works on mobile/tablet/desktop
- 🌓 **Dark Mode** - Light/dark theme toggle
- 🚀 **Fast** - Static site generation
- 📦 **Easy Deploy** - One command to GitHub Pages

#### Installation

```bash
# Option A: Using pip
pip install -e ".[docs]"

# Option B: Using Makefile
make install-docs

# Option C: Manual install
pip install mkdocs mkdocs-material pymdown-extensions
```

#### Serving Locally

```bash
# Option A: Using Makefile (recommended)
make docs-serve

# Option B: Direct command
mkdocs serve

# Open browser to: http://127.0.0.1:8000
```

You'll see:
```
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.52 seconds
INFO    -  [16:20:30] Serving on http://127.0.0.1:8000/
```

**Features:**
- ✅ Live reload (auto-refresh on file changes)
- ✅ Search functionality
- ✅ Navigation sidebar
- ✅ Dark/light mode toggle
- ✅ Code syntax highlighting
- ✅ Mobile-friendly

#### Building Static Site

```bash
# Option A: Using Makefile
make docs-build

# Option B: Direct command
mkdocs build

# Output: site/ directory with HTML files
```

#### Deploying to GitHub Pages

**One-command deployment:**

```bash
# Option A: Using Makefile
make docs-deploy

# Option B: Direct command
mkdocs gh-deploy
```

This will:
1. Build the documentation
2. Create/update `gh-pages` branch
3. Push to GitHub
4. Your docs will be live at: `https://your-username.github.io/cust-evals/`

**First-time setup on GitHub:**
1. Go to repository Settings → Pages
2. Source: Deploy from `gh-pages` branch
3. Save

**✨ Done! Your docs are now live!**

---

## 🔧 Configuration Files

### mkdocs.yml

Configuration for MkDocs (already created):

```yaml
site_name: Custom Evals Documentation
theme:
  name: material
  palette:
    - scheme: default      # Light mode
    - scheme: slate        # Dark mode
  features:
    - navigation.tabs
    - search.suggest
    - content.code.copy
```

**Customize:**
- `site_name`: Change your site name
- `repo_url`: Update with your GitHub URL
- `nav`: Modify navigation structure

### Makefile

Quick commands (already created):

```bash
make help          # Show all commands
make docs-serve    # Start local server
make docs-build    # Build static site
make docs-deploy   # Deploy to GitHub Pages
```

---

## 📝 File Structure

```
cust-evals/
├── docs/                    # Documentation source
│   ├── index.md            # Home page (MkDocs entry point)
│   ├── README.md           # Also serves as home page
│   ├── getting-started.md
│   ├── examples.md
│   └── ...
├── mkdocs.yml              # MkDocs configuration
├── Makefile                # Quick commands
└── site/                   # Generated HTML (after build)
```

---

## 🚀 Quick Start

### Just View on GitHub

```bash
# 1. Push to GitHub
git add .
git commit -m "Add documentation"
git push

# 2. Done! Navigate to docs/ folder on GitHub
```

### View Locally with MkDocs

```bash
# 1. Install dependencies
make install-docs

# 2. Start server
make docs-serve

# 3. Open http://127.0.0.1:8000
```

### Deploy to GitHub Pages

```bash
# 1. Install dependencies
make install-docs

# 2. Deploy
make docs-deploy

# 3. Visit https://your-username.github.io/cust-evals/
```

---

## 🎨 Customization

### Change Theme Colors

Edit `mkdocs.yml`:

```yaml
theme:
  palette:
    - scheme: default
      primary: indigo     # Change to: blue, teal, green, etc.
      accent: indigo
```

### Add Custom CSS

1. Create `docs/stylesheets/extra.css`
2. Add to `mkdocs.yml`:
```yaml
extra_css:
  - stylesheets/extra.css
```

### Modify Navigation

Edit `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Your New Page: your-page.md
```

---

## 🔍 Comparison

| Method | Setup | Features | Best For |
|--------|-------|----------|----------|
| **GitHub** | None | Basic rendering | Quick sharing |
| **Editor** | None | Preview only | Development |
| **MkDocs** | 5 minutes | Full site, search, themes | Professional docs |

---

## 📖 Documentation URLs

After deployment, your docs will be available at:

- **GitHub**: `https://github.com/your-username/cust-evals/tree/main/docs`
- **GitHub Pages**: `https://your-username.github.io/cust-evals/`
- **Local**: `http://127.0.0.1:8000` (when running `make docs-serve`)

---

## 🐛 Troubleshooting

### MkDocs not installed

```bash
pip install -e ".[docs]"
# or
make install-docs
```

### Port 8000 already in use

```bash
# Use different port
mkdocs serve -a 127.0.0.1:8001
```

### GitHub Pages not working

1. Check repository Settings → Pages
2. Ensure source is set to `gh-pages` branch
3. Wait 2-3 minutes after deployment

### Links not working

- Use relative paths: `[Link](page.md)` ✅
- Not absolute: `[Link](/page.md)` ❌

---

## ✅ Recommendations

**For Open Source Projects:**
1. ✅ Use GitHub (automatic, free)
2. ✅ Add MkDocs for professional site
3. ✅ Deploy to GitHub Pages

**For Internal Projects:**
1. ✅ Use GitHub if you have GitHub Enterprise
2. ✅ Use MkDocs and self-host the `site/` directory

**For Development:**
1. ✅ Use VSCode preview for quick edits
2. ✅ Use MkDocs for full preview

---

## 🎯 Summary

**No Setup Needed:**
- ✅ `.md` files work on GitHub automatically
- ✅ View in any text editor with Markdown preview

**Optional Enhanced Setup (5 minutes):**
- ✅ Install MkDocs: `make install-docs`
- ✅ Serve locally: `make docs-serve`
- ✅ Deploy to GitHub Pages: `make docs-deploy`

**Your docs are ready to use right now! 🎉**

---

## 📚 Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Markdown Guide](https://guides.github.com/features/mastering-markdown/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
