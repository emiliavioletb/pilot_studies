%% Specify paths of pre-defined elements (.LUMO, atlas .mshs, Homer2 preprocessing .cfg file).
clear

toolboxFolder = ['/Users/emilia/Documents/MATLAB']; %path to the DOTHUB toolbox
addpath(genpath(toolboxFolder)); 

experimentPath = ['/Users/emilia/Documents/test']; %path where the data is saved
addpath(genpath(experimentPath));

% NB. Participants 1 & 2 do not have n-back task data so this is not
% analysed here. Participant 1 has altered motion task so this is not
% analysed here.

%% Block averaging of conditions for resting state, VFT and motor 

participant_list = dir('*.LUMO');
plotFlag = 0;

for i = 1:22
    
    i=1;
    LUMODirName = '1.LUMO';
%     LUMODirName = [sprintf('%d',i), '.LUMO'];

    %% Step 2. Covert .LUMO to .nirs
    [nirs, nirsFileName, SD3DFileName] = DOTHUB_LUMO2nirs(LUMODirName);
    
    %% Step 3. Run data quality checks 
    if plotFlag
        DOTHUB_dataQualityCheck(nirsFileName);
    end

    %% Pre-processing
    dod = hmrIntensity2OD(nirs.d);
    SD3D = enPruneChannels(nirs.d,nirs.SD3D,ones(size(nirs.t)),[0 1e11],12,[0 100],0); 

    %Force MeasListAct to be the same across wavelengths
    nWavs = length(SD3D.Lambda);
    tmp = reshape(SD3D.MeasListAct,length(SD3D.MeasListAct)/nWavs,nWavs);
    tmp2 = ~any(tmp'==0)';
    SD3D.MeasListAct = repmat(tmp2,nWavs,1);

    %Set SD2D
    SD2D = nirs.SD; 
    SD2D.MeasListAct = SD3D.MeasListAct;

    %Bandpass filter and convert to Concentration
    dod = hmrBandpassFilt(dod,nirs.t,0,0.5);
    dc = hmrOD2Conc(dod,SD3D,[6 6]);
    dc = dc*1e6;

    %Regress short channels
    dc = DOTHUB_hmrSSRegressionByChannel(dc,SD3D,12,1);
    
    %% Comparing conditions
    % Define parameters for comparing conditions 
%     nod_col = find(strcmp(nirs.CondNames, 'J'));
%     nod_events = nirs.s(:,nod_col);
%     restmotor_col = find(strcmp(nirs.CondNames, 'L'));
%     restmotor_events = nirs.s(:,restmotor_col);
%     tap_col = find(strcmp(nirs.CondNames, 'K'));
%     tap_events = nirs.s(:,tap_col);
    shake_col = find(strcmp(nirs.CondNames, 'Event_shake'));
    shake_events = nirs.s(:,shake_col);
%     VFTsem_col = find(strcmp(nirs.CondNames, 'B'));
%     VFTsem_events = nirs.s(:,VFTsem_col);
% %     VFTpho_col = find(strcmp(nirs.CondNames, 'C'));
% %     VFTpho_events = nirs.s(:,VFTpho_col);
% %     rest_col = find(strcmp(nirs.CondNames, 'A'));
% %     rest_events = nirs.s(:,rest_col);
        
    %Block avg
%     [nod_Avg,nod_AvgStd,nod_HRF] = hmrBlockAvg(dc,nod_events,nirs.t,[-5 15]);
%     [restmotor_Avg,restmotor_AvgStd,restmotor_HRF] = hmrBlockAvg(dc,restmotor_events,nirs.t,[-5 15]);
%     [tap_Avg,tap_AvgStd,tap_HRF] = hmrBlockAvg(dc,tap_events,nirs.t,[-5 15]);
    [shake_Avg,shake_AvgStd,shake_HRF] = hmrBlockAvg(dc,shake_events,nirs.t,[-5 15]);
%     [VFTsem_Avg,VFTsem_AvgStd,VFTsem_HRF] = hmrBlockAvg(dc,VFTsem_events,nirs.t,[-5 65]);
%     [VFTpho_Avg,VFTpho_AvgStd,VFTpho_HRF] = hmrBlockAvg(dc,VFTpho_events,nirs.t,[-5 65]);
%     [rest_Avg,rest_AvgStd,rest_HRF] = hmrBlockAvg(dc,rest_events,nirs.t,[-5 65]);

%     [dcAvg_ded,dcAvgStd_ded,~] = hmrDeconvHRF_DriftSS(dc,VFTsem_events,nirs.t,SD3D,[],ones(size(nirs.t)),[-5 65],1,1,[1 1],12,1,0,0);

    % Output data for every run of every loop
%     dcAvg_ded_group(i,:,:,:) = dcAvg_ded;
%     dcAvgStd_ded_group(i,:,:,:) = dcAvgStd_ded;
%     restAvg_group(i,:,:,:) = rest_Avg;
%     restAvgStd_group(i,:,:,:) = rest_AvgStd;
%     nodAvg_group(i, :, :, :) = nod_Avg;
%     nodAvgstd_group(i, :, :, :) = nod_AvgStd;
%     restmotor_group(i, :, :, :) = restmotor_Avg;
%     restmotorStd_group(i, :, :, :) = restmotor_AvgStd;
%     tapAvg_group(i, :, :, :) = tap_Avg;
%     tapAvgStd_group(i, :, :, :) = tap_AvgStd;
%     shakeAvg_group(i, :, :, :) = shake_Avg;
%     shakeAvgStd_group(i, :, :, :) = shake_AvgStd;
%     VFTsemAvg_group(i, :, :, :) = VFTsem_Avg;
%     VFTsemAvgStd_group(i, :, :, :) = VFTsem_AvgStd;
%     VFTphoAvg_group(i, :, :, :) = VFTpho_Avg;
%     VFTphoAvgStd_group(i, :, :, :) = VFTpho_AvgStd;

    %% Save each participant block
    filename_eachparticipant = [sprintf('%d',i)]
     save([filename_eachparticipant, 'shake.mat'], 'shake_Avg');
     save([filename_eachparticipant, 'shakeStd.mat'], 'shake_AvgStd');
%     save([filename_eachparticipant, 'restStd.mat'], 'rest_AvgStd');
%     save([filename_eachparticipant, 'rest.mat'], 'rest_Avg');
%     save([filename_eachparticipant, 'restStd.mat'], 'rest_AvgStd');
%     save([filename_eachparticipant, 'nod.mat'], 'nod_Avg');
%     save([filename_eachparticipant, 'nodStd.mat'], 'nod_AvgStd');
%     save([filename_eachparticipant, 'tap.mat'], 'tap_Avg');
%     save([filename_eachparticipant, 'tapStd.mat'], 'tap_AvgStd');
%     save([filename_eachparticipant, 'restmotor.mat'], 'restmotor_Avg');
%     save([filename_eachparticipant, 'restmotorStd.mat'], 'restmotor_AvgStd');
%     save([filename_eachparticipant, 'VFTsem.mat'], 'VFTsem_Avg');
%     save([filename_eachparticipant, 'VFTsemStd.mat'], 'VFTsem_AvgStd');
%     save([filename_eachparticipant, 'VFTpho.mat'], 'VFTpho_Avg');
%     save([filename_eachparticipant, 'VFTphoStd.mat'], 'VFTpho_AvgStd');

end

% Save each HRF
save('shakeHRF.mat', 'shake_HRF');
% save('nodHRF.mat', 'nod_HRF');
% save('tapHRF.mat', 'tap_HRF');
% save('restmotorHRF.mat', 'restmotor_HRF');
% save('VFTsemHRFtest.mat', 'VFTsem_HRF');
% save('VFTphoHRF.mat', 'VFTpho_HRF');
% save('RestHRF.mat', 'rest_HRF');

%% Distances
% dist = DOTHUB_getSDdists(SD3D);
% save('VFTpho_dists.mat', 'dist')

% Save averaged responses
save('shakeAvg_group.mat', 'shakeAvg_group');
save('shakeAvgStd_group.mat', 'shakeAvgStd_group');
% save('nodAvg_group.mat', 'nodAvg_group');
% save('nodAvgStd_group.mat', 'nodAvgstd_group');
% save('restmotor_group.mat', 'restmotor_group');
% save('restmotorStd_group.mat', 'restmotorStd_group');
% save('tapAvg_group.mat', 'tapAvg_group');
% save('tapAvgStd_group.mat', 'tapAvgStd_group');
% save('VFTsemAvg_grouptest.mat', 'VFTsemAvg_group');
% save('VFTsemAvgStd_grouptest.mat', 'VFTsemAvgStd_group');
% save('VFTphoAvg_group.mat', 'VFTphoAvg_group');
% save('VFTphoAvgStd_group.mat', 'VFTphoAvgStd_group');
% save('RestAvg_group.mat', 'restAvg_group');
% save('RestAvgStd_group.mat', 'restAvgStd_group');

%% Group averaging

dist = DOTHUB_getSDdists(SD3D);
filt30mm = dist > 27.5 & dist < 32.5;
filt20mm = dist > 17.5 & dist < 22.5;
filt10mm = dist > 7.5 & dist < 12.5;

%% VFT semantic
% VFT semantic 30mm
VFTsem30 = VFTsemAvg_group(:,:,:,filt30mm);
Av_channels_VFTsem30mm = squeeze(mean(VFTsem30,4));
Av_participants_VFTsem_30mm = squeeze(mean(Av_channels_VFTsem30mm,1));
VFTsemStd30 = VFTsemAvgStd_group(:,:,:,filt30mm);
Av_channels_VFTsem30mmStd = squeeze(mean(VFTsemStd30,4));
Av_participants_VFTsem_30mmStd = squeeze(mean(Av_channels_VFTsem30mmStd,1));
SEM_VFTsem_30mm = Av_participants_VFTsem_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTsem_HRF,Av_participants_VFTsem_30mm,SEM_VFTsem_30mm,60)

