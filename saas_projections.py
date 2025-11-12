def generate_saas_forecast(users, avg_revenue):
    ARR = users * avg_revenue * 12
    MRR = users * avg_revenue
    return ARR, MRR
