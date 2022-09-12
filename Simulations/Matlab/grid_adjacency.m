function A = grid_adjacency(which_grid,nbh,N,M) 

% Generates a random spanning tree of a N*M grid 
% size = N
% nbh = 4 for Von Neumann nbh, and 8 for Moore nbh
% which_grid = 1 for periodic boundary condition, 0 for no bounday
% condition, 2 for triangular grid
% nr_iteration =  # of iterations of transition map

% get size of grid from initial configuratoin  

% build adjacency matrix of N bccy M grid 
%# which distance function
if nbh == 4,     distFunc = 'cityblock';
elseif nbh == 8, distFunc = 'chebychev'; end

%# compute adjacency matrix
[T S] = meshgrid(1:N,1:M);
T = T(:); S = S(:);
A = squareform( pdist([T S], distFunc) == 1 );

% torus boundary condition now only works for 4 nbh case
if which_grid == 1
    A1 = zeros(N*M,N*M);
    for k=1:N
        A1((k-1)*M+1,(k-1)*M+M)=1;
        A1((k-1)*M+M,(k-1)*M+1)=1;
    end 
    
    for k=1:M
        A1((N-1)*M+k,k)=1;
        A1(k,(N-1)*M+k)=1;
    end
    
    A = A + A1; % adding boundary adjaceny 
    A(A==2)=1;
end

if N==1
    D = 2*ones(1,M);
    D(1,1)=1; D(1,M)=1; D=diag(D);  
else
    D = 4*ones(N,M);
    D(1,:)=3; D(M,:)=3; D(:,1)=3; D(:,N)=3;
    D(1,1)=2; D(1,M)=2; D(N,1)=2; D(N,M)=2;
    D=D(:)';
    D=diag(D);  
end


% triangular grid in which all interior vertices have 6 neighbors 
if which_grid == 2
    A2 = zeros(N*M,N*M);
    for k=1:N*(M-1)
        if mod(k,N)~=1
            A2(k,k+N-1)=1;
        end
    end 
    
    A2 = A2 + A2';
    
    A = A + A2; % adding boundary adjaceny 
    A(A==2)=1;
end

% half-triangular grid

if which_grid == 3
    A2 = zeros(N*M,N*M);
    for k=1:N*(M-1)
        if mod(k,N)~=1 && mod(k,2)==1 
            A2(k,k+N-1)=1;
            A2(k,k+N+1)=1;
        end
        
        A2(10,15)=1;
        
        A2(13,19)=1;
        
    end 
    
    A2 = A2 + A2';
    
    A = A + A2; % adding boundary adjaceny 
    A(A==2)=1;
    
end


% ER graph 

if which_grid == 4
    p = 0.1/2500; %ER - G(n,p)
    A = rand(N*M,N*M) < p;
    A = triu(A,1);
    A = A + A';    
   
end



%    p = 300/10^8; %ER - G(n,p)
%    A = rand(10000,10000) < p;
%    A = triu(A,1);
%    A = A + A';   

%    T1 = T1+A;






end