% VFT semantic 20mm
VFTsem20 = VFTsemAvg_group(:,:,:,filt20mm);
Av_channels_VFTsem20mm = squeeze(mean(VFTsem20,4));
Av_participants_VFTsem_20mm = squeeze(mean(Av_channels_VFTsem20mm,1));
VFTsemStd20 = VFTsemAvgStd_group(:,:,:,filt20mm);
Av_channels_VFTsem20mmStd = squeeze(mean(VFTsemStd20,4));
Av_participants_VFTsem_20mmStd = squeeze(mean(Av_channels_VFTsem20mmStd,1));
SEM_VFTsem_20mm = Av_participants_VFTsem_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTsem_HRF,Av_participants_VFTsem_20mm,SEM_VFTsem_20mm,60)

% VFT semantic 10mm
VFTsem10 = VFTsemAvg_group(:,:,:,filt10mm);
Av_channels_VFTsem10mm = squeeze(mean(VFTsem10,4));
Av_participants_VFTsem_10mm = squeeze(mean(Av_channels_VFTsem10mm,1));
VFTsemStd10 = VFTsemAvgStd_group(:,:,:,filt10mm);
Av_channels_VFTsem10mmStd = squeeze(mean(VFTsemStd10,4));
Av_participants_VFTsem_10mmStd = squeeze(mean(Av_channels_VFTsem10mmStd,1));
SEM_VFTsem_10mm = Av_participants_VFTsem_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTsem_HRF,Av_participants_VFTsem_10mm,SEM_VFTsem_10mm,60)

