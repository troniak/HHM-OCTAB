function plotCompGraphBetweenTwoBinAnnots(inputAMTGroundTruthAnnotFilePath, inputAMTAnnotFilePath, outputDir, FPS)
% Plot a comparison graph between the ground truth binary annotations done
% by an expert and the binary annotations done by a turker, and outputs the
% results to a output directory. The input files are csv files that are
% retrieved from the Amazon Mechanical Turk using OCTAB interface.
%
% Assumptions:
%   Input csv result files are from the Amazon Mechanical Turk using OCTAB
%   interface. There should be only 1 instance of annotations in each file.
%
%   Input CSV result file
%     - Column 16 has the AMT worker IDs.
%     - Column 28 has the video names.
%     - Column 29 has the video lengths.
%     - Column 30 has the behavior name.
%     - Column 31 has the video links.
%     - Column 32 has the annotation end times.
%     - Column 34 has the annotation start times.
%
%
% Inputs:
%    inputAMTGroundTruthAnnotFilePath - Path of the AMT result file by an
%    expert coder (ground truth binary annotations).
%
%    inputAMTAnnotFilePath - Path of the AMT result files by turkers
%    (binary annotations to compare against ground truth).
%
%    outputDir - The folder where the output graph will be placed.
%
%    FPS - Frame/second for the videos.
%
% Outputs:
%
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: 

% Author: Sunghyun Park
% July 2013; Last revision: 7/29/2013

workerIDColumn = 16;
videoLinkColumn = 31;
videoNameColumn = 28;
videoLengthColumn = 29;
behaviorName = 30;
annotEndTimeColumn = 32;
annotStartTimeColumn = 34;


% Import annotations
groundTruthAnnot = importdata(inputAMTGroundTruthAnnotFilePath);
groundTruthAnnot = regexp(groundTruthAnnot, ',', 'split');
groundTruthAnnot(1) = []; % remove column headers

testAnnot = importdata(inputAMTAnnotFilePath);
testAnnot = regexp(testAnnot, ',', 'split');
testAnnot(1) = []; % remove column headers


% Sanity checks (video names, links, and lengths should match)
groundTruthVidName = groundTruthAnnot{1,1}{1,videoNameColumn};
groundTruthVidLink = groundTruthAnnot{1,1}{1,videoLinkColumn};
groundTruthVidLength = groundTruthAnnot{1,1}{1,videoLengthColumn};
groundTruthVidLinkVidName = regexp(groundTruthVidLink, '/', 'split');
groundTruthVidLinkVidName = groundTruthVidLinkVidName{end};
groundTruthBehName = groundTruthAnnot{1,1}{1,behaviorName};

testAnnotVidName = testAnnot{1,1}{1,videoNameColumn};
testAnnotVidLink = testAnnot{1,1}{1,videoLinkColumn};
testAnnotVidLength = testAnnot{1,1}{1,videoLengthColumn};
testAnnotVidLinkVidName = regexp(testAnnotVidLink, '/', 'split');
testAnnotVidLinkVidName = testAnnotVidLinkVidName{end};
testAnnotBehName = testAnnot{1,1}{1,behaviorName};

assert( strcmp(groundTruthVidName, groundTruthVidLinkVidName) == true, 'In plotCompGraphBetweenTwoBinAnnots.m ==> Video name and the link video name do not match.\n');
assert( strcmp(testAnnotVidName, testAnnotVidLinkVidName) == true, 'In plotCompGraphBetweenTwoBinAnnots.m ==> Video name and the link video name do not match.\n');
assert( strcmp(groundTruthVidName, testAnnotVidName) == true, 'In plotCompGraphBetweenTwoBinAnnots.m ==> Video names do not match.\n');
assert( strcmp(groundTruthVidLength, testAnnotVidLength) == true, 'In plotCompGraphBetweenTwoBinAnnots.m ==> Video lengths do not match.\n');
assert( strcmp(groundTruthBehName, testAnnotBehName) == true, 'In plotCompGraphBetweenTwoBinAnnots.m ==> Behavior names do not match.\n');

vidLength = str2double(groundTruthVidLength);
frameCnt = floor(vidLength * FPS);



