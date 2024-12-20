import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                parse_dates=['date'],
                index_col='date')

# Clean data
cond = ( df['value'] <= df['value'].quantile(0.975) ) & \
       ( df['value'] >= df['value'].quantile(0.025) )
df = df.loc[cond]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(10, 4))
    axes.plot(df.index, df['value'], color='red')
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar_plot = df.copy()
    # create numeric months and years columns
    df_bar_plot['month_num'] = df_bar_plot.index.month
    df_bar_plot['year'] = df_bar_plot.index.year
    # group by year and month
    df_bar = df_bar_plot.groupby(by=['year', 'month_num']).mean().sort_values(by=['year','month_num'])

    # Draw bar plot
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
          'September', 'October', 'November', 'December']

    fig, ax = plt.subplots(figsize=(12, 6))
    # unstack numeric months so that the bar plot works
    df_bar.unstack(level='month_num').plot(kind='bar', ax=ax, legend=True)
    ax.legend(title='Months', labels=labels)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plot_objects = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    fig, ((ax1, ax2)) = plot_objects
    sns.boxplot(data=df_box, x='year', y='value', ax=ax1, orientation='vertical')
    sns.boxplot(data=df_box, x='month', y='value', ax=ax2, order=months_order, orientation='vertical')
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
