import moviepy.editor as mpe

# extract
clip = mpe.VideoFileClip('subclip_nbc.mp4')
clip.audio.write_audiofile("c.mp3")

# add audio
newclip = mpe.VideoFileClip('new_subclip_nbc.avi')
newaudio = mpe.AudioFileClip('c.mp3')
final = newclip.set_audio(newaudio)
final.write_videofile("sub_nbc15_add_audio.mp4")