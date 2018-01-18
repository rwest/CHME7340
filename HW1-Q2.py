
# coding: utf-8

# # Homework 1 Question 2
# 
# We have the rate law
# $$r = -k C_{A}^{2}$$
# and the final conversion
# $$X_f = 0.98$$
# which in a batch reactor would take
# $$t_\text{batch} = 12\text{ hours} $$
# but for our flow reactors 
# $$v = 0.8\text{ m$^3$/hour}$$
# First, set the parameters

# In[1]:

t_batch = 12 # hours
Xf = 0.98
v = 0.8 # m^3/hours


# By integrating the batch reactor design equation we can find $(k C_{A0})$:
# 
# $$t_\text{batch} = \int\frac{dC_A}{-k C_A^2}= \int\frac{-C_{A0} dX}{-k C_{A0}^2(1-X)^2}$$
# 
# $$k C_{A0} = \frac{-\left(1-\frac{1}{(1-X_f)}\right) }{t_\text{batch}}$$
# 

# In[2]:

k_Ca0 = -(1.-1./(1-Xf))/t_batch # hours
print("k_Ca0 is {0} hours".format(k_Ca0))


# An underestimate of total volume would be if it were one PFR:

# In[3]:

t_batch * v  # m3


# An overestimate of total volume would be if it were one CSTR:

# In[4]:

(v/k_Ca0) * Xf / (1-Xf)**2 # m3


# This is such a wide range that we had better do something more precise!
# It is better modelled as 6 CSTRs in series, one for each compartment, with volumes $V_c$. For each compartment:
# 
# $$ V_c = \frac{-(F_{Ai} - F_{A(i-1)})}{kC_{Ai}^{2}} $$
# 
# Substitute to be in terms of conversion of A:
# $$ V_c = \frac{-v_{0} C_{A0} (X_{i} - X_{(i-1)})}{ k C_{A0}^2(1-X_{i})^{2} }$$
# 
# Then refactor the equation for $X_{(i-1)}$
# $$X_{(i-1)} = X_{i} - k C_{A0}(V_c/v_{0}) (1-X_{i})^{2} $$
# 
# Let $j = i-1$:
# $$X_{j} = X_{(j+1)} - k C_{A0}(V_c/v_{0}) (1-X_{(j+1)})^{2} $$
# 
# 
# And we know that when $V_c$ is correct $X_6 = 0.98$ and $X_0 = 0$.
# 
# Let's define one function for $X_j = f_1(j, V_c)$ (which calls itself -- a recursive function), and another for $X_0= f_2(V_c)$

# In[5]:

def X(j, V_compartment):
    """
    Returns the conversion leaving the j'th compartment,
    assuming all compartments have volume V_compartment,
    and the sixth compartment has conversion 0.98
    """
    if j == 6:
        return 0.98
    X_exit = X(j+1, V_compartment)
    return X_exit - k_Ca0 * V_compartment/v * (1-X_exit)**2

def zeroth_X(V_compartment):
    """
    Return the conversion entering the first compartment,
    (i.e. leaving the zeroth compartment) assuming all 
    compartments have volume V_compartment,
    and the sixth compartment has conversion 0.98
    """
    return X(0, V_compartment)


# We want to find the $V_c$ so that $X_0= f_2(V_c) = 0$. Or in Python terms the value of `V_compartment` that will give 
# ```python
# zeroth_X(V_compartment) == 0.0
# ```
# Let's guess a few

# In[6]:

zeroth_X(1.)


# In[7]:

zeroth_X(10.)


# In[8]:

zeroth_X(3.)


# Surely we can do better than guess and check? We have Python and all its scientific computing libraries at our fingertips!
# 
# After [some Googling](http://lmgtfy.com/?q=nonlinear+equation+solver+in+Python), we choose to use a nonlinear equation solver from the `optimize` module of the `scipy` library. First import what we need

# In[9]:

import scipy.optimize


# Then check the documentation by executing the function name followed by a question mark. A help window should pop up in a frame below when you press (shift+enter) on the following cell. You can close it when done reading.

# In[10]:

get_ipython().magic(u'pinfo scipy.optimize.fsolve')


# According to the [documentation](http://lmgtfy.com/?q=scipy.optimize.fsolve) we need to pass the `fsolve` function at least two variables: our function that we want to set equal to zero, and an initial guess for its input.

# In[11]:

initial_guess = 2.
root = scipy.optimize.fsolve(zeroth_X, initial_guess)
root


# i.e. $V_c = 2.85 m^3$
# 
# So the total volume of one of the horizontal tank reactors, allowing for internals, is

# In[12]:

V_compartment = root[0] # 'root' was an array, we need the first (and only) element of it
tank_volume = 3 * V_compartment / 0.9 # 3 compartments, 10% occupied by baffles etc.
tank_volume # m3


# If it's a cylinder that is three times as long as the diameter (looks about right in the picture) then we can calculate the diameter
# $$ V_{tank} = \frac{(3D)  \pi  D^2}{4} $$
# $$D = \left(\frac{ 4 V_{tank}}{3 \pi}\right)^{1/3} $$
# 

# In[13]:

import numpy # just to get pi
(4*tank_volume/(3*numpy.pi))**(1/3) # metres


# Ooops! If you're using Python 2, that gave you a diameter of 1.0 m because `(1/3)` in is zero. Try again with a float instead of integer in the exponent!

# In[14]:

(4*tank_volume/(3*numpy.pi))**(1./3) # metres


# A bit over 5 feet. So now you can draw your picture to scale.
# 
# Here is Prof. West next to his reactors. Don’t forget your hard hat and safety goggles!
# ![Prof. West next to his reactors](https://raw.githubusercontent.com/rwest/CHME4510/master/images/HW1ReactorsDrawing.jpg)

# In[ ]:



