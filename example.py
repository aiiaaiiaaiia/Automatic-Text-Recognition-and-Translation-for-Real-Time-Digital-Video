from rt_atrt_lib import RT_ATRT
import time

def main():
    start = time.time()
    video = "dataset/chinese/ch1.mp4"
    position = "above"
    language = "chinese"
    translanguage = "thai"
    output_path = "output/"
    rt_atrt = RT_ATRT(video, position, language, translanguage, output_path)
    end = time.time()
    print('time process video ',end - start)

if __name__ == "__main__":
    main()