import json
import os
from dominate.tags import *
from dominate import document
from PIL import Image,ImageDraw
import math


def draw_star(image, center):
    # 创建五角星的顶点
        draw = ImageDraw.Draw(image)
        # 创建五角星的顶点
        color='red'
        size=10
        points = []
        for i in range(5):
            angle_deg = 72 * i - 90  # 五角星每个顶点相隔72度，起始点向上
            angle_rad = math.radians(angle_deg)
            x = center[0] + size * math.cos(angle_rad)
            y = center[1] + size * math.sin(angle_rad)
            points.append((x, y))

        # 五角星的内顶点
        for i in range(5):
            angle_deg = 72 * i - 90 + 36  # 内顶点偏移36度
            angle_rad = math.radians(angle_deg)
            x = center[0] + size * math.cos(angle_rad) * 0.5  # 内顶点的半径是外顶点的一半
            y = center[1] + size * math.sin(angle_rad) * 0.5
            points.insert(2 * i + 1, (x, y))

        # 绘制实心五角星
        draw.polygon(points, fill=color)
        return image

dst="E:\Omni_3D_img\\3doi\\6_val_sub_sub\ChaHGreen.github.io\cambrian_8b_new"
src_dir = 'F:\\3DOI\images'  
indi='bbox'

################################# Different Mode #############################################
mode=0
tar_file="F:\cambrian\\3doi\8b_crop\8b_cropoption.json"

visualize_images_names=[]
## Name list 1
with open(tar_file, 'r') as tar:
    if mode==1:    ## load names
        visualize_images_names=json.load(tar)
    else:   ## generate name from result file
        items=json.load(tar)
        for item in items:
            name=f"{item['bbox']}_{item['img_name']}"
            visualize_images_names.append(name)
visualize_images_names=visualize_images_names[:400]
print(len(visualize_images_names))
################################################################################################

with open('E:\Omni_3D_img\\3doi\\3doi_annotation\data_test.json', 'r') as f:
    val_sub = json.load(f)

with open('F:\cambrian\\3doi\8b_2\8b_2option.json', 'r') as f:
    batch_output = json.load(f)

# 创建HTML文档
doc = document(title='Image Visualization')

with doc.head:
    style("""
    img {
        max-width: 100%;
        max-height: 300px;
        object-fit: contain;
        border: 1px solid #ccc;
    }
    .image-container {
        width: 50%; /* 两列布局，每列占50% */
        flex: none;
    }
    .info-container {
        width: 50%; /* 两列布局，每列占50% */
        padding-left: 20px;
    }
    .flex-container {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #ccc;
        padding: 10px 0;
    }
    .info-below-image {
        padding-top: 10px;
    }
    """)


with doc:
    for img_name_coord in visualize_images_names:
        coord, img_name = img_name_coord.split('_', 1)
        with div(_class='flex-container'):
            dst_dir = os.path.join(dst, 'images')
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            url = f"images/{img_name_coord}"
            src_img = os.path.join(src_dir, img_name)
            dst_img = os.path.join(dst_dir, img_name_coord)
            image = Image.open(src_img)
            if not os.path.exists(dst_img):
                width, height = image.size
                x_left, y_top, x_right, y_bottom = json.loads(coord)  # str-->float
                x_left = int(x_left * width)
                y_top = int(y_top * height)
                x_right = int(x_right * width)
                y_bottom = int(y_bottom * height)
                draw = ImageDraw.Draw(image)
                draw.rectangle([x_left, y_top, x_right, y_bottom], outline="green", width=4)
                image.save(dst_img)
            with div(_class='image-container'):
                div(img(src=url, alt=img_name_coord))
                with div(_class='info-below-image'):
                    for item in val_sub:
                        if item['img_name'] == img_name:
                            for instance in item['instances']:
                                coord_int=json.loads(coord)
                                if instance[indi] == coord_int:
                                    for k, v in instance.items():
                                        if k in ['movable', 'rigid', 'kinematic', 'pull_or_push']:
                                            if k == 'pull_or_push':
                                                k = 'interaction_type'
                                            p(f'{k}: {v}', br())

            with div(_class='info-container'):
                for item in batch_output:
                    if item['img_name'] == img_name and item[indi] == coord:
                        for k, v in item.items():
                            p(f'{k}: {v}', br())

# 保存HTML文档
with open(os.path.join(dst, 'index.html'), 'w') as f:
    f.write(str(doc))
    print(f"file saved to {dst}")