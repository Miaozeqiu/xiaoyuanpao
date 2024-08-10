from PIL import Image
import pytesseract

def ocr_image(image_path):
    # 使用 Pillow 库打开图片
    img = Image.open(image_path)

    # 使用 pytesseract 进行 OCR 文本识别
    text = pytesseract.image_to_string(img,lang='chi_sim')

    return text

# 示例用法：
image_path = 'adShorts\openingAd_left_top.png'  # 你的图片路径

# 执行 OCR 识别
recognized_text = ocr_image(image_path)

# 输出识别的文本
print("识别结果:")
print(recognized_text)
