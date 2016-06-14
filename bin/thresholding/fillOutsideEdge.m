% Author: Andrew Petersen
% Copyright 2016, ADAPT @ Colorado School of Mines

% Performs edge detection to find object boundry, then
% fills outside the boundry with fill value

%Note: Works best with fully convex shapes, any shaped with partial
%concavitiy may cause unexpected results

function imOut =  fillOutsideEdge(im,imEdge,fillValue,transitionsUntilFill)

%INPUTS:
% im = input image
% imEdge = image to perform edge detection on
% fillValue =  value to fill outside boundry
% transitionsUntilFill = 0 means fill outerbost boundry, 1 means fill
% inside 1 transition...
%
%OUTPUTS
% imOut = output image


imOut = im;
imc = edge(imEdge);

%ADDED dialation to help combat discontinuous edge detection
%also adds a small buffer to this
se = strel('square',2);
imc = imdilate(imc,se);

rows = size(im,1);
cols = size(im,2);

%transitions counts the transition row by row, from 0 to 1
transitions = zeros(rows,cols);

tcount=0;
for(i=1:rows)
    for(j=1:cols-1)
        if(imc(i,j) == 0 && imc(i,j+1) == 1)
            transitions(i,j:end) = tcount + 1;
            tcount=tcount+1;
        end
    end
    tcount=0;
end

for(i=1:rows)
    for(j=1:cols)
        if(transitions(i,j) == transitionsUntilFill || (transitions(i,end)-transitions(i,j)) == transitionsUntilFill)
            imOut(i,j) = fillValue;
        end
    end
end