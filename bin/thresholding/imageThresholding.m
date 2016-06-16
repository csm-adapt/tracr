% Author: Andrew Petersen
% Copyright 2016, ADAPT @ Colorado School of Mines

%Version 1.1
% To use, run the script (F5)
% A dialog box will open, select one more images to process. The program
% will then runs statistics on them to find thresholding values, then will
% ask for an output directory to save the thresholded images to. This
% process takes some time
%
%Note, the code can be cleaned up and optimized. Right now its WIP. Lots fo
%debug variables and info are included

% ensure that we are running in the directory in which this file is stored
thisfile = mfilename('fullpath');
[pathstr, name, ext] = fileparts(thisfile);
oldpwd = cd(pathstr);

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

%calculates some statistics such as median, mean, and otsu threshold for
%each individual image
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

%uses median otsu threshold over all images, as well as std dev to create a
%baseline for the entire sample's images

disp(['Image Processing Complete in ',num2str(toc),'s']);


%% Image  Processing and Saving

% Gets outputs directory
choice = menu('.tif Saving Options','Save as Multiple Images','Save as Multilayer');

if(choice==0)
    return;
end

if(choice == 1)
    [d1] = uigetdir('Select output file directory');
elseif(choice == 2)
    [s1,s2] = uiputfile('Select where to save the multilayered .tif');
end


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

    %zeros out values less than determined threshold
    imOUT(imOUT < thresh) = 0;

    %At this point we get v1 of thresholded image, this v1 image is used for
    %edge detection in the function "fillOutsudeEdge"

    %performs edge detection and fills outside edge
    imOUT2 = fillOutsideEdge(im,imOUT,0,0);

    gtv = multithresh(imOUT2,2);
    imOUT2(imOUT2<=gtv(2))=0;

    % writes thresholded image to outpute directory
    if(choice == 1)
        imwrite(imOUT2,fullfile(d1,['image',num2str(i,'%04i'),'.tif']));
    elseif(choice == 2)
       if(i==1)
             imwrite(imOUT2,fullfile(s2,s1));
        else
            imwrite(imOUT2,fullfile(s2,s1),'writemode','append');
       end
    end

    waitbar(i/n,wb,['Saving Images ',num2str(i),'/',num2str(n)]);
end
close(wb)
disp(['Image Saving Complete in ',num2str(toc),'s']);

% cleanup
% return the original directory (may be unnecessary...)
cd(oldpwd);
