import cv2
from PIL import Image, ImageTransform
image = cv2.imread('thank.jpeg')
zoom = 1.0
center = [image.shape[1] / 2, image.shape[0] / 2]
window_size = [image.shape[1], image.shape[0]]
prev_mouse_pos = [0, 0]
im = Image.open('thank.jpeg').convert('RGB')
refPt = []
rectangles = []
rect_id = 0
# define a function to draw the rectangles on the image

def draw_rectangles(image, rectangles):
    fixed_rectangles = []
    for rect in rectangles:
        # calculate fixed coordinates based on original image size
        fixed_rect = [(int(p[0] * image.shape[1] / window_size[0]),
                       int(p[1] * image.shape[0] / window_size[1])) for p in rect]
        fixed_rectangles.append(fixed_rect)

    # draw lines between all the points that have been clicked
    for i in range(len(refPt) - 1):
        fixed_line = [(int(refPt[i][0] * image.shape[1] / window_size[0]),
                       int(refPt[i][1] * image.shape[0] / window_size[1])),
                      (int(refPt[i+1][0] * image.shape[1] / window_size[0]),
                       int(refPt[i+1][1] * image.shape[0] / window_size[1]))]
        cv2.line(image, fixed_line[0], fixed_line[1], (0, 255, 0), 1)

    # draw the fixed rectangles on the image
    for rect in fixed_rectangles:
        cv2.line(image, rect[0], rect[1], (0, 255, 0), 1)
        cv2.line(image, rect[1], rect[2], (0, 255, 0), 1)
        cv2.line(image, rect[2], rect[3], (0, 255, 0), 1)
        cv2.line(image, rect[3], rect[0], (0, 255, 0), 1)

    return image

def zoom_at(img, zoom, coord=None):

    # Translate to zoomed coordinates
    h, w, _ = [zoom * i for i in img.shape]

    if coord is None:
        cx, cy = w / 2, h / 2
    else:
        cx, cy = [zoom * c for c in coord]

    img = cv2.resize(img, (0, 0), fx=zoom, fy=zoom)
    img = img[int(round(cy - h / zoom * .5)): int(round(cy + h / zoom * .5)),
          int(round(cx - w / zoom * .5)): int(round(cx + w / zoom * .5)),
          :]
    return img

# define a mouse callback function
def get_coords(event, x, y, flags, param):
    global refPt, rectangles, rect_id, zoom, center, prev_mouse_pos

    if event == cv2.EVENT_LBUTTONUP:
        if flags & cv2.EVENT_FLAG_CTRLKEY:
            refPt.append((int(round(x / zoom + center[0] - window_size[0] / 2 / zoom)),
                           int(round(y / zoom + center[1] - window_size[1] / 2 / zoom))))
            if len(refPt) == 4:
                # add the four points to the rectangles list
                rectangles.append(refPt)
                # draw the four lines for the rectangle
                fixed_rect = [(int(p[0] * image.shape[1] / window_size[0]),
                               int(p[1] * image.shape[0] / window_size[1])) for p in refPt]
                for i in range(3):
                    cv2.line(image, fixed_rect[i], fixed_rect[i+1], (0, 255, 0), 1)
                cv2.line(image, fixed_rect[3], fixed_rect[0], (0, 255, 0), 1)

                # save the coordinates to a text file with an ID for each set of four clicked points
                with open('coordinates.txt', 'a') as f:
                    f.write("{}:{} ,{}, {}, {}, {}, {}, {}, {}\n".format(rect_id, refPt[0][0], refPt[0][1], refPt[1][0],
                                            refPt[1][1],refPt[2][0], refPt[2][1], refPt[3][0], refPt[3][1]))
                    refPt = []
                    rect_id += 1
            else:
                # draw the line for the latest point
                if len(refPt) > 1:
                    fixed_line = [(int(p[0] * image.shape[1] / window_size[0]),
                                   int(p[1] * image.shape[0] / window_size[1])) for p in refPt[-2:]]
                    cv2.line(image, fixed_line[0], fixed_line[1], (0, 255, 0), 1)
            # show the image with the latest changes
            draw_rectangles(image, rectangles)
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(refPt) == 1:
            # if only one point has been clicked, remove it from the list and reset refPt
            refPt = []
        elif len(refPt) == 2:
            # if two points has been clicked, remove the line and point from the list
            refPt.pop()
            refPt.pop()
        elif len(refPt) == 3:
            # if three points has been clicked, remove the latest line and point from the list
            refPt.pop()

        elif rectangles:
            # if no points have been clicked, remove the last rectangle from the list and text file
            rectangles.pop()
            rect_id -= 1
            with open("coordinates.txt", "r") as f:
                lines = f.readlines()
            with open("coordinates.txt", "w") as f:
                for line in lines[:-1]:
                    f.write(line)
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags < 0:
            # zoom out
            zoom /= 1.1
            if zoom < 1.0:
                zoom = 1.0
        else:
            # zoom in
            zoom *= 1.1
        img = zoom_at(image, zoom, center)
        try:
            cv2.imshow('image', img)
        except:
            print("")

    elif event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON:
        # pan
        center[0] += (x - prev_mouse_pos[0]) / zoom
        center[1] += (y - prev_mouse_pos[1]) / zoom
        if center[0] < window_size[0] / 2 / zoom:
            center[0] = window_size[0] / 2 / zoom
        elif center[0] > image.shape[1] - window_size[0] / 2 / zoom:
            center[0] = image.shape[1] - window_size[0] / 2 / zoom
        if center[1] < window_size[1] / 2 / zoom:
            center[1] = window_size[1] / 2 / zoom
        elif center[1] > image.shape[0] - window_size[1] / 2 / zoom:
            center[1] = image.shape[0] - window_size[1] / 2 / zoom
        img = zoom_at(image, zoom, center)
        cv2.imshow('image', img)

    # Add boundary check
    if center[0] < window_size[0] / 2 / zoom:
        center[0] = window_size[0] / 2 / zoom
    elif center[0] > image.shape[1] - window_size[0] / 2 / zoom:
        center[0] = image.shape[1] - window_size[0] / 2 / zoom
    if center[1] < window_size[1] / 2 / zoom:
        center[1] = window_size[1] / 2 / zoom
    elif center[1] > image.shape[0] - window_size[1] / 2 / zoom:
        center[1] = image.shape[0] - window_size[1] / 2 / zoom

    prev_mouse_pos[0] = x
    prev_mouse_pos[1] = y

# create a window and set the mouse callback function
while(True):
    image = cv2.imread('thank.jpeg')
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("image", get_coords)
# display the image and wait for a key press
    draw_rectangles(image, rectangles)
    img = zoom_at(image, zoom, center)
    cv2.imshow('image', cv2.resize(img, (image.shape[1], image.shape[0])))
    key = cv2.waitKey(1) & 0xFF
    # if the 'reset' key is pressed, reset to original state
    if key == ord("e"):
        break
    if key == ord("s"):
        cv2.imwrite("Your_Image.jpeg",image)
# cleanup
cv2.destroyAllWindows()