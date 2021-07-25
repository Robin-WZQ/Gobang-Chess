# coding:utf-8
# from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2
import Camera


def capture():
    image_path = "/home/pi/ArmPi/play_the_chess/lab3/test/picture/"

    # image = cv2.imread(image_path+'1.jpg')
    # cv2.imshow('test',image)
    def cut(image_to_cut):
        sp = image_to_cut.shape  # 获取图像形状：返回【行数值，列数值】列表
        sz1 = sp[0]  # 图像的高度（行 范围）
        sz2 = sp[1]
        #sz1=image_to_cut.height
        #sz2=image_to_cut.width
        a = int(sz1 / 2 - 150)  # x start
        b = int(sz1 / 2 + 165)  # x end
        c = int(sz2 / 2 - 150)  # y start
        d = int(sz2 / 2 + 155)  # y end
        resized_image = image_to_cut[a:b,c:d]  # 裁剪图像
        cv2.imshow('resized', resized_image)
        return resized_image

    # 这里的长之差得315，宽之差305，有所畸变，非正方形
    # 不过无伤大雅——后续可直接用w和h作为长宽除法的单位

    def compare_between(first, second):
        # load the two input images
        imageA = cv2.imread(image_path + first)
        imageB = cv2.imread(image_path + second)
        resized_orig = cut(imageA)
        resized_mod = cut(imageB)
        #
        # resized_orig = cv2.resize(imageA, (500, 500))
        # resized_mod = cv2.resize(imageB, (500, 500))

        # 去噪声增加图像质量
        resultA = cv2.GaussianBlur(resized_orig, (5, 5), 1, 1)
        resultB = cv2.GaussianBlur(resized_mod, (5, 5), 1, 1)

        # convert the images to grayscale
        grayA = cv2.cvtColor(resultA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(resultB, cv2.COLOR_BGR2GRAY)
        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = structural_similarity(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        # print("SSIM: {}".format(score))

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ

            (x, y, w, h) = cv2.boundingRect(c)
            if w * h > 500 and w*h<1600:
                cv2.rectangle(resultA, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(resultB, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print(
                    "l_t bound({},{});r_b bound({},{});center:({},{})".format(x, y, (x + w), (y + h),
                                                                              (x + w / 2),
                                                                              (y + h / 2)))
                # print("move:({},{})".format(int((x + w )/63),int((y+h )/61)))
                #print("move:({},{})".format(round((x + w) / w), round((y + h) / h)))
                # break
            # print(y)

        # show the output images
        cv2.imshow("Original", resultA)
        cv2.imshow("Modified", resultB)
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)
        # cv2.waitKey(0)
        return round((x + w) / w), round((y + h) / h)

    # import cv2
    # cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # flag = cap.isOpened()
    index = 1
    # 表示第几张图片
    compared = 0
    # 是否和之前的图片比较过

    my_camera = Camera.Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            # Frame = run(frame)
            cv2.imshow('Frame', frame)
            k = cv2.waitKey(1)
            if k == ord('s'):  # 按下s键，进入下面的保存图片操作
                cv2.imwrite(image_path + str(index) + ".jpg", frame)
                print("save" + str(index) + ".jpg successfuly!")
                print("-------------------------")
                index += 1
                compared = 0
            elif k == ord('q'):  # 按下q键，程序退出
                break
            if (not compared) and index > 2:
                # print(str(index) + '.jpg')
                move = compare_between(str(index - 1) + '.jpg', str(index - 2) + '.jpg')
                compared = 1
    my_camera.camera_close()
    cv2.destroyAllWindows()
    return move

    # while flag:
    #
    #     ret, frame = cap.read()
    #     cv2.imshow("Camera_window", frame)
    #     k = cv2.waitKey(1) & 0xFF
    #     if k == ord('s'):  # 按下s键，进入下面的保存图片操作
    #         cv2.imwrite("D:/rainwork/Gobang/lab1/picture/" + str(index) + ".jpg", frame)
    #         print("save" + str(index) + ".jpg successfuly!")
    #         print("-------------------------")
    #         index += 1
    #         compared = 0
    #     elif k == ord('q'):  # 按下q键，程序退出
    #         break
    #     if (not compared) and index > 2:
    #         # print(str(index) + '.jpg')
    #         move = [compare_between(str(index - 1) + '.jpg', str(index - 2) + '.jpg')]
    #         compared = 1
    #
    # #         调用compare比较两个图片的区别
    # cap.release()  # 释放摄像头
    # cv2.destroyAllWindows()  # 释放并销毁窗口
    


print("move",capture())