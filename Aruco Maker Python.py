import io
from dataclasses import dataclass
from typing import List, Dict

import cv2
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# GUI
from tkinter import Tk, filedialog, messagebox


@dataclass
class BinRecord:
    bin_id: int
    item_name: str
    shelf: str
    row: str
    col: str


def load_records_from_excel(path: str) -> List[BinRecord]:
    df = pd.read_excel(path)

    required_cols = ["Item Name", "Bin ID", "Shelf", "Row", "Column"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["Bin ID"])

    records = []
    for _, row in df.iterrows():
        try:
            bin_id = int(row["Bin ID"])
        except:
            continue

        records.append(
            BinRecord(
                bin_id=bin_id,
                item_name=str(row["Item Name"]),
                shelf=str(row["Shelf"]),
                row=str(row["Row"]),
                col=str(row["Column"]),
            )
        )

    records.sort(key=lambda r: r.bin_id)
    return records


def generate_aruco_marker_image(marker_id: int, size_px: int = 600) -> ImageReader:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)

    try:
        marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, size_px)
    except AttributeError:
        marker_img = np.zeros((size_px, size_px), dtype=np.uint8)
        cv2.aruco.drawMarker(aruco_dict, marker_id, size_px, marker_img, 1)

    if len(marker_img.shape) == 2:
        marker_img = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2RGB)
    else:
        marker_img = cv2.cvtColor(marker_img, cv2.COLOR_BGR2RGB)

    success, png_bytes = cv2.imencode(".png", marker_img)
    if not success:
        raise RuntimeError("Failed to encode marker")

    return ImageReader(io.BytesIO(png_bytes.tobytes()))


def build_marker_cache(records):
    cache = {}
    for r in records:
        if r.bin_id not in cache:
            cache[r.bin_id] = generate_aruco_marker_image(r.bin_id)
    return cache


def draw_layout_pdf(records, output_path="aruco_custom.pdf"):
    c = canvas.Canvas(output_path, pagesize=letter)
    page_w, page_h = letter

    page_margin = 0.25 * inch
    num_cols = 2
    available_width = page_w - 2 * page_margin
    block_w = (available_width / num_cols) * 0.8

    marker_size = (50.0 / 25.4) * inch
    inner_margin = 0.01 * block_w
    marker_size = min(marker_size, block_w - 2 * inner_margin)

    block_h = marker_size + 0.4 * inch

    shelf_font_size = 40
    rowcol_label_font_size = 10
    rowcol_value_font_size = 24
    id_font_size = 10
    item_font_size = 10

    marker_cache = build_marker_cache(records)

    col_idx = 0
    current_y = page_h - page_margin - block_h

    for rec in records:
        if current_y < page_margin:
            c.showPage()
            current_y = page_h - page_margin - block_h
            col_idx = 0

        total_blocks_width = block_w * num_cols
        leftover_width = available_width - total_blocks_width
        horizontal_offset = page_margin + leftover_width / 2.0

        block_x = horizontal_offset + col_idx * block_w
        block_y = current_y

        c.rect(block_x, block_y, block_w, block_h, stroke=1, fill=0)

        marker_img = marker_cache[rec.bin_id]
        marker_x = block_x + inner_margin
        marker_y = block_y + block_h - inner_margin - marker_size

        c.drawImage(marker_img, marker_x, marker_y,
                    width=marker_size, height=marker_size,
                    preserveAspectRatio=True, mask="auto")

        text_area_x0 = marker_x + marker_size
        text_area_x1 = block_x + block_w - inner_margin
        text_area_w = max(0.0, text_area_x1 - text_area_x0)

        marker_center_y = marker_y + marker_size / 2.0

        # Shelf
        c.setFont("Helvetica-Bold", shelf_font_size)
        shelf_text = str(rec.shelf)
        shelf_width = c.stringWidth(shelf_text, "Helvetica-Bold", shelf_font_size)

        shelf_x = text_area_x0 + (text_area_w - shelf_width) / 2.0
        shelf_y = marker_center_y + 0.1 * inch
        c.drawString(shelf_x, shelf_y, shelf_text)

        # Row/Column
        rowcol_gap = 0.06 * inch
        rowcol_label_y = shelf_y - rowcol_gap - 0.05 * inch
        rowcol_value_y = rowcol_label_y - (rowcol_label_font_size * 2.0 / 72.0 * inch)
        rowcol_label_y += 2

        c.setFont("Helvetica", rowcol_label_font_size)

        half = text_area_w / 2.0 if text_area_w > 0 else 0
        r_center = text_area_x0 + half * 0.5
        c_center = text_area_x0 + half * 1.5

        c.drawString(r_center, rowcol_label_y, "r")
        c.drawString(c_center, rowcol_label_y, "c")

        c.setFont("Helvetica-Bold", rowcol_value_font_size)

        row_text = str(rec.row)
        col_text = str(rec.col)

        row_w = c.stringWidth(row_text, "Helvetica-Bold", rowcol_value_font_size)
        col_w = c.stringWidth(col_text, "Helvetica-Bold", rowcol_value_font_size)

        c.drawString(r_center - row_w/2, rowcol_value_y, row_text)
        c.drawString(c_center - col_w/2, rowcol_value_y, col_text)

        # Bottom text
        bottom_margin = 0.05 * inch
        baseline_y = block_y + bottom_margin

        c.setFont("Helvetica", id_font_size)
        id_text = f"ID: {rec.bin_id}"
        c.drawString(block_x + inner_margin, baseline_y, id_text)

        c.setFont("Helvetica", item_font_size)
        id_width = c.stringWidth(id_text, "Helvetica", id_font_size)

        item_x = block_x + inner_margin + id_width + (0.04 * inch)
        max_item_width = block_x + block_w - inner_margin - item_x

        item_text = rec.item_name
        while c.stringWidth(item_text, "Helvetica", item_font_size) > max_item_width and len(item_text) > 3:
            item_text = item_text[:-4] + "..."

        c.drawString(item_x, baseline_y, item_text)

        col_idx += 1
        if col_idx >= num_cols:
            col_idx = 0
            current_y -= block_h

    c.save()


# 🚀 MAIN (GUI FLOW)
def main():
    Tk().withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        print("No file selected.")
        return

    try:
        records = load_records_from_excel(file_path)
        output_file = "aruco_custom.pdf"

        draw_layout_pdf(records, output_file)

        messagebox.showinfo("Success", f"PDF generated:\n{output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()