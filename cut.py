from PIL import Image

def crop_image(input_image, output_image, left, top, right, bottom):
    """
    使用PIL库裁剪图片

    参数:
    input_image (str): 输入图片的文件路径
    output_image (str): 输出图片的文件路径
    left (int): 左边界的像素坐标
    top (int): 上边界的像素坐标
    right (int): 右边界的像素坐标
    bottom (int): 下边界的像素坐标
    """
    image = Image.open(input_image)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(output_image)

if __name__ == '__main__':
    # 示例用法:
    input_image = 'cache.png'  # 输入图片的路径
    output_image = 'cache_croped.png'  # 输出图片的路径
    left = 15# 左边界
    top = 65# 上边界
    right = 60# 右边界
    bottom = 110 # 下边界

    crop_image(input_image, output_image, left, top, right, bottom)
