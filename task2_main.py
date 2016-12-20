# -*- coding: utf-8 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
* ---------------------------------------------------
*  Theme: Launch a Module
*  Filename: task2_main.py
*  Version: 1.0.0  
*  Date: November 28, 2016
*  How to run this file: python task2_main.py
*  Author: e-Yantra Project, Department of Computer Science and Engineering, Indian Institute of Technology Bombay.
* ---------------------------------------------------

* ====================== GENERAL Instruction =======================
* 1. Check for "DO NOT EDIT" tags - make sure you do not change function name of main().
* 2. Return should be a list named occupied_grids and a dictionary named planned_path.
* 3. Do not keep uncessary print statement, imshow() functions in final submission that you submit
* 4. Do not change the file name
* 5. Your Program will be tested through code test suite designed and graded based on number of test cases passed 
**************************************************************************
'''
import cv2
import numpy as np

# ******* WRITE YOUR FUNCTION, VARIABLES etc HERE
'''
    * Team Id : eYRC-LM#2719
    * Author List : Sudarshan Samal, Saswat Sahoo, Pratik Sahoo
    * Filename: Integrated_2.py
    * Theme: Launch a Module
    * Functions:
                * updatePriority(), nextdistance(), estimate(), pathfind(), find_path(), printMap()
                * check_task(), first_out(),do_obstacle(), do_path(), xyz()
    * Global Variables: c, b_object,output_1,output_2,the_map,row, img_base_1, gray_base_1, board_values, key_val
