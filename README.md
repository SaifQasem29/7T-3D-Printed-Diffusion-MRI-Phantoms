# 7T Diffusion MRI Phantoms

**Exploring Diameter-Dependent Diffusion Metric Changes During PVA Dissolution in 3D-Printed Axon-Mimetic 7T MRI Phantoms**

**Research repository · 7T diffusion MRI · 3D printing · Quantitative MRI · Longitudinal phantom characterization**

This repository documents the design, fabrication, preparation, 7T MRI acquisition, and quantitative characterization of three custom 3D-printed axon-mimetic diffusion phantoms. The exploratory study examines how phantom diameter may influence water penetration, dissolution of the water-soluble polyvinyl alcohol (PVA) component of GEL-LAY filament, and longitudinal changes in diffusion MRI metrics.

> **Study status:** Eight MRI sessions over 25 days. Findings are exploratory and do not establish a definitive PVA dissolution time, a causal mechanism, or an optimal phantom diameter.

## Scientific background and aim

Validating diffusion MRI measurements remains challenging. Physical diffusion phantoms offer controlled structures, but conventional designs can be costly and difficult to customize. GEL-LAY 3D printing provides an accessible route to customizable, axon-mimetic structures. Dissolution of the filament's water-soluble PVA component creates microscopic pores that may support anisotropic diffusion. Because the pores are expected to be predominantly oriented within the printing plane, phantom diameter may affect lateral water penetration and the time course of dissolution.

**Aim:** Explore diameter-dependent temporal changes in fractional anisotropy (FA), mean diffusivity (MD), and orientation dispersion index (ODI) in parallel- and crossing-fiber regions during preparation for 7T diffusion MRI.

## Phantom geometry

Three disc-shaped phantoms were designed in **Autodesk Fusion 360** and sliced in **PrusaSlicer**. Each contains a central region mimicking fibers crossing at 90° and a surrounding annulus of parallel fibers.

| Phantom | Outer diameter | Central crossing-region diameter | Thickness | Crossing angle |
|---|---:|---:|---:|---:|
| Small | 40 mm | 20 mm | 6.7 mm | 90° |
| Medium | 60 mm | 30 mm | 6.7 mm | 90° |
| Large | 80 mm | 40 mm | 6.7 mm | 90° |

The central crossing diameter is half the outer diameter in all designs; thickness and nominal printing strategy were held constant.

## 3D printing and phantom preparation

| Parameter | Value |
|---|---|
| Printing technology | Fused deposition modeling (FDM) |
| Printer | Prusa XL |
| Filament | GEL-LAY |
| Nozzle diameter | 0.4 mm |
| Layer height | 0.1 mm |
| Extrusion width | 0.4 mm |
| Central crossing-region infill | 99% grid |
| Outer parallel-region infill | 100% parallel lines |
| Water immersion | 500 mL room-temperature tap water per phantom |
| Water replacement | Daily |

**PrusaSlicer modifier:** The central crossing region was implemented as a smaller, centered modifier within the main disc, allowing its 99% grid infill to differ from the surrounding 100% parallel-line infill. Other print settings apply to the main object or are inherited from the overall slicer configuration.

| Phantom | Filament used | Printing time | Estimated material cost |
|---|---:|---:|---:|
| Small | 11.08 g | 1 h 25 min | €1.11 |
| Medium | 24.88 g | 2 h 50 min | €2.49 |
| Large | 44.50 g | 4 h 45 min | €4.45 |

## MRI acquisition

Eight scanning sessions per phantom were conducted approximately twice weekly across 25 days during immersion.

| Parameter | Protocol |
|---|---|
| Scanner | 7T MAGNETOM Terra.X Impulse Edition (Siemens Healthineers) |
| RF coil | 8Tx/64Rx head coil |
| DWI acquisition | Multi-shell |
| DWI resolution | 1 × 1 × 1 mm³ isotropic |
| DWI TR / TE | 7000 / 35 ms |
| b-values | 0, 1000, 2500 s/mm² |
| b = 0 | 4 averages |
| b = 1000 | 30 directions |
| b = 2500 | 64 directions |
| Structural scan | MP2RAGE, 0.7 mm isotropic |
| MP2RAGE TR / TE | 6000 / 1.7 ms |
| MP2RAGE TI1 / TI2 | 800 / 2700 ms |

**Acquisition timeline:** Session 1 (day 1), session 2 (day 4), session 3 (day 8), session 4 (day 11), session 5 (day 15), session 6 (day 18), session 7 (day 23), and session 8 (day 25).

## Processing and quantitative analysis

Preprocessing and analysis used **MRtrix3**, **FSL**, and **Python**, including diffusion-image denoising, diffusion metric estimation, and manual ROI delineation. Tensor-derived **FA** and **MD** and NODDI-derived **ODI** maps were evaluated. Two manually defined, filtered, slice-based ROIs were used for each phantom: a **central crossing-fiber ROI (C-ROI)** and a **surrounding parallel-fiber ROI (P-ROI)**. Mean metric values were extracted from the middle slice for each session.

