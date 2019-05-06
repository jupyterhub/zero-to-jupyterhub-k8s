import numpy as np
from datetime import datetime as py_dtime
from datetime import timedelta
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs4

from bqplot import LinearScale, Axis, Lines, Figure, DateScale
from bqplot.interacts import HandDraw
from ipywidgets import widgets
from IPython.display import display
import locale
import warnings
warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, '')

# --- MACHINE COSTS ---
resp = requests.get('https://cloud.google.com/compute/pricing')
html = bs4(resp.text)

# Munge the cost data
def clean_promo(in_value, use_promo=False):
    # cleans listings with promotional pricing
    # defaults to non-promo pricing with use_promo
    if in_value.find("promo") > -1:
        if use_promo:
            return re.search("\d+\.\d+", in_value)[0]
        else:
            return re.search("\d+\.\d+", in_value[in_value.find("("):])[0]
    else:
        return in_value

all_dfs = []
for table in html.find_all('table'):
    header = table.find('thead').find_all('th')
    header = [item.text for item in header]

    data = table.find('tbody').find_all('tr')
    rows = []
    for ii in data:
        thisrow = []
        for jj in ii.find_all('td'):
            if 'default' in jj.attrs.keys():
                thisrow.append(jj.attrs['default'])
            elif 'ore-hourly' in jj.attrs.keys():
                thisrow.append(clean_promo(jj.attrs['ore-hourly'].strip('$')))
            elif 'ore-monthly' in jj.attrs.keys():
                thisrow.append(clean_promo(jj.attrs['ore-monthly'].strip('$')))
            else:
                thisrow.append(jj.text.strip())
        rows.append(thisrow)
    df = pd.DataFrame(rows[:-1], columns=header)
    all_dfs.append(df)


# Pull out our reference dataframes
disk = [df for df in all_dfs if 'Price (per GB / month)' in df.columns][0]

machines_list = pd.concat([df for df in all_dfs if 'Machine type' in df.columns]).dropna()
machines_list = machines_list.drop('Preemptible price (USD)', axis=1)
machines_list = machines_list.rename(columns={'Price (USD)': 'Price (USD / hr)'})
active_machine = machines_list.iloc[0]

# Base costs, all per day
disk['Price (per GB / month)'] = disk['Price (per GB / month)'].astype(float)
cost_storage_hdd = disk[disk['Type'] == 'Standard provisioned space']['Price (per GB / month)'].values[0]
cost_storage_hdd /= 30.  # To make it per day
cost_storage_ssd = disk[disk['Type'] == 'SSD provisioned space']['Price (per GB / month)'].values[0]
cost_storage_ssd /= 30.  # To make it per day
storage_cost = {False: 0, 'ssd': cost_storage_ssd, 'hdd': cost_storage_hdd}

# --- WIDGET ---
date_start = py_dtime(2017, 1, 1, 0)
n_step_min = 2

def autoscale(y, window_minutes=30, user_buffer=10):
    # Weights for the autoscaling
    weights = np.logspace(0, 2, window_minutes)[::-1]
    weights /= np.sum(weights)

    y = np.hstack([np.zeros(window_minutes), y])
    y_scaled = y.copy()
    for ii in np.arange(window_minutes, len(y_scaled)):
        window = y[ii:ii - window_minutes:-1]
        window_mean = np.average(window, weights=weights)
        y_scaled[ii] = window_mean + user_buffer
    return y_scaled[window_minutes:]


def integrate_cost(machines, cost_per_day):
    cost_per_minute = cost_per_day / (24. * 60. / n_step_min)  # 24 hrs * 60 min / N minutes per step
    cost = np.nansum([ii * cost_per_minute for ii in machines])
    return cost

def calculate_machines_needed(users, mem_per_user, active_machine):
    memory_per_machine = float(active_machine['Memory'].values[0].replace('GB', ''))
    total_gigs_needed = [ii * mem_per_user for ii in users]
    total_machines_needed = [int(np.ceil(ii / memory_per_machine)) for ii in total_gigs_needed]
    return total_machines_needed

def create_date_range(n_days):
    delta = timedelta(n_days)
    date_stop = date_start + delta
    date_range = pd.date_range(date_start, date_stop, freq='{}min'.format(n_step_min))
    return date_stop, date_range


