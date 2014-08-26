load('annotation_matrix.mat')
frames  = annotation_matrix(501:749,501:749);
tags    = tag_matrix(501:749,501:749);

%convert nxn matrix to n*nx2 matrix
framesx = [];
framesd = [];
tagsx   = {};
for i = 1:size(frames,1)
  for j = 1:size(frames,2)
    if frames(i,j) > 0
      %manual outlier removal
      if((i ~= 139 || j ~= 249) && (i ~= 28 || j ~= 87) && (i ~= 33 || j ~= 96) && (i ~= 69 || j ~= 125) && (i ~= 166 || j ~= 225)) 
          framesx = [framesx;[i j-i]];
          framesd = [framesd;[i j]];
          tag = tags{i,j};
          tagsx = [tagsx; tag(2:end)];
      end
    end
  end
end
size(framesx,1)
numclusters = int16(size(framesx,1)/10);
[idx,ctrs] = kmeans(framesx,numclusters,'Distance','city','Replicates',50);
%[idxd,ctrsd] = kmeans(framesd,numclusters,'Distance','city','Replicates',20);
framestep = size(framesx,1)/4;

clf;
plot(framesx(:,1),framesx(:,2),'b.','MarkerSize',2);
ylabel('Annotation duration (frames)','FontSize',16);
xlabel('Annotation start frame','FontSize',16);
title('Annotation Clusters with Heirarchies','FontSize',18);
%%pause
hold on
h = plot(ctrs(:,1),ctrs(:,2),'r.','MarkerSize',35,'LineWidth',2);
%pause
hold on
for j = 1:length(framesx)
  hold on;
  plot([framesx(j,1) ctrs(idx(j),1)], [framesx(j,2) ctrs(idx(j),2)],'Color',[0.6 0.6 0.6],'LineWidth',0.5);
  %hold on
  %text(ctrs(idx(j),1)+0.5, ctrs(idx(j),2)+0.5, tagsx{j});
  %text(framesx(j,1)+0.5, framesx(j,2)+0.5, tagsx{j});
end
% text(framesx(:,1)+0.5, framesx(:,2)+0.5, tagsx);
% rotate(h,[0 0 1],-45);
% figure;
% plot(ctrsd(:,1),ctrsd(:,2),'b.','MarkerSize',35,'LineWidth',2);
% for j = 1:numclusters
%     text(ctrsd(j,1)+0.5, ctrsd(j,2)+0.5, num2str(j));
% end
% ylabel('annotation duration','FontSize',24);
% xlabel('annotation start time','FontSize',24);

cluster_starts = zeros(numclusters,1);
cluster_ends   = zeros(numclusters,1);
cluster_tags   = cell(numclusters,1);
for i = 1:numclusters
    for j = 1:length(tagsx)
        if(idx(j) == i)
            cluster_starts(i) = ctrs(idx(j),1);
            cluster_ends(i)   = ctrs(idx(j),2);
            if(isempty(cluster_tags{i}))
                cluster_tags{i}   = [tagsx{j}];
            else
                cluster_tags{i}   = [cluster_tags{i} '|' tagsx{j}];
            end
        end
    end
end

%tag clouds
non_interesting_words = {'the' '' 'she' 'her' 'right' 'left' 'to' 'of' 'from' 'with' 'is' 'that'};
[sorted,indices] = sort(cluster_starts);
for j = 1:numclusters
    text(ctrs(indices(j),1)+2, ctrs(indices(j),2)+0.5, num2str(j),'FontSize',16);
end
fileID = fopen(['clusters' num2str(numclusters)],'w+');
count = 1;
for i = 1:length(indices)
    fprintf(fileID,['\n\ncluster' num2str(i) ...
        '(start frame: ' num2str(cluster_starts(indices(i))) ...
        ', end frame: ' num2str(cluster_ends(indices(i))) '):' '\n']);
    %fprintf(fileID,cluster_tags{indices(i)});
    tags_str = cluster_tags{indices(i)};
    cleaned_up = regexprep(tags_str, '[\s|;]', ' ');
    cleaned_up = regexprep(cleaned_up, 'cutting board', 'cuttingboard');
    cleaned_up = regexprep(cleaned_up, 'reach for', 'reachfor');
    cleaned_up = regexprep(cleaned_up, 'reaching for', 'reachingfor');
    cleaned_up = regexprep(cleaned_up, '[^a-zA-Z0-9 ]', '');
    words = regexpi(cleaned_up, '\s+', 'split');
    words = lower(words);
    for j = 1:length(non_interesting_words)
        [rn,cn] = find(strcmp(words,non_interesting_words{j}));
        words(cn) = [];
    end
    [unique_words, ii, jj] = unique(words);
    frequency_count = hist(jj, 1:max(jj));
    [~, sorted_locations] = sort(frequency_count);
    sorted_locations = fliplr(sorted_locations);
    words_sorted_by_frequency = unique_words(sorted_locations);
    frequencies = frequency_count(sorted_locations).';
    [~,frequency_bins] = histc(frequencies,[1 2 3 4 5 7 9 12 15]);
