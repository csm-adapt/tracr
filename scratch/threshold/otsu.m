fpath = 'C:\Users\andyp\Documents\RESEARCH\xray\tomo images\C12-0.4X\Multilayer Tiff\C12-0.4X0096.tif';

im = double(imread(fpath));
N = size(im,1)*size(im,2);
bins = 250;

v = multithresh(im,2);

%% Otsu

% Histogram
hist = zeros(1,bins);
normed = (im-min(min(im)))./(max(max(im))-min(min(im)));
for(i=1:size(im,1))
    for(j=1:size(im,2))
        bv = ceil(bins*normed(i,j));
        if(bv==0)
            bv=1;
        end
        hist(bv) = hist(bv) + 1;
    end
end

disp('hist complete, performing otsu');
prob = hist./(size(im,1)*size(im,2));
lhist = length(hist);

%Based on method (source A fast algorithm for multi-level
%thresholding,Liao et al)

% creates mask for dot product based sum, using form
% 1 1 1 1
% 0 1 1 1
% 0 0 1 1
% 0 0 0 1
sumMask = triu(ones(lhist,lhist));

%creates probability table, form
% p1 p2 p3 p4
% p1 p2 p3 p4
% p1 p2 p3 p4
% p1 p2 p3 p4
prob_table = (prob'*ones(1,lhist))';
i_table = ((1:lhist)'*ones(1,lhist))';
pi_table = prob_table.*i_table;

P_table = zeros(lhist,lhist);
S_table = zeros(lhist,lhist);
for(i=1:lhist)
    sumMask = triu(ones(lhist,lhist));
    sumMask(:,i:end) = 0;
    
    P_table(:,i) = dot(sumMask,prob_table,2);
    S_table(:,i) = dot(sumMask,pi_table,2);
end


H_table = S_table.^2./P_table;
H_table(H_table == NaN) = 0;

m=0;
ind = [0,0];
for(i=1:lhist-1)
    for(j=i:lhist)
        tm = H_table(1,i) + H_table(i+1,j) + H_table(j,lhist);
        if(tm>m)
            m = tm;
            ind = [i,j];
        end
    end
end

ind = (ind/bins)*(max(max(im))-min(min(im))) - min(min(im)); 
probx = ((1:lhist)/bins)*(max(max(im))-min(min(im))) - min(min(im)); 


disp(['MATLAB Function = ',num2str(v(1)),' ',num2str(v(2))])
disp(['Programmed Function = ',num2str(ind(1)),' ',num2str(ind(2))])

%% image comparisions

figure
subplot(2,3,1)
imagesc(im);
title('Original')

subplot(2,3,2)
tim = ones(size(im));
tim(im<=v(2))=.5;
tim(im<=v(1))=0;
imagesc(tim);
title('Matlab function')

subplot(2,3,3)
tim = ones(size(im));
tim(im<=ind(2))=.5;
tim(im<=ind(1))=0;
imagesc(tim);
title('Coded function')

subplot(2,3,5)
plot(probx,prob,'b')
ylims = ylim(gca);
hold on
plot([v(1),v(1)],ylims,'r');
plot([v(2),v(2)],ylims,'r');
title('Histogram (matlab function)')

subplot(2,3,6)
plot(probx,prob,'b')
ylims = ylim(gca);
hold on
plot([ind(1),ind(1)],ylims,'r');
plot([ind(2),ind(2)],ylims,'r');
title('Histogram (coded function)')