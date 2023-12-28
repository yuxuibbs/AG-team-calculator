import pandas as pd
from PIL import Image

players = pd.read_csv('2023-2024/qualified_players.csv')
players['Name'] = players['FirstName'] + ' ' + players['LastName']

for name in players['Name']:
    player_name = name.replace(' ', '')
    # Get images
    # all matches
    image1 = Image.open(f"2023-2024/raw_charts/{player_name}_all.png")
    # individual score from each match
    image2 = Image.open(f"2023-2024/raw_charts/{player_name}_individual.png")
    # prez graph
    image3 = Image.open(f"2023-2024/raw_charts/{player_name}_prez.png")
    # prez results
    image4 = Image.open(f"2023-2024/raw_charts/{player_name}_prez_data.png")
    # json
    image5 = Image.open(f"2023-2024/raw_charts/{player_name}_json.png")
    # Get the dimensions of the images
    width1, height1 = image1.size
    width2, height2 = image2.size
    width3, height3 = image3.size
    width4, height4 = image4.size
    width5, height5 = image5.size
    # Create a new image with the total dimensions
    stitched_image = Image.new('RGB',
        (width1 + width3, max(height1, height3 + height5)),
        'white')
    # Paste the images onto the new image
    padding = 20
    stitched_image.paste(image1, (0, 0))
    stitched_image.paste(image2, (width1 + padding, 0))
    stitched_image.paste(image3, (width1, height5))
    stitched_image.paste(image4, (width1 + width2 + padding * 2, 0))
    stitched_image.paste(image5, (width1 + width2 + width4 + padding * 3, 0))
    # Save image
    stitched_image.save(f"2023-2024/charts_by_name/{player_name}.png")
