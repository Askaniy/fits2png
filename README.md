# fits2png
A small GUI program for converting space images

## Installation

1. Clone the repository or download archive by the GitHub web interface;
2. Make sure you have Python (recommended 3.10 or higher) and the required libraries: [Astropy](https://www.astropy.org/), [NumPy](https://numpy.org/), [Pillow](https://pillow.readthedocs.io/) and [PySimpleGUI](https://pysimplegui.readthedocs.io/). You can install the libraries all at once using [`requirements.txt`](requirements.txt): `python -m pip install -r requirements.txt`;
3. Run [`fits2png.py`](fits2png.py).

## Notes

- To save as TIFF without compression, release the button `compress to PNG`
- To recognize New Horizon's MVIC image and apply conversion factor, the corresponding button must be pressed and the file name must begin with `mc0`, `mc1`, `mc2` or `mc3`. This happens by itself if you download images from [OPUS](https://opus.pds-rings.seti.org/).
