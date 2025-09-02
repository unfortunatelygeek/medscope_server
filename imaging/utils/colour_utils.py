import cv2
import numpy as np

def gray_world_white_balance(img):
    result = img.astype(np.float32)

    mean_b, mean_g, mean_r = cv2.mean(result)[:3]
    mean_gray = (mean_b + mean_g + mean_r) / 3

    result[:, :, 0] = np.minimum(result[:, :, 0] * (mean_gray / mean_b), 255)
    result[:, :, 1] = np.minimum(result[:, :, 1] * (mean_gray / mean_g), 255)
    result[:, :, 2] = np.minimum(result[:, :, 2] * (mean_gray / mean_r), 255)

    return result.astype(np.uint8)

def adjust_brightness(img, alpha=1.2, beta=30):
    """
    alpha > 1.0 increases contrast
    beta > 0 increases brightness
    """
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def colour_transforms(img):
    wb_img = gray_world_white_balance(img)
    fixed = adjust_brightness(wb_img, alpha=1.2, beta=40)
    return fixed

# img = cv2.imread("input.jpg")

# wb_img = gray_world_white_balance(img)

# fixed = adjust_brightness(wb_img, alpha=1.2, beta=40)

# cv2.imwrite("fixed_whitebalance_bright.jpg", fixed)
