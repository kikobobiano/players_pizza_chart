import matplotlib.pyplot as plt
import sys
import requests
import constants

from mplsoccer import PyPizza, add_image, FontManager
from bs4 import BeautifulSoup

#constants
metric_names = []
metric_per90_values = []
metric_percentile_values = []
title = ""
subtitle = ""
atack = 0
possession = 0
defense = 0

notInArray = ["Statistic", "Shooting", "Defense", "Passing", "Goal and Shot Creation", "Possession", "Miscellaneous Stats", "Pass Types"]

# main function
def make(url):
    get_player_data(url)
    make_chart(metric_names, metric_percentile_values, atack, possession, defense, title, subtitle)
    exit()
    

def Convert(string):
    li = list(string.split(" "))
    return li

# scrape fbref to get player stats
def get_player_data(url):
    page =requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    global metric_names
    global metric_per90_values
    global metric_percentile_values
    global title 
    global subtitle    
    global atack
    global possession
    global defense

    #get season
    element = soup.find("div", class_="stats_pullout")
    season = element.find_next("strong").text

    #get Club
    element = soup.find("strong", string="Club:")
    club = element.find_next("a").text   
    
    #get player name
    names = [element.text for element in soup.find_all("span")]
    name = names[7]
    
    #get position
    positions = [element.text for element in soup.find_all("a", class_="sr_preset")
                            if element.find_parent(class_="current") ]
    position = positions[0][4:]

    #get league
    league = soup.find_all("div", class_="section_heading_text")[0].findAll('li')[0].text
    if(league == "Last 365 Days"):
        subtitle = "Percentile vs Big 5 Leagues " + position + " | " + season
    else:
         subtitle = "Percentile vs " + league[10:] + " " + position + " | " + season
    
    title = name + " - " + club
    
    m_names = []
    m_per90_values = []
    m_percentile_values = []
    
    remove_content = ["'", "[", "]", ","]
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('th')[0].contents

        if first_column and first_column[0] not in notInArray:
            m_names.append(first_column[0])
 
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        tds = row.findAll('td')
        if tds:
            first_per90_column = tds[0].contents
            
            if first_per90_column:
                first_percentile_column = row.findAll('td')[1].findAll('div')[0].contents
                
                m_per90_values.append(first_per90_column)
                m_percentile_values.append(first_percentile_column)
    m_per90_values = repr(m_per90_values)
    m_percentile_values = repr(m_percentile_values)
    
    for content in remove_content:
        m_per90_values = m_per90_values.replace(content, '')
        m_percentile_values = m_percentile_values.replace(content, '')
    m_per90_values = Convert(m_per90_values)
    m_percentile_values = Convert(m_percentile_values)
    
    #populate global data
    if(position == 'Midfielders'):
        atack = constants.MIDFIELDERS_ATTACK
        possession = constants.MIDFIELDERS_POSSESSION
        defense = constants.MIDFIELDERS_DEFENSE
        
        for i in constants.MIDFIELDERS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    elif(position == 'Att Mid / Wingers'):
        atack = constants.WINGERS_ATTACK
        possession = constants.WINGERS_POSSESSION
        defense = constants.WINGERS_ATTACK
        
        for i in constants.WINGERS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    elif(position == 'Goalkeepers'):
        atack = constants.MIDFIELDERS_ATTACK
        possession = constants.MIDFIELDERS_POSSESSION
        defense = constants.MIDFIELDERS_DEFENSE
        
        for i in constants.MIDFIELDERS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    elif(position == 'Center Backs'):
        atack = constants.CENTERBACKS_ATTACK
        possession = constants.CENTERBACKS_POSSESSION
        defense = constants.CENTERBACKS_DEFENSE
        
        for i in constants.CENTERBACKS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    elif(position == 'Fullbacks'):
        atack = constants.FULLBACKS_ATTACK
        possession = constants.FULLBACKS_POSSESSION
        defense = constants.FULLBACKS_DEFENSE
        
        for i in constants.FULLBACKS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    elif(position == 'Forwards'):
        atack = constants.FORWARDS_ATTACK
        possession = constants.FORWARDS_POSSESSION
        defense = constants.FORWARDS_DEFENSE
        
        for i in constants.FORWARDS:
            metric_names.append(m_names[i])
            metric_percentile_values.append(int(m_percentile_values[i]))
    else:
        print("Player position error")
        exit()
        
    return
        
# Make pizza chart
# params_name - array with chart names
# params_values - array with percentile values
# attack - number of attack params
# possession - number of possession params
# defense - number of defense params
# title
# subtitle
def make_chart(params_name, params_values, attack, possession, defense, title, subtitle):
    font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                            "Roboto-Regular.ttf?raw=true"))
    font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                            "Roboto-Italic.ttf?raw=true"))
    font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                            "Roboto-Medium.ttf?raw=true"))

    # parameter list
    params = params_name

    # value list
    values = params_values  

    # color for the slices and text
    slice_colors = ["#1A78CF"] * attack + ["#FF9300"] * possession + ["#D70232"] * defense
    text_colors = ["#000000"] * (attack + possession) + ["#F2F2F2"] * defense

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#EBEBE9",     # background color
        straight_line_color="#EBEBE9",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )

    # add title
    fig.text(
        0.515, 0.975, title, size=16,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    # add subtitle
    fig.text(
        0.515, 0.953,
        subtitle,
        size=13,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    # add credits
    CREDIT_1 = "data: statsbomb via fbref"
    CREDIT_2 = "made by: @fbobiano"

    fig.text(
        0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        fontproperties=font_italic.prop, color="#000000",
        ha="right"
    )

    # add text
    fig.text(
        0.34, 0.925, "Attack              Possession        Defense", size=14,
        fontproperties=font_bold.prop, color="#000000"
    )

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])
    
    filename = title.replace(" ", "")
    fig.savefig("charts/" + filename + ".png",pad_inches=10)
    
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])