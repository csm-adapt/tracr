% Author: Andy Petersen
% Copyright 2016, ADAPT @ Colorado School of Mines

%Versions 1.1
% To use, run the script (F5)
% A dialog box will open, select one more images to process. The program
% will then runs statistics on them to find thresholding values, then will
% ask for an output directory to save the thresholded images to. This
% process takes some time
%
%Note, the code can be cleaned up and optimized. Right now its WIP. Lots fo
%debug variables and info are included


%% Proceses image statistics
[t1,t2] = uigetfile('*.*','Select Images to Process','Multiselect','on');
if(~ischar(t2))
    return
end

n = size(t1,2);

gt = ones(n,2);
med = ones(n,1);
avg = ones(n,1);
hist = zeros(300,1);

tic
wb = waitbar(0,'Processing Image Statistics');
for(i=1:n)
   im=imread(fullfile(t2,t1{i})); 
   
   if(i==1)
       soa=double(im);
   else
       soa = soa + double(im);
   end
   
   gt(i,:) = multithresh(im,2);
   med(i) = median(median(im));
   avg(i) = mean(mean(im));
   
   hist = hist + imhist(im,300);
   waitbar(i/n,wb,['Processing Image Statistics ',num2str(i),'/',num2str(n)]);
end
close(wb)
soa=soa./n;
stDev_gt = std(gt(:,2));

gt_median = [median(gt(:,1)),median(gt(:,2))];
disp(['Image Processing Complete in ',num2str(toc),'s']);

% Outputs images
[d1] = uigetdir('Select output file directory');

wb = waitbar(0,'Saving Images');
tic
for(i=1:n)
    im=imread(fullfile(t2,t1{i})); 
    imOUT = double(im);
    
    gtN = multithresh(imOUT,2);
    thresh = gtN(2);
    
    if(abs(gt_median(2)-thresh) > 2*stDev_gt)
        thresh = gt_median(2);
    end
    
    imOUT(imOUT < thresh) = 0;
    
    %At this point we get v1 of thrsholded images
    
    %performs edge detection and fills outside edge
    imOUT2 = fillOutsideEdge(im,imOUT,0,0);
    
    gtv = multithresh(imOUT2,2);
    imOUT2(imOUT2<=gtv(2))=0;
    
    
%     imwrite(imOUT,fullfile(d1,['image',num2str(i,'%04i'),'.tif']));
    imwrite(imOUT2,fullfile(d1,['image',num2str(i,'%04i'),'.tif']));
    
    waitbar(i/n,wb,['Saving Images ',num2str(i),'/',num2str(n)]);
end
close(wb)
disp(['Image Saving Complete in ',num2str(toc),'s']);