% VFT semantic all distances
Av_channels_VFTsem = squeeze(mean(VFTsemAvg_group,4));
Av_participants_VFTsem = squeeze(mean(Av_channels_VFTsem,1));
Av_channels_VFTsemStd = squeeze(mean(VFTsemAvgStd_group,4));
Av_participants_VFTsem_Std = squeeze(mean(Av_channels_VFTsemStd,1));
SEM_VFTsem = Av_participants_VFTsem_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTsem_HRF,Av_participants_VFTsem,SEM_VFTsem,60)

%% VFT phonemic
% VFT phonemic 30mm
VFTpho30 = VFTphoAvg_group(:,:,:,filt30mm);
Av_channels_VFTpho30mm = squeeze(mean(VFTpho30,4));
Av_participants_VFTpho_30mm = squeeze(mean(Av_channels_VFTpho30mm,1));
VFTphoStd30 = VFTphoAvgStd_group(:,:,:,filt30mm);
Av_channels_VFTpho30mmStd = squeeze(mean(VFTphoStd30,4));
Av_participants_VFTpho_30mmStd = squeeze(mean(Av_channels_VFTpho30mmStd,1));
SEM_VFTpho_30mm = Av_participants_VFTpho_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTpho_HRF,Av_participants_VFTpho_30mm,SEM_VFTpho_30mm,60)

