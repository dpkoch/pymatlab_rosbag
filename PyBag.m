classdef PyBag
    %PYBAG A class for reading data from ROS bags using the Python API.
    %
    % This class is only compatible with Matlab version 2014b or later.
    
    properties
        path % path to the bag
        time_begin % timestamp of first message in the bag
        time_end % timestamp of last message in the bag
    end
    
    properties (Hidden)
        bag
    end
    
    methods(Static)
        function [obj] = load(path)
            % Construct a bag using path.
            %
            % Function exists because it autocompletes paths when you hit
            % tab.
            obj =  PyBag(path);
        end
    end
    
    methods
        function obj = PyBag(path)
            if verLessThan('matlab', '8.4')
                error('Python only supported since R2014b (Version 8.4)')
            end
            
            if ~exist(path, 'file')
                error('The input file ''%s'' does not exist', path)
            end
            
            obj.path = path;
            obj.bag = py.pybag.PyBag(path);
            obj.time_begin = obj.bag.start_time();
            obj.time_end = obj.bag.end_time();
        end
        
        function info = info(obj)
            info = python2matlab(obj.bag.info());
        end
        
        function [topics, types] = topics(obj)
            topics = python2matlab(obj.bag.topics());
            if nargout > 1
                types = python2matlab(obj.bag.types());
            end
        end
        
        function data = data(obj)
            data = python2matlab(obj.bag.data());
        end
        
    end
    
end