ROI-derived values reflect the selected slices and masks rather than whole-phantom averages. NODDI-derived ODI should be treated as a model-dependent measure in this synthetic porous material, not a direct measurement of microscopic fiber crossing geometry.

## Results: eight-session longitudinal observations

### Fractional anisotropy

The expected **C-ROI FA < P-ROI FA** contrast appeared in the small phantom from day 15 (0.481 vs 0.548) and in the large phantom from day 18 (0.406 vs 0.424). The medium phantom fluctuated and showed this contrast by day 25 (0.512 vs 0.529). Low-FA bands were visible in the parallel regions of medium and large phantoms, suggesting potential printing-related heterogeneity or localized water accumulation; their physical origin remains unverified.

### Mean diffusivity

MD maps showed spatial changes progressing from the edges of the crossing regions toward their centers. On day 25, crossing-region MD was **1.059** (small), **1.001** (medium), and **0.661** (large), expressed in **10⁻³ mm²/s**. The lower crossing-region MD in the large phantom may be consistent with slower water penetration or incomplete dissolution, but does not establish either mechanism.

### Orientation dispersion index

On day 25, crossing-region ODI was **0.086** (small), **0.075** (medium), and **0.306** (large). Crossing ODI exceeded parallel ODI by day 23 only in the small phantom in the reported comparisons. ODI behavior may also reflect model-fitting limitations and differences in pore geometry, rather than dissolution alone.

### Summary

The smaller phantom generally exhibited earlier changes in diffusion metrics, while the medium and large phantoms displayed visible low-FA bands and possible structural heterogeneity. These patterns are **hypothesis-generating**, not proof of diameter-dependent dissolution rates or printing defects.

## Interpretation and limitations

- **Diameter and dissolution:** Diameter was varied to explore its possible influence on lateral water penetration and PVA dissolution. The data suggest earlier metric changes in smaller phantoms but do not directly quantify dissolved PVA or pore connectivity.
- **Printing heterogeneity:** Low-FA bands in medium and large parallel regions may reflect printing artifacts and localized water trapping. Structural imaging is required to confirm this interpretation.
- **Spatial gradients:** MD patterns from crossing-region edges toward the center could reflect nonuniform water penetration, heterogeneous printed density, or other factors.
- **Air bubbles:** Air bubbles were visible in mean b = 0 images and may influence image quality and quantitative metrics.
- **Model assumptions:** ODI is derived from a biophysical diffusion model developed for tissue; its interpretation in GEL-LAY pores requires independent validation.
- **Study scope:** Only three diameters at a single thickness and nominal printing configuration were examined, with manually selected central-slice ROIs.

**Future work:** Use micro-CT to characterize pore geometry and connectivity, evaluate more complex white-matter-mimicking geometries using customized printer instructions, optimize diameter-specific printing parameters, and assess vacuum degassing to reduce trapped air.

## Figures

The following figure files are provided alongside this README in the accompanying figure package. Upload them to a `figures/` directory to enable the relative links and previews below.

### Phantom configuration, photographs, mean b = 0 images, and printing summary

![Phantom designs, physical specimens, mean b0 images, and printing summary](figures/Project_Overview.png)

### Longitudinal FA, MD, and ODI measurements

![FA MD ODI across eight sessions](figures/FA%2C%20ODI%2C%20MD%20Vs%20Sessions.png)

### Longitudinal FA maps

![FA maps across eight sessions](figures/FA%20Map%20Vs%20Sessions.png)

### Longitudinal MD maps

![MD maps across eight sessions](figures/MD%20Map%20Vs%20Sessions.png)

### Visual study overview

![Study overview](figures/ISMRM_Preview_300dpi%281%29.png)

## Repository contents

The repository is intended to share the phantom design files, slicer/printing settings, figure outputs, and Python analysis scripts. Exact links to the existing design and script files should be added once their GitHub paths are confirmed; no filenames or directories for these materials are assumed here.

## Reproducibility notes

- Print geometry, infill, water replacement, and acquisition parameters are documented above.
- Comparisons use manually delineated, filtered middle-slice ROIs; ROI placement can influence the means.
- Some figure panels use per-image display ranges to reveal local contrast. Do not compare apparent brightness across such panels as though they share a common scale; consult numeric plots and color bars.
- The reported material costs are estimates based on filament consumption and do not include labor, equipment, electricity, or imaging costs.
- Raw MRI data and complete processing environments are not represented as publicly available unless explicitly uploaded.

## Project and attribution

Developed as part of research on customizable axon-mimetic diffusion MRI phantoms at **Otto von Guericke University Magdeburg**, Germany.

**Repository:** [SaifQasem29/7T-Diffusion-MRI-Phantoms](https://github.com/SaifQasem29/7T-Diffusion-MRI-Phantoms)

**Contact / maintainer:** [Saif Qasem](https://github.com/SaifQasem29)

If you use these designs or analysis materials, please acknowledge the repository and any associated publication when available. No software license is implied unless a `LICENSE` file is added.