% VFT phonemic 20mm
VFTpho20 = VFTphoAvg_group(:,:,:,filt20mm);
Av_channels_VFTpho20mm = squeeze(mean(VFTpho20,4));
Av_participants_VFTpho_20mm = squeeze(mean(Av_channels_VFTpho20mm,1));
VFTphoStd20 = VFTphoAvgStd_group(:,:,:,filt20mm);
Av_channels_VFTpho20mmStd = squeeze(mean(VFTphoStd20,4));
Av_participants_VFTpho_20mmStd = squeeze(mean(Av_channels_VFTpho20mmStd,1));
SEM_VFTpho_20mm = Av_participants_VFTpho_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTpho_HRF,Av_participants_VFTpho_20mm,SEM_VFTpho_20mm,60)

% VFT phonemic 10mm
VFTpho10 = VFTphoAvg_group(:,:,:,filt10mm);
Av_channels_VFTpho10mm = squeeze(mean(VFTpho10,4));
Av_participants_VFTpho_10mm = squeeze(mean(Av_channels_VFTpho10mm,1));
VFTphoStd10 = VFTphoAvgStd_group(:,:,:,filt10mm);
Av_channels_VFTpho10mmStd = squeeze(mean(VFTphoStd10,4));
Av_participants_VFTpho_10mmStd = squeeze(mean(Av_channels_VFTpho10mmStd,1));
SEM_VFTpho_10mm = Av_participants_VFTpho_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTpho_HRF,Av_participants_VFTpho_10mm,SEM_VFTpho_10mm,60)

% VFT phonemic all distances
Av_channels_VFTpho = squeeze(mean(VFTphoAvg_group,4));
Av_participants_VFTpho = squeeze(mean(Av_channels_VFTpho,1));
Av_channels_VFTphoStd = squeeze(mean(VFTphoAvgStd_group,4));
Av_participants_VFTpho_Std = squeeze(mean(Av_channels_VFTphoStd,1));
SEM_VFTpho = Av_participants_VFTpho_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(VFTpho_HRF,Av_participants_VFTpho,SEM_VFTpho,60)

%% Nodding

load('nodAvg_group.mat');
load('nodAvgStd_group.mat');
load('nodHRF')
% Nodding 30mm
Nod30 = nodAvg_group(:,:,:,filt30mm);
Av_channels_Nod30mm = squeeze(mean(Nod30,4));
Av_participants_Nod_30mm = squeeze(mean(Av_channels_Nod30mm,1));
NodStd30 = nodAvgstd_group(:,:,:,filt30mm);
Av_channels_Nod30mmStd = squeeze(mean(NodStd30,4));
Av_participants_Nod_30mmStd = squeeze(mean(Av_channels_Nod30mmStd,1));
SEM_Nod_30mm = Av_participants_Nod_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(nod_HRF,Av_participants_Nod_30mm,SEM_Nod_30mm,10)

% Nodding 20mm
Nod20 = nodAvg_group(:,:,:,filt20mm);
Av_channels_Nod20mm = squeeze(mean(Nod20,4));
Av_participants_Nod_20mm = squeeze(mean(Av_channels_Nod20mm,1));
NodStd20 = nodAvgstd_group(:,:,:,filt20mm);
Av_channels_Nod20mmStd = squeeze(mean(NodStd20,4));
Av_participants_Nod_20mmStd = squeeze(mean(Av_channels_Nod20mmStd,1));
SEM_Nod_20mm = Av_participants_Nod_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(nod_HRF,Av_participants_Nod_20mm,SEM_Nod_20mm,10)

% Nodding 10mm
Nod10 = nodAvg_group(:,:,:,filt10mm);
Av_channels_Nod10mm = squeeze(mean(Nod10,4));
Av_participants_Nod_10mm = squeeze(mean(Av_channels_Nod10mm,1));
NodStd10 = nodAvgstd_group(:,:,:,filt10mm);
Av_channels_Nod10mmStd = squeeze(mean(NodStd10,4));
Av_participants_Nod_10mmStd = squeeze(mean(Av_channels_Nod10mmStd,1));
SEM_Nod_10mm = Av_participants_Nod_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(nod_HRF,Av_participants_Nod_10mm,SEM_Nod_10mm,10)

