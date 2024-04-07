# Bibliotecas

import math
import os
import numpy as np
import pandas as pd
from collections import Counter
from scipy import stats
from scipy.stats import spearmanr, chi2_contingency

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML


def feature_summary(dataframe, SAVE_PATH, FileName, categorical_threshold=20, SavePlots=True, SaveTable=True):
    os.makedirs(SAVE_PATH+'BasicPlots/', exist_ok=True)
    replacement_value = np.nan #-1 # You can replace with any other value as needed
    dataframe.replace(-np.inf, replacement_value, inplace=True)
    dataframe.replace(np.inf, replacement_value, inplace=True)

    # Initialize lists for numerical and categorical features
    numerical_features = []
    categorical_features = []
    ListGoodFeatures = []
    summary = []

    Feature_count = 0
    # Loop through all columns to identify numerical and categorical features
    for column in dataframe.columns:
        unique_values_count = dataframe[column].dropna().nunique()
        dtype = dataframe[column].dropna().dtype
        print('\r Processing Feature {} out of {}'.format(Feature_count, len(dataframe.columns)), end="")
        if unique_values_count <= categorical_threshold or dtype=='object' or dtype=='bool' or dtype=='category':
            categorical_features.append(column)
            median = None
            mean = None
            iqr = None
            Q3 = None
            Q1 = None
            std = None
            max_value = None
            min_value = None
            skew = None
            kurt = None
            NZeros = None
            NNegatives = None
            NUnique = None

            # Todo esse bloco pra calcular a frequencia de cada categoria
            b = Counter(dataframe[column].dropna())
            total = sum(b.values())
            stringaux = "{"
            counter = 0
            Arraysize = len(b.most_common())
            for face, count in b.most_common():
                if counter==(Arraysize-1):
                  stringaux = stringaux + "\""+str(face)+"\""+ ":" + str(count) + " ( " + str(round(100*count/total,2)) + " %)"
                else:
                  stringaux = stringaux + "\""+str(face)+"\""+ ":" + str(count) + " ( " + str(round(100*count/total,2)) + " %), "
                counter = counter+1
            stringaux = stringaux + "}"
            frequency = stringaux

            num_nan = '{} ({} %)'.format(dataframe[column].isnull().sum(), round(dataframe[column].isnull().sum()/len(dataframe)*100,2))
            nan_percentage = round(dataframe[column].isnull().sum()/len(dataframe)*100,2)

        else:
            numerical_features.append(column)
            median = dataframe[column].dropna().median()
            mean = round(dataframe[column].dropna().mean(),2)
            Q3 = dataframe[column].dropna().quantile(0.75)
            Q1 = dataframe[column].dropna().quantile(0.25)
            iqr = Q3 - Q1
            std = round(dataframe[column].dropna().std(),2)
            max_value = dataframe[column].dropna().max()
            min_value = dataframe[column].dropna().min()

            NZeros = '{} ({} %)'.format(len(dataframe[dataframe[column]==0]), round(len(dataframe[dataframe[column]==0])/len(dataframe)*100,2))
            NNegatives = '{} ({} %)'.format(len(dataframe[dataframe[column]<0]), round(len(dataframe[dataframe[column]<0])/len(dataframe)*100,2))
            NUnique = dataframe[column].dropna().nunique()

            values, counts = np.unique(dataframe[column].dropna(), return_counts=True)
            ind = np.argmax(counts)
            #print('value: {}, Freq. (%): {}'.format(values[ind], round(counts[ind]/len(dataframe[column])*100, 2)))  # prints the most frequent element

            frequency = '{{\"{}\":{} ({} %)}}'.format(values[ind], counts[ind], 100*round(counts[ind]/len(dataframe[column]), 2))
            num_nan = '{} ({} %)'.format(dataframe[column].isnull().sum(), round(dataframe[column].isnull().sum()/len(dataframe)*100,2))
            nan_percentage = round(dataframe[column].isnull().sum()/len(dataframe)*100,2)

            uniques = round(counts[ind]/len(dataframe[column])*100, 2)

            # Skewness and kurtosis
            skew = round(dataframe[column].dropna().astype(float).skew(), 2)
            kurt = round(dataframe[column].dropna().astype(float).kurt(), 2)

        if (dtype=='datetime64' or dtype=='timedelta[ns]'):
            # Non-numeric, non-categorical columns (e.g., datetime)
            median = None
            mean = None
            Q3 = None
            Q1 = None
            std = None
            max_value = None
            min_value = None
            skew = None
            kurt = None
            frequency = None
            num_nan = None
            NZeros = None
            NNegatives = None
            NUnique = None

            nan_percentage = round(dataframe[column].isnull().sum()/len(dataframe)*100,2)

        summary.append({
                    'Feature': column,
                    'Dtype': dtype,
                    'Mean': mean,
                    'STD': std,
                    'Median': median,
                    'IQ (Q1, Q3)': '[{}, {}]'.format(Q1, Q3),
                    'Min, Max': '[{}, {}]'.format(min_value, max_value),
                    'Skewness':skew,
                    'Kurtosis':kurt,
                    'Frequency': frequency,
                    'N. Zeros':NZeros,
                    'N. Negatives':NNegatives,
                    'N. Uniques':NUnique,
                    'N. NaN': num_nan,
                })

        if nan_percentage<=10 or uniques<=95:
          ListGoodFeatures.append(column)
          
        Feature_count = Feature_count + 1

    # Creating sample  
    if len(dataframe)>=5000:
      sample = dataframe.sample(frac=5000/len(dataframe), replace=False, random_state=1)
    else:
      sample = dataframe
      
    summarydf = pd.DataFrame(summary)
    
    if SaveTable:
    	# create a excel sheet
    	with pd.ExcelWriter(SAVE_PATH+"ExploratoryTable_{}.xlsx".format(FileName)) as writer:
    		sample.to_excel(writer, sheet_name="Sample", index=False)
    		summarydf.to_excel(writer, sheet_name="Statistics", index=False)
    
    # QA Plots:
    
    if SavePlots:
            # Create and save histograms for numerical features
        for feature in numerical_features:
            plt.figure(figsize=(7, 7))
            plt.hist(dataframe[feature].dropna(), histtype='step', fill=False, edgecolor='blue',bins=40, log=True, align='mid', linewidth=1, density=False)
            plt.xlabel(feature, fontsize=20)
            plt.ylabel('Counts', fontsize=20)
            plt.title(f'Histogram of {feature}', fontweight="bold", fontsize=20)
            plt.savefig(SAVE_PATH+'BasicPlots/'+f'{feature}_histogram.png', bbox_inches='tight')
            plt.clf()
            plt.close()
        
        # Create and save barplots for categorical features
        for feature in categorical_features:
            plt.figure(figsize=(8, 6))
            sns.countplot(data=dataframe, x=feature, palette='Set3')
            plt.xlabel(feature)
            plt.ylabel('Counts')
            plt.title(f'Barplot of {feature}')
            plt.xticks(rotation=45)
            plt.savefig(SAVE_PATH+'BasicPlots/'+f'{feature}_barplot.png', bbox_inches='tight')
            plt.clf()
            plt.close()

    
    return summarydf, sample, categorical_features, numerical_features, ListGoodFeatures


