%load('annotation_matrix.mat')
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
[idx,ctrs] = kmeans(framesx,120,'Distance','city','Replicates',5);

plot(framesx(:,1),framesx(:,2),'b.','MarkerSize',10);
ylabel('annotation end time','FontSize',12);
xlabel('annotation start time','FontSize',12);
%%pause
hold on
plot(ctrs(:,1),ctrs(:,2),'r.','MarkerSize',35,'LineWidth',2);

%pause
hold on
text(framesx(:,1)+0.5, framesx(:,2)+0.5, tagsx);
%pause
for i = 1:length(framesx)
  hold on;
  plot([framesx(i,1) ctrs(idx(i),1)], [framesx(i,2) ctrs(idx(i),2)],'k');
  %hold on
  %text(ctrs(idx(i),1)+0.5, ctrs(idx(i),2)+0.5, tagsx{i});
  text(framesx(i,1)+0.5, framesx(i,2)+0.5, tagsx{i});
end

