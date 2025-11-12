# Dobble Gen 🎴

Create your own personalized **Dobble** (or **Spot It!**) card game using your own set of images. This project generates a complete, print-ready PDF of cards based on the mathematical principles of finite projective planes, ensuring that any two cards have exactly one symbol in common.

## Features

*   **Mathematically Perfect**: Generates a complete set of cards where every card has a unique symbol in common with any other card.
*   **Use Your Own Images**: Simply drop your `.jpg`, `.png`, or `.heif` files into the `images` directory.
*   **Customizable**: Easily change the number of symbols per card, the card size, and other parameters in the `generator.py` script.
*   **Print-Ready Output**: Produces a multi-page A4 PDF (`output/dobble.pdf`) with cards ready for printing and cutting.

## How It Works

The script first loads all images from the `images-dir` directory. It then calculates the required number of cards and symbols based on the `symbols-per-card` parameter using the properties of a finite projective plane.

For each card, it:
1.  Draws a white circular background with a visible border for easy cutting.
2.  Arranges the corresponding symbols on the card with random sizes, rotations, and positions, ensuring they don't overlap.
3.  Saves the card as a `.png` file in the output directory.

Finally, it assembles all the individual card images into a single `dobble.pdf` file, laid out to fit on A4 pages.

## Usage

You can download the python package with `pip`.

```sh
pip install dobble-gen
```

Then the command line utility should be available for you.

Eg.

```sh
dobble-gen --image-dir images/ --symbols-per-card 7  --output-dir output/
```

## Contributing
### Prerequisites

* Python 3.10+
* `curl` and `sh` (for automatically installing `uv` if not present).
  
### Steps

1.  **Clone the repository:**
    ```sh
    git clone git@github.com:baptistegh/dobble-gen.git
    cd dobble-gen
    ```

2.  **Add your images:**
    Create an `images` directory and place your desired symbol images inside it. The more unique images you have, the better!
    ```sh
    mkdir images
    # Add your .png, .jpg, .heif files here
    ```
    > **Note**: The number of unique images required depends on the `SYMBOLS_PER_CARD` setting. The script will tell you if you don't have enough and will reuse images to complete the set.

3.  **Install dependencies:**
    The `Makefile` handles everything for you. It will create a virtual environment and install all necessary packages using `uv`.
    ```sh
    make install
    ```

## Usage

To generate the cards and the final PDF, simply run:

```sh
make run
```

Your files will be created in the `output/` directory:
*   `output/cartes/`: Contains the individual `.png` image for each card.
*   `output/dobble.pdf`: The final, print-ready PDF file.

## Customization

You can easily tweak the game's parameters by editing the constants at the top of the `src/dobble_gen/generator.py` file:

*   `CARD_DIAMETER_CM`: The physical diameter of the cards when printed.
*   `SYMBOLS_PER_CARD`: The number of symbols on each card. This determines the total number of cards and symbols needed. (e.g., 7 symbols/card = 43 cards, 8 symbols/card = 57 cards).
*   `DPI`: The print quality of the output images.
