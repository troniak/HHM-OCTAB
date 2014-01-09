1) ./park_iui2014_crowdsourcing_v3.pdf
- Take a look at the paper at IUI 2014 for more information about the interface and results showing that one can use crowdsourcing with appropriate training to obtain high-quality micro-behavior annotations in videos.


2) ./nonverbal_annotation_webpage_nolabel_v1.9.html
- You can copy and paste the source code of this html file to directly use it with Amazon Mechanical Turk. For batch operation, all you need to do is replace the text in the file (e.g. input file links) where variable name is needed to create a batch of HITs (http://docs.aws.amazon.com/AWSMechTurk/2011-10-01/RequesterUI/CreatingaHITTemplate.html). MTurk will crawl all the input values for you when the turkers submit the work. 


3) ./instructions
- This folder contains the instructions for using the interface and some sample instructions for several behaviors. Note that the interface currently works with Google Chrome, but with a little bit of more work, you can make it compatible with other web browsers.


4) ./training
- You usually need to train turkers in order to make them perform well. There are 2 training interfaces that you can use for training the turkers. First is a bar-graph visualization that shows the turkers their mistakes against ground-truth annotations ("overallVisualizationAnnotDifference.tif"). For example, this graph can be populated with Matlab with the provided script by using the command (of course with proper modified paths for your computer)...

    plotCompGraphBetweenTwoBinAnnots('...\octab\training\training1_frown_sampleGroundtruth.csv', '...\octab\training\training1_sampleResult1.csv', '...\octab\training\', 30);
	
You can also use "nonverbal_annotation_webpage_nolabel_v1.9_autopopulate_v1.0.html" to let the turkers review their annotations against ground-truth annotations side by side. Take a look at the lines 238~246 in the file.

You can create these 2 training interfaces automatically with a server and some scripts or you can do them manually with a few steps.

