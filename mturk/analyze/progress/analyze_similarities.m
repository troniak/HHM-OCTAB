matrix_files = dir('output/similarity_matrix_*.mat');
header_files = dir('output/similarity_header_*.mat');
full_header = {'5.0';'5.04';'5.64';'6.12';'6.76';'6.8';'9.68'};
header_labels = {'dressing-pick';'mdew-place';'soda-cup-pick';'mdew-pick';'salad-pick';'soymilk-pick';'pizza-pick'};
D3 = zeros(length(full_header));
matrix_counter = 0;
for files = [matrix_files'; header_files']
    clearvars -except D3 matrix_counter matrix_files header_files files full_header full_header1 full_header2 header_labels
    load(['output/' files(1).name]);
    load(['output/' files(2).name]);
    mean_similarity_header
    mean_similarity_matrix
    D = mean_similarity_matrix;
    H = mean_similarity_header;
    data_labels = cellstr(num2str(nan(size(full_header,1),1)));
    full_similarity_matrix = zeros(size(full_header));
    
    [tf,loc] = ismember(H,full_header);
    full_similarity_matrix(:,loc) = D';
    D2 = full_similarity_matrix;
    %loc = sort(loc);
    %data_labels(size(data_labels,1)-size(loc,1)+1:end) = header_labels(loc);

    Hfig = figure();
    colormap('gray');
    imagesc(D2);
    colorbar;
    title(strrep(files(1).name(1:end-4),'_',' '));
    set(gca,'XTickLabel',header_labels,'YTickLabel',header_labels)
    print('-dpng',[files(1).name(1:end-4) '.png']);
%     pause;
    close all
    
%     D2 = L';%U;%(L'+U)./2;
    D2 = abs(9-D2); %convert similarity matrix to distance matrix
    D2 = D2 - D2.*eye(size(D2)); %zeros on diagonal
    D3 = D3 + D2;
    %D3 = D3 + D3';
    matrix_counter = matrix_counter + 1;
end
D3 = D3./matrix_counter;
L = tril(D3);
U = triu(D3);
MDS = mdscale(L+L',3);
% scatter(MDS(:,1),MDS(:,2),'filled')
scatter3(MDS(:,1),MDS(:,2),MDS(:,3),'filled')
text(MDS(:,1)+.1, MDS(:,2)+.1, MDS(:,3)+.1,header_labels,'FontSize',16)