% Build binary annotations
annotBinary = zeros(frameCnt, 2);
for iSet = 1:2 % 1 for ground truth and 1 for test annotation by turkers
    if( iSet == 1 ) % for ground truth
        startTimesStr = groundTruthAnnot{1,1}{1,annotStartTimeColumn};
        endTimesStr = groundTruthAnnot{1,1}{1,annotEndTimeColumn};
    else
        startTimesStr = testAnnot{1,1}{1,annotStartTimeColumn};
        endTimesStr = testAnnot{1,1}{1,annotEndTimeColumn};
    end
        
    startTimesStr(startTimesStr == '"') = []; % remove quotation marks
    startTimesStr(startTimesStr == '|') = ','; % replace all '|' with ',' because the string won't split
    startTimesStr = regexp(startTimesStr, ',', 'split');
    startTimesStr(1) = []; % remove the first element which is the name of the string
    
    endTimesStr(endTimesStr == '"') = []; % remove quotation marks
    endTimesStr(endTimesStr == '|') = ','; % replace all '|' with ',' because the string won't split
    endTimesStr = regexp(endTimesStr, ',', 'split');
    endTimesStr(1) = []; % remove the first element which is the name of the string
    
    % Sanity check
    assert( length(startTimesStr) == length(endTimesStr), 'In plotCompGraphBetweenTwoBinAnnots.m ==> The number of elements for start times, end times, and behavior names should be the same.\n');
    
    for iAnnot = 1:length(startTimesStr)
        startFrame = round(str2double(startTimesStr(iAnnot)) * FPS);
        if(startFrame == 0 )
            startFrame = 1;
        end
        endFrame = round(str2double(endTimesStr(iAnnot)) * FPS);
        
        annotBinary(startFrame:endFrame, iSet) = 1;
    end
end

groundTruthAnnotBinary = annotBinary(:,1);
testAnnotBinary = annotBinary(:,2);


% plot the graphs (red = ground truth, blue = test annotation)
graphMaxLength = 15; % in seconds
stepSize = graphMaxLength * FPS;
graphCnt = ceil(frameCnt / stepSize);
iter = 1;
while( (iter-1) * stepSize < frameCnt )
    startTime = (iter-1) * graphMaxLength + 1/FPS;
    endTime = iter * graphMaxLength;
    xGroundTruth = linspace(startTime, endTime, stepSize);
    xTestAnnot = linspace(startTime, endTime, stepSize);
    
    startFrame = startTime * FPS;
    endFrame = endTime * FPS;
    if( endFrame < length(groundTruthAnnotBinary) )
        yGroundTruth = groundTruthAnnotBinary(startFrame:endFrame);
        yTestAnnot = testAnnotBinary(startFrame:endFrame);
    else
        yGroundTruth = [groundTruthAnnotBinary(startFrame:end); zeros(endFrame - length(groundTruthAnnotBinary), 1)];
        yTestAnnot = [testAnnotBinary(startFrame:end); zeros(endFrame - length(testAnnotBinary), 1)];
    end
    
    % just plot the annotated portions (labeled 1 instead of 0)
    yGroundTruth(yGroundTruth == 1) = 2.2;
    yTestAnnot(yTestAnnot == 1) = 1.8;
   
    subplot(graphCnt, 1, iter);
    h1 = plot(xTestAnnot, yTestAnnot, 's', 'color', 'b');
    set(h1, 'MarkerFaceColor', 'b');
    hold on;    
    h2 = plot(xGroundTruth, yGroundTruth, 's', 'color', 'r');
    set(h2, 'MarkerFaceColor', 'r');

    axis([floor(startTime) endTime 1 3]);
    set(gca, 'XTick', linspace(floor(startTime), endTime, graphMaxLength+1));
    set(gca, 'YTickLabel', []);
    set(gca, 'YTick', []);
    
    if( iter == 1 )
        title( sprintf('Video: %s,  Behavior: %s,  Worker: %s', testAnnotVidName, groundTruthBehName, testAnnot{1,1}{1,workerIDColumn}) );
    end
    
    if( iter * stepSize > frameCnt )
        legend([h2 h1], 'Answer Key', 'Your Selection');
        xlabel('Time (in seconds)');
    end
        
    iter = iter + 1;
end
    
%saveas(h, [outputDir '_' testAnnotVidName '_' testAnnot{1,1}{1,workerIDColumn} '.tiff']);


