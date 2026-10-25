"""Automated phantom ROI analysis for MD using new masks."""



from pathlib import Path
import argparse
import os

import numpy as np

import nibabel as nib

import matplotlib.pyplot as plt

from openpyxl import Workbook

from openpyxl.styles import Font, PatternFill, Alignment

from openpyxl.utils import get_column_letter



# ============================================================

# CONFIGURATION

# ============================================================



ROOT = Path(os.environ.get("PHANTOM_DATA_DIR", str(Path(__file__).resolve().parent.parent / "data"))).expanduser().resolve()



PHANTOMS = {

    "Large Phantom": "L",

    "Medium Phantom": "M",

    "Small Phantom": "S"

}



SESSIONS = range(1, 9)

# Days since the first scan (Monday/Thursday schedule; session 7 on Tuesday).
SESSION_DAYS = {1: 1, 2: 4, 3: 8, 4: 11, 5: 15, 6: 18, 7: 23, 8: 25}



METRIC = "MD"



MAP_RELATIVE_PATH = Path("dti") / "MD.nii"



MASK_FOLDER = Path("masks") / "Filtered_Masks"



OUTPUT_PREFIX = f"Phantom_{METRIC}_FilteredMasks"
OUTPUT_DIR = Path(os.environ.get("PHANTOM_OUTPUT_DIR", str(Path(__file__).resolve().parent.parent / "results"))).expanduser().resolve()



REGIONS = {

    "Crossing": 1,

    "Parallel": 2

}





# ============================================================

# FIND THE CORRECT MASK

# ============================================================



def find_mask(folder, size_letter):



    mask_dir = folder / MASK_FOLDER



    for extension in (".nii", ".nii.gz"):



        candidate = mask_dir / ("MD_mask" + extension)



        if candidate.is_file():

            return candidate



    return mask_dir / "MD_mask.nii"





# ============================================================

# ANALYZE ALL PHANTOMS AND SESSIONS

# ============================================================



def analyze():



    results = {}

    failures = []



    for phantom, size_letter in PHANTOMS.items():



        for session in SESSIONS:



            session_name = f"Sess {session:02d}"



            folder = ROOT / phantom / session_name



            mask_path = find_mask(folder, size_letter)

            map_path = folder / MAP_RELATIVE_PATH



            key = (phantom, session)



            if not mask_path.is_file() or not map_path.is_file():



                failures.append(

                    f"{phantom} / {session_name}: "

                    f"missing {'mask ' if not mask_path.is_file() else ''}"

                    f"{'map' if not map_path.is_file() else ''}"

                )



                continue



            try:



                mask_img = nib.load(str(mask_path))

                map_img = nib.load(str(map_path))



                if mask_img.shape != map_img.shape:



                    raise ValueError(

                        f"Different shapes: "

                        f"{mask_img.shape} vs {map_img.shape}"

                    )



                if not np.allclose(

                    mask_img.affine,

                    map_img.affine,

                    atol=1e-3

                ):



                    raise ValueError(

                        "Different image affines; "

                        "register/resample mask first "

                        "(nearest-neighbor)"

                    )



                mask = np.asarray(mask_img.dataobj)

                metric = np.asarray(map_img.dataobj)



                valid = np.isfinite(metric)



                stats = {}



                for region, label in REGIONS.items():



                    values = metric[

                        (mask == label) & valid

                    ]



                    if values.size == 0:



                        raise ValueError(

                            f"No valid voxels in {region} "

                            f"(label {label})"

                        )



                    stats[region] = (

                        float(np.mean(values)),

                        float(np.std(values)),

                        int(values.size)

                    )



                results[key] = stats



                print(

                    f"{phantom} / {session_name}: "

                    + ", ".join(

                        f"{r} mean={stats[r][0]:.6f}, "

                        f"std={stats[r][1]:.6f}"

                        for r in REGIONS

                    )

                )



            except Exception as exc:



                failures.append(

                    f"{phantom} / {session_name}: {exc}"

                )



    return results, failures





# ============================================================

# SAVE EXCEL

# ============================================================



