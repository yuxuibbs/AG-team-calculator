
import json
from PIL import Image, ImageDraw


with open('data.json', 'r') as f:
    raw_data = json.load(f)


data_type_and_size = {
    'Saturday_Tournaments': 600,
    'Prez': 650,
    'Friday_Tournaments': 500,
    'Worksheets': 100,
    'Rankings': 100,
    'Friday_sweeps_calculation': 100,
    'States': 500,
    'States_sweeps_scores': 500
}

def make_image(raw_text, data_type, size):
    image = Image.new('RGB', (200, size), 'white')
    draw = ImageDraw.Draw(image)
    # insert json
    draw.multiline_text((10, 10), json.dumps(raw_text, indent=2), fill='black')
    # label json
    draw.text((15, 10), data_type, fill='blue')
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
    friday_sweeps = images['Friday_sweeps_calculation']
    states = images['States']
    states_sweeps = images['States_sweeps_scores']

    image = Image.new('RGB', (700, 900), 'white')

    # paste json as images
    image.paste(satTourn, (0, 0))
    image.paste(worksheets, (0, 600))
    image.paste(friTourn, (175, 0))
    image.paste(rankings, (175, 600))
    image.paste(prez, (350, 0))
    image.paste(friday_sweeps, (350, 600))
    image.paste(states, (500, 0))
    image.paste(states_sweeps, (500, 600))

    image.save(filename)



for division in raw_data:
    for person in raw_data[division]:
        images = {}
        for data, size in data_type_and_size.items():
            player_data = person[data]
            images[data] = make_image(player_data, data, size)
        combine_image(images, f"2023-2024/raw_charts/{person['Name'].replace(' ', '')}_json.png")
