import cv2
'''
Program for extracting grid boxes from the grid,
and identify the shape, area and color of the object
'''

def check_task(img_task,gray_task,x):
    counter = ''
    img_extract_size = 60
    img_extract_adjust = 0
    check_value = []
    area_value = []
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
                area_value.append(0)
            else:
                for cnt in contours:
                    if counter == str(i1) + str(j1):
                        break
                    approx = cv2.approxPolyDP(cnt, 0.0107 * cv2.arcLength(cnt, True), True)
                    if len(approx) == 3:
                        str_temp += ("Triangle",)
                        #cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
                    elif len(approx) == 4:
                        str_temp += ("4-sided",)
                        #cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
                    elif len(approx) > 10:
                        str_temp += ("Circle",)
                        #cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)
                    cv2.imshow("win" + counter, thresh)
                    counter = str(i1) + str(j1)
                    area_value.append(cv2.contourArea(cnt))

            check_value.append(str_temp)

    return check_value, area_value

img_base_1 = cv2.imread('test_image4.jpg')
gray_base_1 = cv2.imread('test_image4.jpg', 0)

board_values, area_task_values1 = check_task(img_base_1, gray_base_1, 10)
board_values_final = []

for i in range(1, 10):
    indx = (i,)
    board_values_final.append(indx+board_values[i-1])

for block in board_values:                          # just to ignore the blank blocks in the grid
    if block != ('NoShape',):
        print block

#print board_values
print area_task_values1

k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()