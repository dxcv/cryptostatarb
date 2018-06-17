class Strategy:

    def __init__ (self, zscore_lvl, close_zscore):

        self.zscore_lvl = zscore_lvl
        self.close_zscore = close_zscore

    # Function for generating trading signals
    def generate_signal(self, zscore, beta, price_one, price_two, sum_one, sum_two, commission, exposure):

        if zscore < -self.zscore_lvl and sum_two == 0 and sum_one == 0:

            n = exposure / (abs(price_two) + abs(beta * price_one))

            value = -n * price_two + n * beta * price_one - commission * \
                    (abs(n * price_two) + abs(n * beta * price_one))

            # Short beta unit of the first crypto
            position_one = -n * beta

            # Long one unit of the second crypto
            position_two = n

        elif zscore > self.zscore_lvl and sum_two == 0 and sum_one == 0:

            n = exposure / (abs(price_two) + abs(beta * price_one))

            value = n * price_two - n * beta * price_one - commission * (abs(n * price_two) + abs(n * beta * price_one))

            # Long beta unit of the first crypto
            position_one = n * beta

            # Short one unit of the second crypto
            position_two = -n

        # Closes positions if the spread is too narrow
        elif -self.close_zscore < zscore < self.close_zscore and abs(sum_two) + abs(sum_one) > 0:

            value = +sum_two * price_two + sum_one * price_one - commission * \
                    (abs(sum_two * price_two) + abs(sum_one * beta * price_one))

            position_one = -sum_one
            position_two = -sum_two

        # Else wait
        else:

            value = 0.0
            position_one = 0.0
            position_two = 0.0

        return value, position_one, position_two

    # Rebalancing function
    def rebalance(self, zscore, beta, beta_new, price_one, price_two, sum_one, sum_two, commission, exposure):

        position_two = 0.0

        if zscore < -self.zscore_lvl:

            n = exposure / (abs(price_two) + abs(beta * price_one))

            value = sum_one * price_one + n * beta_new * price_one - commission * abs(exposure * (beta_new - beta))

            position_one = -n * beta_new - sum_one

        elif zscore > self.zscore_lvl:

            n = exposure / (abs(price_two) + abs(beta * price_one))

            value = -sum_one * price_one + n * beta_new * price_one - commission * abs(exposure * (beta_new - beta))

            position_one = n * beta_new - sum_one

        else:

            value = sum_two * price_two + sum_one * price_one - commission * \
                    (abs(sum_two * price_two) + abs(sum_one * beta * price_one))

            position_one = -sum_one
            position_two = -sum_two

        return value, position_one, position_two
