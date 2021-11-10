import matplotlib.pyplot as plt
import numpy as np

if in_data is not None:
    print(type(in_data))
    #print(in_data.X)

if in_object is not None:
    maxi = in_object[0]
    img = in_object[1]
    g = in_object[2]
    shape = maxi.shape
    x,y = np.meshgrid(np.linspace(0,shape[1]-1,shape[1]),
            np.linspace(0,shape[0]-1,shape[0]))
    
    positions = np.argwhere(maxi==1)
    r = 0
    for pos in positions:
        alpha = np.log(g[pos[0],pos[1]]/img[pos[0],pos[1]])
        print(pos,alpha)
        d = (x-pos[1])**2 + (y-pos[0])**2
        r += img[pos[0],pos[1]]*np.exp(alpha*d)
    
    plt.imshow(r)
    plt.show()