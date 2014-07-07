matrix_files = dir('similarity_matrix_*.mat');
header_files = dir('similarity_header_*.mat');
full_header = {'5.0';'5.04';'5.64';'6.12';'6.76';'6.8';'9.68'};
header_labels = {'dressing';'mdew-place';'soda-cup';'mdew-pick';'salad';'soymilk';'pizza'};
for files = [matrix_files'; header_files']
    clearvars -except matrix_files header_files files full_header full_header1 full_header2 header_labels
    load(files(1).name);
    load(files(2).name);
    mean_distance_header
    mean_distance_matrix
    D = mean_distance_matrix;
    H = mean_distance_header;
    D = padarray(D,[7-size(D,1) 7-size(D,2)],NaN,'pre');
    L = tril(D);
    U = triu(D);
    D2 = D';%L';%U;%(L'+U)./2;
    D3 = D2 - D2.*eye(size(D2,1)); %zeros on diagonal
    D3 = D3 + D3';
    data_labels = cellstr(num2str(nan(size(full_header,1),1)));
    %labels = cellstr(mean_distance_header)
    
    [tf,loc] = ismember(H,full_header);
    %size(labels,1)
    %size(loc,1)
    %if(sum(loc) <= 0)
    %    [tf,loc] = ismember(H,full_header2);
    %end
    loc = sort(loc);
    data_labels(size(data_labels,1)-size(loc,1)+1:end) = header_labels(loc);
    %labels = padarray(labels,7-size(labels,1),'0','pre');
    
    Hfig = figure();
    %HM = HeatMap(D2-5,'RowLabels',header_labels,'ColumnLabels',data_labels,'DisplayRange',4);
    %plot(HM);
    colormap('gray');
    imagesc(D2);
    colorbar;
    title(strrep(files(1).name(1:end-4),'_',' '));
    set(gca,'XTickLabel',data_labels,'YTickLabel',header_labels)
    print('-dpng',[files(1).name(1:end-4) '.png']);
    %pause
    close all
    
    %MDS = mdscale(D3,2);
    %scatter(MDS(:,1),MDS(:,2),'filled')
    %text(MDS(:,1)+.1, MDS(:,2)+.1,labels,'FontSize',16)
end