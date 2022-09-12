function Z = parking_ring(p, N, iter)
   % simulates n-periodic firefly network on rings
   % from random initial configuration
   % shows time progression like in Wolfram's work

  
R = rand(1,N);
R1 = (R<p); R2 = (R>p);
Cars = diag( R1 );
Spots = diag( R2 );

A = grid_adjacency(0,4,1,N); 

Z = zeros(iter, N);

for k=1:iter

    I_car = sum(Cars)>0;
    I_car = double(I_car);
    I_spot = sum(Spots)>0;
    I_spot = double(I_spot);
    Z(iter-k+1,:) = I_car + 2*I_spot; % 1 by N vector with 1 for car, 2 for spots, 0 for vacant sites 
    
   [Cars, Spots] = parking(A, Cars, Spots);    

    k
end


    
h = imagesc(Z);
%axis square

map = [ 1,1,1
        0,0,1
        1,0,0
];
caxis([0 2])
colormap(map)
colorbar




end
