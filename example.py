from rt_atrt import RT_ATRT
import time

def main():
    start = time.time()
    video = "dataset/chinese/ch1.mp4"
    position = "above"
    language = "chinese"
    translanguage = "thai"
    rt_atrt = RT_ATRT(video, position, language, translanguage)
    end = time.time()
    print('time process video ',end - start)

if __name__ == "__main__":
    main()