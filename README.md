# Monte Carlo Portfolio Simulation (Student-t)

This project simulates portfolio returns using a Monte Carlo framework with Student-t distributed shocks to better capture real-world market behavior and tail risk. Unlike traditional models that assume normally distributed returns, this approach accounts for fat tails, meaning extreme price movements occur more frequently and realistically.  

Historical price data is collected and converted into returns, from which the mean return vector and covariance matrix are estimated. The covariance matrix captures both individual asset volatility and the relationships between assets. To preserve these relationships during simulation, the covariance matrix is decomposed using Cholesky decomposition, allowing independent random shocks to be transformed into correlated returns that reflect actual market structure.  

Instead of drawing shocks from a Gaussian distribution, the model samples from a Student-t distribution with a specified degree of freedom. This introduces heavier tails and increases the likelihood of extreme gains and losses. The samples are scaled to maintain a consistent variance, ensuring the simulation remains stable while still capturing fat-tailed behavior.  

Using these simulated returns, thousands of potential portfolio paths are generated. Each path applies portfolio weights to the asset returns and compounds them over time to produce a full trajectory of portfolio value. This provides a distribution of possible outcomes rather than a single expected path.  

From these simulations, key risk metrics are analyzed, including maximum drawdown, worst-case scenarios, median outcomes, and the distribution of final portfolio values. This approach highlights how correlation and tail events can significantly impact performance, offering a more realistic assessment of portfolio risk compared to models that rely solely on average returns or normality assumptions.  

Overall, this project demonstrates how combining Monte Carlo simulation, correlation modeling via Cholesky decomposition, and fat-tailed distributions can provide deeper insight into portfolio behavior under uncertainty.
