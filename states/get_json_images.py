
import json
from PIL import Image, ImageDraw


with open('data.json', 'r') as f:
    raw_data = json.load(f)


data_type_and_size = {
    'Saturday_Tournaments': 600,
    'Prez': 500,
    'Friday_Tournaments': 500,
    'Worksheets': 100,
    'Rankings': 100,
    'sweeps_calculation': 100
}

def make_image(raw_text, size):
    image = Image.new('RGB', (200, size), 'white')
    draw = ImageDraw.Draw(image)
    draw.multiline_text((10, 10), json.dumps(raw_text, indent=2), fill='black')
    return image

def combine_image(images, filename):
    # layout
    # saturday, friday, prez
    # worksheets, rankings, sweeps
    satTourn = images['Saturday_Tournaments']
    friTourn = images['Friday_Tournaments']
    prez = images['Prez']
    worksheets = images['Worksheets']
    rankings = images['Rankings']
    sweeps = images['sweeps_calculation']

    image = Image.new('RGB', (600, 700), 'white')

    image.paste(satTourn, (0, 0))
    image.paste(worksheets, (0, 600))
    image.paste(friTourn, (200, 0))
    image.paste(rankings, (200, 600))
    image.paste(prez, (400, 0))
    image.paste(sweeps, (400, 600))

    image.save(filename)



for division in raw_data:
    for person in raw_data[division]:
        images = {}
        for data, size in data_type_and_size.items():
            player_data = person[data]
            images[data] = make_image(player_data, size)
        combine_image(images, f"2023-2024/raw_charts/{person['Name'].replace(' ', '')}_json.png")