def save_excel(results, failures):



    wb = Workbook()



    wide = wb.active

    wide.title = "Mean values"



    std = wb.create_sheet("STD values")



    detail = wb.create_sheet("All measurements")



    headings = [

        "Session",

        "Large Crossing",

        "Large Parallel",

        "Medium Crossing",

        "Medium Parallel",

        "Small Crossing",

        "Small Parallel"

    ]



    for sheet, index in ((wide, 0), (std, 1)):



        sheet.append(headings)



        for session in SESSIONS:



            row = [session]



            for phantom in PHANTOMS:



                for region in REGIONS:



                    stat = results.get(

                        (phantom, session), {}

                    ).get(region)



                    row.append(

                        stat[index] if stat else None

                    )



            sheet.append(row)



    detail.append([

        "Phantom",

        "Session",

        "Region",

        "Mean",

        "STD (population)",

        "Valid voxels"

    ])



    for phantom in PHANTOMS:



        for session in SESSIONS:



            for region in REGIONS:



                item = results.get(

                    (phantom, session), {}

                ).get(region)



                detail.append([

                    phantom,

                    f"Sess {session:02d}",

                    region,

                    item[0] if item else None,

                    item[1] if item else None,

                    item[2] if item else None

                ])



    if failures:



        errors = wb.create_sheet("Skipped scans")

        errors.append(["Reason"])



        for reason in failures:

            errors.append([reason])



    for sheet in wb.worksheets:



        sheet.freeze_panes = "A2"

        sheet.auto_filter.ref = sheet.dimensions



        for cell in sheet[1]:



            cell.font = Font(

                bold=True,

                color="FFFFFF"

            )



            cell.fill = PatternFill(

                "solid",

                fgColor="17365D"

            )



            cell.alignment = Alignment(

                wrap_text=True

            )



        for col in sheet.columns:



            letter = get_column_letter(

                col[0].column

            )



            width = max(

                len(str(cell.value or ""))

                for cell in col

            )



            sheet.column_dimensions[letter].width = min(

                max(width + 3, 15),

                90

            )



        for row in sheet.iter_rows(min_row=2):



            for cell in row:



                if isinstance(cell.value, float):

                    cell.number_format = "0.000000"



    path = OUTPUT_DIR / f"{OUTPUT_PREFIX}.xlsx"



    wb.save(path)



    print(f"Excel saved: {path}")





# ============================================================

# SAVE MD PLOTS

# ============================================================



def save_plots(results):



    for region in REGIONS:



        fig, ax = plt.subplots(

            figsize=(11, 7)

        )



        for phantom, color, marker in zip(

            PHANTOMS,

            ("tab:blue", "tab:orange", "tab:green"),

            ("o", "s", "^")

        ):



            xs, ys = [], []



            for session in SESSIONS:



                item = results.get(

                    (phantom, session), {}

                ).get(region)



                if item:



                    xs.append(session)

                    ys.append(item[0] * 1000)



            if xs:



                ax.plot(

                    xs,

                    ys,

                    marker=marker,

                    linewidth=2,

                    markersize=7,

                    color=color,

                    label=phantom

                )



                for x, y in zip(xs, ys):



                    ax.annotate(

                        f"{y:.3f}",

                        (x, y),

                        textcoords="offset points",

                        xytext=(0, 10),

                        ha="center",

                        fontsize=9,

                        color=color

                    )



        ax.set(

            xlabel="Session",

            ylabel="Mean MD (×10⁻³ mm²/s)",

            title=(

                f"Mean {METRIC} Across Sessions "

                f"- {region} Regions"

            )

        )



        ax.set_xticks(list(SESSIONS))
        ax.set_xticklabels(
            [f"Sess {s}\n(Day {SESSION_DAYS[s]})" for s in SESSIONS],
            fontsize=9
        )



        ax.set_ylim(0, 1.5)

        ax.yaxis.set_major_formatter(

            plt.FuncFormatter(lambda y, _: f"{y:.3f}")

        )



        ax.grid(

            True,

            linestyle="--",

            alpha=0.4

        )



        ax.legend()



        fig.tight_layout()



        path = OUTPUT_DIR / (

            f"{OUTPUT_PREFIX}_{region.lower()}.png"

        )



        fig.savefig(

            path,

            dpi=300,

            bbox_inches="tight"

        )



        print(f"Figure saved: {path}")



    plt.close("all")





# ============================================================

# MAIN

# ============================================================



if __name__ == "__main__":



    if not ROOT.is_dir():



        raise SystemExit(

            f"Root folder does not exist: {ROOT}"

        )



    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results, failures = analyze()



    if not results:



        raise SystemExit(

            "No valid scans found. "

            "Check paths and mask/map alignment."

        )



    save_excel(results, failures)



    save_plots(results)



    print(

        f"Finished: {len(results)}/{len(PHANTOMS) * len(SESSIONS)} scans processed."

    )



    if failures:



        print(

            "Skipped scans (also listed in Excel):"

        )



        for failure in failures:

            print(" -", failure)
