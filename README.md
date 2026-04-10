# Symbiotic AI: Lab Environment Setup

## Preface
This document walks through setting up the lab environment used in the Symbiotic AI project. This exact setup is not required—similar objects and layouts can be substituted.

---

## Curating a Dataset

You can use any assortment of distinct objects. The reference setup used **120 unique objects**.

### Recommended Object Types
- Acrylic Gems (lighting-sensitive, reflective)
- Foam Letters (shape variation)
- Plastic Tableware (similar shapes, different colors)

### Other Ideas
- Lego Bricks
- Nuts, Bolts, Screws

> Ensure you have **at least 3 copies of each object**, since picklists may request the same object multiple times.

---

## Creating the Dataset

1. Create a new Excel spreadsheet.
2. Add columns:

![Excel Format](images/page_2.png)

- Item Name  
- Bin ID  
- Shelf  
- Row  
- Column  

3. Fill in Item Name + Bin ID.
4. Run the **Rack Randomizer script** to assign Shelf/Row/Column.
5. Sort by:
   - Shelf → Row → Column

Example config:

![Config](images/page_3.png)

---

## Creating ArUco Markers

Use the ArUco generator script/notebook to create markers.

![Markers Example](images/page_4.png)

Also create markers:
- 990
- 991
- 992

These are used for output bins.

---

## Setting Up the Lab Environment

### Requirements
- Storage bins
- Shelving system
- Dataset objects
- ArUco markers

### Steps

#### 1. Label Shelves
Use letters + colored tape.

![Shelf Labeling](images/page_6.png)

---

#### 2. Prepare Bins
Place objects + attach marker.

![Object + Marker](images/page_7.png)

---

#### 3. Mount Marker
Ensure marker is upright and visible.

![Mounted Marker](images/page_8.png)

---

#### 4. Place Bins
Position bins according to (row, column).

![Placement](images/page_9.png)

---

#### 5–6. Fill Shelves
Repeat for all bins and shelves.

![Full Shelf](images/page_10.png)

---

#### 7. Output Bins
Set up 3 bins labeled:
- 990
- 991
- 992

---

## Generating Tasks

Use the picklist generator notebook/script:
- Input: randomized dataset
- Output: task PDFs

Each task contains multiple sub-tasks (one per shelf).

---

## Collecting Data

### Equipment
- Egocentric camera (GoPro recommended)

### Workflow

1. Start recording
2. Follow task sheet
3. For each object:
   - Pick one item
   - Move to output bin
   - Place correctly

4. Repeat for all grids
5. Stop recording

---

## Resetting

After each task:
- Return items from output bins

---

## Appendix: Example Objects

- Acrylic Gems
- Paperclips
- Foam Letters
- Plastic utensils
- Clips, tiles, beads, etc.

Substitutions are acceptable.
