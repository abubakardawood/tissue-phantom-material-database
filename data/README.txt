Title:
A Database of Silicone Phantom Materials for Modeling Human Tissue Mechanics Across Varying Stiffnesses

Description:
This dataset contains processed mechanical compression test data for soft silicone phantoms
fabricated using Ecoflex (Smooth-On) with varying base materials and thinner concentrations.
The dataset provides force–compression measurements together with derived engineering and
true stress–strain quantities, intended for mechanical characterization, constitutive model
fitting, and the design of tissue-equivalent phantoms.

All files in this dataset are processed outputs generated from raw experimental measurements.
The raw data files are not included in this archive.

------------------------------------------------------------
Directory structure
------------------------------------------------------------

Each material has a dedicated folder. Example:

<material_name>/
  ├── sample_A_01_processed.csv
  ├── ...
  ├── sample_A_05_processed.csv  
  ├── sample_B_01_processed.csv
  ├── ...
  └── sample_B_5_processed.csv

Each CSV file corresponds to a single compression test and contains both measured and
derived quantities, preceded by a metadata header.

------------------------------------------------------------
File format
------------------------------------------------------------

File type:
- CSV 

Each CSV file consists of:
1. A metadata header describing specimen geometry, test conditions, and material information
2. A blank line
3. A data table with the following columns:

- Time
- Compression (mm)
- Load (N)
- Engineering strain (-)
- Engineering stress (N/mm^2)
- True strain (-)
- True stress (N/mm^2)

------------------------------------------------------------
Experimental conditions (summary)
------------------------------------------------------------

- Test type: Uniaxial compression
- Testing machine: Instron 5900
- Load cell: 1 kN / 10 kN
- Compression speed: 10 mm/min
- Laboratory: Centre for Advanced Robotics @ QM, Queen Mary University of London, UK

Specimen geometry and additional details are recorded in the metadata header of each file.

------------------------------------------------------------
Derivation of strain and stress measures
------------------------------------------------------------

Measured quantities:
- Compression (mm): crosshead displacement during compression
- Load (N): measured compressive force

Engineering strain is calculated as:

  engineering strain = compression / initial specimen height

Engineering stress is calculated as:

  engineering stress = load / initial cross-sectional area

True strain is calculated from engineering strain as:

  true strain = | ln(1 − engineering strain) |

True stress is calculated from engineering stress as:

  true stress = | engineering stress × (1 − engineering strain) |

Compressive stress and strain are reported using a negative sign convention.

------------------------------------------------------------
Notes
------------------------------------------------------------

- No filtering or smoothing is applied to the data.
- Engineering and true measures are derived solely from force and compression measurements.
- Each file represents one independent compression test.

------------------------------------------------------------
Intended use
------------------------------------------------------------

This dataset is suitable for:
- Hyperelastic material model fitting
- Mechanical characterization of soft elastomers
- Soft tissue phantom development
- Validation of stiffness sensing and palpation systems
- Inverse design of phantom material compositions

------------------------------------------------------------
Citation
------------------------------------------------------------

If you use this dataset, please cite the associated publication and acknowledge the data source.
