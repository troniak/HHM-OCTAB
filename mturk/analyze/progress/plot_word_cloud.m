function plot_word_cloud(word,frequencies,center)
    figure;
    for i = 1:length(word)
        text(center(1)+length(word)-i, center(2)+length(word)-i, word{i});
    end
end