'''
import cv2
from heapq import heappush, heappop  # for priority queue
import math
import time

# variables declaration

c = 1  # counter variable
b_object = []
temp_object = []

output_1 = []  # first required output (list)
output_2 = {}  # second required ouput (dictionary)

directions = 4  # number of possible directions to move on the map
if directions == 4:
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
elif directions == 8:
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

# map matrix
n = 10  # horizontal size
m = 10  # vertical size
the_map = []
row = [0] * n
for i in range(m):
    the_map.append(list(row))


# extract a list of colour, shape and area from the image for all objects and obstacles
def check_task(img_task, gray_task, x):
    counter = ''
    img_extract_size = 60
    img_extract_adjust = 0
    check_value = []
    str_temp = ""
    for column in range(0, x):
        for row in range(0, x):

            i1 = column * img_extract_size + img_extract_adjust
            i2 = (column + 1) * img_extract_size - img_extract_adjust
            j1 = row * img_extract_size + img_extract_adjust
            j2 = (row + 1) * img_extract_size - img_extract_adjust

            img = img_task[i1:i2, j1:j2]
            gray = gray_task[i1:i2, j1:j2]

            color_value = img[30, 30]
            if (color_value[0] < 10 and color_value[1] < 10 and color_value[2] > 240):
                str_temp = ("red",)
            elif (color_value[0] > 240 and color_value[1] < 10 and color_value[2] < 10):
                str_temp = ("blue",)
            elif (color_value[0] < 10 and color_value[1] > 240 and color_value[2] < 10):
                str_temp = ("green",)
            elif (color_value[0] < 10 and color_value[1] > 240 and color_value[2] > 240):
                str_temp = ("yellow",)
            elif (color_value[0] < 10 and color_value[1] < 10 and color_value[2] < 10):
                str_temp = ("black",)

            ret, thresh = cv2.threshold(gray, 160, 255, 1)
            contours, h = cv2.findContours(thresh, 1, 2)

            if len(contours) == 0:
                str_temp = ("NoShape",)
            else:
                for cnt in contours:
                    if counter == str(i1) + str(j1):
                        break
                    approx = cv2.approxPolyDP(cnt, 0.0107 * cv2.arcLength(cnt, True), True)
                    if len(approx) == 3:
                        str_temp += ("Triangle",)
                    elif len(approx) == 4:
                        str_temp += ("4-sided",)
                    elif len(approx) > 10:
                        str_temp += ("Circle",)
                    cv2.imshow("win" + counter, thresh)
                    counter = str(i1) + str(j1)
                    str_temp += (cv2.contourArea(cnt),)

            check_value.append(str_temp)

    return check_value


# node creation
class node:
    # current position
    xPos = 0
    yPos = 0
    # total distance already travelled to reach the node
    distance = 0
    # priority = distance + remaining distance estimate
    priority = 0  # smaller: higher priority

    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority

    def __lt__(self, other):  # for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10  # A*

    # give better priority to going straight instead of diagonally
    def nextdistance(self, i):  # i: direction
        if i % 2 == 0:
            self.distance += 10
        else:
            self.distance += 14

    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return (d)


# A-star algorithm.
# Path returned will be a string of digits of directions.
def pathFind(the_map, directions, dx, dy, xStart, yStart, xFinish, yFinish):
    closed_nodes_map = []  # map of closed (tried-out) nodes
    open_nodes_map = []  # map of open (not-yet-tried) nodes
    dir_map = []  # map of directions
    row = [0] * n
    for i in range(m):  # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []]  # priority queues of open (not-yet-tried) nodes
    pqi = 0  # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xStart, yStart, 0, 0)
    n0.updatePriority(xFinish, yFinish)
    heappush(pq[pqi], n0)
    open_nodes_map[yStart][xStart] = n0.priority  # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0]  # top node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi])  # remove the node from the open list
        open_nodes_map[y][x] = 0
        # mark it on the closed nodes map
        closed_nodes_map[y][x] = 1

        # quit searching when the goal state is reached
        # if n0.estimate(xFinish, yFinish) == 0:
        if x == xFinish and y == yFinish:
            # generate the path from finish to start
            # by following the directions
            path = ''
            while not (x == xStart and y == yStart):
                j = dir_map[y][x]
                c = str((j + directions / 2) % directions)
                path = c + path
                x += dx[j]
                y += dy[j]
            return path

        # generate moves (child nodes) in all possible directions
        for i in range(directions):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n - 1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
                # generate a child node
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextdistance(i)
                m0.updatePriority(xFinish, yFinish)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + directions / 2) % directions
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority info
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction info
                    dir_map[ydy][xdx] = (i + directions / 2) % directions
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi])  # remove the wanted node
                    # empty the larger size pq to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0)  # add the better node instead

    return ''  # no route found


# path finding function
def find_path((xA, yA), temp):
    # (xA, yA, xB, yB) = (0, 0, 0, 0)
    xB = temp[0][0]
    yB = temp[0][1]
    print 'Map Size (X,Y): ', n, m
    print 'Start: ', xA, yA
    print 'Finish: ', xB, yB
    t = time.time()
    route = pathFind(the_map, directions, dx, dy, xA, yA, xB, yB)
    print 'Route : ',
    for i in route:
        if i == '0':  # right
            print 'right ',
        elif i == '1':  # down
            print 'down ',
        elif i == '2':  # left
            print 'left ',
        elif i == '3':  # up
            print 'up ',
    print
    print 'Length =',len(route)
    print
    print
    route1 = xyz(xA, yA, route)

    output_2[(xA, yA)].append(route1)
    output_2[(xA, yA)].append(len(route1))

    # mark the route on the map
    if len(route) > 0:
        x = xA
        y = yA
        the_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            the_map[y][x] = 3
        the_map[y][x] = 4


# display the map with the route
def printMap():
    print 'Map:'
    for y in range(m):
        for x in range(n):
            xy = the_map[y][x]
            if xy == 0:
                print '.',  # space
            elif xy == 1:
                print 'O',  # obstacle
            elif xy == 2:
                print 'S',  # start
            elif xy == 3:
                print 'R',  # route
            elif xy == 4:
                print 'F',  # finish
        print


# extract all the obstacles' and objects' positions
def first_out(board):
    c = 1
    for block in board:
        if block != ('NoShape',):
            x = c % 10
            y = c / 10
            output_1.append((x, y))

            temp_object.append(block)
            block += (c,)
            b_object.append(block)
        c += 1


# present obstacles on map
def do_obstacle(board, tmap):
    c = 1
    for block in board:
        if block == ('black', '4-sided', 3136.0):
            x = c % 10
            y = c / 10
            tmap[y][x] = 1
        c += 1

    return tmap


# takes the b_object as input and
# updates the required dictionary with keys only (starting positions)
def do_path(board):
    for block in board:
        if block[0:2] != ('black', '4-sided',):
            for block2 in board:
                if block != block2 and block[0:3] == block2[0:3]:
                    output_2[(block[3] % 10, block[3] / 10 + 1)] = [(block2[3] % 10, block2[3] / 10 + 1)]
                # else:
                 #   output_2[(block[3] % 10, block[3] / 10 + 1)] = ['NO MATCH']



def xyz(xA, yA, route1):
    path_temp = []
    xA1 = xA
    yA1 = yA
    for i in route1:
        if i == '0':  # right
            xA1 += 1
        elif i == '1':  # down
            yA1 += 1
        elif i == '2':  # left
            xA1 -= 1
        elif i == '3':  # up
            yA1 -= 1
        path_temp.append((xA1, yA1))

    return path_temp



def main(image_filename):
    """
    This function is the main program which takes image of test_images as argument.
    Team is expected to insert their part of code as required to solve the given
    task (function calls etc).

    ***DO NOT EDIT THE FUNCTION NAME. Leave it as main****
    Function name: main()

    ******DO NOT EDIT name of these argument*******
    Input argument: image_filename

    Return:
    1 - List of tuples which is the coordinates for occupied grid. See Task2_Description for detail.
    2 - Dictionary with information of path. See Task2_Description for detail.
    """

    occupied_grids = []		# List to store coordinates of occupied grid -- DO NOT CHANGE VARIABLE NAME
    planned_path = {}		# Dictionary to store information regarding path planning  	-- DO NOT CHANGE VARIABLE NAME




    ##### WRITE YOUR CODE HERE - STARTS

    img_base_1 = cv2.imread(image_filename)
    gray_base_1 = cv2.imread(image_filename, 0)

    board_values = check_task(img_base_1, gray_base_1, 10)

    first_out(board_values)  # list of all objects
    print output_1

    do_path(b_object)

    key_val = list(output_2.keys())

    for i in range(len(key_val)):
    if output_2[key_val[i]] == ['NO MATCH']:
        output_2[key_val[i]].append([])
        output_2[key_val[i]].append(0)
    else:
        find_path(key_val[i], output_2[key_val[i]])




        # cv2.imshow("board_filepath - press Esc to close",cv2.imread(board_filepath))			- For check - remove
        # cv2.imshow("container_filepath - press Esc to close",cv2.imread(container_filepath))


        # #### NO EDIT AFTER THIS

    # DO NOT EDIT
    # return Expected output, which is a list of tuples. See Task1_Description for detail.
    return occupied_grids, planned_path



'''
Below part of program will run when ever this file (task1_main.py) is run directly from terminal/Idle prompt.

'''
if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image3.jpg"

    main(image_filename)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