def Exploratory_Plots(df, continuous_vars, categorical_vars, SAVE_PATH):

  categorical_names = categorical_vars #.columns.tolist()
  categorical_names.insert(0, None)
  GraphType = None

  ##################### LISTA DE  WIDGETS ###############################

  ## 1sr Layer
  column_names = df.columns.tolist()
  column_names.insert(0, None)
  feature1_dropdown = widgets.Dropdown(options=column_names,description='x-axis:',)
  feature2_dropdown = widgets.Dropdown(options=column_names,description='y-axis:',)
  set_button1 = widgets.Button(description='Set', button_style='success')

  # 2nd Layer:
  Type_dropdown1 = widgets.Dropdown(options=['Histogram2D', 'Scatter'],description='Plot Type')
  Type_dropdown2 = widgets.Dropdown(options=['Barplot', 'CrossTab'],description='Plot Type')
  Log_dropdown = widgets.Dropdown(options=[False, True],description='Log scale')
  Density_dropdown = widgets.Dropdown(options=[False, True],description='Density')
  NBins = widgets.IntSlider(value=200,min=0,max=400,step=1,description='N. Bins')
  set_button2 = widgets.Button(description='Set', button_style='success')
  save_button = widgets.Dropdown(options=[False, True],description='Save Figure?')

  # 3rd Layer:
  Cat_dropdown = widgets.Dropdown(options=categorical_names,description='Categorical')
  xmin = widgets.FloatText(value=np.nan,description='x min',disabled=False)
  xmax = widgets.FloatText(value=np.nan,description='x max',disabled=False)
  ymin = widgets.FloatText(value=np.nan,description='y min',disabled=False)
  ymax = widgets.FloatText(value=np.nan,description='y max',disabled=False)

  # 4th Layer:
  update_button = widgets.Button(description='Update Plot',button_style='success')
  reset_button = widgets.Button(description='Reset', button_style='danger')
  output = widgets.Output()

  # Organize widgets into columns using VBox
  column1 = widgets.VBox([feature1_dropdown, feature2_dropdown, set_button1])

  column2_v0 = widgets.VBox([NBins, Log_dropdown, Density_dropdown, save_button]) # 1D plots
  column2_v1 = widgets.VBox([NBins, Log_dropdown, Type_dropdown1, save_button])  # 2D plots numerical
  column2_v2 = widgets.VBox([Type_dropdown2, save_button]) # 2D plots categorical

  column3 = widgets.VBox([xmin, xmax, ymin, ymax])
  column3_v1 = widgets.VBox([Cat_dropdown, xmin, xmax, ymin, ymax])
  column4 = widgets.VBox([update_button, reset_button])

  # Define a function to reset widget values to default
  def reset_defaults(b):
      # Reset feature dropdowns to None (default)
      feature1_dropdown.value = None
      feature2_dropdown.value = None

      # Reset other widget values to default
      Type_dropdown1.value = 'Histogram2D'
      Type_dropdown2.value = 'Barplot'
      Log_dropdown.value = False
      save_button.value = False
      Density_dropdown.value = False
      NBins.value = 200
      xmin.value = np.nan
      xmax.value = np.nan
      ymin.value = np.nan
      ymax.value = np.nan

  # Attach the reset function to the reset button
  reset_button.on_click(reset_defaults)

  # Combine the columns into an HBox to display side by side
  columns = widgets.HBox([column1])
  display(columns)

  def add_buttoms1(b):
    # 1D plots
    if feature1_dropdown.value==None or feature2_dropdown.value==None:
      feature = feature1_dropdown.value if feature2_dropdown.value==None else feature2_dropdown.value

      if feature in continuous_vars:
        columns = widgets.HBox([column2_v0, column3, column4])
        GraphType = 'Histo1D'
        print("IMPORTANT: Do not click the \"Set\" buttom again! \nTo refresh the options or the plot, run the cell again or just click the  \"Update Plot\" buttom.")

      else:
        columns = widgets.HBox([column4])
        GraphType = 'Barplot1D'
        print("IMPORTANT: Do not click the \"Set\" buttom again! \nTo refresh the options or the plot, run the cell again or just click the  \"Update Plot\" buttom.")

    # 2D plots
    if feature1_dropdown.value!=None and feature2_dropdown.value!=None:

      if (feature1_dropdown.value in continuous_vars and feature2_dropdown.value in categorical_vars) or \
           (feature2_dropdown.value in continuous_vars and feature1_dropdown.value in categorical_vars):

        columns = widgets.HBox([column2_v0, column3, column4])
        GraphType = 'Histo1D_withCat'
        print("IMPORTANT: Do not click the \"Set\" buttom again! \nTo refresh the options or the plot, run the cell again or just click the  \"Update Plot\" buttom.")

      if (feature1_dropdown.value in continuous_vars and feature2_dropdown.value in continuous_vars):
        columns = widgets.HBox([column2_v1, column3_v1, column4])
        GraphType = 'Numerical_2D'
        print("IMPORTANT: Do not click the \"Set\" buttom again! \nTo refresh the options or the plot, run the cell again or just click the  \"Update Plot\" buttom.")

      if (feature1_dropdown.value in categorical_vars and feature2_dropdown.value in categorical_vars):
        columns = widgets.HBox([column2_v2, column4])
        GraphType = 'Categorical_2D'
        print("IMPORTANT: Do not click the \"Set\" buttom again! \nTo refresh the options or the plot, run the cell again or just click the  \"Update Plot\" buttom.")

    display(columns, output)

  # Plot functions
  def update_plot(b):
      with output:
          if save_button.value:
            os.makedirs(SAVE_PATH+'SavedPlots/', exist_ok=True)
          output.clear_output(wait=True)  # Clear previous output
          feature1 = feature1_dropdown.value
          feature2 = feature2_dropdown.value

          # 1D plots
          if feature1_dropdown.value==None or feature2_dropdown.value==None:
            feature = feature1_dropdown.value if feature2_dropdown.value==None else feature2_dropdown.value

            # Check if xmin and xmax are both NaN
            if math.isnan(xmin.value) or math.isnan(xmax.value):
                # Calculate the default x-axis limits based on the feature1 min and max values
                default_xmin = df[feature].dropna().min()
                default_xmax = df[feature].dropna().max()
            else:
                # Use the provided values of xmin and xmax
                default_xmin = xmin.value
                default_xmax = xmax.value


            if feature in continuous_vars:
              GraphType = 'Histo1D'
              plt.figure(figsize=(6, 4))
              plt.hist(df[feature].dropna(), histtype='step', fill=False, edgecolor='blue', bins=NBins.value, log=Log_dropdown.value, align='mid', range=(default_xmin, default_xmax), linewidth=1, density=Density_dropdown.value)
              plt.xlabel(feature, fontsize=20)
              plt.ylabel('Counts', fontsize=20)
              plt.title(f'Histogram of {feature}', fontweight="bold", fontsize=20)
              plt.xlim(default_xmin, default_xmax)
              if not math.isnan(ymin.value) and not math.isnan(ymax.value):
                plt.ylim(ymin.value, ymax.value)
              plt.grid(True)
              if save_button.value:
                  plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}.png'.format(GraphType, feature), bbox_inches='tight')
              plt.show()

            else:
              GraphType = 'Barplot1D'
              plt.figure(figsize=(8, 6))
              sns.countplot(data=df, x=feature, palette='Set3')
              plt.xlabel(feature)
              plt.ylabel('Counts')
              plt.title(f'Barplot of {feature}')
              plt.xticks(rotation=45)
              plt.grid(True)
              if save_button.value:
                plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}.png'.format(GraphType, feature), bbox_inches='tight')
              plt.show()

          # 2D continuous Plots
          if feature1_dropdown.value!=None and feature2_dropdown.value!=None:

            if (feature1_dropdown.value in continuous_vars and feature2_dropdown.value in continuous_vars):
                
                # Check if xmin and xmax are both NaN
                if math.isnan(xmin.value) or math.isnan(xmax.value):
                    # Calculate the default x-axis limits based on the feature1 min and max values
                    default_xmin = df[feature1].dropna().min()
                    default_xmax = df[feature1].dropna().max()
                else:
                    # Use the provided values of xmin and xmax
                    default_xmin = xmin.value
                    default_xmax = xmax.value

                # Check if xmin and xmax are both NaN
                if math.isnan(ymin.value) or math.isnan(ymax.value):
                    # Calculate the default x-axis limits based on the feature1 min and max values
                    default_ymin = df[feature2].dropna().min()
                    default_ymax = df[feature2].dropna().max()
                else:
                    # Use the provided values of xmin and xmax
                    default_ymin = ymin.value
                    default_ymax = ymax.value

                if Type_dropdown1.value=='Histogram2D':
                  GraphType = 'Histo2D'
                  if Cat_dropdown.value==None:
                    # Both features are continuous, create a scatterplot
                    plt.figure(figsize=(6, 4))

                    if Log_dropdown.value:
                      lognorm = mpl.colors.LogNorm()
                    else:
                      lognorm = None

                    # Create the 2D histogram
                    x = df[feature1].values
                    y = df[feature2].values

                    # Create boolean arrays to identify NaN values in both columns
                    bad_indices = np.isnan(x) | np.isnan(y)
                    good_indices = ~bad_indices

                    # Use boolean indexing to extract non-NaN values from both columns
                    good_x = x[good_indices]
                    good_y = y[good_indices]

                    plt.hist2d(good_x, good_y, bins=(NBins.value, NBins.value), range=[[default_xmin, default_xmax], [default_ymin, default_ymax]], cmap='turbo', 
                               norm=lognorm)

                    # Add colorbar for the z-axis (optional)
                    cbar = plt.colorbar()
                    cbar.set_label('Counts')

                    plt.xlabel(feature1)
                    plt.ylabel(feature2)
                    plt.xlim(default_xmin, default_xmax)
                    plt.ylim(default_ymin, default_ymax)
                    #plt.title(f'Scatterplot of {feature1} vs {feature2}')
                    plt.grid(True)
                    if save_button.value:
                        plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, feature1, feature2), bbox_inches='tight')
                    plt.show()

                  else:
                    Categories = df[Cat_dropdown.value].dropna().unique()

                    # Calculate the number of rows and columns that come closest to creating a square grid
                    if len(Categories)==2:
                      cols = 2
                      rows = 1
                    else:
                      sqrt_N = math.sqrt(len(Categories))
                      cols = math.ceil(sqrt_N)
                      rows = math.ceil(len(Categories) / cols)

                    # Create a figure and a set of subplots
                    fig, axes = plt.subplots(rows, cols, figsize=(16, 8))
                    # Flatten the axes array to make it easier to iterate
                    axes = axes.flatten()

                    # Create 2D histograms in each subplot
                    for i in range(0,len(Categories)):
                      ax = axes[i]

                      x = df[df[Cat_dropdown.value]==Categories[i]][feature1].values
                      y = df[df[Cat_dropdown.value]==Categories[i]][feature2].values

                      # Create boolean arrays to identify NaN values in both columns
                      bad_indices = np.isnan(x) | np.isnan(y)
                      good_indices = ~bad_indices

                      # Use boolean indexing to extract non-NaN values from both columns
                      good_x = x[good_indices]
                      good_y = y[good_indices]

                      hist = ax.hist2d(good_x,good_y, bins=(NBins.value, NBins.value), range=[[default_xmin, default_xmax], [default_ymin, default_ymax]], cmap='turbo', norm=mpl.colors.LogNorm())

                      # Add colorbar for the z-axis (optional)
                      cbar = plt.colorbar(hist[3], ax=ax)  # Use the fourth element of hist to get the color bar object

                      ax.set_title('{}'.format(Categories[i]))
                      ax.set_xlabel(feature1)
                      ax.set_ylabel(feature2)

                      # Add gridlines
                      ax.grid(True, linestyle='--')

                      # Set custom x and y limits
                      ax.set_xlim(default_xmin, default_xmax)
                      ax.set_ylim(default_ymin, default_ymax)

                    # Adjust the spacing between subplots
                    plt.tight_layout()
                    # Show the plot

                    plt.xlim(default_xmin, default_xmax)
                    plt.ylim(default_ymin, default_ymax)
                    #plt.title(f'Scatterplot of {feature1} vs {feature2}')
                    plt.grid(True)
                    if save_button.value:
                        plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, feature1, feature2), bbox_inches='tight')
                    plt.show()

                else:
                  GraphType = 'Scatter'
                  plt.figure(figsize=(6, 4))

                  if Cat_dropdown.value==None:
                    plt.scatter(df[feature1], df[feature2])

                  else:

                    groups = df.groupby(Cat_dropdown.value)
                    for name, group in groups:
                        plt.plot(group[feature1], group[feature2], marker='o', linestyle='', markersize=2, label=name)
                    plt.legend()

                  plt.xlabel(feature1)
                  plt.ylabel(feature2)
                  plt.xlim(default_xmin, default_xmax)
                  plt.ylim(default_ymin, default_ymax)
                  plt.grid(True)
                  if save_button.value:
                    plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, feature1, feature2), bbox_inches='tight')
                  plt.show()

            # Continuous x categorical:

            if (feature1_dropdown.value in continuous_vars and feature2_dropdown.value in categorical_vars) or \
           (feature2_dropdown.value in continuous_vars and feature1_dropdown.value in categorical_vars):
               
                      GraphType = 'Histo1D_withCat'

                      num_feature = feature1_dropdown.value if feature1_dropdown.value in continuous_vars else feature2_dropdown.value
                      cat_feature = feature1_dropdown.value if feature1_dropdown.value in categorical_vars else feature2_dropdown.value

                      if math.isnan(xmin.value) or math.isnan(xmax.value):
                          # Calculate the default x-axis limits based on the feature1 min and max values
                          default_xmin = df[num_feature].min()
                          default_xmax = df[num_feature].max()
                      else:
                          # Use the provided values of xmin and xmax
                          default_xmin = xmin.value
                          default_xmax = xmax.value
                          
                      plt.figure(figsize=(8, 6))

                      # Calculate the overall range for the numerical feature
                      overall_range = (df[num_feature].min(), df[num_feature].max())
                      bin_width = (overall_range[1] - overall_range[0]) / NBins.value
                      bins = np.arange(overall_range[0], overall_range[1] + bin_width, bin_width)

                      # Create histograms of num_feature for each category in cat_feature
                      for category in df[cat_feature].unique():
                          subset = df[df[cat_feature] == category][num_feature].dropna()
                          plt.hist(subset,bins=bins, histtype='step', fill=False,
                                  log=Log_dropdown.value,label=f'{category}', align='mid', linewidth=1, density=Density_dropdown.value, range=(default_xmin, default_xmax))

                      plt.legend()
                      plt.title(f'Histograms of {num_feature} by {cat_feature}')
                      plt.xlabel(num_feature)
                      plt.ylabel('Counts')
                      plt.grid(True)
                      plt.xlim(default_xmin, default_xmax)

                      if not math.isnan(ymin.value) and not math.isnan(ymax.value):
                        plt.ylim(ymin.value, ymax.value)
                        
                      if save_button.value:
                        plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, num_feature, cat_feature), bbox_inches='tight')
                      plt.show()

            # Categorical x categorical
            if(feature1_dropdown.value in categorical_vars and feature2_dropdown.value in categorical_vars):

              if Type_dropdown2.value=='Barplot':
                GraphType = 'Barplot2D'
                plt.figure(figsize=(6, 4))
                # Create crosstab for stacked barplot
                crosstab = pd.crosstab(df[feature1_dropdown.value], df[feature2_dropdown.value])

                # Create stacked barplot
                crosstab.plot(kind='bar', stacked=False)

                plt.title(f'Stacked Barplot of {feature1_dropdown.value} vs. {feature2_dropdown.value}')
                plt.xlabel(feature1_dropdown.value)
                plt.ylabel('Counts')
                plt.legend(title=feature2_dropdown.value, bbox_to_anchor=(1.0, 1.0))
                plt.xticks(rotation=45)
                plt.grid(True)
                if save_button.value:
                    plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, feature1_dropdown.value, feature2_dropdown.value), bbox_inches='tight')
                plt.show()

              else:
                GraphType = 'CrossTab'
                plt.figure(figsize=(6, 4))
                cross_tab = pd.crosstab(df[feature1_dropdown.value], df[feature2_dropdown.value])
                sns.heatmap(cross_tab, cmap='rocket_r', annot=True, fmt='g')
                if save_button.value:
                    plt.savefig(SAVE_PATH+'SavedPlots/'+'{}_{}_vs_{}.png'.format(GraphType, feature1_dropdown.value, feature2_dropdown.value), bbox_inches='tight')
                plt.show()

  #update buttom
  update_button.on_click(update_plot)

  # Attach observation to the button
  set_button1.on_click(add_buttoms1)