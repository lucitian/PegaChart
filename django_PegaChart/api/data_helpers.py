import json
import datetime, pytz
from dateutil import parser
from pymongo import MongoClient

def get_daily_incidence_with_earnings(pegas, data):
    all_winnings = []

    day_today = datetime.datetime.now().day

    earnings_today = 0

    for pega in pegas:
        pega_id = pega['id']
        renter_percentage = pega['renter_percentage'] / 100

        data = json.loads(data)

        race_history = data['data']

        pega_dict = {
            'pega_id': pega_id,
            'pega_name': pega['name'],
            'races': []
        }

        tz = pytz.timezone('Asia/Manila')

        current_day = parser.parse(race_history[0]['updatedAt']).astimezone(tz).day
        last_dt = None
        gold = silver = bronze = earnings = races = 0

        for race_data in race_history:
            pos = race_data['position'] 
            dt = parser.parse(race_data['updatedAt']).astimezone(tz)
            day = dt.day

            if current_day != day:
                pega_dict['races'].append(
                    {
                        'date': str(datetime.date(last_dt.year, last_dt.month, last_dt.day)),
                        'incidence': {
                            'gold': gold,
                            'silver': silver,
                            'bronze': bronze
                        },
                        'no_of_races': races,
                        'wr_per_day': (gold+silver+bronze)/races,
                        'earnings': earnings
                    }
                )

                earnings = races = 0

                gold = silver = bronze = 0
                current_day = day
            
            if pos == 1:
                gold += 1
            elif pos == 2:
                silver += 1
            elif pos == 3:
                bronze += 1
            
            earnings += race_data['reward'] * renter_percentage

            if current_day == day_today:
                earnings_today += race_data['reward'] * renter_percentage
            
            races += 1

            last_dt = parser.parse(race_data['updatedAt']).astimezone(tz)

        all_winnings.append(pega_dict)
    
    return all_winnings, earnings_today