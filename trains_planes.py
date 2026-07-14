# Name: Marvel Jefferson Luke
# Student Number: 24722784

'''This function find_root() is used to get the root of a given city that we would like to find and use in the city_union() function later. In here, we also add
   the argument ancestor_dict because we define the function outside the main trains_planes function, so we need to give this ancestor_dict argument so that
   the function knows which dictionary we are using and can execute the code. The ancestor_dict itself is a dictionary that maps the key of a city to its parent/ancestor which is also another city or can
   be that city itself it is not yet been union with a set of cities, which we will see and explained below. The function first check if that given city is in the ancestor dictionary or not,
   meaning that it has already been assigned an ancestor or not, and if not yet, we assign that city as its own ancestor/parent. Next, we check if the ancestor of that given city is itself, if not,
   then we recursively call the find_root() function with the argument of the city as the ancestor of that given city, so we have the recursion going on until we get the root, which is when ancestor is itself.
   After that, we will put that 'root' city into the ancestor dictionary of key given dict, meaning that root is now the parent of the given city. This way is called the path compression (as what I learned and researched so far), where
   we flatten the tree (in this case we can visualize this whole as a tree, so that it can be easier) to make the lookup of root for a given city much faster, rather than each attempt of finding root we traceback again, which will cost much time.
   This function has on average time complexity of O(1), which is very fast compared if not using this way and also optimizing it with the path compression. More detail for each line of code is as below.'''
# The function has argument of given_city as the city we want to lookup the root for, and the ancestor_dict as the dictionary used
def find_root(given_city, ancestor_dict):
    # Checking if the city is i the ancestor dictionary or not, if not then assign that city as its own ancestor
    if given_city not in ancestor_dict:
        ancestor_dict[given_city] = given_city
    # Checking if the city's ancestor is that city itself or not, if not then that means there are still ancestor of the ancestor, so we use recursive function of find_root() using the ancestor as argument, and thus we can find the root of that city
    if ancestor_dict[given_city] != given_city:
        # Here we use the recursive function, but the given city argument, we use the ancestor of that given city so we can finally end up with city that itself is the ancestor of itself
        ancestor_dict[given_city] = find_root(ancestor_dict[given_city], ancestor_dict)
    # Returning the ancestor of that given city, which here it is now the root of that given city
    return ancestor_dict[given_city]

'''This function city_union() is used to union or join the two given city, which in this case are the cities where they are just have a rail line connection between those two given city.
   We will also see later that this function will also join or union sets of cities with sets of cities, but as we have previously make a function to know the root of a given city, we can just
   use that root city to check if the two given city here are in the same set, so if they have same root, that means they are already connected, so no need to join/union them. However, if they have different root,
   that means either one of the city is still not in the set, and not yet been connected, so we will need to union it with the current set of cities already connected, by using this union function. So we will first,
   use the find_root() function to get the root of each city. Then we will check if those two root cities are the same or not, if they are the same we will directly return as we do not need to continue to union them because
   they are already connected. After that, we need to check if both root cities are already in the rank dictionary or not (here the rank_dict is used to map each key of city with rank value starting from 0 then 1, and so forth, 
   where this rank is like how many level of nodes are there below this current node, for example a leaf node will have rank 0 because it does not have any level below it/no children at all), then if 
   they are not yet in dictionary, we can just initialize it with rank 0, and will be incrementing by 1 when that root city have 'children'. Then we can check if one of that root, here I use the left root
   as like a pivot to check if its rank is less than the right root, then we will swap both root cities, so that when we put or union the two city roots, we put the smaller tree under the bigger one (the higher rank of a root city
   means that that root city has much more cities below it, thus bigger tree), in order to make the tree not too long in depth. After that, we can check if the rank of both root cities are the same, that means we can just choose either oe of them, as before I choose the 
   left root as the pivot, so I just increment the rank of left root by 1, which means the left root is now the ancestor of the right root. The amortized/average time complexity of this function is almost constant (O(1)), which is also
   still very fast and thus why we use the Union-Find data structure and algorithm for this problem, as it help to make the lookup and comparison much faster. The detail of each code is as below.'''
# The function as some arguments, which are the left city, right city, ancestor_dict, and rank_dict
def city_union(lcity, rcity, ancestor_dict, rank_dict):
    # Using the find_root() function to get the root of each of the given city, then assign them each to left and right root
    left_root = find_root(lcity, ancestor_dict)
    right_root = find_root(rcity, ancestor_dict)
    # Checking if left root is same as right root, then we know that they are already connected, so just return directly
    if left_root == right_root:
        return
    # Checking if left root is already in rank_dict or not, if not then just assign rank 0 to it, because it means that it is not yet been connected
    if left_root not in rank_dict:
        rank_dict[left_root] = 0
    # Checking if right root is already in rank_dict or not, if not then just assign rank 0 to it, because it means that it is not yet been connected
    if right_root not in rank_dict:
        rank_dict[right_root] = 0
    # Checking if the left root rank is smaller than the right one, if so then we need to swap the both root with each other, as we want to make sure the smaller tree (in this case smaller rank) will be put under the bigger one, where here I use the left root as the 'pivot'
    if rank_dict[left_root] < rank_dict[right_root]:
        left_root, right_root = right_root, left_root
    # Union the two root cities, with left root/bigger tree(rank) as the ancestor/parent of the right/smaller one
    ancestor_dict[right_root] = left_root
    # Checking if the rank is both the same, then we can just choose either one to be the ancestor, but here I just use the left root as the ancestor, so I need to increment its rank by 1, because there is now one added level below it.
    if rank_dict[left_root] == rank_dict[right_root]:
        rank_dict[left_root] = rank_dict[left_root] + 1

