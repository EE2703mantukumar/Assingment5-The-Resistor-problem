#Name:-Mantu kumar 
#Roll no :- EE19B039
# Week 5 assignment on Python: Laplace Equation

import numpy as np
import sys

import scipy.linalg as s
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3


#Taking inputs from users
if(len(sys.argv)==5):
    Nx=int(sys.argv[1])
    Ny=int(sys.argv[2])
    radius=int(sys.argv[3])  
    Niter=int(sys.argv[4])
    print(" user provided parameters")
else:
    #Defining the parameters
    Nx=25 # size along x
    Ny=25 # size along y
    radius=8 #radius of central lead
    Niter=1500 #Number of iterations to perform
    print(" Puting all 4 optional parameters if we want to use our own parameters")

#Initialize Potential
phi=np.zeros((Nx,Ny),dtype = float)
x,y=np.linspace(-0.5,0.5,num=Nx,dtype=float),np.linspace(-0.5,0.5,num=Ny,dtype=float)
Y,X=np.meshgrid(y,x)
phi[np.where(X**2+Y**2<=(0.35)**2)]=1.0

#Ploting potential
plt.xlabel("X")
plt.ylabel("Y")
plt.contourf(X,Y,phi)
plt.colorbar()
plt.show()

#Helper functions for the iterations
def New_phi(phi,phiold):
    phi[1:-1,1:-1]=0.25*(phiold[1:-1,0:-2]+ phiold[1:-1,2:]+ phiold[0:-2,1:-1] + phiold[2:,1:-1])
    return phi

def Boundary(phi,mask = np.where(X**2+Y**2<(0.35)**2)):
    phi[:,0]=phi[:,1] # Left Boundary
    phi[:,Nx-1]=phi[:,Nx-2] # Right Boundary
    phi[0,:]=phi[1,:] # Top Boundary
    phi[Ny-1,:]=0
    phi[mask]=1.0
    return phi

err = np.zeros(Niter)
#the iterations
for k in range(Niter):
    phiold = phi.copy()
    phi = New_phi(phi,phiold)
    phi = Boundary(phi)
    err[k] = np.max(np.abs(phi-phiold))
    if(err[k] == 0):
        print("Reached steady state at ",k," Iterations")
        break

#Plotting Error on semilog
plt.title(" Semilog plot Error")
plt.xlabel("No of iterations")
plt.ylabel("Error")
plt.semilogy(range(Niter),err)
plt.show()
#Plotting Error on loglog
plt.title(" loglog plot Error")
plt.xlabel("No of iterations")
plt.ylabel("Error")
plt.loglog((np.asarray(range(Niter))+1),err)
plt.loglog((np.asarray(range(Niter))+1)[::50],err[::50],'ro')
plt.legend(["real","every 50th value"])
plt.show()

#Helper function for getting best fit
def Get_fit(y,Niter,lastn=0):
    log_err = np.log(err)[-lastn:]
    X = np.vstack([(np.arange(Niter)+1)[-lastn:],np.ones(log_err.shape)]).T
    log_err = np.reshape(log_err,(1,log_err.shape[0])).T
    return s.lstsq(X, log_err)[0]

#Helper function to plot errors
def Plot_error(err,Niter,a,a_,b,b_):
    plt.title(" error-iteration on a loglog scale")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    x = np.asarray(range(Niter))+1
    plt.loglog(x,err)
    plt.loglog(x[::100],np.exp(a+b*np.asarray(range(Niter)))[::100],'ro')
    plt.loglog(x[::100],np.exp(a_+b_*np.asarray(range(Niter)))[::100],'go')
    plt.legend(["errors","fit1","fit2"])
    plt.show()
    #now semilog
    plt.title(" error ver iteration on a semilog scale")
    plt.xlabel("No of iterations")
    plt.ylabel("Error")
    plt.semilogy(x,err)
    plt.semilogy(x[::100],np.exp(a+b*np.asarray(range(Niter)))[::100],'ro')
    plt.semilogy(x[::100],np.exp(a_+b_*np.asarray(range(Niter)))[::100],'go')
    plt.legend(["errors","fit1","fit2"])
    plt.show()

def find_net_error(a,b,Niter):
    return -a/b*np.exp(b*(Niter+0.5))

b,a = Get_fit(err,Niter)
b_,a_ = Get_fit(err,Niter,500)
Plot_error(err,Niter,a,a_,b,b_)
#Plotting cumulative error
iter=np.arange(100,1501,100)
plt.grid(True)
plt.title(r'Plot of Cumulative Error values On a loglog scale')

plt.loglog(iter,np.abs(find_net_error(a_,b_,iter)),'ro')
plt.xlabel("iterations")
plt.ylabel("Net  maximum error")
plt.show()


#plotting 2d contour of final potential
plt.title("2D Contour plot of potential")
plt.xlabel("X")
plt.ylabel("Y")
xp,yp=np.where(X**2+Y**2<(0.35)**2)
plt.plot((xp-Nx/2)/Nx,(yp-Ny/2)/Ny,'ro')
plt.contourf(Y,X[::-1],phi)
plt.colorbar()
plt.show()

#plotting 3d contour of final potential
fig1=plt.figure(4)     # open a new figure
ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
plt.title('The 3-D surface plot of the potential')
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=plt.cm.jet)
plt.show()
#finding Current density
Jx,Jy = (1/2*(phi[1:-1,0:-2]-phi[1:-1,2:]),1/2*(phi[:-2,1:-1]-phi[2:,1:-1]))

#Plotting current density

plt.title("The Vector plot of the current flow")
plt.quiver(Y[1:-1,1:-1],-X[1:-1,1:-1],-Jx[:,::-1],-Jy)
xp,yp=np.where(X**2+Y**2<(0.35)**2)
plt.plot((xp-Nx/2)/Nx,(yp-Ny/2)/Ny,'ro')
plt.show()


#initialize temp
temp=300 * np.ones((Nx,Ny),dtype = float)

#boundary conditions
def Temper(phi,mask = np.where(X**2+Y**2<(0.35)**2)):
    phi[:,0]=phi[:,1] # Left Boundary
    phi[:,Nx-1]=phi[:,Nx-2] # Right Boundary
    phi[0,:]=phi[1,:] # Top Boundary
    phi[Ny-1,:]=300.0
    phi[mask]=300.0
    return phi

#laplaces equation
def Tempdef(temp,oldtemp,Jx,Jy):
    temp[1:-1,1:-1]=0.25*(tempold[1:-1,0:-2]+ tempold[1:-1,2:]+ tempold[0:-2,1:-1] + tempold[2:,1:-1]+(Jx)**2 +(Jy)**2)
    return temp

#the iterations
for k in range(Niter):
    tempold = temp.copy()
    temp = Tempdef(temp,tempold,Jx,Jy)
    temp = Temper(temp)


#plotting 2d contour of final temp
plt.title("2D Contour plot of temperature")
plt.xlabel("X")
plt.ylabel("Y")
plt.contourf(Y,X[::-1],temp)
plt.colorbar()
plt.show()



