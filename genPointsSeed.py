from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def genSpace(num, size, dist, grid_size, num_grid):
    """
    Generates a space filled with points and their corresponding sizes based on specified parameters.
    Parameters:
    num (tuple): A tuple containing the minimum and maximum number of points to generate per grid.
    size (tuple): A tuple containing the lower and upper bounds for the size of each point.
    dist (tuple): A tuple containing the minimum and maximum distance between points.
    grid_size (float): The size of each grid cell.
    num_grid (int): The number of grid cells along one dimension (total grid cells = num_grid^2).
    Returns:
    tuple: A tuple containing:
        - pos (list of numpy.ndarray): A list of 2D coordinates for each generated point.
        - sizeAr (list of float): A list of sizes corresponding to each generated point.
    """


    pos = []
    min_dist = dist[0]
    max_dist = dist[1]
    size_lb = size[0]
    size_ub = size[1]
    sizeAr = []
    
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
                for i in range(0, num_grid):
                    for j in range(0, num_grid):
                        x = (grid_size/4)*(np.random.randint(0,1)*2-1)*np.random.rand()+i*grid_size + grid_size/2
                        y = (grid_size/4)*(np.random.randint(0,1)*2-1)*np.random.rand()+j*grid_size + grid_size/2
                        point = np.array([x, y])
                        pos.append(point)
                        sizeNew = np.random.randint(size_lb+1, size_ub-1)+(np.random.randint(0,1)*2-1)*np.random.rand()
                        sizeAr.append(sizeNew)
            else:
                x = pos[lastPoint][0] + np.random.rand()+np.random.randint(-max_dist+1, max_dist+1)
                y = pos[lastPoint][1] + np.random.rand()+np.random.randint(-max_dist+1, max_dist+1)
                point = np.array([x, y])
                sizeNew = np.random.randint(size_lb+1, size_ub-1)+(np.random.randint(0,1)*2-1)*np.random.rand()
                if checkDist(point, sizeNew):
                    pos.append(point)
                    sizeAr.append(sizeNew)
                    attempt = 0
                    loop = 0
                    count = 0
                else:
                    attempt += 1
            if len(pos) >= lower_bound:
                count += 1
            if len(pos) >= upper_bound:
                cond = False
            if attempt >= 30:
                lastPoint += 1
                if lastPoint >= len(pos):
                    lastPoint = 0
                    loop += 1
            if count >= 1000:
                cond = False
            

    def checkDist(point, sizeNew):
        dist = cdist([point], pos)
        for i in range(0, len(pos)):
            if np.any(dist[i] < min_dist+sizeNew/2+sizeAr[i]/2):
                return False
            if np.all(point >= 2) and np.all(point <= grid_size*num_grid-2):
                return True
            else:
                return False
    
    genPoints()
    return pos, sizeAr
    

f, s = genSpace([3,10], [3,7], [1.5, 7], 20, 10)
print("Particle Count = ",len(f))
size_aveC = 0.
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)
ax.set_aspect("equal")
for i in range(0,len(f)):
    ax.add_patch(plt.Circle((f[i][0], f[i][1]), s[i]/2, color='k', alpha=.5))
plt.xlim(0, 20*10)
plt.ylim(0, 20*10)
plt.axis('off')
plt.show()
size_av = size_aveC/len(f)
print("Average particle size = ",size_av)


fig, ax = plt.subplots()
t = np.linspace(0, 1, len(f))
ax.set_aspect("equal")
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
