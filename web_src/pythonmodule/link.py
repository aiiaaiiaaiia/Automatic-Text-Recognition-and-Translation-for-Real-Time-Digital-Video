# import pafy
# import cv2
# import time
# from moviepy.editor import *
# from ffpyplayer.player import MediaPlayer


# video = pafy.new('https://www.youtube.com/watch?v=DKYATp0M9f8')
# # https://www.youtube.com/watch?v=KuncL9Fb_D0
# # best = video.getbest(preftype='mp4')
# streams = video.streams 

# for i in streams: 
#     print(i) 
      
# #---get best resolution regardless of format--- 
# best = video.getbest() 
# print(best.resolution, best.extension)
# #---get best resolution regardless of format---

# # bestaudio = video.getbestaudio() 
# # bestaudio.download() 

# player = MediaPlayer(video.title+'.webm')
# stream = video.getbest(preftype='mp4')
# print('[INFO] Video Title : ' +video.title) 

# video = VideoFileClip(stream.url)
# audio = video.audio
# fps = video.fps
# print('[INFO] FPS : ' + str(fps))
# prev = 0


# # i = True
# # for t, video_frame in video.iter_frames(with_times=True):
# #     # time_elapsed = time.time() - prev
# #     # prev = time.time()
# #     # audio_frame = audio.get_frame(t)
# #     # print(audio_frame)
# #     # print(video_frame)
# #     video_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
# #     while time.time() - prev < 1./fps:
# #         continue
# #     cv2.imshow('video output', video_frame)
# #     prev = time.time()
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break 

# # capture.release()
# cv2.destroyAllWindows()