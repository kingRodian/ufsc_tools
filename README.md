A collection of scripts which I've written for various tasks related to solving the mysterious ufsc videos.  
More info about them at https://www.unfavorablesemicircle.com/  
  
Maybe they are poorly written or messy, but I've found use for them at least.  
  
  
makecomposite.py [-h] [-i [INPUTDIR]] [-cw [CELLWIDTH]]  
                        [-ch [CELLHEIGHT]]  
                        width [outfile]  
  
positional arguments:  
  width                 Width of composite  
  outfile               Filename of composite image output.  
  
optional arguments:  
-h, --help            show this help message and exit  
  -i [INPUTDIR], --inputdir [INPUTDIR]  
                        The directory from which we get our images.  
  -cw [CELLWIDTH], --cellwidth [CELLWIDTH]  
                        The width to shrink each individual image down to.  
  -ch [CELLHEIGHT], --cellheight [CELLHEIGHT]  
                        The height to shrink each individual image down to.  
  
Requires: PIL  
Given a directory full of png images with filenames consisting of a number and the .png extension,  
will combine them all into a composite image.  
To extract frames from a video the ffmpeg command:  
ffmpeg -i input.mp4 %04d.png to extract images from a video file and give them numbered names.  
Padding the names with zeroes is important to make the names work.  
Width is an obligatory argument. It describes the amount of frames used per row in the resulting composite.  
The height will automatically match, with empty frames at the end if the amount of frames is not a multiple of the width,  
these then being filled with black.  
The size of the frames in the resulting image can be passed to the script as commandline parameters, -cw and -ch,  
the default being 1, 1.  
The name of the resulting composite can be specified with an optional extra argument at the end.  
If not given, the output name will be of the format 'composite_{}x{}.png'  
  
  
  
  
downloader.py [-h] [-g [GPGHOME]] [-c [CONF_PATH]] [-u [USERNAME]]  
                     [-p [PROGRESS_FILE]] [-t [TARGET_DIRECTORY]]  
                     [-l [LOGFILE]]  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -g [GPGHOME], --gpghome [GPGHOME]  
                        Path to gpg home.  
  -c [CONF_PATH], --conf_path [CONF_PATH]  
                        Path to config, logs and tokens used for  
                        authentication.  
  -u [USERNAME], --username [USERNAME]  
                        Twitter username from which we download videos.  
  -p [PROGRESS_FILE], --progress_file [PROGRESS_FILE]  
                        File which keeps track of tweets that have been checked out and the status of an eventual download.  
  -t [TARGET_DIRECTORY], --target_directory [TARGET_DIRECTORY]  
                        Path to target video directory.  
  -l [LOGFILE], --logfile [LOGFILE]  
                        File to which we log.  
Requires: tweepy, gnupg, wget  (gnupg can easily be removed if you don't mind having your secrets unencrypted)  
Paths are hardcoded, so use of this script means you have to modify the default paths in the argparse arguments, or pass them  
as commandline arguments.  
To use this you have to register an app with twitter and get a consumer_key, consumer_secret, access_token and access_secret.  
Each of these has its own file in a conf directory, with the secrets being encrypted with gpg.  
The program asks for the passphrase to decrypt these and gets the tokens for use with the twitter api.  
The program keeps a progress json file in the conf directory which tracks which ids have been looked at,  
the eventual filename for a video and the status of the download, if there was one.  
It uses this to see from which tweet we start. If there is no such file, it will start as far back as possible.  
A daily rotating log file is kept.  
Gpghome is simply the home directory for gnupg, where keys and such are kept.  
  
  
rot.py [-h] n text [text ...]  
Just what you'd think, rotates a given string by n spaces.
