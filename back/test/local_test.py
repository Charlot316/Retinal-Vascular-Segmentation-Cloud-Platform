import cv2
import os
import sys


def test():
    image_path = './media/test/' + sys.argv[1]
    img = cv2.imread(image_path)
    cv2.imwrite('./media/test/' + os.path.splitext(sys.argv[1])[0] + '_origin.png', img, )  # 保存为png
    cv2.imwrite('./media/test/' + os.path.splitext(sys.argv[1])[0] + '_promap.png', img, )  # 保存为png
    os.remove(image_path)


if __name__ == '__main__':
    test()
