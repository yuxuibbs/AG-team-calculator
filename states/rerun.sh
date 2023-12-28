set -e

echo "cleaning data"
python3 clean_data.py

echo "making states json"
python3 states_data.py

echo "creating images for matches"
python3 get_matches_by_name.py

echo "creating images for prez"
python3 make_prez_graphs_by_name.py

echo "creating images from json"
python3 get_json_images.py

echo "combining images"
python3 combine_images.py
