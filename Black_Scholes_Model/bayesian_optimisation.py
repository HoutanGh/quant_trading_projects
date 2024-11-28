from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args
from BS_backtest import BS_backtest


# search space

space = [
    Real(0.01, 0.05, name='delta_threshold'),    
    # Real(0.05, 0.2, name='gamma_threshold'),   
    # Real(-0.05, -0.01, name='theta_max_loss'), 
    # Real(0.01, 0.1, name='vega_threshold')     
]

@use_named_args(space)
def objective(**params):
    # params dic is automatically generated by the skopt library

    delta_t = params['delta_threshold']
    # gamma_t = params['gamma_threshold']
    # theta_t = params['theta_max_loss']
    # vega_t = params['vega_threshold']

    final_pnl, _, _ = BS_backtest(
        ticker="AAPL",
        start_date="2022-01-01",
        end_date="2022-12-31",
        delta_threshold=delta_t,
        # threshold_gamma=gamma_t,
        # max_theta_loss=theta_t,
        option_type="call",
        r=0.05,
        K_multiplier=1.05,
        window=5
    )

    # adding penalty for unrealise scenarios
    if final_pnl == 0:
        return 1000
    if final_pnl < -100:
        return 1000

    return -final_pnl

def optimise_parameters():
    result = gp_minimize(objective, space, n_calls=50, random_state=42)

    best_params = result.x
    best_score = -result.fun # converts back to positive P&L

    print(f"Best Parameters: {best_params}")
    print(f"Best P&L: ${best_score:.2f}")
    
    return best_params, best_score