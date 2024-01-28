import requests
import pandas as pd

import requests
import pandas as pd

def fetch_contributions(contributors, min_amount=None, max_amount=None, transaction_period=2024, apply_grouping=False):
    api_key = 'zaguWLntxb5tWY3ekBg5iB9eoxn7nTKTUDfXKrRa'
    base_url = 'https://api.open.fec.gov/v1/'
    endpoint = 'schedules/schedule_a/'
    url = f'{base_url}{endpoint}'

    all_contributions = []

    for contributor_name, contributor_state in contributors:
        page = 1
        while True:
            params = {
                'api_key': api_key,
                'contributor_name': contributor_name,
                'two_year_transaction_period': transaction_period,
                'contributor_state': contributor_state,
                'page': page,
                'per_page': 100  # Adjust as needed
            }

            if min_amount is not None:
                params['min_amount'] = min_amount
            if max_amount is not None:
                params['max_amount'] = max_amount

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                for contribution in data['results']:
                    # Standardizing ZIP Code to 5 digits
                    zip_code = contribution.get('contributor_zip', '')[:5]

                    all_contributions.append({
                        'Name': contribution['contributor_name'],
                        'State': contribution.get('contributor_state', ''),
                        'ZIP Code': zip_code,
                        'Date': contribution['contribution_receipt_date'],
                        'Amount': contribution['contribution_receipt_amount'],
                        'Recipient': contribution['committee']['name']
                    })

                # Check if there are more pages
                if data['pagination']['pages'] > page:
                    page += 1
                else:
                    break
            else:
                print(f"Error: {response.status_code}")
                break

    contributions_df = pd.DataFrame(all_contributions)
    contributions_df['Date'] = pd.to_datetime(contributions_df['Date'])

    if apply_grouping:
        grouped_contributions = contributions_df.groupby(['Name', 'State', 'ZIP Code', 'Recipient']).agg({
            'Amount': 'sum',
            'Date': 'max'
        }).reset_index()

        grouped_contributions = grouped_contributions.rename(columns={
            'Amount': 'Total Donated (Recipient Specific)',
            'Date': 'Most Recent Contribution (to Candidate)'
        })

        return grouped_contributions

    return contributions_df


# contributors = [("Robert BARTHOLOMEW", "CA")]
# print(fetch_contributions(contributors, apply_grouping=True))