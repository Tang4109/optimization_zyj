
L = 5;
k = 3;
A = 4 * k + 1;
M = 2 ^ L;
C = 5;

S = 1;
y = [];


syms t x  u

g = 1 - t/2;
f = int(g,t,0,x);
double x ;
%z = rand(1,10);


for i=1:32
    S = mod( (A * S + C),M );
    %fprintf('%017.17f\n',S);
    y(i) = S ./ M;
   if (15<=i)&&(i<=24)
        x = vpa(solve(f==y(i)));
        if (0<=x(1))&&(x(1)<2)
        fprintf('%020.20f\n',x(1))
        end
        if (0<=x(2))&&(x(2)<2)
        fprintf('%020.20f',x(2))
        end
   end

end
