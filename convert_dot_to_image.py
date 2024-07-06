import pydotplus
import sys

if len(sys.argv) != 3:
    print("Usage: python convert_dot_to_image.py input.dot output.png/jpg")
    sys.exit(1)

input_dot = sys.argv[1]
output_image = sys.argv[2]

# อ่านไฟล์ DOT
with open(input_dot, "r") as f:
    dot_graph = f.read()

# ใช้ pydotplus เพื่อแปลง DOT เป็นกราฟ
graph = pydotplus.graph_from_dot_data(dot_graph)

# แปลงกราฟเป็นรูปภาพ
graph.write(output_image)

print(f"Graph has been saved as {output_image}")
