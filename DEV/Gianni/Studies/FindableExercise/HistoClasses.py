import numpy as np

def Rebin(NewBins, OldBins, Histobinsvalues, axis=None):
    if not isinstance(NewBins, np.ndarray) or not isinstance(OldBins, np.ndarray):
        raise ValueError("NewBins and OldBins must be numpy arrays")

    if axis is None and Histobinsvalues.ndim > 1:
        raise ValueError("Please specify the axis to rebin for multidimensional histograms")

    if Histobinsvalues.ndim == 1:
        return rebin_nd(NewBins, OldBins, Histobinsvalues, axis=0)
    elif 1 < Histobinsvalues.ndim <= 3:
        return rebin_nd(NewBins, OldBins, Histobinsvalues, axis)
    else:
        raise ValueError("Unsupported histogram dimensionality. Only 1D, 2D, and 3D histograms are supported.")

def rebin_nd(NewBins, OldBins, Histobinsvalues, axis):
    # Ensure New_Bin and New_Error are initialized as arrays of appropriate shape
    New_Bin = None
    New_Error = None

    for i in range(len(NewBins) - 1):
        inf_lim = np.where(OldBins == NewBins[i])[0][0]
        sup_lim = np.where(OldBins == NewBins[i + 1])[0][0]

        if inf_lim == -1 or sup_lim == -1:
            raise ValueError('Bin didn\'t match! Please, modify the rebin array!')

        slices = [slice(None)] * Histobinsvalues.ndim
        slices[axis] = slice(inf_lim, sup_lim)
        summed_array = np.sum(Histobinsvalues[tuple(slices)], axis=axis)
        summedError_array = np.sqrt(summed_array)

        if New_Bin is None:
            New_Bin = summed_array[np.newaxis]
            New_Error = summedError_array[np.newaxis]
        else:
            New_Bin = np.concatenate((New_Bin, summed_array[np.newaxis]), axis=0)
            New_Error = np.concatenate((New_Error, summedError_array[np.newaxis]), axis=0)

    # Reshape New_Bin and New_Error to the correct shape
    shape = list(Histobinsvalues.shape)
    shape[axis] = len(NewBins) - 1
    New_Bin = New_Bin.reshape(shape)
    New_Error = New_Error.reshape(shape)

    return New_Bin, New_Error

# # Example usage:
# NewBins = np.array([0, 2, 4])
# OldBins = np.array([0, 1, 2, 3, 4])
# Histobinsvalues1D = np.array([1, 2, 3, 4])
# Histobinsvalues2D = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
# Histobinsvalues3D = np.random.rand(4, 4, 4)  # Example 3D histogram data

# # Rebin 1D histogram
# New_Bin1D, New_Error1D = Rebin(NewBins, OldBins, Histobinsvalues1D)

# print("New_Bin1D", New_Bin1D)
# print("New_Error1D", New_Error1D)

# # Rebin 2D histogram along axis 0
# New_Bin2D_axis0, New_Error2D_axis0 = Rebin(NewBins, OldBins, Histobinsvalues2D, axis=0)

# print("New_Bin2D_axis0", New_Bin2D_axis0)
# print("New_Error2D_axis0", New_Error2D_axis0)

# # Rebin 2D histogram along axis 1
# New_Bin2D_axis1, New_Error2D_axis1 = Rebin(NewBins, OldBins, Histobinsvalues2D, axis=1)

# print("New_Bin2D_axis1", New_Bin2D_axis1)
# print("New_Error2D_axis1", New_Error2D_axis1)


# Rebin 3D histogram along axis 0
# New_Bin3D_axis0, New_Error3D_axis0 = Rebin(NewBins, OldBins, Histobinsvalues3D, axis=0)
