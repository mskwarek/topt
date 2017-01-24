function varargout = TOPT_GUI(varargin)
% TOPT_GUI MATLAB code for TOPT_GUI.fig
%      TOPT_GUI, by itself, creates a new TOPT_GUI or raises the existing
%      singleton*.
%
%      H = TOPT_GUI returns the handle to a new TOPT_GUI or the handle to
%      the existing singleton*.
%
%      TOPT_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in TOPT_GUI.M with the given input arguments.
%
%      TOPT_GUI('Property','Value',...) creates a new TOPT_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before TOPT_GUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to TOPT_GUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help TOPT_GUI

% Last Modified by GUIDE v2.5 24-Jan-2017 19:49:47

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @TOPT_GUI_OpeningFcn, ...
                   'gui_OutputFcn',  @TOPT_GUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before TOPT_GUI is made visible.
function TOPT_GUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to TOPT_GUI (see VARARGIN)

% Choose default command line output for TOPT_GUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes TOPT_GUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = TOPT_GUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function param_m_Callback(hObject, eventdata, handles)
% hObject    handle to param_m (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_m as text
%        str2double(get(hObject,'String')) returns contents of param_m as a double
handles.param_m = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_m_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_m (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function param_p_Callback(hObject, eventdata, handles)
% hObject    handle to param_p (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_p as text
%        str2double(get(hObject,'String')) returns contents of param_p as a double
handles.param_p = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_p_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_p (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in calculatebutton.
function calculatebutton_Callback(hObject, eventdata, handles)
% hObject    handle to calculatebutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

lambda=(handles.param_lam)*1e-6;  %dlugosc fali
nc=(handles.param_nc);
n=(handles.param_n);   %wsp. zalamania nc-rdzen, n plaszcz 
a=(handles.param_a) * 1e-6;        %promieï¿½ rdzenia, b->inf
m=(handles.param_m);
p=(handles.param_p); 

[u, w] = projekt2(m, p, lambda, a, n, nc);
x=linspace(-2*a,2*a,150);
Ey = zeros(length(x), length(x));

    %Obliczanie pola elektrycznego
    if length(u)>=p
        x=linspace(-2*a,2*a,150);
        for i=1:length(x)
            for j=1:length(x)
               [fi,r]=cart2pol(x(i),x(j));
                if r<=a
                    Ey(i,j)=( besselj(m, (u(p).*r) ./a) ./ ( besselj(m,u(p))  ) ) .* cos(m.*fi);

                else
                    Ey(i,j)=( besselk(m, (w(p).*r) ./a) ./ ( besselk(m,w(p))  ) ) .* cos(m.*fi);
                end
            end
        end
    else
        cla(handles.plot_3, 'reset')
        cla(handles.plot_2, 'reset')
        msgbox('Podany mod nie rozchodzi siê w takim œwiat³owodzie')
        return;
    end
    surf(handles.plot_3, x,x,Ey)

    surf(x,x,Ey)
    view(0,90)
    

function param_lam_Callback(hObject, eventdata, handles)
% hObject    handle to param_lam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_lam as text
%        str2double(get(hObject,'String')) returns contents of param_lam as a double
handles.param_lam = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_lam_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_lam (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function param_a_Callback(hObject, eventdata, handles)
% hObject    handle to param_a (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_a as text
%        str2double(get(hObject,'String')) returns contents of param_a as a double
handles.param_a = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_a_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_a (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function param_n_Callback(hObject, eventdata, handles)
% hObject    handle to param_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_n as text
%        str2double(get(hObject,'String')) returns contents of param_n as a double
handles.param_n = str2double(get(hObject,'String'));
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_n_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_n (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function param_nc_Callback(hObject, eventdata, handles)
% hObject    handle to param_nc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of param_nc as text
%        str2double(get(hObject,'String')) returns contents of param_nc as a double
handles.param_nc = str2double(get(hObject,'String'))
guidata(hObject, handles);

% --- Executes during object creation, after setting all properties.
function param_nc_CreateFcn(hObject, eventdata, handles)
% hObject    handle to param_nc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
