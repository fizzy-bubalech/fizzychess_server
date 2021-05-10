def sort_rating(ls):

    """
    The job of this function if to sort a give list of queued player obejcts and sorts them by their Elo rating.
    
    This functions returns the sorted list. 
    
    """

    if len(ls) > 1:
     #  r is the point where the ls is divided into two sublss
        r = len(ls)//2
        L = ls[:r]
        M = ls[r:]

        # Sort the two halves
        sort_rating(L)
        sort_rating(M)

        i = j = k = 0

        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        while i < len(L) and j < len(M):
            if L[i].rating < M[j].rating:
                ls[k] = L[i]
                i += 1
            else:
                ls[k] = M[j]
                j += 1
            k += 1

        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            ls[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            ls[k] = M[j]
            j += 1
            k += 1
    return ls

def search_list(ls, que_item):
    """
    The job of this function is to search in the given list of queued player for a match to a given, specifc, queued player object.

    This function returns a tuple of the matched player's index and the users id:

        return match_index, que_item[match_index].user_id

    If a match is not found the function returns null: None.  
    """
    ls = sort_rating(ls)
    item_index = 0
    while ls[0] != que_item:
        item_index += 1
    match = False 
    match_index = item_index +1
    for i in range(0,len(ls)):
        if(match_index == len(ls)-1):
            match_index = 0
        if(que_item.time_format == ls[match_index].time_format and que_item != ls[match_index]):
            match = True
            break
        else:
            match_index += 1

    if(match):
        return match_index, que_item[match_index].user_id
    else:
        return None

def in_que(ls, item):
    for i in ls:
        if i.user_id == item.user_id:
            return False
    return True

def get_index(ls, item):
    for i in range(0,len(ls)):
        if(ls[i].user_id == item.user_id):
            return i
    return None
