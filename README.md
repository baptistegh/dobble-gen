# Dobble Gen 🎴

Create your own personalized **Dobble** (or **Spot It!**) card game using your own set of images. This project generates a complete, print-ready PDF of cards based on the mathematical principles of finite projective planes, ensuring that any two cards have exactly one symbol in common.

## Features

- **Mathematically Perfect**: Generates a complete set of cards where every two cards share exactly one symbol (based on finite projective plane theory).
- **Use Your Own Images**: Simply drop your `.jpg`, `.png`, or `.heif` files into the `images` directory.
- **Customizable**: Easily configure symbols per card, card size, DPI, and other parameters via CLI options.
- **Print-Ready Output**: Produces a multi-page A4 PDF (`output/dobble.pdf`) with cards ready for printing and cutting.
- **Circle Packing**: Uses advanced circle packing algorithms to arrange symbols elegantly on each card.
- **No Symbol Overlap**: Intelligent placement ensures symbols are properly spaced and don't overlap.

## How It Works

The generation process follows these steps:

1. **Load Images**: Loads all supported images from the input directory (`.jpg`, `.png`, `.heif`)
2. **Validate**: Ensures you have enough unique images for the desired card configuration
3. **Generate Combinations**: Uses finite projective plane mathematics to create perfect card combinations
4. **Create Cards**: For each card:
   - Draws a circular white background with a styled border
   - Uses circle packing to optimally arrange symbols with random sizes and rotations
   - Ensures no symbols overlap while maximizing visual interest
5. **Assemble PDF**: Combines all card images into a print-ready, multi-page A4 PDF

## Installation

Install the package from PyPI:

```sh
pip install dobble-gen
```

## Quick Start

### Using the CLI

```sh
dobble-gen --image-dir images/ --symbols-per-card 7 --output-dir output/
```

### Available Options

```
--image-dir        Directory containing symbol images (default: images)
--output-dir       Directory for output files (default: output)
--symbols-per-card Number of symbols per card, must be prime + 1 (default: 8)
--card-diameter-cm Diameter of each card in cm (default: 10)
--dpi              Output resolution in DPI (default: 300)
--max-placement-retries Maximum attempts to place symbols (default: 1000)
```

### Example Configurations

- **7 symbols per card**: Creates 43 cards with 43 unique symbols
  ```sh
  dobble-gen --symbols-per-card 7 --image-dir images/
  ```

- **6 symbols per card**: Creates 31 cards with 31 unique symbols
  ```sh
  dobble-gen --symbols-per-card 6 --image-dir images/
  ```

- **Custom card size and quality**:
  ```sh
  dobble-gen --card-diameter-cm 12 --dpi 600 --image-dir images/
  ```

## Development Setup

### Prerequisites

- Python 3.10+
- `uv` (for package management)

### Steps

1. **Clone the repository:**
   ```sh
   git clone git@github.com:baptistegh/dobble-gen.git
   cd dobble-gen
   ```

2. **Add your images:**
   Create an `images` directory and place your symbol images inside:
   ```sh
   mkdir images
   # Add your .png, .jpg, .heif files here
   ```
   
   > **Note**: For 7 symbols per card, you need exactly 43 unique images. For 8 symbols per card, you need 57 images. The script will inform you of the required count.

3. **Install dependencies:**
   ```sh
   make install
   ```

4. **Generate the cards:**
   ```sh
   make run
   ```

## Output

Your generated files will be created in the `output/` directory:

- `output/cards/`: Contains individual `.png` images for each card
- `output/dobble.pdf`: The final, print-ready PDF file ready for printing and cutting

## Mathematical Background

This project uses the theory of **finite projective planes** to ensure the Dobble property (any two cards share exactly one symbol). For a projective plane of order `n`:

- Each card has `n + 1` symbols
- Total cards = `n² - n + 1`
- Total unique symbols = `n² - n + 1`
- Any two cards share exactly one symbol

Example: With 8 symbols per card (order 7), you get 57 cards with 57 unique symbols.

## Troubleshooting

**"You need X unique images"** - You don't have enough unique images for your configuration. Provide more images or reduce `symbols-per-card`.

**Symbols overlapping** - Increase `--max-placement-retries` to allow more placement attempts.

**Poor symbol arrangement** - Try with different `--symbols-per-card` values to find a configuration that works best with your images.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
