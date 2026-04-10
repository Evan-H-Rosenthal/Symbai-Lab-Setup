Symbiotic AI: Lab Environment Setup



Preface:

The following document will walk you through setting up the lab environment used in this Symbiotic AI project. Please note that this exact lab environment is not required for the project, and similar objects/setup can be used to fit your specific application.



Curating a Dataset:

You can use any assortment of distinct, unique objects to curate the dataset. Our dataset consisted of120 unique objects.The Excel Spreadsheet for the dataset is included in this repo as Randomized_Objects_List.xlsx. You can find links to most of the objects (or substitutes) inAppendix 1.



In particular, we chose objects that were challenging for computer vision models to recognize, which includes:

- Acrylic Gems:Complex facets and transparent material make their appearance change as the light shifts.
- Foam Letters:Similarly-colored/textured objects with differing distinct shapes that could be interpreted differently depending on orientation.
- Plastic Tableware:Similarly-shaped (yet not identical) objects with distinct colors.



Other objects that we haven’t tested, but would (probably) make good objects for the dataset could be:

- Lego Bricks:The sheer variety of pieces allows for objects that have similar shapes with different colors, and similar colors with different shapes. There are also pieces that have similar shapes, but different lengths/sizes (1x1 vs 2x2).
- Nuts/Bolts/Screws:Similar shapes and colors that differ only in length or in size. This one might be really tricky.



When sourcing your dataset, it’s important to make sure you haveat least three copies of each object.With the way picklists are generated (see “Generating Picklists”), each object has the potential to be selected up to three times per task. Having sufficient amounts of each object will allow the data collection to go smoothly.



Creating the Dataset:

Our project implementation uses120 unique objectsrandomly divided amongstfive banks of shelves.This section will show you how to create and format anExcel Spreadsheetwhich will be used torandomize the positions of the objects, create Aruco Markers, and create Picklists.



1. Create a new Excel Spreadsheet.
2. At the top, enter in the following column names:
3. For each of your unique items, enter in its name, as well as which bin it’s going in. If you haven’t labeled your bins, then just start sequentially (their positions will be randomized in the next step). Don’t enter anything into the other three columns.
4. Use theRack RandomizerColab(Or the regular Python Script) to automatically assign and randomize the positions of the items.Make sure to adjust the parameters to match your lab setup.For instance, if you havethree racks of shelves, where each rack hastwo shelves,and each shelf can holdthree bins,you’d make the parameters look like this:
5. In the newly downloaded spreadsheet, select all five columns, then go todata > sort.Add two additional levels, and sort by Shelf, Row, Column in that order.



Your Excel spreadsheet is now ready to use! Don’t forget to save your work.

Creating the Aruco Markers

Once you have your Excel spreadsheet, you can use theAruco Maker Colabnotebook (or the regular Python Script) to automatically generate Aruco markers for each item in the dataset. Simply run all the cells (or the script), select yourRandomized Objects List,and the PDF will automatically be created.



You will also need Aruco Markers 990, 991, and 992 for the output bins.You can find them in the repository as a printable PDF, or you can make your own using the5x5 Aruco Library.After printing, you should cut along the solid lines.

Setting up the Lab Environment

You will need:

