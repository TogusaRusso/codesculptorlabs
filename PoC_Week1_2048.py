"""
Merge function for 2048 game.
"""
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #create empty array equal to line
    outline = [0] * len(line)
    #index in output array
    index = 0
    #flag meaning we can merge
    can_merge = False
    for cell in line:
        if cell > 0:
            if can_merge:
                if cell == outline[index - 1]:
                    #current cel equal to previous
                    #let's merge them together
                    outline[index - 1] += cell
                    #and we can't merge more
                    #for now
                    can_merge = False
                else:
                    #not equal just put it to next cell
                    outline[index] = cell
                    index += 1
            else:
                #we can't merge, so just put
                outline[index] = cell
                index += 1
                #and on next step we can merge
                can_merge = True
    return outline

                
    
