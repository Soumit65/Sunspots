# Sunspots Package - Quick Reference Card

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Update your email in pyproject.toml
# 2. Commit and push to GitHub
git add .
git commit -m "Convert to Python package"
git push origin main

# 3. Enable GitHub Pages in Settings → Pages
# 4. GitHub Actions will auto-deploy docs
# 5. Visit https://soumit65.github.io/Sunspots/
```

## 📦 Install Command

```bash
pip install sunspots
```

## 💻 Basic Usage

```python
import sunspots

# Load image
image = sunspots.load_image("solar.jpg")

# Detect sunspots
spots, stats = sunspots.analyze_contours(image)

# Print results
print(f"Found {stats['count']} sunspots")
print(f"Total area: {stats['total_area']:.2f}")
```

## 🔧 Key Files

| File | What to Do |
|------|-----------|
| `pyproject.toml` | Update your email |
| `README.md` | Already complete |
| `docs/` | Already complete |
| `.github/workflows/deploy-docs.yml` | Auto-deploys docs |

## 🎯 Main Functions

```python
# Thresholding
sunspots.bradley_roth_threshold(image, block_size=51, constant=10)

# Detection
sunspots.detect_sunspots(image, min_area=50)

# Analysis
spots, stats = sunspots.analyze_contours(image)

# Visualization
sunspots.draw_sunspots(image, spots)

# Utilities
sunspots.load_image(path)
sunspots.apply_clahe(image)
sunspots.normalize_image(image)
```

## 📊 Sunspot Properties

```python
spot.area              # Size in pixels
spot.perimeter         # Boundary length
spot.centroid          # (x, y) center
spot.circularity       # 0-1 (1 = perfect circle)
spot.aspect_ratio      # Width/height
spot.bounding_box      # (x, y, w, h)
spot.contour           # OpenCV contour
```

## 📈 Statistics Dictionary

```python
stats['count']              # Number of sunspots
stats['total_area']         # Sum of areas
stats['mean_area']          # Average area
stats['std_area']           # Standard deviation
stats['min_area']           # Minimum area
stats['max_area']           # Maximum area
stats['mean_circularity']   # Average circularity
stats['mean_aspect_ratio']  # Average aspect ratio
```

## 🐛 Common Parameters to Tune

| Parameter | Default | Effect |
|-----------|---------|--------|
| `block_size` | 50 | Larger = more context |
| `constant` | 10 | Larger = more detection |
| `min_area` | 50 | Minimum sunspot size |

## 🔗 Important Links

- **Repository**: https://github.com/Soumit65/Sunspots
- **Documentation**: https://soumit65.github.io/Sunspots/ (after setup)
- **Issues**: https://github.com/Soumit65/Sunspots/issues

## ✅ Checklist for Deployment

- [ ] Update email in `pyproject.toml`
- [ ] Review `README.md` (already complete)
- [ ] Commit all changes
- [ ] Push to GitHub (`git push`)
- [ ] Go to repo Settings → Pages
- [ ] Ensure "GitHub Actions" is selected
- [ ] Wait for Actions to complete
- [ ] Visit your docs site

## 📚 Documentation Sections

- **Getting Started**: Quick intro & workflow
- **Installation**: Multiple install methods
- **API Reference**: All functions documented
- **Tutorials**: Deep dives into concepts
- **Examples**: 8+ working code examples
- **FAQ**: 40+ questions answered

## 💡 Pro Tips

1. Start with `min_area=50` to filter noise
2. Use `apply_clahe()` before thresholding for better results
3. Adjust `constant` to fine-tune detection (5-20 range)
4. Use `resize_image(scale=0.5)` to speed up processing
5. Filter results: `[s for s in spots if s.circularity > 0.7]`

## 🎓 Learning Path

1. Read: Getting Started guide
2. Install: From source (editable install)
3. Try: First example (basic detection)
4. Learn: Tutorials section
5. Explore: API Reference
6. Build: Your own examples

## 🔑 Key Concepts

**Bradley-Roth**: Adaptive thresholding algorithm  
**Adaptive Threshold**: Local threshold vs global threshold  
**Contour**: Boundary of an object  
**Circularity**: How round an object is (0-1)  
**Centroid**: Center point of an object  

## 🚁 Deployment Overview

```
Your code push
    ↓
GitHub Actions triggered
    ↓
Sphinx builds HTML
    ↓
Uploaded to gh-pages
    ↓
Published at GitHub Pages URL
    ↓
Live documentation! ✨
```

## 📞 Getting Help

1. **Documentation**: https://soumit65.github.io/Sunspots/
2. **FAQ Section**: Search for your question
3. **Examples**: See working code
4. **GitHub Issues**: Report bugs or ask questions
5. **API Reference**: Check function signatures

---

**You're all set! Push your code and enjoy your new Python package! 🎉**
