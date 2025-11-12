import numpy as np
def monte_carlo_forecast(initial_investment, years=50, simulations=1000):
    results=[]
    for _ in range(simulations):
        wealth = initial_investment
        for _ in range(years):
            growth = np.random.normal(0.08,0.15)
            wealth *= (1+growth)
        results.append(wealth)
    return results
