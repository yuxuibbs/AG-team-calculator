from flask import Flask, render_template, url_for
import json

SATURDAY_TOURNAMENT_MONTHS = ['Sept', 'Oct', 'Nov', 'Dec', 'Jan']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'


@app.route('/')
def home():
    return render_template('index.html')


def get_data(level, data):
    person_data = []
    level = data[level]
    for person in level:
        temp_data = {}
        # all data
        temp_data['all'] = json.dumps(person, indent=4)
        # name
        temp_data['name'] = person['Name']
        # states team
        temp_data['team'] = person['States']['TeamNumber']
        # sweeps
        temp_data['Friday_sweeps'] = person['Friday_sweeps']
        temp_data['Friday_sweeps_calculation'] = json.dumps(person['Friday_sweeps_calculation'], indent=4, sort_keys=True)
        temp_data['States_sweeps'] = person['States_sweeps']
        temp_data['States'] = json.dumps(person['States'], indent=4, sort_keys=True)
        # worksheets
        if 'Worksheets' in person:
            temp_data['worksheets'] = person['Worksheets']['total']
            temp_data['worksheets_calculation'] = json.dumps(person['Worksheets'], indent=4, sort_keys=True)
        else:
            temp_data['worksheets'] = None
            temp_data['worksheets_calculation'] = None
        # challenge matches
        if 'Challenge_Matches' in person:
            temp_data['challenge_matches'] = json.dumps(person['Challenge_Matches'], indent=4, sort_keys=True)
        else:
            temp_data['challenge_matches'] = None
        # friday tournaments
        if 'Friday_Tournaments' in person:
            if 'EQ' in person['Friday_Tournaments']:
                eq_data = {
                    "matches": person['Friday_Tournaments']['EQ'],
                    "num_matches": person['Friday_Tournaments']['EQ_num_matches'],
                    "total": person['Friday_Tournaments']['EQ_total'],
                    "mean": person['Friday_Tournaments']['EQ_mean']
                }
                temp_data['friday_eq_data'] = json.dumps(eq_data, indent=4, sort_keys=True)
                temp_data['friday_eq'] = person['Friday_Tournaments']['EQ_mean']
            if 'OS' in person['Friday_Tournaments']:
                os_data = {
                    "matches": person['Friday_Tournaments']['OS'],
                    "num_matches": person['Friday_Tournaments']['OS_num_matches'],
                    "total": person['Friday_Tournaments']['OS_total'],
                    "mean": person['Friday_Tournaments']['OS_mean']
                }
                temp_data['friday_os_data'] = json.dumps(os_data, indent=4, sort_keys=True)
                temp_data['friday_os'] = person['Friday_Tournaments']['OS_mean']
            if 'Ling' in person['Friday_Tournaments']:
                ling_data = {
                    "matches": person['Friday_Tournaments']['Ling'],
                    "num_matches": person['Friday_Tournaments']['Ling_num_matches'],
                    "total": person['Friday_Tournaments']['Ling_total'],
                    "mean": person['Friday_Tournaments']['Ling_mean']
                }
                temp_data['friday_ling_data'] = json.dumps(ling_data, indent=4, sort_keys=True)
                temp_data['friday_ling'] = person['Friday_Tournaments']['Ling_mean']
        # prez
        if 'Prez' in person:
            temp_data['prez_mean'] = person['Prez']['prez_mean']
            prez_data = {
                "prez_scores": person['Prez']['prez_scores'],
                "prez_mean": person['Prez']['prez_mean'],
                "prez_total": person['Prez']['prez_total'],
                "prez_scaled": person['Prez']['prez_scaled'],
                "prez_1st_half": person['Prez']['prez_first_half'],
                "prez_2nd_half": person['Prez']['prez_second_half']
            }
            temp_data['prez_data'] = json.dumps(prez_data, indent=4, sort_keys=True)
        # saturday tournaments
        if 'Saturday_Tournaments' in person:
            for month in SATURDAY_TOURNAMENT_MONTHS:
                temp_data['saturday_top_3_mean'] = person['Saturday_Tournaments']['saturday_top_3_mean']
                if month in person['Saturday_Tournaments']:
                    temp_data[month + '_saturday'] = '<strong>' + str(person['Saturday_Tournaments'][month]['score']) + '</strong> at table <strong>' + str(person['Saturday_Tournaments'][month]['table']) + "</strong> " + person['Saturday_Tournaments'][month]['game']
                    temp_data['saturday_data'] = json.dumps({
                                                'scores': person['Saturday_Tournaments']['saturday_scores'],
                                                'num': person['Saturday_Tournaments']['num_sat_tournaments'],
                                                'mean': person['Saturday_Tournaments']['saturday_mean_score'],
                                                'tables': person['Saturday_Tournaments']['saturday_mean_table'],
                                                'mean_table': person['Saturday_Tournaments']['saturday_mean_table'],
                                                'top_3_sum': person['Saturday_Tournaments']['saturday_top_3']
                                                }, indent=4)
        # ranks
        if 'Rankings' in person:
            temp_data['friday_rank'] = int(person['Rankings']['friday_rank'])
            temp_data['saturday_rank'] = int(person['Rankings']['saturday_rank'])
            temp_data['states_rank'] = int(person['Rankings']['states_rank'])
            temp_data['total_rank'] = int(person['Rankings']['total_rank'])
            temp_data['adjusted_Friday_sweeps'] = person['adjusted_Friday_sweeps']
            temp_data['adjusted_States_sweeps'] = person['adjusted_States_sweeps']
        # challenge matches
        if 'Challenge_Matches' in person:
            temp_data['challenge_matches'] = json.dumps(person['Challenge_Matches'], indent=4, sort_keys=True)
        person_data.append(temp_data)
    return person_data

@app.route('/elementary')
def elementary():
    with open('data.json') as f:
        data = json.load(f)
    person_data = get_data('Elementary', data)
    return render_template('display.html', level="Elementary" , data=person_data)

@app.route('/middle')
def middle():
    with open('data.json') as f:
        data = json.load(f)
    person_data = get_data('Middle', data)
    return render_template('display.html', level="Middle", data=person_data)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)