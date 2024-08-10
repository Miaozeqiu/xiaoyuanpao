from PIL import Image
import numpy as np

def Dispersion(input_path, output_path,max_difference = 25,min_rgb_value = 70,shape = 'circle'):
    # 打开图像文件
    image = Image.open(input_path)

    # 获取图像的宽度和高度
    width, height = image.size

    # 创建一个新的图像对象，用于存储处理后的结果
    result_image = Image.new('RGB', (width, height), (0, 0, 0))

    # 定义允许的误差范围和最小RGB值
    



    left = -1
    right = -1
    top = -1
    bottom = -1

    def setEdge(x, y):
        nonlocal left, right, top, bottom
        if x < left or left == -1:
            left = x
        elif x > right or right == -1:
            right = x
        if y > top or top == -1:
            top = y
        elif y < bottom or bottom == -1:
            bottom = y




    #二维矩阵
    matrix = [[0 for _ in range(height)] for _ in range(width)]
    matrix_ = []
    # 遍历每个像素
    for x in range(width): #逐列扫描
        for y in range(height):
            # 获取像素的RGB值
            pixel = image.getpixel((x, y))

            # 判断是否是灰度或无色像素的条件
            if (abs(pixel[0] - pixel[1]) <= max_difference and
                abs(pixel[1] - pixel[2]) <= max_difference and
                abs(pixel[2] - pixel[0]) <= max_difference and
                pixel[0] > min_rgb_value and pixel[1] > min_rgb_value and pixel[2] > min_rgb_value):
                # 将像素设为白色
                result_image.putpixel((x, y), (255, 255, 255))
                matrix[x][y] = 1
                setEdge(x,y)
            else:
                # 将像素设为黑色
                result_image.putpixel((x, y), (0, 0, 0))
                
                

    # 保存处理后的图像
    result_image.save(output_path)

    #矩阵分析
    o = ((left+right)/2,(top+bottom)/2)
    print(left,right,top,bottom)

    visited = set()
    def add_to_matrix(i, j):
        if (i, j) not in visited:
            matrix_.append((i, j))
            visited.add((i, j))

    for i in range(width):
        flag = False
        for j in range(height):
            if matrix[i][j] == 1:
                flag = True
                add_to_matrix(i,j)
            elif flag:
                break
        flag = True
        for j in range(height-1,-1,-1):
            if matrix[i][j] == 1:
                flag = True
                add_to_matrix(i,j)
            elif flag:
                break

    for j in range(height):
        flag = False
        for i in range(width):
            if matrix[i][j] == 1:
                flag = True
                add_to_matrix(i,j)
            elif flag:
                break
        flag = False
        for i in range(width-1,-1,-1):
            if matrix[i][j] == 1:
                flag = True
                add_to_matrix(i,j)
            elif flag:
                break

    image = np.zeros((height, width), dtype=np.uint8)
    if not matrix_ :
        return 1
    x_sum = 0
    y_sum = 0
    # 将指定的点设置为白色
    for (x, y) in matrix_:
        if 0 <= x < width and 0 <= y < height:  # 确保点在图像范围内
            image[y, x] = 255
        x_sum += x
        y_sum += y
    
    distence = ( (x_sum - o[0]*len(matrix_)) **2 + (y_sum - o[1]*len(matrix_)) **2 )**0.5
    # 将 NumPy 数组转换为图像
    img = Image.fromarray(image)

    # 保存图像
    img.save('output__.png')
    print(distence)
    
    distances = np.linalg.norm(np.array(matrix_) - o, axis=1)

    # # 计算距离的标准差
    # std_distance = np.std(distances)

    # # 打印结果
    # print(f"Center Point: {o}")
    # print(f"Standard Deviation of Distances: {std_distance}")
    # print()

    # 提取x和y坐标
    x_coords = [point[0] for point in matrix_]
    y_coords = [point[1] for point in matrix_]

    # 计算最小值和最大值
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # 归一化
    try:
        normalized_matrix = [[(x - min_x) / (max_x - min_x), (y - min_y) / (max_y - min_y)] for x, y in matrix_]
    except:
        return False
    normalized_center_point = [(o[0] - min_x) / (max_x - min_x), (o[1] - min_y) / (max_y - min_y)]

    if shape == 'circle':
        # 计算每个点到中心点的距离
        distances = np.linalg.norm(np.array(normalized_matrix) - normalized_center_point, axis=1)

        # 计算距离的标准差
        std_distance = np.std(distances)

        # 打印结果
        # print(f"Normalized Matrix: {normalized_matrix}")
        # print(f"Normalized Center Point: {normalized_center_point}")
        print(f"归一化后的标准差为: {std_distance}")
        if std_distance < 0.9:
            return True
        else:
            return False
    elif shape == 'cross':
        threshold = 0.1  # 设定的误差阈值
        total_vector = np.array(normalized_center_point)
        for x, y in normalized_matrix:
            vector = np.array([x, y]) - normalized_center_point
            total_vector += vector

        # 计算总向量的模长
        magnitude = np.linalg.norm(total_vector)

        # 判断总向量模长是否小于等于设定的误差阈值
        is_within_threshold = magnitude <= threshold
        print("Total Vector:", total_vector)
        print("Magnitude:", magnitude)
        print("Is Within Threshold:", is_within_threshold)
        if magnitude <1.5:
            return True
        else:
            return False



# 调用示例
if __name__ == '__main__':
    input_image_path = 'cache_croped.png'
    output_image_path = 'cache_TwoColor.png'
    Dispersion(input_image_path, output_image_path)