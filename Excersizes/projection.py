from pylab import *

K = array([[5,0,0],[0,5,0],[0,0,1]])
def plotpoints(k):
    th = k*pi/16
    XYZ=array([(5*i,5*j*cos(th),50+5*j*sin(th)) \
        for i in range(-2,3) for j in range(-2,3)]).T
    xys = dot(K,XYZ)
    xy = 1.0*xys[:2,:]/xys[-1,:]
    plot(xy[0], xy[1], 'o')
    axis('equal')

ion()
for k in range(0, 16*20, 1):
    clf()
    plotpoints(k%16)

    pause(0.05)