def cost_display(n_days=7):

    users = widgets.IntText(value=8, description='Number of total users')
    storage_per_user = widgets.IntText(value=10, description='Storage per user (GB)')
    mem_per_user = widgets.IntText(value=2, description="RAM per user (GB)")
    machines = widgets.Dropdown(description='Machine',
                                options=machines_list['Machine type'].values.tolist())
    persistent = widgets.Dropdown(description="Persistent Storage?",
                                  options={'HDD': 'hdd', 'SSD': 'ssd'},
                                  value='hdd')
    autoscaling = widgets.Checkbox(value=False, description='Autoscaling?')
    text_avg_num_machine = widgets.Text(value='', description='Average # Machines:')
    text_cost_machine = widgets.Text(value='', description='Machine Cost:')
    text_cost_storage = widgets.Text(value='', description='Storage Cost:')
    text_cost_total = widgets.Text(value='', description='Total Cost:')

    hr = widgets.HTML(value="---")

    # Define axes limits
    y_max = 100.
    date_stop, date_range = create_date_range(n_days)

    # Create axes and extra variables for the viz
    xs_hd = DateScale(min=date_start, max=date_stop, )
    ys_hd = LinearScale(min=0., max=y_max)

    # Shading for weekends
    is_weekend = np.where([ii in [6, 7] for ii in date_range.dayofweek], 1, 0)
    is_weekend = is_weekend * (float(y_max) + 50.)
    is_weekend[is_weekend == 0] = -10
    line_fill = Lines(x=date_range, y=is_weekend,
                      scales={'x': xs_hd, 'y': ys_hd}, colors=['black'],
                      fill_opacities=[.2], fill='bottom')

    # Set up hand draw widget
    line_hd = Lines(x=date_range, y=10 * np.ones(len(date_range)),
                    scales={'x': xs_hd, 'y': ys_hd}, colors=['#E46E2E'])
    line_users = Lines(x=date_range, y=10 * np.ones(len(date_range)),
                       scales={'x': xs_hd, 'y': ys_hd}, colors=['#e5e5e5'])
    line_autoscale = Lines(x=date_range, y=10 * np.ones(len(date_range)),
                           scales={'x': xs_hd, 'y': ys_hd}, colors=['#000000'])
    handdraw = HandDraw(lines=line_hd)
    xax = Axis(scale=xs_hd, label='Day', grid_lines='none',
               tick_format='%b %d')
    yax = Axis(scale=ys_hd, label='Numer of Users',
               orientation='vertical', grid_lines='none')
    # FIXME add `line_autoscale` when autoscale is enabled
    fig = Figure(marks=[line_fill, line_hd, line_users],
                 axes=[xax, yax], interaction=handdraw)

    def _update_cost(change):
        # Pull values from the plot
        max_users = max(handdraw.lines.y)
        max_buffer = max_users * 1.05  # 5% buffer
        line_users.y = [max_buffer] * len(handdraw.lines.y)
        if max_users > users.value:
            users.value = max_users

        autoscaled_users = autoscale(handdraw.lines.y)
        line_autoscale.y = autoscaled_users

        # Calculate costs
        active_machine = machines_list[machines_list['Machine type'] == machines.value]
        machine_cost = active_machine['Price (USD / hr)'].values.astype(float) * 24  # To make it cost per day
        users_for_cost = autoscaled_users if autoscaling.value is True else [max_buffer] * len(handdraw.lines.y)
        num_machines = calculate_machines_needed(users_for_cost, mem_per_user.value, active_machine)
        avg_num_machines = np.mean(num_machines)
        cost_machine = integrate_cost(num_machines, machine_cost)
        cost_storage = integrate_cost(num_machines, storage_cost[persistent.value] * storage_per_user.value)
        cost_total = cost_machine + cost_storage

        # Set the values
        for iwidget, icost in [(text_cost_machine, cost_machine),
                               (text_cost_storage, cost_storage),
                               (text_cost_total, cost_total),
                               (text_avg_num_machine, avg_num_machines)]:
            if iwidget is not text_avg_num_machine:
                icost = locale.currency(icost, grouping=True)
            else:
                icost = '{:.2f}'.format(icost)
            iwidget.value = icost

        # Set the color
        if autoscaling.value is True:
            line_autoscale.colors = ['#000000']
            line_users.colors = ['#e5e5e5']
        else:
            line_autoscale.colors = ['#e5e5e5']
            line_users.colors = ['#000000']

    line_hd.observe(_update_cost, names='y')
    # autoscaling.observe(_update_cost)  # FIXME Uncomment when we implement autoscaling
    persistent.observe(_update_cost)
    machines.observe(_update_cost)
    storage_per_user.observe(_update_cost)
    mem_per_user.observe(_update_cost)

    # Show it
    fig.title = 'Draw your usage pattern over time.'
    # FIXME autoscaling when it's ready
    display(users, machines, mem_per_user, storage_per_user, persistent, fig, hr,
            text_cost_machine, text_avg_num_machine, text_cost_storage, text_cost_total)
    return fig

