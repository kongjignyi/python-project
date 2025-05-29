from PIL import Image
import os # 导入 os 模块来处理文件路径

# 分割图片
def cut_image(image, count):
    width, height = image.size
    item_width = width // count
    item_height = height
    box_list = []
    # (left, upper, right, lower)
    for i in range(count):
        box = (i * item_width, 0, (i + 1) * item_width, item_height)
        box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


# 保存分割后的图片
def save_images(image_list, dir_name, file_name_prefix):
    # 确保输出目录存在
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    index = 1
    for image in image_list:
        # PNG 格式保存可以保留透明背景
        image.save(os.path.join(dir_name, f'{file_name_prefix}_{index}.png'), 'PNG')
        index += 1


if __name__ == '__main__':
    # >>> 重点修改这里 <<<
    original_image_path = os.path.join('assets', 'dog_4_walk_sheet.png') # <--- 从 assets 文件夹读取原始图

    output_directory = r'.\out' # 输出文件夹，相对路径，在项目根目录
    output_file_prefix = r'dog_4_walk_sheet' # 输出图片的前缀，例如 dog_4_walk_sheet_1.png

    try:
        image = Image.open(original_image_path)
        # 确认图片尺寸是否符合预期 (8帧, 每帧48宽, 47高 -> 总宽 384, 高 47)
        if image.size != (384, 47):
            print(f"警告：原始图片 {original_image_path} 的尺寸不是预期的 384x47，而是 {image.size}。请检查！")

        image_list = cut_image(image, 8) # 分割成 8 帧
        save_images(image_list, output_directory, output_file_prefix) # 保存分割后的图片
        print(f"图片已成功分割为 8 帧，并保存在 '{output_directory}' 文件夹下，文件名为 '{output_file_prefix}_1.png' 等。")
    except FileNotFoundError:
        print(f"错误：未找到原始图片 '{original_image_path}'。请确保图片文件存在且路径正确。")
    except Exception as e:
        print(f"分割图片时发生错误：{e}")