% Nodding all distances
Av_channels_Nod = squeeze(mean(nodAvg_group,4));
Av_participants_Nod = squeeze(mean(Av_channels_Nod,1));
Av_channels_NodStd = squeeze(mean(nodAvgstd_group,4));
Av_participants_Nod_Std = squeeze(mean(Av_channels_NodStd,1));
SEM_Nod = Av_participants_Nod_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(nod_HRF,Av_participants_Nod,SEM_Nod,10)

%% Rest motor
% Rest motor 30mm
RestM30 = restmotor_group(:,:,:,filt30mm);
Av_channels_RestM30mm = squeeze(mean(RestM30,4));
Av_participants_RestM_30mm = squeeze(mean(Av_channels_RestM30mm,1));
RestMStd30 = restmotorStd_group(:,:,:,filt30mm);
Av_channels_RestM30mmStd = squeeze(mean(RestMStd30,4));
Av_participants_RestM_30mmStd = squeeze(mean(Av_channels_Nod30mmStd,1));
SEM_RestM_30mm = Av_participants_RestM_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(restmotor_HRF,Av_participants_RestM_30mm,SEM_RestM_30mm,10)

% Rest motor 20mm
RestM20 = restmotor_group(:,:,:,filt20mm);
Av_channels_RestM20mm = squeeze(mean(RestM20,4));
Av_participants_RestM_20mm = squeeze(mean(Av_channels_RestM20mm,1));
RestMStd20 = restmotorStd_group(:,:,:,filt20mm);
Av_channels_RestM20mmStd = squeeze(mean(RestMStd20,4));
Av_participants_RestM_20mmStd = squeeze(mean(Av_channels_Nod20mmStd,1));
SEM_RestM_20mm = Av_participants_RestM_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(restmotor_HRF,Av_participants_RestM_20mm,SEM_RestM_20mm,10)

% Rest motor 10mm
RestM10 = restmotor_group(:,:,:,filt10mm);
Av_channels_RestM10mm = squeeze(mean(RestM10,4));
Av_participants_RestM_10mm = squeeze(mean(Av_channels_RestM10mm,1));
RestMStd10 = restmotorStd_group(:,:,:,filt10mm);
Av_channels_RestM10mmStd = squeeze(mean(RestMStd10,4));
Av_participants_RestM_10mmStd = squeeze(mean(Av_channels_Nod10mmStd,1));
SEM_RestM_10mm = Av_participants_RestM_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(restmotor_HRF,Av_participants_RestM_10mm,SEM_RestM_10mm,10)

% Rest motor all distances
Av_channels_RestM = squeeze(mean(restmotor_group,4));
Av_participants_RestM = squeeze(mean(Av_channels_RestM,1));
Av_channels_RestMStd = squeeze(mean(restmotorStd_group,4));
Av_participants_RestM_Std = squeeze(mean(Av_channels_RestMStd,1));
SEM_RestM = Av_participants_RestM_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(restmotor_HRF,Av_participants_RestM,SEM_RestM,10)

%% Tapping
% Tapping 30mm
Tap30 = tapAvg_group(:,:,:,filt30mm);
Av_channels_Tap30mm = squeeze(mean(Tap30,4));
Av_participants_Tap_30mm = squeeze(mean(Av_channels_Tap30mm,1));
TapStd30 = tapAvgStd_group(:,:,:,filt30mm);
Av_channels_Tap30mmStd = squeeze(mean(TapStd30,4));
Av_participants_Tap_30mmStd = squeeze(mean(Av_channels_Tap30mmStd,1));
SEM_Tap_30mm = Av_participants_Tap_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(tap_HRF,Av_participants_Tap_30mm,SEM_Tap_30mm,10)

