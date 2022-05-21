def interpret(stat_method, compute_res, alpha=0.05):
    interpretations = []

    if stat_method == 'Pearson R Correlation Test':
        r = None
        p = None
        for var_name, var_val in compute_res:
            if var_name == 'R Coefficient':
                r = var_val 
            elif var_name == 'P-value':
                p = var_val 

        if abs(r) <= 1 and abs(r) >= 0.99:
            interpretations.append(f"The two variables have perfect linear correlation having a strength of {r * 100:.2f}%. It is shown that the two variables have almost 100% strength of linear relationship which means X is perfectly correlated to Y and vice versa. Their graph would look like a straight line.")
        elif abs(r) < 0.99 and abs(r) >= 0.5:
            sign = " upwards because the sign of r is positive." if r > 0 else " downwards because the sign of r is negative."
            interpretations.append(f"The two variables have a high degree of linear correlation. A strength of {r * 100:.2f}% is detected from both variables which means they have a high degree of linear correlation. Their graph would look like a line trending" + sign)
        elif abs(r) < 0.49 and abs(r) >= 0.30:
            sign = " upwards because the sign of r is positive." if r > 0 else " downwards because the sign of r is negative."
            interpretations.append(f"The two variables have a medium degree of linear correlation having a strength of {r * 100:.2f}%. Though not strong, a significant amount of correlation is seen between the two variables. Their graph might not be as explicit in showing these, but it will have a trend" + sign)
        elif abs(r) < 0.29:
            interpretations.append(f"The two variables have a weak correlation having a strength of {r * 100:.2f}%. Both variables have a weak sign of correlation. Their graphs might not give any inferences on their trend and direction having this low correlation value.")
        elif abs(r) == 0:
            interpretations.append(f"The two variables are not correlated with each other having a strength of {r * 100:.2f}%. The two variables do not have a linear relationship and is not related to each other statistically. Their graph do not constitute a linear relationship.")

        if r < 0:
            interpretations.append("The trend of both variables are downward since their r value is negative.")
        elif r > 0:
            interpretations.append("The trend of both variables are upward since their r value is positive.")

        if p < alpha:
            interpretations.append(f"Since the P-value {p:.4f} is less than the set alpha {alpha}, the resulting r correlation is not likely caused by chance and randomness.")
        elif p > alpha:
            interpretations.append(f"Since the P-value {p:.4f} is greater than the set alpha {alpha}, the resulting r correlation is non-significant and is likely caused by chance.")
        else:
            interpretations.append("error on comparing p-value of both variables x and y.")
    
    return interpretations