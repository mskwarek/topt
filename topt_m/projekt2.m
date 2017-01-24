% Dane wejsciowe
%('Wprowad� wektor z warto�ciami kolejno: d�. fali [nm], promie� rdzenia [um], wsp. za�amania p�aszcza, wsp. za�amania rdzenia, warto�� m, warto�� p')


function [u, w] = projekt2(m, p, lambda, a, n, nc)

%lambda=1.55e-6;   %dlugosc fali
%nc=1.46; n=1.45;   %wsp. zalamania nc-rdzen, n plaszcz 
%a=5e-6;        %promie� rdzenia, b->inf
%m=1; p=2;       %oznaczenia modu
%a=a1*1e-6;
%lambda=lambda1.*1e-9;
    if n>=nc
        ('Niepoprawne dane wej�ciowe')
        return
    end
    
    % Czestotliwosc znormalizowana
    v=((2.*pi.*a)./lambda).*sqrt(nc.^2-n.^2);

    %Wyznaczenie rozwiazan ukladu rownan
    u0=linspace(1e-3.*v,v-1e-3.*v, ceil(v));
    w0=sqrt(v.^2-u0.^2);
    n=1;

    for i=1:length(u0)
            xprim = fsolve(@(x)[(x(1).*( besselj(m-1,x(1))./besselj(m,x(1)) ) ) + (  x(2).* (besselk(m-1,x(2))./besselk(m,x(2)))  ), (v.^2-x(1).^2-x(2).^2)], [u0(i), w0(i)]);
            if imag(xprim(1))==0 && imag(xprim(2))==0 && xprim(1)>=0 && xprim(2)>=0
                x(:,n) = xprim; 
                n=n+1;
            end
    end
    
    if x==-3 
        return
    end
    x=round(10.*x)/10;
    x=unique(x','rows');
    u=x(:,1);
    w=x(:,2);
end
