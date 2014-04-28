tag_matrix = cell(size(h1_tag_matrix));
for i = 1:size(h1_tag_matrix,1)
    for j = 1:size(h1_tag_matrix,2)
        if(ischar(h1_tag_matrix{i,j}) && ischar(h2_tag_matrix{i,j}))
            tag_matrix{i,j} = strcat(h1_tag_matrix{i,j},',',h2_tag_matrix{i,j});
        elseif(ischar(h2_tag_matrix{i,j}))
            tag_matrix(i,j) = h2_tag_matrix(i,j);
        elseif(ischar(h1_tag_matrix{i,j}))
            tag_matrix(i,j) = h1_tag_matrix(i,j);
        else
            tag_matrix(i,j) = {0};
        end
    end
end