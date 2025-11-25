# cs476-project

#A substantial amount of this project used code generated from ChatGPT. This is a link to the specific conversation where this code originates from: https://chatgpt.com/share/692592ba-1ea8-8001-8947-adcb04623f0b 

# Problem: 

	In areas with high rates of poverty and homelessness, the lack of sharps containers and high drug use creates a serious concern for needlestick hazards. Used needles can transmit bloodborne diseases such as Human Immunodeficiency Virus, which can cause lifelong complications. Sharps can also cause general injuries and wounds. Less importantly, these syringes create a visually unpleasant environment and are a grim reminder to a variety of economic and social issues that the United States faces today. Having these used materials around presents a serious biohazard to homeless people. With limited access to clean supplies, people suffering from addiction may use unsterile materials out of desperation. Sharps can also present a needlestick hazard to those looking to camp in a park, which is where these used supplies are commonly found.
	Cleaning up used syringes is an amazing deed to the community, but does not come without challenges. People must wear PPE to protect themselves and be careful about where they step to search for any sharps. If one is not careful, they can step on these objects and potentially harm themselves. Since syringes are small, they can be easy to miss and may not be picked up.

# Our solution: 

The emerging platform that we used was a UAV. A UAV aids in the solution of our problem because it allows people to easily find used needles remotely by recognizing needles and placing markers on or around them. Without a UAV, people would need to go to public spaces in-person and manually search for the used needles. Utilizing our solution would make the process of finding used needles significantly easier and faster. The UAVs would use neon-colored flags to highlight identified needles and syringes. With the assistance of a UAV, accidental needlesticks for both people cleaning up sharps and those in the area trying to avoid them will be prevented.

We used Python as our programming language, and PyBullet for our simulator. The emerging platform that we used was GPU-based computer 
vision. For our perception module, we used "Faster R-CNN". We used 
a SLAM-like library for navigation and path planning. 

# installation and execution directions

#run this line in your terminal if you do not already have the dependencies installed:

#pip3 install -r requirements.txt

#we used a virtual environment when testing.

#use cd to navigate to the cs476-project directory

#run "python3 generateDummyModel.py" and "python3 perception/train_detector.py" to create the faster_rcnn_syringe.pth file. This file is too large to upload to GitHub, which is why you have to run these commands. 

#run "cp faster_rcnn_syringe.pth assets/models/faster_rcnn_syringe.pth"

#run "python3 main.py"

#A GUI window should pop up!

#The program execution might be a little slow, but eventually, it will 
place a good amount of markers. Use ctrl+C in the terminal to terminate 
the program.