'''This function sorting() is used to determine the sorting key that we will use to sort the entries of trains and planes later in the main function trains_planes(). We will use
   the first index of the tuple which is the date as the primary sorting key, then if the same, we will use the secondary key which is they second index, which is the train or plane label (0 or 1), where here
   train is labeled with 0 because for the same date, we want to make sure that the train is processed first, so that the algorithm will return the correct logic, because on that same date the train line is already connected first, so the flight
   can be replaced.'''
# The function has an argument of the dictionary that will contain all the entries of both trains and planes
def sorting(given_dict):
    # Returning the required value for the specified index
    return (given_dict[0], given_dict[1])

'''This function trains_planes() is the main function that we will use to check if a flight can be replaced by the train, where we keep track of which cities are already connected
   by rail lines as the lines open over the time. This function has overall time complexity of O(n log n) as the sorting algorithm that we use here from the sort function by Python
   when I research, it uses Timsort, where it has O(n log n) time complexity, which sorting n items will required n levels of comparison. Some of parts of this function also has time complexity of O(n), such 
   as the for loop. Thus, overall, not only from this function, but the overall implementation of this problem has time complexity of O(n log n), as the sorting algorithm has the largest complexity.
   This function will first initialize empty dictionary for both ancestor_dict and rank_dict, also empty list for all entries of trains and planes combined, and also later initialize empty list to put 
   all the tuple of flights that can be replaced. Then, here I assign the value 0 for the train label that will use for the sorting, and value 1 for the plane label, because we want to make sure that tr=he train entry is processed first, so that on the same date, we can
   replace the flight. After that, we can make for loop to append each given argument or trains and planes and can append them into our created list for the combined entries, where it has the tuple of (date, label, data).
   This will be used for sorting in the order of date first, then secondary if same date, will be the label, where 0 must be processed first. Then, we can just use our sorting()
   function defined earlier as the key to sort the combined entries. Moreover, we create a list to keep all the flights that can be replaced. After that, we make for loop to iterate through each entries,
   and check if it is a train label, then we can use our city_union() function to merge them if needed. However, if it is a plane label, we can just check using our find_root()
   function if that departure and arrival city both have the same root or not, if the same it means that on that date, there is already connection of railway between the two cities, so the that flight can be replaced, and just append the data of that flight
   to the our flights_replaceable list. The detail of the code is as below.'''
def trains_planes(trains, planes):
    """Find what flights can be replaced with a rail journey.

    Initially, there are no rail connections between cities. As rail connections
    become available, we are interested in knowing what flights can be replaced
    by a rail journey, no matter how indirect the route. All rail connections
    are bidirectional.

    Target Complexity: O(N lg N) in the size of the input (trains + planes).

    Args:
        trains: A list of `(date, lcity, rcity)` tuples specifying that a rail
            connection between `lcity` and `rcity` became available on `date`.
        planes: A list of `(code, date, depart, arrive)` tuples specifying that
            there is a flight scheduled from `depart` to `arrive` on `date` with
            flight number `code`.

    Returns:
        A list of flights that could be replaced by a train journey.
    """
    # Initializing list for the combined entries of trains and planes
    combined_trains_planes = []
    # Initializing dictionary for the ancestor/parent of a city
    ancestor_dict = {}
    # Initializing dictionary for the rank/how many level a city has below it
    rank_dict = {}

    # Assigning value 0 for the train label, which will be processed first when sorting encounter same date
    train_label = 0
    # Assigning value 1 for the plane label, which will be processed after train when sorting encounter same date
    plane_label = 1

    # Creating for loop to iterate through each given entries of trains, and then append the (date, label, data) tuple to the combined entries list
    for train_data in trains:
        date, lcity, rcity = train_data
        combined_trains_planes.append((date, train_label, train_data))
    # Creating for loop to iterate through each given entries of planes, and then append the (date, label, data) tuple to the combined entries list
    for plane_data in planes:
        code, date, depart, arrive = plane_data
        combined_trains_planes.append((date, plane_label, plane_data))

    # Sort the combined entries of trains and planes using the sorting key made earlier
    combined_trains_planes.sort(key=sorting)

    # Initializing the list to contain all the flights data that can be replaced
    flights_replaceable = []

    # Creating for loop to iterate through each combined entries
    for date, label, data in combined_trains_planes:
        # When the label is 0 (train label), we union the given cities together if needed
        if label == train_label:
            date, lcity, rcity = data
            city_union(lcity, rcity, ancestor_dict, rank_dict)
        # When the label is 1 (plane label), we find the root of both cities and compare them, if same then it means those cities are already connected, so can be replaced, then append that flight data to the list
        else:
            code, date, depart, arrive = data
            # Using find_root() function to compare the root of the two given cities, if same then can be replaced
            if find_root(depart, ancestor_dict) == find_root(arrive, ancestor_dict):
                # Appending that flight to the list
                flights_replaceable.append(data)

    # Returning the list containing the data of flights that can be replaced by trains
    return flights_replaceable









