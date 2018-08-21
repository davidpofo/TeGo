#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections
import seaborn as sns
import pandas as pd


def offset_violinplot_halves(ax, delta, width, inner, direction):
    """
    This function offsets the halves of a violinplot to compare tails
    or to plot something else in between them. This is specifically designed
    for violinplots by Seaborn that use the option `split=True`.
    For lines, this works on the assumption that Seaborn plots everything with
     integers as the center.
    Args:
     <ax>    The axis that contains the violinplots.
     <delta> The amount of space to put between the two halves of the violinplot
     <width> The total width of the violinplot, as passed to sns.violinplot()
     <inner> The type of inner in the seaborn
     <direction> Orientation of violinplot. 'hotizontal' or 'vertical'.
    Returns:
     - NA, modifies the <ax> directly
    """
    
    
    
    # offset stuff
    if inner == 'sticks':
        lines = ax.get_lines()
        for line in lines:
            if direction == 'horizontal':
                data = line.get_ydata()
                print(data)
                if int(data[0] + 1)/int(data[1] + 1) < 1:
                    # type is top, move neg, direction backwards for horizontal
                    data -= delta
                else:
                    # type is bottom, move pos, direction backward for hori
                    data += delta
                line.set_ydata(data)
            elif direction == 'vertical':
                data = line.get_xdata()
                print(data)
                if int(data[0] + 1)/int(data[1] + 1) < 1:
                    # type is left, move neg
                    data -= delta
                else:
                    # type is left, move pos
                    data += delta
                line.set_xdata(data)

   
    for ii, item in enumerate(ax.collections):
        # axis contains PolyCollections and PathCollections
        if isinstance(item, matplotlib.collections.PolyCollection):
            # get path
            path, = item.get_paths()
            vertices = path.vertices
            half_type = _wedge_dir(vertices, direction)
            # shift x-coordinates of path
            if half_type in ['top','bottom']:
               if inner in ["sticks", None]:
                    if half_type == 'top': # -> up
                        vertices[:,1] -= delta
                    elif half_type == 'bottom': # -> down
                        vertices[:,1] += delta
            elif half_type in ['left', 'right']:
                if inner in ["sticks", None]:
                    if half_type == 'left': # -> left
                        vertices[:,0] -= delta
                    elif half_type == 'right': # -> down
                        vertices[:,0] += delta
                        
def _wedge_dir(vertices, direction):
    """
    Args:
      <vertices>  The vertices from matplotlib.collections.PolyCollection
      <direction> Direction must be 'horizontal' or 'vertical' according to how
                   your plot is laid out.
    Returns:
      - a string in ['top', 'bottom', 'left', 'right'] that determines where the
         half of the violinplot is relative to the center.
    """
    if direction == 'horizontal':
        result = (direction, len(set(vertices[1:5,1])) == 1)
    elif direction == 'vertical':
        result = (direction, len(set(vertices[-3:-1,0])) == 1)
    outcome_key = {('horizontal', True): 'bottom',
                   ('horizontal', False): 'top',
                   ('vertical', True): 'left',
                   ('vertical', False): 'right'}
    # if the first couple x/y values after the start are the same, it
    #  is the input direction. If not, it is the opposite
    return outcome_key[result]

sns.set()
# initialise new axes;
# if there is random other crap on the axis (e.g. a previous plot),
# the hacky code below won't work
fig, (ax2) = plt.subplots(1)


inner = "sticks" # Note: 'box' is default
width = 0.75
delta = 0.05
final_width = width - delta

SQL_df = pd.read_excel('violin_df.xlsx')
SQL_df2= SQL_df[SQL_df.clicks >= 1]


#transpose COI column data into 'sum of clicks' which will be x
#sns.violinplot(data=SQL_df[SQL_df.clicks <= 100].head(500), x='clicks', y='COI',
#               split=True, hue = 'age_abs', scale='count',
#               ax = ax1, inner='box', 
#               bw = 0.2)
               
               
sns.violinplot(data=SQL_df2[SQL_df2.clicks <= 4], x='COI', y='clicks',
               split=True, hue = 'age_abs', scale='count',
               ax = ax2, inner='box', 
               bw = 0.2)


# Count Plot (a.k.a. Bar Plot)
sns.countplot(x='COI', data=SQL_df2)# Rotate x-labels
plt.xticks(rotation=-45)


#print((SQL_df[SQL_df.clicks <= 5]).describe())

#offset_violinplot_halves(ax1, delta, final_width, inner, 'horizontal')
#offset_violinplot_halves(ax2, delta, final_width, inner, 'vertical')

plt.show()

 










