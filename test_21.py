import cv2
from Integrated import *

from AstarAlgo import *

'''
Program for extracting grid boxes from the grid,
and identify the shape, area and color of the object
'''

def check_task(img_task,gray_task,x):
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
                    str_temp +=(cv2.contourArea(cnt),)

            check_value.append(str_temp)

    return check_value

img_base_1 = cv2.imread('test_image3.jpg')
gray_base_1 = cv2.imread('test_image3.jpg', 0)

board_values = check_task(img_base_1, gray_base_1, 10)


#print b_object

first_out(board_values)

print output_1
print b_object

the_map = do_obstacle(board_values, the_map)

do_path(b_object, the_map)

printMap()

k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()