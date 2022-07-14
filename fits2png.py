import numpy as np
import PySimpleGUI as sg
from astropy.io import fits
from PIL import Image

# New Horizons' MVIC conversion factors
# https://pdssbn.astro.umd.edu/holdings/nh-j-alice-3-jupiter-v1.0/document/soc_inst_icd/soc_inst_icd.pdf table 10.6, p.63
#              red     blue    NIR     CH4
mvic_coeffs = (0.8088, 2.1752, 0.7898, 0.5752)


sg.LOOK_AND_FEEL_TABLE["MaterialDark"] = {
    'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
    'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#424242',
    'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
}
sg.ChangeLookAndFeel("MaterialDark")


layout = [
    [sg.Text("FITS path", s=14), sg.Input(key="open path", s=36), sg.FileBrowse()],
    [sg.Text("PNG folder", s=14), sg.Input(key="save path", s=36), sg.FolderBrowse()],
    [sg.Checkbox("compress to PNG", default=True, s=16, key="PNG"), sg.Text("Multiply by", s=8),
    sg.Input("1", s=5, key="scale"), sg.T("", s=2), sg.Checkbox("NH's MVIC filters", s=15, key="MVIC"),
    sg.Button("Start")],
    [sg.Multiline("\nWelcome! This is the log output.\n\n", size=(69, 16), key="ml")]
]

window = sg.Window("FITS to PNG", layout)

def p(text):
    window["ml"].print(text)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Start":

        path = values["open path"]
        save = values["save path"]
        if save == "":
            save = "/".join(path.split("/")[:-1])
        
        try:
            with fits.open(path) as hdul:
                p("FITS info:")
                for i in hdul.info(False):
                    p(i)
                
                name = "".join(path.split("/")[-1].split(".")[:-1])
                k = 1
                if values["MVIC"] and name[:2] == "mc":
                    k = mvic_coeffs[int(name[2])]
                scale = float(values["scale"])

                img_np = np.flip(hdul[0].data, 1).clip(0, None) * k * scale
                img_pil = Image.fromarray(img_np)

                ext = "tiff"
                if values["PNG"]:
                    ext = "png"
                    img_pil = img_pil.convert("I")
                
                img_pil.save(f'{save}/{name}.{ext}')

                p("Done\n")

        except Exception as e:
            p(e)

window.close()