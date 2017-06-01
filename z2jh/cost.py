import numpy as np
from datetime import datetime as py_dtime
from datetime import timedelta
import pandas as pd

from bqplot import LinearScale, Axis, Lines, Figure, DateScale
from bqplot.interacts import HandDraw
from ipywidgets import widgets
from IPython.display import display
import locale
import warnings
warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, '')

# Base costs, all per day
cost_ram = 2.  # Per gig
cost_cpu = 20.  # Per CPU
cost_storage_hdd = 5.  # Per gig
cost_storage_ssd = 10.  # Per gig
storage_cost = {False: 0, 'ssd': cost_storage_ssd, 'hdd': cost_storage_hdd}

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


def integrate_cost(users, cost_per_day):
    cost_per_minute = cost_per_day / (24. * 60. / n_step_min)  # 24 hrs * 60 min / N minutes per step
    cost = np.nansum([ii * cost_per_minute for ii in users])
    return cost


def create_date_range(n_days):
    delta = timedelta(n_days)
    date_stop = date_start + delta
    date_range = pd.date_range(date_start, date_stop, freq='{}min'.format(n_step_min))
    return date_stop, date_range


def cost_display(n_days=7):

    users = widgets.IntText(value=8, description='Number of total users')
    ram = widgets.FloatText(value=1.0, description='RAM (gigs/user)')
    cpu = widgets.FloatText(value=.1, description='CPU (fraction / user)')
    persistent = widgets.Dropdown(description="Persistent Storage?",
                                  options={'None': False, 'HDD': 'hdd',
                                           'SSD': 'ssd'},
                                  value=False)
    autoscaling = widgets.Checkbox(value=False, description='Autoscaling?')
    text_cost_ram = widgets.Text(value='', description='RAM Cost:')
    text_cost_cpu = widgets.Text(value='', description='CPU Cost:')
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
    fig = Figure(marks=[line_fill, line_hd, line_users, line_autoscale],
                 axes=[xax, yax], interaction=handdraw)

    def _update_cost(change):
        # Pull values from the plot
        max_users = max(handdraw.lines.y)
        line_users.y = [max_users] * len(handdraw.lines.y)
        if max_users > users.value:
            users.value = max_users

        autoscaled_users = autoscale(handdraw.lines.y)
        line_autoscale.y = autoscaled_users

        # Calculate costs
        users_for_cost = autoscaled_users if autoscaling.value is True else [max_users] * len(handdraw.lines.y)
        cost_ram = integrate_cost(users_for_cost, ram.value)
        cost_cpu = integrate_cost(autoscaled_users, cpu.value)
        cost_storage = integrate_cost(autoscaled_users, storage_cost[persistent.value])
        cost_total = cost_ram + cost_cpu + cost_storage

        # Set the values
        for iwidget, icost in [(text_cost_ram, cost_ram),
                               (text_cost_cpu, cost_cpu),
                               (text_cost_storage, cost_storage),
                               (text_cost_total, cost_total)]:

            iwidget.value = locale.currency(icost, grouping=True)

        # Set the color
        if autoscaling.value is True:
            line_autoscale.colors = ['#000000']
            line_users.colors = ['#e5e5e5']
        else:
            line_autoscale.colors = ['#e5e5e5']
            line_users.colors = ['#000000']

    line_hd.observe(_update_cost, names='y')
    autoscaling.observe(_update_cost)
    persistent.observe(_update_cost)

    # Show it
    fig.title = 'Draw your usage pattern over time.'
    display(users, ram, cpu, persistent, autoscaling, fig, hr,
            text_cost_ram, text_cost_cpu, text_cost_storage, text_cost_total)
    return fig
