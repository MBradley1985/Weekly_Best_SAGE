#!/usr/bin/env python

import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd

from random import sample, seed

import warnings
warnings.filterwarnings("ignore")

# ========================== USER OPTIONS ==========================

# File details
DirName = './output/millennium/'
FileName = 'model_0.hdf5'

# Simulation details
Hubble_h = 0.73        # Hubble parameter
BoxSize = 62.5         # h-1 Mpc
VolumeFraction = 1.0   # Fraction of the full volume output by the model

# Simulation details
#Hubble_h = 0.677400        # Hubble parameter
#BoxSize = 400         # h-1 Mpc
#VolumeFraction = 1.0   # Fraction of the full volume output by the model
FirstSnap = 0          # First snapshot to read
LastSnap = 63          # Last snapshot to read
redshifts = [127.000, 79.998, 50.000, 30.000, 19.916, 18.244, 16.725, 15.343, 14.086, 12.941, 11.897, 10.944, 10.073, 
             9.278, 8.550, 7.883, 7.272, 6.712, 6.197, 5.724, 5.289, 4.888, 4.520, 4.179, 3.866, 3.576, 3.308, 3.060, 
             2.831, 2.619, 2.422, 2.239, 2.070, 1.913, 1.766, 1.630, 1.504, 1.386, 1.276, 1.173, 1.078, 0.989, 0.905, 
             0.828, 0.755, 0.687, 0.624, 0.564, 0.509, 0.457, 0.408, 0.362, 0.320, 0.280, 0.242, 0.208, 0.175, 0.144, 
             0.116, 0.089, 0.064, 0.041, 0.020, 0.000]  # Redshift of each snapshot

#redshifts = [13.9334, 12.67409, 11.50797, 10.44649, 9.480752, 8.58543, 7.77447, 7.032387, 6.344409, 5.721695,
           # 5.153127, 4.629078, 4.26715, 3.929071, 3.610462, 3.314082, 3.128427, 2.951226, 2.77809, 2.616166,
           # 2.458114, 2.309724, 2.16592, 2.027963, 1.8962, 1.770958, 1.65124, 1.535928, 1.426272, 1.321656,
           # 1.220303, 1.124166, 1.031983, 0.9441787, 0.8597281, 0.779046, 0.7020205, 0.6282588, 0.5575475, 0.4899777,
           # 0.4253644, 0.3640053, 0.3047063, 0.2483865, 0.1939743, 0.1425568, 0.09296665, 0.0455745, 0.02265383, 0.0001130128]

# Plotting options
whichimf = 1        # 0=Slapeter; 1=Chabrier
dilute = 7500       # Number of galaxies to plot in scatter plots
sSFRcut = -11.0     # Divide quiescent from star forming galaxies
SMFsnaps = [63, 40, 32, 27, 23, 20, 18, 16]  # Snapshots to plot the SMF
BHMFsnaps = [63, 40, 32, 27, 23, 20, 18, 16]  # Snapshots to plot the SMF
#SMFsnaps = [49, 38, 32, 23, 17, 13, 10, 8, 7, 5, 4]  # Snapshots to plot the SMF
#BHMFsnaps = [49, 38, 32, 23, 17, 13, 10, 8, 7, 5, 4]  # Snapshots to plot the BHMF

OutputFormat = '.png'
plt.rcParams["figure.figsize"] = (8.34,6.25)
plt.rcParams["figure.dpi"] = 96
plt.rcParams["font.size"] = 14


# ==================================================================

def read_hdf(filename = None, snap_num = None, param = None):

    property = h5.File(DirName+FileName,'r')
    return np.array(property[snap_num][param])


# ==================================================================

if __name__ == '__main__':

    print('Running allresults (history)\n')

    seed(2222)
    volume = (BoxSize/Hubble_h)**3.0 * VolumeFraction

    OutputDir = DirName + 'plots/'
    if not os.path.exists(OutputDir): os.makedirs(OutputDir)

    # Read galaxy properties
    print('Reading galaxy properties from', DirName+FileName, '\n')

    StellarMassFull = [0]*(LastSnap-FirstSnap+1)
    SfrDiskFull = [0]*(LastSnap-FirstSnap+1)
    SfrBulgeFull = [0]*(LastSnap-FirstSnap+1)
    BlackHoleMassFull = [0]*(LastSnap-FirstSnap+1)
    BulgeMassFull = [0]*(LastSnap-FirstSnap+1)
    HaloMassFull = [0]*(LastSnap-FirstSnap+1)

    for snap in range(FirstSnap,LastSnap+1):

        Snapshot = 'Snap_'+str(snap)

        StellarMassFull[snap] = read_hdf(snap_num = Snapshot, param = 'StellarMass') * 1.0e10 / Hubble_h
        SfrDiskFull[snap] = read_hdf(snap_num = Snapshot, param = 'SfrDisk')
        SfrBulgeFull[snap] = read_hdf(snap_num = Snapshot, param = 'SfrBulge')
        BlackHoleMassFull[snap] = read_hdf(snap_num = Snapshot, param = 'BlackHoleMass') * 1.0e10 / Hubble_h
        BulgeMassFull[snap] = read_hdf(snap_num = Snapshot, param = 'BulgeMass') * 1.0e10 / Hubble_h
        HaloMassFull[snap] = read_hdf(snap_num = Snapshot, param = 'Mvir') * 1.0e10 / Hubble_h