% Tapping 20mm
Tap20 = tapAvg_group(:,:,:,filt20mm);
Av_channels_Tap20mm = squeeze(mean(Tap20,4));
Av_participants_Tap_20mm = squeeze(mean(Av_channels_Tap20mm,1));
TapStd20 = tapAvgStd_group(:,:,:,filt20mm);
Av_channels_Tap20mmStd = squeeze(mean(TapStd20,4));
Av_participants_Tap_20mmStd = squeeze(mean(Av_channels_Tap20mmStd,1));
SEM_Tap_20mm = Av_participants_Tap_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(tap_HRF,Av_participants_Tap_20mm,SEM_Tap_20mm,10)

% Tapping 10mm
Tap10 = tapAvg_group(:,:,:,filt10mm);
Av_channels_Tap10mm = squeeze(mean(Tap10,4));
Av_participants_Tap_10mm = squeeze(mean(Av_channels_Tap10mm,1));
TapStd10 = tapAvgStd_group(:,:,:,filt10mm);
Av_channels_Tap10mmStd = squeeze(mean(TapStd10,4));
Av_participants_Tap_10mmStd = squeeze(mean(Av_channels_Tap10mmStd,1));
SEM_Tap_10mm = Av_participants_Tap_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(tap_HRF,Av_participants_Tap_10mm,SEM_Tap_10mm,10)

% Tapping all distances
Av_channels_Tap = squeeze(mean(nodAvg_group,4));
Av_participants_Tap = squeeze(mean(Av_channels_Tap,1));
Av_channels_TapStd = squeeze(mean(tapAvgStd_group,4));
Av_participants_Tap_Std = squeeze(mean(Av_channels_TapStd,1));
SEM_Tap = Av_participants_Tap_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(tap_HRF,Av_participants_Tap,SEM_Tap,10)

%% Shaking
% Shaking 30mm
Shake30 = shakeAvg_group(:,:,:,filt30mm);
Av_channels_Shake30mm = squeeze(mean(Shake30,4));
Av_participants_Shake_30mm = squeeze(mean(Av_channels_Shake30mm,1));
ShakeStd30 = shakeAvgStd_group(:,:,:,filt30mm);
Av_channels_Shake30mmStd = squeeze(mean(ShakeStd30,4));
Av_participants_Shake_30mmStd = squeeze(mean(Av_channels_Shake30mmStd,1));
SEM_Shake_30mm = Av_participants_Shake_30mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(shake_HRF,Av_participants_Shake_30mm,SEM_Shake_30mm,10)

% Shaking 20mm
Shake20 = shakeAvg_group(:,:,:,filt20mm);
Av_channels_Shake20mm = squeeze(mean(Shake20,4));
Av_participants_Shake_20mm = squeeze(mean(Av_channels_Shake20mm,1));
ShakeStd20 = shakeAvgStd_group(:,:,:,filt20mm);
Av_channels_Shake20mmStd = squeeze(mean(ShakeStd20,4));
Av_participants_Shake_20mmStd = squeeze(mean(Av_channels_Shake20mmStd,1));
SEM_Shake_20mm = Av_participants_Shake_20mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(shake_HRF,Av_participants_Shake_20mm,SEM_Shake_20mm,10)

% Shaking 10mm
Shake10 = shakeAvg_group(:,:,:,filt10mm);
Av_channels_Shake10mm = squeeze(mean(Shake10,4));
Av_participants_Shake_10mm = squeeze(mean(Av_channels_Shake10mm,1));
ShakeStd10 = shakeAvgStd_group(:,:,:,filt10mm);
Av_channels_Shake10mmStd = squeeze(mean(ShakeStd10,4));
Av_participants_Shake_10mmStd = squeeze(mean(Av_channels_Shake10mmStd,1));
SEM_Shake_10mm = Av_participants_Shake_10mmStd/sqrt(22);
figure(1);
DOTHUB_plotHRF(shake_HRF,Av_participants_Shake_10mm,SEM_Shake_10mm,10)

% Shaking all distances
Av_channels_Shake = squeeze(mean(shakeAvg_group,4));
Av_participants_Shake = squeeze(mean(Av_channels_Shake,1));
Av_channels_ShakeStd = squeeze(mean(shakeAvgStd_group,4));
Av_participants_Shake_Std = squeeze(mean(Av_channels_ShakeStd,1));
SEM_Shake = Av_participants_Shake_Std/sqrt(22);
figure(1);
DOTHUB_plotHRF(shake_HRF,Av_participants_Shake,SEM_Shake,10)
