# Imports
import numpy as np

# Factor the length as square-like as possible
# for maximum swirlage
def factosize(msg):
    ln = len(msg)
    # Start at the square
    start = int(np.sqrt(ln))
    # Keep checking
    for i in range((start+2)//1):
        x = start + i
        if ln % x == 0:
            return ln // x, x
    return "Not square enough! :C"

def WannaSwirl(in_bytes, nperm=-1):

    # Ceil function
    def ceil(a, b):
        return -(-a // b)

    # Shape input bytes to a matrix
    while True:
        arrshape = factosize(in_bytes)
        if type(arrshape) != str:
            break
        # Add padding when necessary
        in_bytes += b'\x00'
    bytmat = np.array(list(in_bytes)).reshape(arrshape)
    
    # Some standard amount of swirl
    if nperm < 0:
        nperm = bytmat.size//5
    
    # Move dictionaries
    move_dic = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
    turn_dic = {'N':'E','E':'S','S':'W','W':'N'}
    
    # SWIRL TIME 
    i_mat = np.arange(bytmat.size).reshape(bytmat.shape)
    # Get matrix shape
    h, w = bytmat.shape
    # Initial conditions
    y,x = 0,0    # start at 0,0
    movdir = 'E' # start going East
    vortex = [i_mat[y,x]]
    # Loop time
    i = 1
    while len(vortex) < i_mat.size:
        try:
            # Get new coords
            xnew = x + move_dic[movdir][1]
            ynew = y + move_dic[movdir][0]
            # Check if we hit an edge or a previous path
            if (movdir=='N') and (ynew < i//4): raise
            if (movdir=='E') and (xnew >= w-i//4): raise
            if (movdir=='S') and (ynew >= h-i//4): raise
            if (movdir=='W') and (xnew < i//4): raise
            # Append it to vortex list
            vortex.append(i_mat[ynew,xnew])
        except:
            # Turn clockwise
            movdir = turn_dic[movdir]
            i += 1
            continue
        # Set new coords
        x = xnew
        y = ynew
    # Permutate vortex
    if (nperm != 0) or (nperm != len(vortex)):
        perm = np.append(vortex[-nperm:], vortex[:-nperm])
    else:
        perm = vortex
    # Permutation dictionary
    perm_dic = { vortex[i] : int(perm[i]) for i in range(bytmat.size) }
    # Swirl the data
    swirled = np.zeros(bytmat.size, dtype=int)
    for i in range(bytmat.size):
        swirled[i] = bytmat.flatten()[ perm_dic[i] ]
    # Ta-da!
    return bytes(list(swirled))

def no(msg):
    bytmat = np.array(list(msg)).reshape(factosize(msg))
    
    # Some standard amount of swirl
    nperm = bytmat.size//5
    
    # Move dictionaries
    move_dic = {'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
    turn_dic = {'N':'E','E':'S','S':'W','W':'N'}
    
    # SWIRL TIME 
    i_mat = np.arange(bytmat.size).reshape(bytmat.shape)
    # Get matrix shape
    h, w = bytmat.shape
    # Initial conditions
    y,x = 0,0    # start at 0,0
    movdir = 'E' # start going East
    vortex = [i_mat[y,x]]
    # Loop time
    i = 1
    while len(vortex) < i_mat.size:
        try:
            # Get new coords
            xnew = x + move_dic[movdir][1]
            ynew = y + move_dic[movdir][0]
            # Check if we hit an edge or a previous path
            if (movdir=='N') and (ynew < i//4): raise
            if (movdir=='E') and (xnew >= w-i//4): raise
            if (movdir=='S') and (ynew >= h-i//4): raise
            if (movdir=='W') and (xnew < i//4): raise
            # Append it to vortex list
            vortex.append(i_mat[ynew,xnew])
        except:
            # Turn clockwise
            movdir = turn_dic[movdir]
            i += 1
            continue
        # Set new coords
        x = xnew
        y = ynew
    # Permutate vortex
    if (nperm != 0) or (nperm != len(vortex)):
        perm = np.append(vortex[-nperm:], vortex[:-nperm])
    else:
        perm = vortex
    # Permutation dictionary
    perm_dic = { vortex[i] : int(perm[i]) for i in range(bytmat.size) }
    # Swirl the data
    swirled = np.zeros(bytmat.size, dtype=int)

    for i in range(bytmat.size):
        swirled[perm_dic[i]] = msg[i]

    print(bytes(list(swirled)))
   

trial = b'flag{w0w_1m_g3tt1ng_s0_d1zzy_1_th1nk_1m_g0nn4_puk3}'




#with open("Test.txt") as f:
#	trial = f.read().encode()

print(len(trial))

enc = (WannaSwirl(trial,nperm=-1))

print(enc)
print(len(enc))

no(enc)