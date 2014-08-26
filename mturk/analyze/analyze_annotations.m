load('annotation_matrix.mat')
%frames= annotation_matrix(first_frame:last_frame-1,first_frame:last_frame-1);
frames  = annotation_matrix;
tags    = tag_matrix;
%tags  = tag_matrix(first_frame:last_frame-1,first_frame:last_frame-1);
G=fspecial('gaussian',[9 9],5);
%framesg = imfilter(frames,G,'same');
%framesg = framesg/norm(framesg);
framesg = frames;
framesx = [];
tagsx   = {};
for i = 1:size(framesg,1)
  for j = 1:size(framesg,2)
    if framesg(i,j) > 0
      framesx = [framesx;[i j]];
      tagsx = [tagsx; tags(i,j)];
    end
  end
end
size(framesx,1)
%numclusters = int16(size(framesx,1)*0.05)
[idx,ctrs] = kmeans(framesx,5,'Distance','city','Replicates',5);
framestep = size(framesx,1)/4;

for i = 1:framestep:size(framesx,1)
    plot(framesx(i:i+framestep,1),framesx(i:i+framestep,2),'b.','MarkerSize',10);
    ylabel('annotation end time','FontSize',12);
    xlabel('annotation start time','FontSize',12);
    %%pause
    hold on
    plot(ctrs(i:i+framestep,1),ctrs(i:i+framestep,2),'r.','MarkerSize',35,'LineWidth',2);
    %pause
    hold on
    text(framesx(i:i+framestep,1)+0.5, framesx(i:i+framestep,2)+0.5, tagsx);
    %pause
    for j = i:i+framestep%1:length(framesx)
      hold on;
      plot([framesx(j,1) ctrs(idx(j),1)], [framesx(j,2) ctrs(idx(j),2)],'k');
      %hold on
      %text(ctrs(idx(j),1)+0.5, ctrs(idx(j),2)+0.5, tagsx{j});
      text(framesx(j,1)+0.5, framesx(j,2)+0.5, tagsx{j});
    end
end

