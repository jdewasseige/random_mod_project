# -*- coding: utf-8 -*-
"""
Created on Tue May  16 2017

@author: john
"""
import numpy as np
np.set_printoptions(threshold=np.nan) # this line allows to print all elements of matrix

def fillMatrix():
    """
    Fill the two board transition matrices following their get out of jai strategy:
    - M_DOUBLE : wait 3 times and try to make double strategy,
    - M_FINE : pay 50 euro fine and immediately get out of jail.
    """
    # number of squares
    n = 40
    # if double strategy to get out of jail (40 normal states + 3 for the jail part)
    M_double = np.zeros((n+3, n+3))
    # if 50 euro fine strategy to get out of jail (40 normal states)
    M_fine = np.zeros((n, n))
    
    # dice sum probability 2:1/36, 3:2/36, ...
    dice_prob = np.array([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])/36.0
    l = len(dice_prob)
    
    for i in range(40):
        # fill until dice_prob exceeds end of row
        if i < 40 - l - 1:
            M_fine[i,2+i:l+(2+i)] = dice_prob
        # fill the end of row then the beginning with the rest of dice_prob
        elif i < n-2:
            M_fine[i,2+i:n] = dice_prob[0:n-(2+i)]
            M_fine[i,0:l-n+2+i] = dice_prob[n-i-2:l]
        # fill the two last squares with dice_prob starting in columns 0 and 1
        else:
            M_fine[i,i-n+2:l+(i-n+2)] = dice_prob 
        
    print(M_fine)
    return M_fine

if __name__ == "__main__":
    fillMatrix()