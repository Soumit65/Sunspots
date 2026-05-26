# SuryaPy - Complete Setup & Deployment Guide

You now have a **production-ready Python package** built from your internship code.

## 📊 What You Have

**Package Name**: `suryapy` (from Surya = the Sun in Sanskrit)

**Core Modules** (your exact code, refactored):
- `sunspots/thresholding.py` — Your `b_roth()` and `mask_sun()` functions
- `sunspots/tracking.py` — Your `find_spot()`, `process()`, `display_spot()` pipeline
- `sunspots/correction.py` — Your limb darkening correction (radial median + poly fit)
- `sunspots/area.py` — Your connected components analysis, foreshortening, unit conversions

**Documentation** (8 files):
- `docs/index.rst` — Main landing page
- `docs/getting_started.rst` — Concepts and workflow
- `docs/quick_start.rst` — 5-minute intro
- `docs/installation.rst` — Setup instructions
- `docs/tutorials.rst` — 5 deep-dive tutorials
- `docs/examples.rst` — 7 practical examples from notebooks
- `docs/api_reference.rst` — Complete function docs
- `docs/faq.rst` — 30+ Q&A

**Configuration Files**:
- `pyproject.toml` — Package metadata (dependencies: astrolab, numpy, scipy, matplotlib)
- `LICENSE` — MIT (open source, free to use)
- `README.md` — Project overview with examples
- `CHANGELOG.md` — Version history
- `MANIFEST.in` — What to include in distribution
- `.gitignore` — Standard Python project ignores
- `.github/workflows/deploy-docs.yml` — Auto-deploy docs to GitHub Pages

---

## 🚀 Next Steps (In Order)

### Step 1: Update Your Email

Edit `pyproject.toml`, line 7:

```toml
authors = [
    {name = "Soumit Dey", email = "your.actual.email@example.com"}
]
```

Replace `your.actual.email@example.com` with your real email.

### Step 2: Commit to Git

```bash
cd path/to/SuryaPy
git add .
git commit -m "Package SuryaPy: convert internship notebooks to production package"
git push origin main
```

(Or `master` if that's your default branch)

### Step 3: Enable GitHub Pages

1. Go to your repository: **https://github.com/Soumit65/SuryaPy**
2. Click **Settings** (top right)
3. In left sidebar, click **Pages**
4. Under "Build and deployment":
   - Source: **GitHub Actions** (select from dropdown)
   - Click **Save**

That's it! GitHub Actions will auto-build and deploy docs on every push.

### Step 4: Verify Deployment

1. Go to your repo's **Actions** tab
2. You should see a workflow run "Build and Deploy Documentation"
3. Wait for it to complete (green checkmark = success)
4. Visit: **https://soumit65.github.io/SuryaPy/**
5. You should see your beautiful documentation website! 🎉

---

## 📁 Directory Structure

```
SuryaPy/
│
├── sunspots/                              # Main package
│   ├── __init__.py                       # Exports
│   ├── thresholding.py                   # b_roth, mask_sun
│   ├── tracking.py                       # find_spot, process
│   ├── correction.py                     # limb_darkening_correction
│   └── area.py                           # Connected components, conversions
│
├── docs/                                  # Sphinx documentation
│   ├── conf.py                           # Sphinx config
│   ├── index.rst                         # Main index
│   ├── getting_started.rst               # Overview
│   ├── quick_start.rst                   # 5-min intro
│   ├── installation.rst                  # Setup
│   ├── tutorials.rst                     # 5 tutorials
│   ├── examples.rst                      # 7 examples
│   ├── api_reference.rst                 # Function docs
│   └── faq.rst                           # 30+ Q&A
│
├── .github/workflows/                    # CI/CD
│   └── deploy-docs.yml                   # Auto-deploy GitHub Pages
│
├── pyproject.toml                        # Package config
├── LICENSE                               # MIT License
├── README.md                             # Project overview
├── CHANGELOG.md                          # Version history
├── MANIFEST.in                           # Distribution manifest
├── requirements-docs.txt                 # Doc dependencies
└── .gitignore                            # Git ignores
```

---

## 🔧 How to Use SuryaPy Locally

After setup, you can use it:

```python
from astrolab import imaging as im
from scipy import ndimage as scp
import suryapy

# Load and process
image = im.load_image("solar.jpg")
filtered = scp.gaussian_filter(image, sigma=0.5, radius=2)
cropped = suryapy.mask_sun(filtered)
br = suryapy.b_roth(cropped, threshold=9)
labeled, n, large, sizes, bbox = suryapy.find_components(br, cropped)

print(f"Found {n} components")
```

---

## 📖 Building Docs Locally (Optional)

To build and preview the documentation on your computer:

```bash
# Install doc dependencies
pip install -r requirements-docs.txt

# Build HTML
cd docs
sphinx-build -b html . _build/html

# Open in browser
open _build/html/index.html  # macOS/Linux
# or
start _build/html/index.html  # Windows
```

---

## ✅ Checklist Before Sharing

- [ ] Updated email in `pyproject.toml`
- [ ] Committed and pushed to GitHub
- [ ] Enabled GitHub Pages (Settings → Pages)
- [ ] Verified docs build (Actions tab shows green checkmark)
- [ ] Visited your docs site: https://soumit65.github.io/SuryaPy/
- [ ] README looks good
- [ ] LICENSE is there
- [ ] Examples in README work

---

## 📤 Publishing to PyPI (Optional, Later)

When you want to publish to PyPI so anyone can `pip install suryapy`:

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload to TestPyPI first (recommended)
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ suryapy

# Once happy, upload to real PyPI
python -m twine upload dist/*
```

Then users can:

```bash
pip install suryapy
```

---

## 🎓 Your Package in a Nutshell

**What it does**: Detects and measures sunspots from solar images using:
- Bradley-Roth adaptive thresholding (O(1) integral image method)
- Morphological cleanup
- Connected component labeling
- Limb darkening correction
- Foreshortening correction
- Unit conversions to standard solar physics measurements

**Who can use it**: Astronomy researchers, students, solar enthusiasts

**License**: MIT (free, open source)

**Dependencies**: astrolab, numpy, scipy, matplotlib (no OpenCV!)

**Documentation**: Complete API, tutorials, examples, FAQ

**GitHub Pages**: Auto-deployed on every push

---

## 🆘 Troubleshooting

**"GitHub Actions failing to build docs"**

Check the Actions tab → click the failed run → see the error message. Usually:
- Missing `requirements-docs.txt`
- Missing Sphinx setup
- Import error in `docs/conf.py`

Fix and push again.

**"Documentation site not showing"**

- Wait 5 minutes (GitHub Pages can take time)
- Go to Settings → Pages and verify source is "GitHub Actions"
- Check Actions tab — is the deployment job green?

**"I want to change the package name from 'suryapy'"**

Edit `pyproject.toml` line 5:

```toml
name = "suryapy"  # ← change this
```

Then push.

**"How do I add more examples?"**

Add new cells to `docs/examples.rst` or create a new `.rst` file in `docs/`, then add it to the table of contents in `docs/index.rst`.

---

## 📞 Support & Next Steps

1. **Your docs site**: https://soumit65.github.io/SuryaPy/
2. **GitHub Issues**: Report bugs or ask questions
3. **GitHub Discussions**: Feature requests
4. **Your college's astrolab docs**: If you need astrolab-specific help

---

## 🎉 Congratulations!

You've transformed your internship work from scattered Jupyter notebooks into a **professional, documented, deployable Python package**.

What you now have:
- ✅ Clean, modular code
- ✅ Professional documentation website
- ✅ Automated deployment (GitHub Actions)
- ✅ MIT license (open source)
- ✅ Production-ready package structure
- ✅ Example-driven docs
- ✅ FAQ and troubleshooting guides
- ✅ Easy installation (`pip install`)

This is genuinely impressive for a portfolio. You can now:
- Show this to employers/grad schools
- Publish to PyPI if you want
- Collaborate with others
- Get feedback via GitHub issues
- Keep improving it

**Let's observe the sun. ☀️**

---

## Final Reminders

1. **Update email** in `pyproject.toml`
2. **Push to GitHub** — `git push origin main`
3. **Enable GitHub Pages** in Settings
4. **Wait ~5 minutes**, then visit your docs site
5. **Share the link** with people: https://soumit65.github.io/SuryaPy/

All files are ready to go!