%     [words_sorted_by_frequency frequencies]
    textc = 20;
    for j = 1:length(words_sorted_by_frequency)
        angle = j / length(words_sorted_by_frequency) * 2 * pi;
        word = words_sorted_by_frequency{j};
        cx = cluster_starts(indices(i));
        cy = cluster_ends(indices(i));
        fprintf(fileID,'%s (%d)\n',word,frequencies(j));
        %text(cx+textc*cos(angle)/10, cy+textc*sin(angle)/20, word,'FontSize',(frequency_bins(j)+1)*5); %word cloud
        textc = textc*-1;
        if(textc < 0)
            textc = textc-1;
        else
            textc = textc+1;
        end
    end
    %plot_word_cloud(words_sorted_by_frequency,frequencies,[cluster_starts(indices(i)) cluster_ends(indices(i))])
%     tags_arr = regexp(cluster_tags{i},'\|','split');
%     for j = 1:length(tags)
%         fprintf(fileID,['\t' tags_arr{j}]);
%     end
    count = count+1;
end

%cluster heirarchy
nearest_parents = zeros(numclusters,1); %assume root is nearest parent
for childID = 1:numclusters
    child_start = cluster_starts(childID);
    child_end   = cluster_ends(childID);
    for parentID = 1:numclusters
        parent_start = cluster_starts(parentID);
        parent_end   = cluster_ends(parentID);
        if(child_start > parent_start && (child_start+child_end) < (parent_start+parent_end))
            if(nearest_parents(childID) == 0)
                nearest_parents(childID) = parentID;
            else
                prev_parentID = nearest_parents(childID);
                prev_parent_start = cluster_starts(prev_parentID);
                prev_parent_end   = cluster_ends(prev_parentID);
                prev_distance = child_start - prev_parent_start + prev_parent_end - child_end;
                curr_distance = child_start - parent_start + parent_end - child_end;
                if(curr_distance < prev_distance)
                    nearest_parents(childID) = parentID;
                end
            end            
%             dist2 = ctrs(j,2) - ctrs(i,2);
%             fprintf(['i: ' num2str(i) '; j: ' num2str(j)])
%             fprintf(['; i1: ' num2str(ctrs(i,1))])
%             fprintf(['; i2: ' num2str(ctrs(i,2))])
%             fprintf(['; j1: ' num2str(ctrs(j,1))])
%             fprintf(['; j2: ' num2str(ctrs(j,2))])
%             fprintf(['; ' num2str(i) '>' num2str(j) '\n'])
%             t = t.addnode(i,j);
        end
    end
end
t = tree;
nearest_parent_nodeIDs = zeros(size(nearest_parents));
for i = 1:length(nearest_parents)
    if(nearest_parents(i)+1 == 1) %adding to root
%         [t, nodeID] = t.addnode(nearest_parents(i)+1,strrep(cluster_tags{i},'|','|'));
        [t, nodeID] = t.addnode(1,i);
        nearest_parent_nodeIDs(i) = nodeID;
    end
end
% t.tostring
% [nearest_parents nearest_parent_nodeIDs]
for repeat = 1:3
    for i = 1:length(nearest_parents)
        if(nearest_parents(i) > 0) %not adding to root
            if(nearest_parent_nodeIDs(nearest_parents(i)) ~= 0)
                [t, nodeID] = t.addnode(...
                    nearest_parent_nodeIDs(nearest_parents(i)),num2str(i));%...
                    %[num2str(i) ' (' num2str(cluster_starts(i)) ', ' num2str(cluster_ends(i)) ')']);
                plot([cluster_starts(i) cluster_starts(nearest_parents(i))],[cluster_ends(i) cluster_ends(nearest_parents(i))],'k','LineWidth',3);
                nearest_parent_nodeIDs(i) = nodeID;
                nearest_parents(i) = 0;
            end
        end
    end
end
% figure
% plot(t)