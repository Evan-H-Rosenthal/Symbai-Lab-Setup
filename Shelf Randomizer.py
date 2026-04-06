import pandas as pd
import random
import os
from tkinter import Tk, filedialog

# ==== Config ====
SHELF_BANKS = ['A','B','C']
ROWS = list(range(1, 3))
COLUMNS = list(range(1, 4))
TOTAL_SLOTS = len(SHELF_BANKS) * len(ROWS) * len(COLUMNS)

SHELF_COL_NAME = 'Shelf'
ROW_COL_NAME = 'Row'
COLUMN_COL_NAME = 'Column'


# ==== Helper functions ====
def generate_all_slots():
    return [(shelf, row, col) for shelf in SHELF_BANKS for row in ROWS for col in COLUMNS]


def assign_slots_to_items(n_items):
    all_slots = generate_all_slots()
    random.shuffle(all_slots)
    return all_slots[:n_items] if n_items <= TOTAL_SLOTS else all_slots


def main():
    # File picker
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        print("No file selected.")
        return

    print(f"Loaded file: {file_path}")

    # Load workbook
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    print("Available sheets:", ", ".join(xls.sheet_names))

    sheet_name = input("Enter sheet name to randomize: ").strip()

    if sheet_name not in xls.sheet_names:
        print("Invalid sheet name.")
        return

    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    print(f"Loaded {len(df)} rows")

    # Normalize column names
    col_map = {}
    for col in df.columns:
        if col.lower() == SHELF_COL_NAME.lower():
            col_map[col] = SHELF_COL_NAME
        elif col.lower() == ROW_COL_NAME.lower():
            col_map[col] = ROW_COL_NAME
        elif col.lower() == COLUMN_COL_NAME.lower():
            col_map[col] = COLUMN_COL_NAME

    df = df.rename(columns=col_map)

    for c in [SHELF_COL_NAME, ROW_COL_NAME, COLUMN_COL_NAME]:
        if c not in df.columns:
            df[c] = pd.NA

    # Random assignment
    n_items = len(df)
    slots = assign_slots_to_items(n_items)

    row_indices = list(df.index)
    random.shuffle(row_indices)

    for i in range(min(n_items, len(slots))):
        idx = row_indices[i]
        shelf, row, col = slots[i]
        df.at[idx, SHELF_COL_NAME] = shelf
        df.at[idx, ROW_COL_NAME] = row
        df.at[idx, COLUMN_COL_NAME] = col

    if n_items > len(slots):
        print(f"WARNING: {n_items - len(slots)} items unassigned")
        for i in range(len(slots), n_items):
            idx = row_indices[i]
            df.at[idx, SHELF_COL_NAME] = "UNASSIGNED"
            df.at[idx, ROW_COL_NAME] = pd.NA
            df.at[idx, COLUMN_COL_NAME] = pd.NA

    # Save output next to input
    base = os.path.basename(file_path)
    out_name = os.path.join(os.path.dirname(file_path), f"randomized_{base}")

    with pd.ExcelWriter(out_name, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Done! Saved to: {out_name}")


if __name__ == "__main__":
    main()
