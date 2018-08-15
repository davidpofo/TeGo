import numpy as np
import seaborn as sns

sns.set()

# Use cubehelix to get a custom sequential palette
pal = sns.cubehelix_palette(p, rot=-.5, dark=.3)

# Show each distribution with both violins and points
sns.violinplot(data=SQL_df, palette=pal, inner="points")