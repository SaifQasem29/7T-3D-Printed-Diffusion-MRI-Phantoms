# Phantom ROI analysis scripts

These scripts calculate mean, population standard deviation and voxel counts for crossing (mask label 1) and parallel (mask label 2) regions for FA, MD and ODI. They export Excel workbooks and 300-dpi line plots.

## Install

```bash
pip install -r requirements.txt
```

## Input data layout

Set `PHANTOM_DATA_DIR` to a local directory containing the following structure (not included in the repository):

```text
data/
  Large Phantom/
    Sess 01/
      dti/FA.nii
      dti/MD.nii
      odi/fit_ODI.nii.gz
      masks/Filtered_Masks/MD_mask.nii.gz
    Sess 02/ ...
  Medium Phantom/
    Sess 01/ ...
  Small Phantom/
    Sess 01/ ...
```

`.nii` masks are also accepted. The scripts expect sessions 01–08, skip missing sessions, and validate matching map/mask dimensions and affines. They do not perform registration.

## Run

From the repository root:

```bash
pip install -r Analysis_Scripts/requirements.txt
python Analysis_Scripts/phantom_automated_fa.py
python Analysis_Scripts/phantom_automated_md.py
python Analysis_Scripts/phantom_automated_odi.py
```

By default, input is read from `data/` and output is written to `results/` relative to the repository root. To use another location, set `PHANTOM_DATA_DIR` and optionally `PHANTOM_OUTPUT_DIR` in your environment.

Windows PowerShell example:

```powershell
$env:PHANTOM_DATA_DIR = "D:\MRI_Phantom_Data"
$env:PHANTOM_OUTPUT_DIR = "D:\MRI_Phantom_Results"
python Analysis_Scripts/phantom_automated_fa.py
```

The scripts use the original session-day mapping: 1, 4, 8, 11, 15, 18, 23, 25. MD plotting scales raw values by 1000 and labels the axis as ×10⁻³ mm²/s. FA and ODI are dimensionless.

**Scope:** These are ROI statistics and plotting scripts, not full diffusion preprocessing or model-fitting pipelines. Original plot styling and calculations are otherwise retained. Test against your own dataset before using generated results for publication.
