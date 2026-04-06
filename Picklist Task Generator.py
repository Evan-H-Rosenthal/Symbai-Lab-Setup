import os
from tkinter import Tk, filedialog

Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Select Excel File",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if not file_path:
    print("No file selected.")
    exit()

print(f"Using file: {file_path}")



import pandas as pd
import io

uploaded = None

filename = list(uploaded.keys())[0]
df = pd.read_excel(io.BytesIO(uploaded[filename]))

print("File uploaded successfully!")
print("Columns detected:", df.columns.tolist())

import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages

# ==============================
# USER-DEFINED VARIABLE
# ==============================
NUM_PICKLISTS = 10
START_PICKLIST_NUMBER = 1  # New variable for starting picklist number
# ==============================

# Standardize columns
df.columns = ["Item Name", "Bin ID", "Shelf", "Row", "Column"]

# Ensure Picklists folder exists
folder_name = "Tasks"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Sort shelves
shelves = sorted(df["Shelf"].unique())

# Updated lighter colors
row_colors = {
    1: "#ff7f7f",      # lighter red
    2: "yellow",
    3: "#90ee90",      # lighter green
    4: "#65aef7"       # custom blue
}

for picklist_number in range(START_PICKLIST_NUMBER, START_PICKLIST_NUMBER + NUM_PICKLISTS):

    pdf_filename = os.path.join(
        folder_name,
        f"TASK {picklist_number}.pdf"
    )

    with PdfPages(pdf_filename) as pdf:

        for shelf_choice in shelves:

            shelf_df = df[df["Shelf"] == shelf_choice]

            # Create 3 tasks per shelf
            groups = []
            for _ in range(3):
                task_size = random.randint(2, 5)
                selected_items = shelf_df.sample(n=task_size, replace=False)
                groups.append(selected_items)

            # Create 8.5x11 portrait page
            fig = plt.figure(figsize=(8.5, 11))
            ax = plt.gca()
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 17)
            ax.axis("off")

            # PICKLIST TITLE
            plt.text(
                7,
                16.8,
                f"TASK {picklist_number}",
                ha="center",
                va="top",
                fontsize=40,
                weight="bold"
            )

            # MUCH BIGGER Shelf Title
            plt.text(
                7,
                15.5,
                f"Shelf: {shelf_choice}",
                ha="center",
                va="center",
                fontsize=55,
                weight="bold"
            )

            grid_width = 6
            cell_size = 0.9
            start_y_positions = [12, 8, 4]

            for group_idx, group in enumerate(groups):

                start_x = 1
                start_y = start_y_positions[group_idx]

                # Draw hollow grid (6x4)
                for row in range(4):
                    for col in range(6):
                        rect = patches.Rectangle(
                            (start_x + col * cell_size,
                             start_y - row * cell_size),
                            cell_size,
                            cell_size,
                            linewidth=1.5,
                            edgecolor="black",
                            facecolor="none"
                        )
                        ax.add_patch(rect)

                # Fill selected squares
                for _, item in group.iterrows():

                    r = int(item["Row"])
                    c = int(item["Column"])

                    x = start_x + (c - 1) * cell_size
                    y = start_y - (r - 1) * cell_size

                    rect = patches.Rectangle(
                        (x, y),
                        cell_size,
                        cell_size,
                        linewidth=1.5,
                        edgecolor="black",
                        facecolor=row_colors[r]
                    )
                    ax.add_patch(rect)

                    # Display row,column
                    plt.text(
                        x + cell_size / 2,
                        y + cell_size / 2,
                        f"{r} {c}",
                        ha="center",
                        va="center",
                        fontsize=14,
                        weight="bold",
                        color="black"
                    )

                # ---------------------------
                # TASK INDICATOR BOXES
                # ---------------------------
                box_start_x = start_x + grid_width * cell_size + 1.5
                box_y = start_y - 1.5
                box_size = 0.8

                for i in range(3):

                    is_highlighted = (i == group_idx)

                    fill_color = "black" if is_highlighted else "none"

                    rect = patches.Rectangle(
                        (box_start_x + i * (box_size + 0.3), box_y),
                        box_size,
                        box_size,
                        linewidth=2,
                        edgecolor="black",
                        facecolor=fill_color
                    )
                    ax.add_patch(rect)

                    # Only show number inside highlighted box
                    if is_highlighted:
                        plt.text(
                            box_start_x + i * (box_size + 0.3) + box_size / 2,
                            box_y + box_size / 2,
                            str(len(group)),
                            ha="center",
                            va="center",
                            fontsize=20,
                            weight="bold",
                            color="white"
                        )

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    print(f"Created: {pdf_filename}")

print("\nAll Tasks generated inside the 'Tasks' folder.")

import shutil


folder_name = "Tasks"
zip_filename = "Tasks"

# Create zip archive (creates Picklists.zip)
shutil.make_archive(zip_filename, 'zip', folder_name)

print("Zip file created: Tasks.zip")

# Download
print(f"{zip_filename}.zip")