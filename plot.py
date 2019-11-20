import numpy as np
import matplotlib.pyplot as plt

'''
height=[320,580]
bars=["positive","negative"]

ypos=np.arange(len(bars)) 
# create plot
fig = plt.figure()

ax1=fig.add_subplot(121)
ax2=fig.add_subplot(122)
explode=(0.1,0)

ax1.bar(ypos,height,color=["green","red"],width=0.3,label=bars)
ax1.set_xticks(np.arange(len(bars)))
ax1.set_xticklabels(bars,rotation = 45)

ax2.pie(height,labels=bars,colors=["green","red"],explode=explode,autopct="%1.1f%%",shadow=True,startangle=140)
plt.show()
'''

class MyPlots:
    def plot(height=[1,1]):
        bars=["positive","negative"]
        ypos=np.arange(len(bars)) 

        fig = plt.figure()
        
        ax1=fig.add_subplot(121)
        ax2=fig.add_subplot(122)
        explode=(0.1,0)
        
        ax1.bar(ypos,height,color=["green","red"],width=0.3,label=bars)
        ax1.set_xticks(ypos)
        ax1.set_xticklabels(bars,rotation = 45)
        
        ax2.pie(height,labels=bars,colors=["green","red"],explode=explode,autopct="%1.1f%%",shadow=True,startangle=140)
        plt.show()