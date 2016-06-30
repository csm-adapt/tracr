% Author: Andrew Petersen
% Copyright 2016, ADAPT @ Colorado School of Mines


% ensure that we are running in the directory in which this file is stored
thisfile = mfilename('fullpath');
[pathstr, name, ext] = fileparts(thisfile);
oldpwd = cd(pathstr);

%turns off warnings, mainly for multithresh in initial images
warning('off','all')

%% Proceses image statistics
prompt = 'Input file directory containing images (string with '' '' surrounding path, example ''C:\\images'' or ''C:\\images\\''): ';
fdir = input(prompt);
directory = dir(fullfile(fdir));

if(isempty(directory))
    disp('Directory not found')
    return
end

prompt = 'Input file output path (string with '' '' surrounding path, example ''C:\\images\\thresh.tif''): ';
finput = input(prompt);
[pname, name, ext] = fileparts(finput);

directory2 = dir(fullfile(pname));
if(isempty(directory2))
    disp('Directory not found, making directory...')
    mkdir(fullfile(pname))
end



n=0;
for(i=1:size(directory,1))
    if(directory(i).name(1) ~= '.')
        n = n+1;
    end
end



gt = ones(n,2);
disp('Processing Image Statistics...')
tic

%calculates some statistics such as median, mean, and otsu threshold for
%each individual image
reverseStr='';
for(i=1:n)
    if(directory(i).name(1) ~= '.')
       im=imread(fullfile(fdir,directory(i).name),'tif');
       gt(i,:) = multithresh(im,2);
    end
    
    %outputs percent progress
    percentDone = 100 * i/n;
    msg = sprintf('Percent done: %3.1f', percentDone);
    fprintf([reverseStr, msg]);
    reverseStr = repmat(sprintf('\b'), 1, length(msg));
end

stDev_gt = std(gt(:,2));
gt_median = [median(gt(:,1)),median(gt(:,2))];

%uses median otsu threshold over all images, as well as std dev to create a
%baseline for the entire sample's images

fprintf('\nImage Processing Complete in %f s\n',toc);


%% Image  Processing and Saving
csa = NaN(n,1);
disp('Saving Images...')
tic
ctt = 0;
reverseStr='';
for(i=1:n)
    if(directory(i).name(1) ~= '.')
        ctt = ctt + 1;
        im=imread(fullfile(fdir,directory(i).name),'tif');
        imOUT = double(im);

%         gtN = multithresh(imOUT,2);
%         thresh = gtN(2);
        thresh = gt(i,2);

        if(abs(gt_median(2)-thresh) > 2*stDev_gt)
            thresh = gt_median(2);
        end

        %zeros out values less than determined threshold
        imOUT(imOUT < thresh) = 0;

        %At this point we get v1 of thresholded image, this v1 image is used for
        %edge detection in the function "fillOutsudeEdge"

        %performs edge detection and fills outside edge
        [imOUT2,csa(i)] = fillOutsideEdge(im,imOUT,0,0);

        gtv = multithresh(imOUT2,2);
        imOUT2(imOUT2<=gtv(2))=0;

        % writes thresholded image to outpute directory

        if(ctt==1)
             imwrite(imOUT2,fullfile(pname,[name,ext]));
        else
            imwrite(imOUT2,fullfile(pname,[name,ext]),'writemode','append');
        end

    end
    
    %outputs percent progress
    percentDone = 100 * i/n;
    msg = sprintf('Percent done: %3.1f', percentDone);
    fprintf([reverseStr, msg]);
    reverseStr = repmat(sprintf('\b'), 1, length(msg));
end
fprintf('\nImage Saving Complete in %f s\n',toc);

%Writes the cross sectional area per image as a csv file
area = size(im,1)*size(im,2)-csa;
csvwrite(fullfile(pname,[[name,'_csa'],'.csv']),area)
disp('CSA File written')
disp('PROGRAM COMPLETE')

% cleanup
% return the original directory (may be unnecessary...)
cd(oldpwd);
