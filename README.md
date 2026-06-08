# Tissue Phantom Materials Database

Open-access database of silicone tissue phantoms for modelling the mechanical behaviour of human soft tissues, including compression-derived hyperelastic material parameters, model selection guidance, and an inverse design framework.

## Overview

This repository provides a comprehensive, open-access dataset of soft silicone phantoms and accompanying analysis code for modelling the mechanical behaviour of human soft tissues under compressive loading.

The database comprises nineteen silicone phantoms fabricated from three EcoFlex families (00-10, 00-30, and 00-50) with systematically varied thinner concentrations, spanning an elastic modulus range of 6.19 to 158.80 kPa. This range covers the stiffness of a wide variety of healthy and pathological human soft tissues, including adipose, liver, kidney, prostate, lung, cardiac muscle, and skeletal muscle.

Each phantom was characterised through ten repeated uniaxial compression tests. Both engineering and true stress-strain responses were used to estimate parameters for six hyperelastic material models: Neo-Hookean, Mooney-Rivlin, Yeoh, Ogden, Veronda-Westmann, and Humphrey. 
The resulting dataset provides validated hyperelastic material model parameters, raw experimental data, and model performance metrics (Standard Error and Akaike Information Criterion) to support reproducible biomechanical simulation, surgical training, and medical device evaluation.

## Repository Contents

- Raw compression stress-strain data (engineering and true) for all nineteen phantoms, each across ten repeated tests
- Inverse design framework web application mapping a target elastic modulus to a validated phantom fabrication recipe
- Organ-to-phantom browsing web applications for stiffness matching

## Web Applications

Two browser-based tools are provided:

**Inverse Design App** — Enter a target elastic modulus and receive a validated phantom fabrication recipe without requiring programming expertise.
Available at: https://phantom-inverse-design.streamlit.app

**Organ Browser** — Select a target tissue from an anatomical body diagram and immediately receive the corresponding literature stiffness range, the subset of database phantoms whose properties fall within that range, and the fabrication recipe for each matching phantom.
Available at: https://phantom-organ-browser.streamlit.app

**Deploy via Streamlit Community Cloud:**
- Repository: this repo
- Branch: `main`
- App file (Inverse Design): `app/inverse_design_app.py`
- App file (Organ Browser): `app/organ_browser_app.py`
- Requirements: `requirements.txt`


## Citation

If you use this dataset or code in your work, please cite the associated publication:

> Dawood, A.B., Zhang, Z., Suulker, C., Osman, D., Abdulali, A., Angelmahr, M., Althoefer, K. (2026). Hyperelastic Characterisation of Silicone Tissue Phantoms: A Parametric Database with Model Selection and Inverse Design Framework.

A `CITATION.cff` file is also provided for automated citation tools.

## License

- The source code in this repository is released under the **MIT License**.
- The experimental data and derived datasets are released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

See `LICENSE` and `DATA_LICENSE.md` for full details.

## Acknowledgements

This work was carried out under the PALPABLE project, funded by UK Research and Innovation (UKRI) through the UK government's Horizon Europe funding guarantee (grant N°101092518) and funded by the European Union.
This work is also supported by ERC grant EndoTheranostics, 101118626, funded by the European Union.
