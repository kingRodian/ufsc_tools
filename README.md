A collection of scripts which I've written for various tasks related to solving the mysterious ufsc videos.\
More info about them at https://www.unfavorablesemicircle.com/\
\
Maybe they are poorly written or messy, but I've found use for them at least.\
\
The procedure for making a composite is as such\
*   First we download a video using youtube-dl, organize as you wish.\
*   When we explode the video, we want to pad the numbers of the images with 0s to make sure the order is correct.\
    *   `ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 input.mpg`\
    *   This gives us the number of frames, for example 1928, which is 4 digits long.\
*   We create a folder for the keyframes: `mkdir keyframes`, then explode the video: `ffmpeg -i input.mpg ./keyframes/image%04d.png` . Here we use %04d to pad with 4 digits.\
*   We use makecomposite.py to create a composite. It looks specifically for images named 'imageNUMBER.png', but there are options to change the regex it uses to lookup. It takes a width argument and pads the last row with black if needed, so see if the framecount gives any hints.\
    *   `cd keyframes; ./makecomposite.py 128;`\

There are various other scripts for stuff I need to do as well.
