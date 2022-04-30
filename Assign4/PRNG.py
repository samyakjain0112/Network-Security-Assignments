import math

def linearCongruentialGenerator(num, seed = 1871, a = 101427, c = 321, m = 2 ** 16):
	p_rand_nums = []
	x = seed

	for i in range(num):
		x = (a*x + c)%m 
		p_rand_nums.append(x / m)

	return p_rand_nums


def blumBlumShubGenerator(num, seed = 1871, p = 4271, q = 5227):
	p_rand_nums = []
	n = p*q
	x = (seed*seed)%n

	for i in range(num):
		x = (x*x)%n 
		p_rand_nums.append(x / n)

	return p_rand_nums
	

def chi_squared_value(rand_nums):
	dist = categorise(rand_nums)
	chi_sq = 0.0
	expected_val = len(rand_nums)/10

	for val in dist:
		chi_sq += ( (dist[val] - expected_val) ** 2 ) / expected_val

	return chi_sq

def categorise(rand_nums, num_cat = 10):
	dist = dict()
	for i in range(0, num_cat):
		dist[i] = 0 

	for x in rand_nums:
		dist[math.floor(x * num_cat)] += 1

	return dist

def chi_squared_test(rand_nums, significance_lvl):
	chi_sq_val = chi_squared_value(rand_nums)

	result = "FAIL TO REJECT null hypothesis"
	
	crit_value = 0.0
	if significance_lvl == 0.8:
		crit_value = 10118.8246
	elif significance_lvl == 0.90:
		crit_value = 10181.6616
	elif significance_lvl == 0.95:
		crit_value = 10233.7489
	else:
		print("**Invalid Significance Level for Chi Sq***")

	if chi_sq_val > crit_value:
		result = "REJECT null hypothesis"

	print("Significance Level: " + str(significance_lvl))
	print("Chi Sq: " + str(chi_sq_val))
	print("Crit Value: " + str(crit_value))
	print("Result is: " + result)
	print("....................................")

	return result

def kolmogorov_smirnov_test_value(rand_nums):
	rand_nums = sorted(rand_nums)
	n = len(rand_nums)
	d_plus_val, d_minus_val = 0, 0 

	for i in range(1, len(rand_nums) + 1):
		d_plus_val = max(d_plus_val, i/n - rand_nums[i-1])
		d_minus_val = max(d_minus_val, rand_nums[i-1] - (i-1)/n)

	d_val = max(d_plus_val, d_minus_val)

	return d_val

def kolmogorov_smirnov_test(rand_nums, alpha_level):
	result = "FAIL TO REJECT null hypothesis"
	critical_value = 0
	n = len(rand_nums)

	if alpha_level == 0.1:
		critical_value = 1.22/math.sqrt(n)
	elif alpha_level == 0.05:
		critical_value = 1.36/math.sqrt(n)
	elif alpha_level == 0.01:
		critical_value = 1.63/math.sqrt(n)
	else:
		print("Invalid alpha level for KS test. Must be: 0.1, 0.05, or 0.01")

	d_statistic = kolmogorov_smirnov_test_value(rand_nums)
	if d_statistic > critical_value:
		result = ("REJECT null hypothesis")
	print("Alpha Level is: " + str(alpha_level))
	print("D_statistic is: " + str(d_statistic))
	print("Critical value is: " + str(critical_value))
	print("Result is: " + result)
	print("............................")

	return result

def runTests(rand_nums):
	print("="*40)
	print("TEST RESULTS")
	print("="*40)

	# divide our output values in 10 equal subdivisions and run chi-square test
	print("---------CHI-SQ_TEST-----------")
	chi_squared_test(rand_nums, 0.8)
	chi_squared_test(rand_nums, 0.9)
	chi_squared_test(rand_nums, 0.95)

	print()

	# get first 100 values from sample and run kolmogorov-smirnov test
	print("---------KS_TEST-----------")
	rand_nums = rand_nums[:100]
	kolmogorov_smirnov_test(rand_nums, 0.1)
	kolmogorov_smirnov_test(rand_nums, 0.05)
	kolmogorov_smirnov_test(rand_nums, 0.01)
	print()


def run():
	num_observations = int(input("Input number of observations: "))
	method = int(input("Input method: 1. Linear Congruential Generator 2. Blum Blum Shub Generator\n"))

	out_file_name = ''
	if method == 1:
		rand_nums = linearCongruentialGenerator(num_observations)
		out_file_name = 'lcg_random_numbers.txt'
	elif method == 2:
		rand_nums = blumBlumShubGenerator(num_observations)
		out_file_name = 'bbs_random_numbers.txt'
	else:
		print('INVALID OPTION')
		return 1

	with open(out_file_name, 'w') as file:
		for val in rand_nums:
			file.write(str(val) + '\n')
	print('\n')
	print('Generated PseudoRandom Numbers are stored at: ' + out_file_name)
	runTests(rand_nums)

	return 0 

def main():
	quit = False
	while not quit:
		run()
		quit = (input('Quit? y - yes n - no\n').lower() == 'y')
		print('='*40)

if __name__ == '__main__':
	main()
