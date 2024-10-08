from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def genSpace(num, min_dist, max_dist, grid_size, num_grid):
    # Function to generate the speckle pattern

    pos = []
    
    def genPoints():
        testVar = 0
        cond = True
        count = 0
        upper_bound = num[1]*num_grid**2
        lower_bound = num[0]*num_grid**2
        attempt = 0
        lastPoint = 0
        loop = 0
        while cond:

            if len(pos) == 0:
                x = 2.0
                y = 2.0
                point = np.array([x, y])
                pos.append(point)
            else:
                x = pos[lastPoint][0] + np.random.rand()+np.random.randint(-max_dist+1, max_dist+1)
                y = pos[lastPoint][1] + np.random.rand()+np.random.randint(-max_dist+1, max_dist+1)
                point = np.array([x, y])
                if checkDist(point):
                    pos.append(point)
                    attempt = 0
                    loop = 0
                else:
                    attempt += 1
            if len(pos) >= lower_bound:
                count += 1
            if len(pos) >= upper_bound:
                cond = False
            if attempt >= 20:
                lastPoint += 1
                if lastPoint >= len(pos):
                    lastPoint = 0
                    loop += 1
            testVar += 1
            

    def checkDist(point):
        if np.all(cdist([point], pos) >= min_dist):
            if np.all(point >= 2) and np.all(point <= grid_size*num_grid-2):
                return True
            else:
                return False
        else:
            return False
    genPoints()
    return pos
    

f = genSpace([3,5], 6, 11, 20, 10)
print(len(f))

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)
ax.set_aspect("equal")
for i in range(0,len(f)):
    ax.add_patch(plt.Circle((f[i][0], f[i][1]), 2, color='r', alpha=1))
plt.xlim(0, 20*10)
plt.ylim(0, 20*10)
plt.show()



fig, ax = plt.subplots()
t = np.linspace(0, 1, len(f))

scat = ax.scatter(f[0][0], f[0][1], c="b", s=5)
plt.xlim(0, 20*10)
plt.ylim(0, 20*10)

def update(frame):
    # for each frame, update the data stored on each artist.
    x = [point[0] for point in f[:frame]]
    y = [point[1] for point in f[:frame]]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    return (scat,)

ani = animation.FuncAnimation(fig=fig, func=update, frames=len(f)-1, interval=30)
plt.show()
