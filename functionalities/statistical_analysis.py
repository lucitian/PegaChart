from collections import Counter
from itertools import groupby
from operator import itemgetter
from scipy import stats as sp
from itertools import chain
import pandas as pd 
import numpy as np
import math

# UNIVARIATE STATISTICAL ANALYSIS
def mean(x):
        return sum(x) / len(x)
    
def median(x):
    s = sorted(x)
    i = ((len(s) + 1) // 2) - 1
    m = None
    if len(s) % 2 == 0:
        m = (s[i] + s[i+1]) / 2
    else:
        m = s[i]
    
    return m

def mode(x):
    c = Counter(iter(x)).most_common()
    i, j = next(groupby(c, key=itemgetter(1)), (0, []))
    return tuple(map(itemgetter(0), j))

def stdev(x):
    sum = 0 

    for i in x:
        sum += (i - mean(x)) ** 2

    return (sum / (len(x) - 1)) ** 0.5

def variance(x):
    return stdev(x) ** 2

# =========================================================================

# RELATIONSHIP / ASSOCIATION STATISTICAL ANALYSIS

def pearsonr(x: np.array, y: np.array):
    n = len(x)

    if n != len(y):
        raise ValueError(f"Dataset size is not equal. Size {len(x)} not equal to {len(y)}.")

    x_num = x - x.mean()
    y_num = y - y.mean()
    
    SSx = (x_num * x_num).sum(axis=0)
    SSy = (y_num * y_num).sum(axis=0)
    
    num = np.matmul(x_num.transpose(), y_num)
    den = np.sqrt(np.outer(SSx, SSy))
    r = num / den
    t = r * np.sqrt((n-2)/(1-r**2))
    p = 2 * sp.t.sf(np.abs(t), n-2)

    if np.isnan(r[0][0]):
        raise TypeError("Pearson R computation returned NaN.")

    return (
        ('R Coefficient', r[0][0]), ('P-value', p[0][0]), ('SSxy', num), ('SSx', SSx), ('SSy', SSy),
        ('X Mean', x.mean()), ('Y Mean', y.mean()), ('Numerator', num), ('Denominator', den[0][0])
    )

def spearmanrho(x, y):
    n = len(x)

    if n != len(y):
        raise ValueError(f"Dataset size is not equal. Size {len(x)} not equal to {len(y)}.")

    df_x = pd.DataFrame(x)
    df_x['rank'] = df_x.rank(ascending=False)

    df_y = pd.DataFrame(y)
    df_y['rank'] = df_y.rank(ascending=False)

    ranked_x = []
    ranked_y = []

    for data, rank in df_x.iterrows():
        ranked_x.append((rank[0],rank['rank']))
    
    for data, rank in df_y.iterrows():
        ranked_y.append((rank[0],rank['rank']))

    d_squared_sum = 0

    for i in range(len(x)):
        d_squared = (ranked_x[i][1] - ranked_y[i][1]) ** 2

        d_squared_sum += d_squared
    
    rho = 1 - ((6*d_squared_sum)/((n)**3 - n))

    t = rho * np.sqrt((n-2)/(1-rho**2))

    p = 2 * sp.t.sf(np.abs(t), n-2)
    
    return (('Rho Value', rho), ('P Value', p), ('Rank Diff Squared Sum', d_squared_sum), ('Denominator', ((n)**3 - n)))

def chi_square(x, expected = None, alpha = 0.05):
    """
    Format
    ----------
    2D Array in which in each array is one row while the size of the inner array is the column number.
    
    The data and the expected array should be in this format:

    >>> format = [['val11','val12','val13'],['val21', 'val12', 'val13']...]
    """
    r = len(x)
    c = len(x[0])

    if expected:
        if r != len(expected) or c != len(expected[0]):
            raise ValueError("Row and column of original data is not equal to the row and column of the expected data.")
    else:
        expected = []

        column_sums = []
        row_sums = []
        
        for i in zip(*x):
            column_sums.append(sum(i))
        
        for row in x:
            row_sums.append(sum(row))
        
        rw = 0
        
        for row in x:
            temp = []
            col = 0

            for c in row:
                temp.append((column_sums[col] * row_sums[rw]) / sum(row_sums))
                col += 1
            
            expected.append(temp)
            rw += 1

    chi = 0

    rw = 0
    for row in x:
        col = 0
        for c in row:
            chi += (c - expected[rw][col])**2 / expected[rw][col]
            col += 1
        rw += 1
    
    df = len(x[0]) - 1

    p = sp.chi2.sf(chi, df)

    critical_value = sp.chi2.ppf(1-alpha, df)
    
    return chi, p, df, expected, critical_value

# =========================================================================

# SIGNIFICANT DIFFERENCE ANALYSIS

def one_way_anova(*x, alpha = 0.05):
    if len(x) < 2:
        raise ValueError("The number of data groups should be at least two or more.")

    N = sum(len(i) for i in x)

    n = set(len(i) for i in x)

    if len(n) > 1:
        raise ValueError("The length of each of the columns should be the same.")

    n = list(n)[0]
    
    a = len(x)

    df_between = a - 1
    df_within = N - a
    df_total = N - 1

    ss_between_sum = sum([sum(data) ** 2 for data in x])
    ss_between_t2 = sum([sum(data) for data in x]) ** 2
    
    ss_between = (ss_between_sum / n) - (ss_between_t2 / N)

    ss_within_sum_all = sum([data**2 for data in chain.from_iterable(x)])
    ss_within = ss_within_sum_all - (ss_between_sum / n)

    ss_total = ss_within_sum_all - (ss_between_t2 / N)

    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    f_statistic = ms_between / ms_within

    p = sp.f.sf(f_statistic, df_between, df_within)

    critical_value = sp.f.ppf(1 - alpha, df_between, df_within)

    return f_statistic, p, critical_value

# =========================================================================

# RANK SUM ANALYSIS

def kruskal_wallis(*x, alpha = 0.05):
    k = set(len(i) for i in x)

    if len(k) > 1:
        raise ValueError("The length of each of the columns should be the same.")
    
    k = list(k)[0]

    df = len(x)-1

    flat = list(chain.from_iterable(x))

    N = len(flat)

    df_x = pd.DataFrame(flat)
    df_x['rank'] = df_x.rank()

    ranked = []
    temp = []

    for index, data in df_x.iterrows():
        temp.append((data[0], data['rank']))

        if (index + 1) % k == 0:
            ranked.append(temp)
            temp = []
 
    sum_rank = 0 

    for r in ranked:
        sum_rank += sum([i[1] for i in r]) ** 2

    H = ((12/(N**2+N)) * sum_rank/k) - (3*(N+1))

    p = sp.chi2.sf(H, df)

    critical_value = sp.chi2.ppf(1-alpha, df)

    return H, p, critical_value

def mann_whitney_u(x, y, alpha = 0.05):    
    df_x = pd.DataFrame(x)
    df_x['group'] = 'x'

    df_y = pd.DataFrame(y)
    df_y['group'] = 'y'

    df_concat = pd.concat([df_x, df_y]).copy()
    df_concat['rank'] = df_concat[0].rank()

    r1 = sum([z['rank'] for i,z, in df_concat.loc[df_concat['group'] == 'x'].iterrows()])
    r2 = sum([z['rank'] for i,z, in df_concat.loc[df_concat['group'] == 'y'].iterrows()])

    U1 = r1 - ((len(x)*(len(x) + 1)) / 2)
    U2 = r2 - ((len(y)*(len(y) + 1)) / 2)

    U = U1 if U1 < U2 else U2

    return U

# =========================================================================

# TEST FOR NORMALITY
def anderson_test(data):
    from scipy.stats import anderson
    
    result = anderson(data)

    return result.statistic, result.critical_values

# =========================================================================

# FREQUENCY DISTRIBUTION

def freq_dist(data: pd.DataFrame):
    size = len(data)

    num_classes = 1

    while(True):
        if 2 ** num_classes >= size:
            break
        else:
            num_classes += 1

    rng = data.max() - data.min()

    class_width = rng / num_classes
    class_width = math.ceil(class_width)

    lower_limits = []
    upper_limits = []

    epoch = data.min()

    for _ in range(num_classes):
        lower_limits.append(epoch)
        epoch += class_width

        upper_limits.append(epoch - 1)
    
    freq_distrib = []

    for index in range(num_classes):
        lower = lower_limits[index]
        upper = upper_limits[index]

        res = data[(data >= lower) & (data <= upper)]
        freq_distrib.append((f"{lower} - {upper}", int(len(res))))
    
    return freq_distrib