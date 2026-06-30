# Legacy Streamlit Applications

This folder contains the original Streamlit implementations of the Inverse
Design and Organ Browser tools.

These were the initial prototypes used during development. They are kept
here for reference and reproducibility, but are **no longer the actively
maintained versions** of these tools.

The current, actively maintained versions are static web applications hosted
via GitHub Pages, requiring no installation, no Python environment, and no
server:

- **Inverse Design Tool:** https://abubakardawood.github.io/tissue-phantom-material-database/inverse-design.html
- **Organ Browser:** https://abubakardawood.github.io/tissue-phantom-material-database/organ-browser.html

If you wish to run the Streamlit versions locally instead, install the
dependencies listed in `requirements.txt` at the repository root, then run:

```bash
streamlit run app/inverse_design_app.py
```
or
```bash
streamlit run app/organ_browser_app.py
```
