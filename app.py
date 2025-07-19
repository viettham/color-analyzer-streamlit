from matplotlib import ticker
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

def split_image_into_grid(img, rows=5, cols=20):
    width, height = img.size
    cell_width = width // cols
    cell_height = height // rows
    centers = []
    for i in range(rows):
        for j in range(cols):
            center_x = j * cell_width + cell_width // 2
            center_y = i * cell_height + cell_height // 2
            centers.append((center_x, center_y))
    return centers

def get_hex_color(img, point):
    rgb = img.getpixel(point)
    return '#%02x%02x%02x' % rgb

def analyze_colors(color_data):
    s_values = []
    s_values1 = []
    s_values0 = []
    s_values2 = []
    s_values3 = []
    s = 0
    s1=0
    s0,s2,s3=0,0,0
    for i in range(len(color_data)):
        if i<len(color_data) - 4:
            c = color_data[i:i+5]

            # Mẫu s += 1
            if (c[0] == "#000000" and c[1] == "#000000" and c[2] != "#000000" and c[3] == "#000000" and c[4] == "#000000") or \
            (c[0] != "#000000" and c[1] != "#000000" and c[2] == "#000000" and c[3] != "#000000" and c[4] != "#000000"):
                s += 1
                s1=0
            
            # Mẫu s = 0
            elif (c[0] == "#000000" and c[1] == "#000000" and c[2] != "#000000" and c[3] == "#000000" and c[4] != "#000000") or \
                (c[0] != "#000000" and c[1] != "#000000" and c[2] == "#000000" and c[3] != "#000000" and c[4] == "#000000"):
                s = 0
                s1+=1
            
            # Trường hợp khác giữ nguyên s
            s_values.append(s)
            s_values1.append(s1)
        if i<len(color_data) - 3:
            c = color_data[i:i+4]

            # Mẫu s += 1
            if (c[0] == "#000000" and c[1] == "#000000" and c[2] != "#000000" and c[3] == "#000000") or \
            (c[0] != "#000000" and c[1] != "#000000" and c[2] == "#000000" and c[3] != "#000000"):
                s2 += 1
                s3=0
            
            # Mẫu s = 0
            elif (c[0] == "#000000" and c[1] == "#000000" and c[2] != "#000000" and c[3] != "#000000") or \
                (c[0] != "#000000" and c[1] != "#000000" and c[2] == "#000000" and c[3] == "#000000"):
                s2 = 0
                s3+=1
            
            # Trường hợp khác giữ nguyên s
            s_values2.append(s2)
            s_values3.append(s3)
        if color_data[i]=="#000000":
            s0=0
        else:
            s0=1
        s_values0.append(s0)
    return s_values0,s_values1,s_values2,s_values3,s_values

st.title("Phân tích mã màu từ ảnh (5x20 ô)")

uploaded_file = st.file_uploader("Chọn ảnh chụp màn hình", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Ảnh đã chọn", use_column_width=True)

    centers = split_image_into_grid(image)
    
    #hex_colors = [get_hex_color(image, pt) for pt in centers]
    hex_colors=[]
    for col in range(20):
        for row in range(5):
            idx = row * 20 + col  # Do danh sách centers lưu theo dòng → cột
            pt = centers[idx]
            hex_colors.append(get_hex_color(image, pt))
    
    s_values0,s_values1,s_values2,s_values3,s_values = analyze_colors(hex_colors)

    # Hiển thị biểu đồ
    fig, (ax0,ax1, ax2,ax3,ax4) = plt.subplots(5, 1, figsize=(8, 5), sharex=True)

    ax0.plot(s_values0, marker='*', color='black')
    ax0.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax0.set_title("giá trị original")
    #ax0.set_xlabel("Chỉ số i")
    #ax0.set_ylabel("0/1")
    ax0.grid(True)
    #ax0.legend()

    # Đồ thị 1
    ax1.plot(s_values, marker='<', color='blue', linestyle='--')
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax1.set_title("Giá trị tăng khi 00100, 11011->ngược")
    #ax1.set_xlabel("Chỉ số i")
    #ax1.set_ylabel("Giá trị tăng khi 00100, 11011")
    ax1.grid(True)
    #ax1.legend()

    # Đồ thị 2
    ax2.plot(s_values1, marker='.', color='red')
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax2.set_title("Giá trị tăng khi 00101, 11010->trùng")
    ax2.grid(True)
    #ax2.legend()

    ax3.plot(s_values2, marker='>', linestyle='--', color='green')
    ax3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax3.set_title("Giá trị tăng khi 0010, 1101-->trùng")
    ax3.grid(True)
    #ax3.legend()

    ax4.plot(s_values3, marker='s', color='gray')
    ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax4.set_title("Giá trị tăng khi 0011, 1100-->ngược")
    ax4.grid(True)
    #ax4.legend()

    plt.tight_layout()
    plt.show()
    st.pyplot(fig)
