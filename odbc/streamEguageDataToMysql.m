% Script to access the Smart Home data stream by repeatedly reading an
% updated XML file and save insert it into an SQL database

smartHomeDataFeed = 'http://152.3.3.246/cgi-bin/egauge?tot' ;   % Address of XML File that eGauage updates once per second
sqlDatabaseConnection = database('localmysql','root','');       %  SQL Database connection host, user, and password

% Set up a message box mechanism for stopping the data feed:
StopLoop = stoploop('Click the button below to stop collecting data','Smart Home Feed') ;
timeStamp = nan;

while(~StopLoop.Stop())      % Check if the loop has to be stopped
    eguageXml = xmlread(smartHomeDataFeed) ;

    % Convert the java structure into a Matlab structure
    Egauge = xml2struct(eguageXml) ;

    % Test if the timestamp is a duplicate - if not record
    cTimeStamp = str2double(Egauge.measurements.timestamp.Text) ;
    if cTimeStamp ~= timeStamp

        % Extract the Matlab structure and relevant entries
        timeStamp = str2double(Egauge.measurements.timestamp.Text) ;
        timeNumber= int32(timeStamp) ; % Convert into a integer unix time number
        power =     str2double(Egauge.measurements.cpower{1}.Text) + ...
                        str2double(Egauge.measurements.cpower{2}.Text);
        current =   str2double(Egauge.measurements.current{1}.Text) + ...
                        str2double(Egauge.measurements.current{2}.Text) ;
        voltage =   str2double(Egauge.measurements.voltage{1}.Text) ;
        
        % Format data for entry into the SQL database
        colnames = {'timestamp' 'voltage' 'current' 'power'};
        exdata = {timeNumber, voltage, current, power} ;
        fastinsert(sqlDatabaseConnection, 'powermonitor', colnames, exdata);
            
        % Iterate
        fprintf('Power = %4.1f [W]\n',power)
    end
end
StopLoop.Clear() ;  % Clear the stop loop box
clear StopLoop ;    % Remove this loop stoping structure