# --------------------------------------------------------

    print('Plotting the halo-stellar mass relation')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure
    
    
    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[0]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[0]][w])
    x = np.log10(HaloMassFull[SMFsnaps[0]][w])

    plt.scatter(x, y, c='k', alpha=0.3, s=5, label='Model galaxies')

    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[1]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[1]][w])
    x = np.log10(HaloMassFull[SMFsnaps[1]][w])

    #plt.plot(x, y, c='k', label='Model galaxies')

    ###### z=0
    
    w = np.where(StellarMassFull[SMFsnaps[2]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[2]][w])
    x = np.log10(HaloMassFull[SMFsnaps[2]][w])

    #plt.plot(x, y, c='k', label='Model galaxies')

    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[3]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[3]][w])
    x = np.log10(HaloMassFull[SMFsnaps[3]][w])

    #plt.plot(x, y, c='k', label='Model galaxies')

    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[4]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[4]][w])
    x = np.log10(HaloMassFull[SMFsnaps[4]][w])

    #plt.plot(x, y, c='k', label='Model galaxies')

    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[5]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[5]][w])
    x = np.log10(HaloMassFull[SMFsnaps[5]][w])

    #plt.plot(x, y, c='k', label='Model galaxies')

    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[6]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(StellarMassFull[SMFsnaps[6]][w])
    x = np.log10(HaloMassFull[SMFsnaps[6]][w])

    #plt.plot(x, y, c='k', alpha=0.1, label='Model galaxies')
    
    print('Plotting the halo-stellar mass relation')

    # Initialize list to store binned data for each redshift
    binned_data = []

    # Define number of bins
    n_bins = 50

    # Define colors for different redshifts
    colors = plt.cm.viridis(np.linspace(0, 1, len(SMFsnaps)))

    for i, snap in enumerate(SMFsnaps):
        # Get valid data points - check for positive values before taking log
        w = np.where((StellarMassFull[snap] > 0.0) & (HaloMassFull[snap] > 0.0))[0]
        
        if len(w) == 0:
            print(f"No valid data for redshift {i}")
            continue
            
        y = np.log10(StellarMassFull[snap][w])
        x = np.log10(HaloMassFull[snap][w])
        
        # Remove any remaining infinities or NaNs
        valid_mask = np.isfinite(x) & np.isfinite(y)
        x = x[valid_mask]
        y = y[valid_mask]
        
        print(f"\nRedshift {i}:")
        print(f"Number of valid points: {len(x)}")
        print(f"X range: {np.min(x):.2f} to {np.max(x):.2f}")
        print(f"Y range: {np.min(y):.2f} to {np.max(y):.2f}")
        
        if len(x) == 0:
            continue
        
        # Create bins
        x_min, x_max = np.min(x), np.max(x)
        bins = np.linspace(x_min, x_max, n_bins+1)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Calculate statistics in each bin
        bin_means_y = np.zeros(n_bins)
        bin_stds_y = np.zeros(n_bins)
        bin_counts = np.zeros(n_bins)
        
        for j in range(n_bins):
            mask = (x >= bins[j]) & (x < bins[j+1])
            n_points = np.sum(mask)
            
            if n_points > 0:
                bin_means_y[j] = np.mean(y[mask])
                bin_stds_y[j] = np.std(y[mask])
                bin_counts[j] = n_points
            else:
                bin_means_y[j] = np.nan
                bin_stds_y[j] = np.nan
                bin_counts[j] = 0
        
        # Store binned data
        binned_data.append((bin_centers, bin_means_y, bin_stds_y, bin_counts))
        
        # Plot binned data as a line with shaded error region
        valid = ~np.isnan(bin_means_y)
        if np.any(valid):
            plt.scatter(bin_centers[valid], bin_means_y[valid], 
                    color=colors[i], label=f'z = {i}')
            plt.fill_between(bin_centers[valid], 
                            bin_means_y[valid] - bin_stds_y[valid],
                            bin_means_y[valid] + bin_stds_y[valid],
                            color=colors[i], alpha=0.2)

    # Write binned data to CSV
    try:
        with open('halostellar_binned_all_redshifts.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            
            # Create and write header
            #header = []
            #for i in range(len(SMFsnaps)):
                #header.extend([f'BulgeMass_z{i}', f'BlackHoleMass_z{i}', f'Std_z{i}', f'Count_z{i}'])
            #writer.writerow(header)
            
            # Write data rows
            for i in range(n_bins):
                row = []
                for bin_centers, means, stds, counts in binned_data:
                    if i < len(bin_centers):  # Make sure we have data for this bin
                        # Replace nan with NaN in the output
                        center = 'NaN' if np.isnan(bin_centers[i]) else bin_centers[i]
                        mean = 'NaN' if np.isnan(means[i]) else means[i]
                        std = 'NaN' if np.isnan(stds[i]) else stds[i]
                        count = 'NaN' if np.isnan(counts[i]) else counts[i]
                        row.extend([center, mean, std, count])
                    else:
                        row.extend(['NaN', 'NaN', 'NaN', 'NaN'])
                writer.writerow(row)
                
        print(f"\nSuccessfully wrote binned data to halostellar_binned_all_redshifts.csv")
        
    except Exception as e:
        print(f"\nError writing to CSV: {e}")

    plt.ylabel(r'$\log_{10} M_{\mathrm{stars}}\ (M_{\odot})$')
    plt.xlabel(r'$\log_{10} M_{\mathrm{halo}}\ (M_{\odot})$')
    plt.legend()


    ######

    plt.axis([10.0, 15.0, 7, 13])

    # Set the x-axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

    leg = plt.legend(loc='lower right', numpoints=1, labelspacing=0.1)
    leg.draw_frame(False)  # Don't want a box frame
    for t in leg.get_texts():  # Reduce the size of the text
        t.set_fontsize('medium')

    outputFile = OutputDir + 'A.HaloStellarMass_z' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()

# --------------------------------------------------------

# --------------------------------------------------------

    print('Plotting the black hole-bulge relation')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure
    
    
    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[0]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[0]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[0]][w])

    plt.scatter(x, y, s=0.5, c='k', alpha=0.6, label='Model galaxies')
    # overplot Haring & Rix 2004
    w = 10. ** np.arange(20)
    BHdata = 10. ** (8.2 + 1.12 * np.log10(w / 1.0e11))
    plt.plot(np.log10(w), np.log10(BHdata), 'b-', label="Haring \& Rix 2004")

    

    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[1]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[1]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[1]][w])

    plt.scatter(x, y, s=0.5, c='k', alpha=0.6, label='Model galaxies')

    ###### z=0
    
    w = np.where(BlackHoleMassFull[SMFsnaps[2]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[2]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[2]][w])

    plt.scatter(x, y, s=0.5, c='k', alpha=0.6, label='Model galaxies')
    """
    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[3]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[3]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[3]][w])

    plt.scatter(x, y, s=0.1, c='k', alpha=0.1, label='Model galaxies')

    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[4]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[4]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[4]][w])

    plt.scatter(x, y, s=0.1, c='k', alpha=0.1, label='Model galaxies')

    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[5]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[5]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[5]][w])

    plt.scatter(x, y, s=0.1, c='k', alpha=0.1, label='Model galaxies')

    ###### z=0

    w = np.where(BlackHoleMassFull[SMFsnaps[6]] > 0.0)[0]
    if(len(w) > dilute): w = sample(list(range(len(w))), dilute)
    y = np.log10(BlackHoleMassFull[SMFsnaps[6]][w])
    x = np.log10(BulgeMassFull[SMFsnaps[6]][w])

    plt.scatter(x, y, s=0.1, c='k', alpha=0.1, label='Model galaxies')
    """
    print('Plotting the black hole-bulge relation')

    # Initialize list to store binned data for each redshift
    binned_data = []

    # Define number of bins
    n_bins = 50

    # Define colors for different redshifts
    colors = plt.cm.viridis(np.linspace(0, 1, len(SMFsnaps)))

    for i, snap in enumerate(SMFsnaps):
        # Get valid data points - check for positive values before taking log
        w = np.where((BlackHoleMassFull[snap] > 0.0) & (BulgeMassFull[snap] > 0.0))[0]
        
        if len(w) == 0:
            print(f"No valid data for redshift {i}")
            continue
            
        y = np.log10(BlackHoleMassFull[snap][w])
        x = np.log10(BulgeMassFull[snap][w])
        
        # Remove any remaining infinities or NaNs
        valid_mask = np.isfinite(x) & np.isfinite(y)
        x = x[valid_mask]
        y = y[valid_mask]
        
        print(f"\nRedshift {i}:")
        print(f"Number of valid points: {len(x)}")
        print(f"X range: {np.min(x):.2f} to {np.max(x):.2f}")
        print(f"Y range: {np.min(y):.2f} to {np.max(y):.2f}")
        
        if len(x) == 0:
            continue
        
        # Create bins
        x_min, x_max = np.min(x), np.max(x)
        bins = np.linspace(x_min, x_max, n_bins+1)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Calculate statistics in each bin
        bin_means_y = np.zeros(n_bins)
        bin_stds_y = np.zeros(n_bins)
        bin_counts = np.zeros(n_bins)
        
        for j in range(n_bins):
            mask = (x >= bins[j]) & (x < bins[j+1])
            n_points = np.sum(mask)
            
            if n_points > 0:
                bin_means_y[j] = np.mean(y[mask])
                bin_stds_y[j] = np.std(y[mask])
                bin_counts[j] = n_points
            else:
                bin_means_y[j] = np.nan
                bin_stds_y[j] = np.nan
                bin_counts[j] = 0
        
        # Store binned data
        binned_data.append((bin_centers, bin_means_y, bin_stds_y, bin_counts))
        
        # Plot binned data as a line with shaded error region
        valid = ~np.isnan(bin_means_y)
        if np.any(valid):
            plt.plot(bin_centers[valid], bin_means_y[valid], '-', 
                    color=colors[i], linewidth=2, label=f'z = {i}')
            plt.fill_between(bin_centers[valid], 
                            bin_means_y[valid] - bin_stds_y[valid],
                            bin_means_y[valid] + bin_stds_y[valid],
                            color=colors[i], alpha=0.2)

    # Write binned data to CSV
    try:
        with open('bhbm_binned_all_redshifts.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            
            # Create and write header
            #header = []
            #for i in range(len(SMFsnaps)):
                #header.extend([f'BulgeMass_z{i}', f'BlackHoleMass_z{i}', f'Std_z{i}', f'Count_z{i}'])
            #writer.writerow(header)
            
            # Write data rows
            for i in range(n_bins):
                row = []
                for bin_centers, means, stds, counts in binned_data:
                    if i < len(bin_centers):  # Make sure we have data for this bin
                        # Replace nan with NaN in the output
                        center = 'NaN' if np.isnan(bin_centers[i]) else bin_centers[i]
                        mean = 'NaN' if np.isnan(means[i]) else means[i]
                        std = 'NaN' if np.isnan(stds[i]) else stds[i]
                        count = 'NaN' if np.isnan(counts[i]) else counts[i]
                        row.extend([center, mean, std, count])
                    else:
                        row.extend(['NaN', 'NaN', 'NaN', 'NaN'])
                writer.writerow(row)
                
        print(f"\nSuccessfully wrote binned data to bhbm_binned_all_redshifts.csv")
        
    except Exception as e:
        print(f"\nError writing to CSV: {e}")

    plt.ylabel(r'$\log_{10} M_{\mathrm{BH}}\ (M_{\odot})$')
    plt.xlabel(r'$\log_{10} M_{\mathrm{bulge}}\ (M_{\odot})$')
    plt.legend()


    ######

    plt.axis([8.0, 12.0, 6.0, 10.0])

    # Set the x-axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

    leg = plt.legend(loc='lower left', numpoints=1, labelspacing=0.1)
    leg.draw_frame(False)  # Don't want a box frame
    for t in leg.get_texts():  # Reduce the size of the text
        t.set_fontsize('medium')

    outputFile = OutputDir + 'A.BlackholeBulgeMass_z' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()

# --------------------------------------------------------

# --------------------------------------------------------

    print('Plotting the stellar mass function')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure
    
    x_z0 = [11.625, 11.5, 11.375, 11.25, 11.125, 11, 10.875, 10.75, 10.625, 10.5, 10.375, 10.25,
          10.125, 10, 9.875, 9.75, 9.625, 9.5, 9.375, 9.25, 9.125, 9, 8.875, 8.75, 8.625,
            8.5, 8.375, 8.25, 8.125, 8, 7.875, 7.75, 7.625, 7.5, 7.375, 7.25, 7.125, 7, 6.875]
    y_z0 = [-4.704, -3.944, -3.414, -3.172, -2.937, -2.698, -2.566, -2.455, -2.355, -2.301,
          -2.305, -2.274, -2.281, -2.259, -2.201, -2.176, -2.151, -2.095, -2.044, -1.986,
            -1.906, -1.812, -1.806, -1.767, -1.627, -1.646, -1.692, -1.599, -1.581,
              -1.377, -1.417, -1.242, -1.236, -1.236, -1.043, -0.969, -0.937, -0.799, -1.009]
    y_z0 = [10**y_z0 for y_z0 in y_z0]
    plt.plot(x_z0, y_z0, 'b:', lw=10, alpha=0.5, label='Driver et al., 2022 z=[0.1]')

    x_z1 = [8.726315789473684, 8.857894736842105, 8.973684210526315, 9.115789474, 9.236842105263158,
          9.363157894736842, 9.5, 9.642105263157895, 9.794736842105262, 9.952631578947368, 10.126315789473683,
            10.305263157894736, 10.51578947368421, 10.742105263157894, 10.921052631578947, 11.136842105263158,
              11.252631578947367, 11.368421052631579, 11.44736842105263, 11.510526315789473, 11.58421052631579,
                11.647368421052631, 11.678947368421053]
    y_z1 = [-2.151750973, -2.186770428, -2.221789883, -2.256809339, -2.291828794, -2.326848249, -2.373540856,
          -2.408560311, -2.455252918, -2.490272374, -2.536964981, -2.618677043, -2.653696498, -2.770428016,
            -2.898832685, -3.143968872, -3.412451362, -3.680933852, -3.996108949, -4.369649805, -4.766536965,
              -5.151750973, -5.420233463]
    y_z1 = [10**y_z1 for y_z1 in y_z1]
    plt.plot(x_z1, y_z1, 'b:', lw=10, alpha=0.5, label='Ilbert et al., 2010 z=[1.0]')
    
    x_z2 = [8.609848485, 8.856060606, 9.140151515, 9.386363636, 9.613636364, 9.897727273, 10.10606061,
             10.37121212, 10.65530303, 10.88257576, 11.14772727, 11.35606061, 11.64015152, 11.90530303]
    y_z2 = [-2.616161616, -2.792929293, -2.919191919, -3.146464646, -3.398989899, -3.727272727,
             -4.055555556, -4.308080808, -4.308080808, -4.585858586, -5.090909091, -5.570707071,
               -5.671717172, -6.050505051]
    y_z2 = [10**y_z2 for y_z2 in y_z2]
    plt.plot(x_z2, y_z2, 'g:', lw=10, alpha=0.5, label='Shuntov et al., 2024 z=[2.0]')
    
    x_z3 = [8.889312977, 9.118320611, 9.385496183, 9.652671756, 9.919847328, 10.16793893,
             10.4351145, 10.66412214]
    y_z3 = [-3.969543147, -4.375634518, -4.578680203, -4.680203046, -5.035532995, -5.390862944,
             -5.517766497, -6.025380711]
    y_z3 = [10**y_z3 for y_z3 in y_z3]
    plt.plot(x_z3, y_z3, 'r:', lw=10, alpha=0.5, label='... z=[3.0]')
    
    ###### z=0

    w = np.where(StellarMassFull[SMFsnaps[0]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[0]][w])

    binwidth = 0.1
    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'k-', label='Model galaxies')

    ###### z=1.3
    
    w = np.where(StellarMassFull[SMFsnaps[1]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[1]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'b-')

    ###### z=2
    
    w = np.where(StellarMassFull[SMFsnaps[2]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[2]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'g-')

    ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[3]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[3]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')
    """
      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[4]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[4]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[5]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[5]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[6]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[6]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[7]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[7]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[8]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[8]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(StellarMassFull[SMFsnaps[9]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[9]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

    w = np.where(StellarMassFull[SMFsnaps[10]] > 0.0)[0]
    mass = np.log10(StellarMassFull[SMFsnaps[10]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')
"""
# Calculate the data for each redshift
    data = []
    for snap in SMFsnaps:
        w = np.where(StellarMassFull[snap] > 0.0)[0]
        mass = np.log10(StellarMassFull[snap][w])

        binwidth = 0.1
        mi = 7.0
        ma = 15.0
        NB = int((ma - mi) / binwidth)
        (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
        xaxeshisto = binedges[:-1] + 0.5 * binwidth
        yaxeshisto = counts / volume / binwidth

        data.append((xaxeshisto, yaxeshisto))

    # Find the maximum length of x and y arrays
    max_length = max(len(x) for x, _ in data)

    # Open a single tab-delimited file for writing
    with open('smf_all_redshifts.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write header
        #header = ['x', 'y'] * len(SMFsnaps)
        #writer.writerow(header)

        # Write data rows
        for i in range(max_length):
            row = []
            for x, y in data:
                if i < len(x):
                    row.extend([x[i], y[i]])
                else:
                    row.extend(['', ''])
            writer.writerow(row)


    ######

    plt.yscale('log')
    plt.axis([8.0, 12.2, 1.0e-6, 1.0e-1])

    # Set the x-axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

    plt.ylabel(r'$\phi\ (\mathrm{Mpc}^{-3}\ \mathrm{dex}^{-1}$)')  # Set the y...
    plt.xlabel(r'$\log_{10} M_{\mathrm{stars}}\ (M_{\odot})$')  # and the x-axis labels

    leg = plt.legend(loc='lower left', numpoints=1, labelspacing=0.1)
    leg.draw_frame(False)  # Don't want a box frame
    for t in leg.get_texts():  # Reduce the size of the text
        t.set_fontsize('medium')

    outputFile = OutputDir + 'A.StellarMassFunction_z' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()

# --------------------------------------------------------

    print('Plotting the black hole mass function')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure
    
    ###### z=0

    w = np.where(BlackHoleMassFull[BHMFsnaps[0]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[0]][w])

    binwidth = 0.1
    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'k-', label='Model galaxies')

    ###### z=1.3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[1]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[1]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'b-')

    ###### z=2
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[2]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[2]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'g-')

    ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[3]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[3]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')
    """
      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[4]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[4]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[5]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[5]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[6]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[6]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[7]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[7]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[8]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[8]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[9]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[9]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')

      ###### z=3
    
    w = np.where(BlackHoleMassFull[BHMFsnaps[10]] > 0.0)[0]
    mass = np.log10(BlackHoleMassFull[BHMFsnaps[10]][w])

    mi = np.floor(min(mass)) - 2
    ma = np.floor(max(mass)) + 2
    NB = int((ma - mi) / binwidth)
    (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
    xaxeshisto = binedges[:-1] + 0.5 * binwidth

    plt.plot(xaxeshisto, counts / volume / binwidth, 'r-')
    """    

# Calculate the data for each redshift
    data = []
    for snap in BHMFsnaps:
        w = np.where(BlackHoleMassFull[snap] > 0.0)[0]
        mass = np.log10(BlackHoleMassFull[snap][w])

        binwidth = 0.1
        mi = 6.0
        ma = 10.0
        NB = int((ma - mi) / binwidth)
        (counts, binedges) = np.histogram(mass, range=(mi, ma), bins=NB)
        xaxeshisto = binedges[:-1] + 0.5 * binwidth
        yaxeshisto = counts / volume / binwidth

        data.append((xaxeshisto, yaxeshisto))

    # Find the maximum length of x and y arrays
    max_length = max(len(x) for x, _ in data)

    # Open a single tab-delimited file for writing
    with open('bhmf_all_redshifts.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write header
        #header = ['x', 'y'] * len(BHMFsnaps)
        #writer.writerow(header)

        # Write data rows
        for i in range(max_length):
            row = []
            for x, y in data:
                if i < len(x):
                    row.extend([x[i], y[i]])
                else:
                    row.extend(['', ''])
            writer.writerow(row)


    ######

    plt.yscale('log')
    plt.axis([6.0, 10.2, 1.0e-6, 1.0e-1])

    # Set the x-axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

    plt.ylabel(r'$\phi\ (\mathrm{Mpc}^{-3}\ \mathrm{dex}^{-1}$)')  # Set the y...
    plt.xlabel(r'$\log_{10} M_{\mathrm{blackhole}}\ (M_{\odot})$')  # and the x-axis labels

    leg = plt.legend(loc='lower left', numpoints=1, labelspacing=0.1)
    leg.draw_frame(False)  # Don't want a box frame
    for t in leg.get_texts():  # Reduce the size of the text
        t.set_fontsize('medium')

    outputFile = OutputDir + 'A.BlackHoleMassFunction_z' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()

# -------------------------------------------------------

    print('Plotting SFR density evolution for all galaxies')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure

    ObsSFRdensity = np.array([
        [0, 0.0158489, 0, 0, 0.0251189, 0.01000000],
        [0.150000, 0.0173780, 0, 0.300000, 0.0181970, 0.0165959],
        [0.0425000, 0.0239883, 0.0425000, 0.0425000, 0.0269153, 0.0213796],
        [0.200000, 0.0295121, 0.100000, 0.300000, 0.0323594, 0.0269154],
        [0.350000, 0.0147911, 0.200000, 0.500000, 0.0173780, 0.0125893],
        [0.625000, 0.0275423, 0.500000, 0.750000, 0.0331131, 0.0229087],
        [0.825000, 0.0549541, 0.750000, 1.00000, 0.0776247, 0.0389045],
        [0.625000, 0.0794328, 0.500000, 0.750000, 0.0954993, 0.0660693],
        [0.700000, 0.0323594, 0.575000, 0.825000, 0.0371535, 0.0281838],
        [1.25000, 0.0467735, 1.50000, 1.00000, 0.0660693, 0.0331131],
        [0.750000, 0.0549541, 0.500000, 1.00000, 0.0389045, 0.0776247],
        [1.25000, 0.0741310, 1.00000, 1.50000, 0.0524807, 0.104713],
        [1.75000, 0.0562341, 1.50000, 2.00000, 0.0398107, 0.0794328],
        [2.75000, 0.0794328, 2.00000, 3.50000, 0.0562341, 0.112202],
        [4.00000, 0.0309030, 3.50000, 4.50000, 0.0489779, 0.0194984],
        [0.250000, 0.0398107, 0.00000, 0.500000, 0.0239883, 0.0812831],
        [0.750000, 0.0446684, 0.500000, 1.00000, 0.0323594, 0.0776247],
        [1.25000, 0.0630957, 1.00000, 1.50000, 0.0478630, 0.109648],
        [1.75000, 0.0645654, 1.50000, 2.00000, 0.0489779, 0.112202],
        [2.50000, 0.0831764, 2.00000, 3.00000, 0.0512861, 0.158489],
        [3.50000, 0.0776247, 3.00000, 4.00000, 0.0416869, 0.169824],
        [4.50000, 0.0977237, 4.00000, 5.00000, 0.0416869, 0.269153],
        [5.50000, 0.0426580, 5.00000, 6.00000, 0.0177828, 0.165959],
        [3.00000, 0.120226, 2.00000, 4.00000, 0.173780, 0.0831764],
        [3.04000, 0.128825, 2.69000, 3.39000, 0.151356, 0.109648],
        [4.13000, 0.114815, 3.78000, 4.48000, 0.144544, 0.0912011],
        [0.350000, 0.0346737, 0.200000, 0.500000, 0.0537032, 0.0165959],
        [0.750000, 0.0512861, 0.500000, 1.00000, 0.0575440, 0.0436516],
        [1.50000, 0.0691831, 1.00000, 2.00000, 0.0758578, 0.0630957],
        [2.50000, 0.147911, 2.00000, 3.00000, 0.169824, 0.128825],
        [3.50000, 0.0645654, 3.00000, 4.00000, 0.0776247, 0.0512861],
        ], dtype=np.float32)

    ObsRedshift = ObsSFRdensity[:, 0]
    xErrLo = np.abs(ObsSFRdensity[:, 0]-ObsSFRdensity[:, 2])
    xErrHi = np.abs(ObsSFRdensity[:, 3]-ObsSFRdensity[:, 0])
    
    ObsSFR = np.log10(ObsSFRdensity[:, 1])
    yErrLo = np.abs(np.log10(ObsSFRdensity[:, 1])-np.log10(ObsSFRdensity[:, 4]))
    yErrHi = np.abs(np.log10(ObsSFRdensity[:, 5])-np.log10(ObsSFRdensity[:, 1]))

    # plot observational data (compilation used in Croton et al. 2006)
    plt.errorbar(ObsRedshift, ObsSFR, yerr=[yErrLo, yErrHi], xerr=[xErrLo, xErrHi], color='g', lw=1.0, alpha=0.3, marker='o', ls='none', label='Observations')
    
    SFR_density = np.zeros((LastSnap+1-FirstSnap))       
    for snap in range(FirstSnap,LastSnap+1):
        SFR_density[snap-FirstSnap] = sum(SfrDiskFull[snap]+SfrBulgeFull[snap]) / volume

    z = np.array(redshifts)
    nonzero = np.where(SFR_density > 0.0)[0]
    plt.plot(z[nonzero], np.log10(SFR_density[nonzero]), lw=3.0)

    plt.ylabel(r'$\log_{10} \mathrm{SFR\ density}\ (M_{\odot}\ \mathrm{yr}^{-1}\ \mathrm{Mpc}^{-3})$')  # Set the y...
    plt.xlabel(r'$\mathrm{redshift}$')  # and the x-axis labels

    # Set the x and y axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.5))

    plt.axis([0.0, 8.0, -3.0, -0.4])            

    outputFile = OutputDir + 'B.History-SFR-density' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()

# -------------------------------------------------------

    print('Plotting stellar mass density evolution')

    plt.figure()  # New figure
    ax = plt.subplot(111)  # 1 plot on the figure
    
    # SMD observations taken from Marchesini+ 2009, h=0.7
    # Values are (minz, maxz, rho,-err,+err)

    dickenson2003 = np.array(((0.6,1.4,8.26,0.08,0.08),
                     (1.4,2.0,7.86,0.22,0.33),
                     (2.0,2.5,7.58,0.29,0.54),
                     (2.5,3.0,7.52,0.51,0.48)),float)
    drory2005 = np.array(((0.25,0.75,8.3,0.15,0.15),
                (0.75,1.25,8.16,0.15,0.15),
                (1.25,1.75,8.0,0.16,0.16),
                (1.75,2.25,7.85,0.2,0.2),
                (2.25,3.0,7.75,0.2,0.2),
                (3.0,4.0,7.58,0.2,0.2)),float)
    PerezGonzalez2008 = np.array(((0.2,0.4,8.41,0.06,0.06),
             (0.4,0.6,8.37,0.04,0.04),
             (0.6,0.8,8.32,0.05,0.05),
             (0.8,1.0,8.24,0.05,0.05),
             (1.0,1.3,8.15,0.05,0.05),
             (1.3,1.6,7.95,0.07,0.07),
             (1.6,2.0,7.82,0.07,0.07),
             (2.0,2.5,7.67,0.08,0.08),
             (2.5,3.0,7.56,0.18,0.18),
             (3.0,3.5,7.43,0.14,0.14),
             (3.5,4.0,7.29,0.13,0.13)),float)
    glazebrook2004 = np.array(((0.8,1.1,7.98,0.14,0.1),
                     (1.1,1.3,7.62,0.14,0.11),
                     (1.3,1.6,7.9,0.14,0.14),
                     (1.6,2.0,7.49,0.14,0.12)),float)
    fontana2006 = np.array(((0.4,0.6,8.26,0.03,0.03),
                  (0.6,0.8,8.17,0.02,0.02),
                  (0.8,1.0,8.09,0.03,0.03),
                  (1.0,1.3,7.98,0.02,0.02),
                  (1.3,1.6,7.87,0.05,0.05),
                  (1.6,2.0,7.74,0.04,0.04),
                  (2.0,3.0,7.48,0.04,0.04),
                  (3.0,4.0,7.07,0.15,0.11)),float)
    rudnick2006 = np.array(((0.0,1.0,8.17,0.27,0.05),
                  (1.0,1.6,7.99,0.32,0.05),
                  (1.6,2.4,7.88,0.34,0.09),
                  (2.4,3.2,7.71,0.43,0.08)),float)
    elsner2008 = np.array(((0.25,0.75,8.37,0.03,0.03),
                 (0.75,1.25,8.17,0.02,0.02),
                 (1.25,1.75,8.02,0.03,0.03),
                 (1.75,2.25,7.9,0.04,0.04),
                 (2.25,3.0,7.73,0.04,0.04),
                 (3.0,4.0,7.39,0.05,0.05)),float)
    
    obs = (dickenson2003,drory2005,PerezGonzalez2008,glazebrook2004,fontana2006,rudnick2006,elsner2008)
    
    for o in obs:
        xval = ((o[:,1]-o[:,0])/2.)+o[:,0]
        if(whichimf == 0):
            ax.errorbar(xval, np.log10(10**o[:,2] *1.6), xerr=(xval-o[:,0], o[:,1]-xval), yerr=(o[:,3], o[:,4]), alpha=0.3, lw=1.0, marker='o', ls='none')
        elif(whichimf == 1):
            ax.errorbar(xval, np.log10(10**o[:,2] *1.6/1.8), xerr=(xval-o[:,0], o[:,1]-xval), yerr=(o[:,3], o[:,4]), alpha=0.3, lw=1.0, marker='o', ls='none')
            
    smd = np.zeros((LastSnap+1-FirstSnap))       
    for snap in range(FirstSnap,LastSnap+1):
      w = np.where((StellarMassFull[snap] > 1.0e8) & (StellarMassFull[snap] < 1.0e13))[0]
      if(len(w) > 0):
        smd[snap-FirstSnap] = sum(StellarMassFull[snap][w]) / volume

    z = np.array(redshifts)
    nonzero = np.where(smd > 0.0)[0]
    plt.plot(z[nonzero], np.log10(smd[nonzero]), 'k-', lw=3.0)

    plt.ylabel(r'$\log_{10}\ \phi\ (M_{\odot}\ \mathrm{Mpc}^{-3})$')  # Set the y...
    plt.xlabel(r'$\mathrm{redshift}$')  # and the x-axis labels

    # Set the x and y axis minor ticks
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.5))

    plt.axis([0.0, 4.2, 6.5, 9.0])   

    outputFile = OutputDir + 'C.History-stellar-mass-density' + OutputFormat
    plt.savefig(outputFile)  # Save the figure
    print('Saved file to', outputFile, '\n')
    plt.close()