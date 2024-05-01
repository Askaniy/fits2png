import numpy as np
import FreeSimpleGUI as sg
from astropy.io import fits
from PIL import Image

# New Horizons' MVIC conversion factors
# https://pdssbn.astro.umd.edu/holdings/nh-j-alice-3-jupiter-v1.0/document/soc_inst_icd/soc_inst_icd.pdf table 10.6, p.63
#              red     blue    NIR     CH4
mvic_coeffs = (0.0554, 0.149, 0.0541, 0.0394)


main_color = '#3884A9'
text_color = '#FFFFFF'
muted_color = '#A3A3A3'
highlight_color = '#5A5A5A'
bg_color = '#333333'
inputON_color = '#424242'
inputOFF_color = '#3A3A3A'

# FreeSimpleGUI custom theme
sg.LOOK_AND_FEEL_TABLE['MaterialDark'] = {
        'BACKGROUND': bg_color, 'TEXT': text_color,
        'INPUT': inputON_color, 'TEXT_INPUT': text_color, 'SCROLL': inputON_color,
        'BUTTON': (text_color, main_color), 'PROGRESS': ('#000000', '#000000'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
    }
sg.ChangeLookAndFeel('MaterialDark')


layout = [
    [sg.Text('FITS path', s=14), sg.Input(key='open path', s=47), sg.FileBrowse()],
    [sg.Text('PNG folder', s=14), sg.Input(key='save path', s=47), sg.FolderBrowse()],
    [
        sg.Checkbox('compress to PNG', default=True, s=19, key='PNG'), sg.Text('multiply by', s=9),
        sg.Input('1', s=5, key='scale'), sg.T('', s=2), sg.Checkbox('NH’s MVIC filters', s=16, key='MVIC'),
        sg.Button('Start')
    ],
    [sg.Multiline('\nWelcome! This is the log output.\n\n', size=(72, 16), key='ml')]
]

window = sg.Window('FITS to PNG', layout)

def w_print(text: str):
    window['ml'].print(text)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Start':

        path = values['open path']
        save = values['save path']
        if save == '':
            save = '/'.join(path.split('/')[:-1])
        
        try:
            with fits.open(path) as hdul:
                w_print('FITS info:')
                for i in hdul.info(False):
                    w_print(i)
                
                name = ''.join(path.split('/')[-1].split('.')[:-1])
                k = 1
                if values['MVIC'] and name[:2] == 'mc':
                    n = int(name[2])
                    w_print(f'Recognized as {("red", "blue", "NIR", "CH4")[n]} MVIC filter')
                    k = mvic_coeffs[n]
                scale = float(values['scale'])

                img_np = np.flip(hdul[0].data, 0).clip(0, None) * k * scale
                img_pil = Image.fromarray(img_np)

                ext = 'tiff'
                if values['PNG']:
                    ext = 'png'
                    img_pil = img_pil.convert('I')
                
                img_pil.save(f'{save}/{name}.{ext}')

                w_print('Done\n')

        except Exception as e:
            w_print(e)

window.close()