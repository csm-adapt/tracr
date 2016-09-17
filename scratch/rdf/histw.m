function [out,xvals] = histw(x, width, vargin)

%histogram where you specify the width of each bin
%it will auto calculate the min # of bins needed to bin all the data
%optionally can set the # of bins
%0 based on left hand side
%
% returns the histogram (not normalized), as well as the left edge
% xvalues corresponding to each bin
% ignores values outside bins

if(nargin>2)
    bins = vargin;
else
    bins = ceil((max(x)/width));
end

out = zeros(1,bins);

ma = width*bins;
xvals = 0:width:ma-width;

for(i=1:length(x))
    if(x(i) == ma)
        out(bins) = out(bins)+1;
    elseif(x(i) < ma)
        out(floor(bins*x(i)/ma) + 1) = out(floor(bins*x(i)/ma) + 1) + 1; 
    end
end
