def test(x):
	x[0] = 5

def main():
	x = [1, 2, 3, 4, 5]
	test(x)
	print(x)

if __name__ == "__main__":
    main()