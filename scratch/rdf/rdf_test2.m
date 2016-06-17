clear all

%% Test Data

%Random N # of points
N = 100;
points = rand(N,2)*30-15;

%PERIODIC SPACED
% points = zeros(N,2);
% for(i=1:10)
%     for(j=1:10)
%         points(10*i+j,1) = i;
%         points(10*i+j,2) = j;
%     end
% end


%% Computation

%annulus width
dr = 0.1;

%overal area bounds
bx = [min(points(:,1)),max(points(:,1))];
by = [min(points(:,2)),max(points(:,2))];

width = bx(2)-bx(1);
height = by(2)-by(1);

%overall density
rho_overall = N/(width*height);

%max r
rmax = min([width,height])/2;

%# of rings(annuli) to compute
numAnnuli = ceil(rmax/dr);

%% computes


rdf = zeros(1,numAnnuli);

for(i=1:N)
    
    %find distances of all points from the reference point
    distances = zeros(1,N);
    for(j=1:N)        
        if(i ~=j) % skips points being correlated to itself
            d = sqrt((points(j,1)-points(i,1))^2+(points(j,2)-points(i,2))^2);
            distances(j) = d;
        end
    end
    
    %creates histogram (counts) # of points within each radial distance bin
    % (annulus)
    [binned,rvals] = histw(distances,dr,numAnnuli);

    %divides by area (2*pi()*r*dr), and divides by overall density
    tempRdf = binned./(2*pi()*rvals*dr)./rho_overall;
    rdf = rdf + tempRdf;
end

%since all the rdf's were summed, we average over the number of summed (N)
% to get our final rdf
rdf=rdf/N;

%plots points
figure
subplot(1,2,1)
scatter(points(:,1),points(:,2))
subplot(1,2,2)
plot(rvals,rdf)