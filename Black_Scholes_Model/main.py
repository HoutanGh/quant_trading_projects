from bayesian_optimisation import optimise_parameters

if __name__ == "__main__":
    best_params, best_score = optimise_parameters()

    print(f"Optimized Parameters: {best_params}")
    print(f"Optimized P&L: ${best_score:.2f}")