- Enough bins to hold your dataset objects (we recommend these ones from Uline:https://www.uline.com/BL_305/Uline-Plastic-Stackable-Bins) + 3 additional bins for the output.
- Enough shelves to hold your bins. Our dataset used five banks of shelves with four shelves each, where each shelf could hold six bins side-by-side for a total of 120 unique objects.
- An additional shelf for your Output Bins
- Your dataset objects
- Your Aruco Markers, plus markers 990, 991, and 992



1. Start with an empty shelf. Clearly label it with a letter (preferably one of the letters you used when creating your Excel Sheet). Use some sort of colored tape to label each shelf in the colors of your choice(remember these colors!)
2. Gather all copies ofone of your objects,as well as itscorresponding Aruco Markerandone bin.
3. Place the objects in the bin and affix the Aruco Marker to the front of the bin such that it is standing up.The bins we are using have a slot in the front that is the perfect size for the markers!However, you can use tape to affix the marker. If your paper is thin, you can tape the marker to a piece of cardboard before affixing it to prop it up and prevent it from sagging over.
4. Place the bin in its corresponding location on the shelf.The marker generator generates the numbers in (row, column) format.
5. Repeat with the rest of the bins on the shelf.
6. Repeat withall other shelves.
7. Place three binsside-by-sidein a suitable location (shelf, table, etc). From left to right, affix Aruco markers990, 991, and 992to the front of each of these bins. These will be youroutput bins.



Generating The Tasks

To make generating tasks easy, a Python Notebook has been developed whichautomatically generates a certain amount of tasksbased on parameters you choose, allowing for easy printing.



To use the Python Notebook, simply upload or choose yourRandomized Objects List(the one you should have made earlier in the guide), and run all the cells. By default, the notebook will generate10 tasks labelled 1 through 10, but you should change this if you want to generate more.



Task PDFs will look something like this:





Collecting the Data

To collect data, you will needany type of egocentric camera,such as a GoPro, Meta Glasses, or other head-wearable camera apparatus. The data for this project was collected using aGoPro Hero 13 Blackwith aWide-Angle Lens.



Every task will haveN amount of sub-tasks (pages),whereNis the amount of shelves you have in your setup. Our experiment hasfive shelves,so each task hasfive sub-tasks. Every sub-task will have one video associated with it.



To complete a sub-task, follow the steps:

1. Mount or wear your camera.Use a friend or camera feed to confirm that the camera can see your hand.
2. Pick up the firstsub-taskpage for the task you are completing.
3. Start recording.It’s useful if your camera has a voice activation function.
4. Start with the topmost grid on the sub-task sheet. Select one object from the grid and locate it on the sub-task’s shelf.

1. Takeonecopy of the object from the bin.Do not take multiple objects.
2. Carry the object,open-palmed,to the output bins.
3. Deposit the object into the corresponding output bin. The top grid corresponds with output bin #1, the middle with #2, etc.
4. Repeat steps a-d with all other objects in the grid.

1. Repeat step 4with the remaining two grids.
2. Stop the recording.



When you arefinished with a sub-task,you may need to reset the lab by putting the objects in the output bins back to where they went.







Appendix 1: Dataset Objects

Please note that any assortment of unique objects should suffice. Some objects are not available anymore, but can be substituted for any other unique object.

Acrylic Gems:https://a.co/d/0iq4STys

Colored Paperclips:https://a.co/d/0iq4STys

IKEA PRIDLIG Owl/Leaf Clips:No longer sold in stores. Replace with9unique object types of any origin.

Foam Letters:https://www.target.com/p/munchkin-bath-letters-and-numbers-36ct-bath-toy-set/-/A-14026155?sid=2137S&afid=google&TCID=OGS&CPNG=Baby&adgroup=30-4(Each set contains 1 of each letter for a total of 26 unique objects. You’ll need at least 3 sets.)

IKEA KALAS Flatware Set:https://www.ikea.com/us/en/p/kalas-18-piece-flatware-set-mixed-colors-seasonal-edition-30620094/(Each set contains 1 fork, knife, and spoon in each of the 6 colors. You’ll need at least 3 sets.)

IKEA BEVARA Plastic Sealing Clips:https://a.co/d/0gydRNhG(Similar item)

Clear Acrylic Circular Tiles:https://a.co/d/02pwj52M

Red Square Tiles:https://a.co/d/0gAE6ubt(Similar item, pick out the red ones or use each color as a unique object)

Wooden Tiles:https://a.co/d/0dLYki0V(Similar item)

Candles:https://a.co/d/013cMZ4N

Black Casing:Unknown origin. Replace with1unique object type of any origin.

Blue Casing:Unknown origin. Replace with1unique object type of any origin.

Alligator Clips:https://a.co/d/0iNJln7d

Clothespins:https://a.co/d/06u5WJJU

Wooden Beads:Unknown origin. Replace with colored marbles similar tohttps://a.co/d/04yI2Qqw(Bigger ones) orhttps://a.co/d/0e0Ahyme(Smaller ones)





