import cv2
import imutils
import numpy as np
from imutils import contours

# 定义了一个字典 FIRST_NUMBER  ，它将第一个数字映射到相应的信用卡类型。
FIRST_NUMBER = {
    "3": "American Express",
    "4": "Visa",
    "5": "MasterCard",
    "6": "Discover Card"
}
# 参考数字图像，用于匹配
# 灰度化及二值化
ref = cv2.imread("1.png")
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
# 查找轮廓，从左往右排序
refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
                           cv2.CHAIN_APPROX_SIMPLE)
refCnts = imutils.grab_contours(refCnts)
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}
# 对于其中每一个轮廓进行提循环，i为数字名称,c为轮廓，我们将每个数字0-9（字典键）与第30行的每个roi   图像（字典值）相关联 。
for (i, c) in enumerate(refCnts):
    (x, y, w, h) = cv2.boundingRect(c)
    roi = ref[y:y + h, x:x + w]
    roi = cv2.resize(roi, (57, 88))
    digits[i] = roi
# 初始化几个结构化内核，构造了两个这样的内核 - 一个矩形和一个正方形。我们将使用矩形的一个用于Top-hat形态运算符，将方形一个用于关闭操作。
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 加载信用卡图像
image = cv2.imread("3.jpg")
image = imutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 执行Top-hat形态操作，将结果存储为 tophat,Top-hat操作显示了深色背景下的亮区（即信用卡号）
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
# 计算沿x方向的渐变在计算gradX   数组中每个元素的绝对值之后 ，我们采取一些步骤将值缩放到范围[0-255]（因为图像当前是浮点数据类型）。要做到这一点，我们计算 MINVAL
#   和 MAXVAL   的 gradX   （线72），然后由我们的缩放方程上显示  线73（即，最小/最大归一化）。最后一步是将gradX转换   为 uint8   ，其范围为[0-255]
gradx = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradx = np.absolute(gradx)
(minval, maxval) = (np.min(gradx), np.max(gradx))
gradx = (255 * ((gradx - minval) / (maxval - minval)))
gradx = gradx.astype("uint8")
# 执行gradX 图像的Otsu和二进制阈值，然后是另一个关闭操作,对数字分段
gradx = cv2.morphologyEx(gradx, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradx, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
# 找到轮廓并初始化数字分组位置列表
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
locs = []
# 循环遍历轮廓，同时根据每个的宽高比进行过滤，允许我们从信用卡的其他不相关区域修剪数字组位置
for (i, c) in enumerate(cnts):
    # compute the bounding box of the contour, then use the
    # bounding box coordinates to derive the aspect ratio
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    # since credit cards used a fixed size fonts with 4 groups
    # of 4 digits, we can prune potential contours based on the
    # aspect ratio
    if ar > 2.5 and ar < 4.0:
        # contours can further be pruned on minimum/maximum width
        # and height
        if (w > 40 and w < 55) and (h > 10 and h < 20):
            # append the bounding box region of the digits group
            # to our locations list
            locs.append((x, y, w, h))
# 从左到右对分组进行排序，并初始化信用卡数字列表
locs = sorted(locs, key=lambda x: x[0])
output = []
# 遍历四个排序的分组并确定其中的数字,循环的第一个块中，我们在每一侧提取并填充组5个像素（第125行）
# ，应用阈值处理（第126和127行），并查找和排序轮廓（第129-135行）。
for (i, (gX, gY, gW, gH)) in enumerate(locs):
    # initialize the list of group digits
    groupOutput = []

    # extract the group ROI of 4 digits from the grayscale image,
    # then apply thresholding to segment the digits from the
    # background of the credit card
    group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
    group = cv2.threshold(group, 0, 255,
                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # detect the contours of each individual digit in the group,
    # then sort the digit contours from left to right
    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    digitCnts = imutils.grab_contours(digitCnts)
    digitCnts = contours.sort_contours(digitCnts,
                                       method="left-to-right")[0]

    # loop over the digit contours
    for c in digitCnts:
        # compute the bounding box of the individual digit, extract
        # the digit, and resize it to have the same fixed size as
        # the reference OCR-A images
        (x, y, w, h) = cv2.boundingRect(c)
        roi = group[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))

        # initialize a list of template matching scores
        scores = []

        # loop over the reference digit name and digit ROI
        for (digit, digitROI) in digits.items():
            # apply correlation-based template matching, take the
            # score, and update the scores list
            result = cv2.matchTemplate(roi, digitROI,
                                       cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)

        # the classification for the digit ROI will be the reference
        # digit name with the *largest* template matching score
        groupOutput.append(str(np.argmax(scores)))

    # draw the digit classifications around the group
    cv2.rectangle(image, (gX - 5, gY - 5),
                  (gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
    cv2.putText(image, "".join(groupOutput), (gX, gY - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

    # update the output digits list
    output.extend(groupOutput)

print(output)

# display the output credit card information to the screen
print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", image)
cv2.waitKey(0)
