from PIL import Image, ImageDraw, ImageFont
import pytesseract
import cv2
import numpy as np
#用途：用来应付需要包含学号和姓名拼音的实验报告
# 配置Tesseract OCR路径
pytesseract.pytesseract.tesseract_cmd = "安装路径"

def recognize_and_replace_text(image_path, output_path, replace_dict, font_path, font_size=24):

    #读取图片并进行OCR识别
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    #使用Tesseract进行文字识别
    text = pytesseract.image_to_string(thresh, lang='chi_sim+eng')
    print("识别到的文字：")
    print(text)
    
    #替换文字
    for old_char, new_char in replace_dict.items():
        text = text.replace(old_char, new_char)
    print("替换后的文字：")
    print(text)
    
    #创建新图片并绘制文字
    #加载字体（修复覆盖问题）
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError as e:
        print(f"字体文件加载失败: {e}，使用默认字体")
        font = ImageFont.load_default()  #仅在加载失败时使用默认字体
    
    lines = text.split('\n')
    
    #计算最大宽度（使用 right - left）
    max_width = max(font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines)
    
    #计算总高度（使用每行的下边界 + 行间距）
    line_heights = [font.getbbox(line)[3] + 5 for line in lines]
    total_height = sum(line_heights)
    
    #创建图片
    new_image = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    
    #绘制文本
    y_offset = 0
    for line, line_height in zip(lines, line_heights):
        draw.text((0, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += line_height  # 高度已包含间距
    
    #保存
    new_image.save(output_path)
    print(f"图片已保存到 {output_path}")

if __name__ == "__main__":
    image_path = "输入"  
    output_path = "输出" 
    replace_dict = {"原文字": "替换文字"}  
    font_path = r'C:\Windows\Fonts\arial.ttf' 
    font_size = 24  
    
    recognize_and_replace_text(image_path, output_path, replace_dict, font_path, font_size)