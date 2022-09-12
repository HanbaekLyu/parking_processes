function [ Cars_new, Spots_new ] = parking_coalescing( A, Cars, Spots )
% Symmetric parking process 
% A = adjacency matrix of the unverlying graph G=(V,E) of N nodes 
% Car : N by N adjacency matrix of cars * locations
% Spot : N by N adjacency matrix of spots * locations

% definition of transition map 

[N,N] = size(A); % get number of vertices 

Cars_new = Cars; Spots_new = Spots;
Num_cars = sum(sum(Cars)');

% if there is no cars, then do nothing
if Num_cars>0
    % choose a car j and its random neighbor u
    for j=1:Num_cars
        C = find(sum(Cars')>0);
        C(j); % random index of car
        v = find(Cars(C(j),:)==1); % location of car C(j)
        
        Nv = find(A(v,:)==1); % row of neighboring nodes of v
        k = randi([1,numel(Nv)],1); % random integer from [1,b]
        u = Nv(1,k); % random neighbor of v
        
        % let the car j at v move to u;
        Cars_new(C(j),v) = 0; 
        Cars_new(C(j),u) = 1; 
    end
    % now all car has moved. For each site, kill a spot with a random car 
    
    C = sum(Cars_new); % indicators of car locations 
    S = sum(Spots_new); % indicators of spot locations
    G = find(C.*S>0); % locations of spots with cars
     
    for k=1:numel(G)
       x = G(k); % current site with spot and cars  
       Spots_new(:,x) = zeros(N,1); % remove spot from site x        
       I = find(Cars_new(:,x)>0); % indices of cars at site x
       Cars_new(I(1),x)=0; % remove car of index I(1) from state x
    end    
    
           H = find(C>1); % locations of at least two cars 
     for k=1:numel(H)
       x = H(k); % current site with spot and cars  
       L = find(Cars_new(:,x)>0); % indices of cars at site x
       Cars_new(:,x) = zeros(N,1); % remove all cars at site x
       Cars_new(L(1),x)=1; % coalesce to a car of index L(1) from state x

     end
       % now deal with swapping cars 
        EC1 = Cars + 2*Cars_new; % cars move from x to y <-> label 1 to 2 
        EC2 = Cars + 3*Cars_new; % cars move from x to y <-> label 1 to 2 
       
        Y = EC1 * EC2'; % Y(i,j)=5 iff cars i and j swapps;
   for i=1:N %zero on the lower triangle of Y to remove duplication of Y(i,j) and Y(j,i) when i and j swaps
   for j=1:i
        Y(i,j)=0;
   end
   end
[row,col] = find(Y==5); %indexing swapping cars i and j as row and col.
      for k=1:numel(row) 
          if rand>.5 %randomly remove one car when two cars swap
             Cars_new(row(k),:)=0; 
          else Cars_new(col(k),:)=0;
          end
      end

    

end    
    


end
