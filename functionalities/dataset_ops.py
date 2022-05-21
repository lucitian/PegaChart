from functionalities.statistical_analysis import freq_dist
from functionalities.statistical_analysis import anderson_test
import numpy as np

def describe_dataset(df):
    details = []

    for i in df.columns:
        mean = "NA"
        std = "NA"
        median = "NA"
        max = "NA"
        min = "NA"
        normal = "NA"
        vis = "NA"
        type = "NA"
        outliers = "NA"
        skew = "NA"
        kurtosis = "NA"
        try:
            if df[i].dtypes != 'O':
                mean = "NaN" if np.isnan(round(float(df[i].mean()), 2)) else round(float(df[i].mean()), 2)
                std = "NaN" if np.isnan(round(float(df[i].std()), 2)) else round(float(df[i].std()), 2)
                median = "NaN" if np.isnan(round(float(df[i].median()), 2)) else round(float(df[i].median()), 2)
                normal = anderson_test(df[i])
                normal = "Normal" if normal[0] < normal[1][4] else "Not Normal"
                vis = freq_dist(df[i])
                low = df[i].quantile(0.10)
                hi = df[i].quantile(0.90)
                outliers = int(len(df[i][(df[i] < low) | (df[i] > hi)]))
                type = "numerical"
                skew = "NaN" if np.isnan(round(float(df[i].skew()), 2)) else round(float(df[i].skew()), 2)
                kurtosis = "NaN" if np.isnan(round(float(df[i].kurtosis()), 2)) else round(float(df[i].kurtosis()), 2)
            else:
                counts = df[i].value_counts()
                if len(counts) > 2:
                    vis = counts[0:2].to_dict()
                    vis['others'] = int(counts[2:].sum())
                else:
                    vis = counts.to_dict()
                type = "object"
            try:
                max = float(df[i].max())
                min = float(df[i].min())
            except:
                max = df[i].max()
                min = df[i].min()
        except Exception as e:
            pass

        details.append({
            'column': i,
            'null_count': int(df.isna().sum()[i]),
            'mean': mean,
            'std': std,
            'median': median,
            'max': max,
            'min': min,
            'distribution': normal,
            'outliers': outliers,
            'type': type,
            'vis': vis,
            'skew': skew,
            'kurtosis': kurtosis
        })

    return {
        'size': int(df.size),
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'details': details
    }