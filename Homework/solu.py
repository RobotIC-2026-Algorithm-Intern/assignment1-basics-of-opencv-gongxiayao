import cv2
import numpy as np
import matplotlib.pyplot as plt #绘图模块的标准格式
import os

class ColorRange:
    # 定义颜色范围,无球，紫球，红球，篮球
    def get_dominant_color(self,roi):
        if roi.size == 0:
            return "no roi"
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # 找到像素数量最多的颜色
        color_ranges = {
            'blue': ((92, 0, 137), (125, 120, 255)),
            'purple': ((146,24, 149), (180, 90, 255))
        }
        max_pixels = 0
        dominant_color = "none"
        for color_name, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            
            mask = cv2.inRange(hsv_roi, lower, upper)
            pixel_count = np.sum(mask > 0)
            
            # 如果当前颜色的像素数量最多，更新主导颜色
            if pixel_count > max_pixels and pixel_count > 350:  # 设置阈值避免噪声
                max_pixels = pixel_count
                dominant_color = color_name
        
        return dominant_color
    

class BallDetector:
    def __init__(self):
        self.color_range = ColorRange()
    # 视频读取
    def read_video_opencv(self,video_path):
        """打开视频文件并逐帧读取"""
        cap = cv2.VideoCapture(video_path)  # 创建视频捕获对象
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()  # 逐帧读取视频
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换颜色空间从BGR到RGB
            frames.append(frame_rgb)
            cv2.imshow("output", frame)  # 显示BGR格式的帧
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 25ms 延迟，按 q 退出
                break  # 等待按键
        cap.release()  # 释放视频捕获对象
        cv2.destroyAllWindows()  # 关闭所有OpenCV窗口
        return frames

    

# 提取roi区域
    def roi_extract(self,video_path,x,y,w,h):
        """提取感兴趣区域（ROI）"""
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            roi = frame[y:y+h, x:x+w]
            dominant_color = self.color_range.get_dominant_color(roi)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Color: {dominant_color}", (x, y-10), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("ROI Detection", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


def main():
    detector = BallDetector()
    video_path = "../res/output1.avi"
    roi_x, roi_y, roi_w, roi_h = 220, 200, 190, 55
    detector.roi_extract(video_path, roi_x, roi_y, roi_w, roi_h)



if __name__ == "__main__":
    main()